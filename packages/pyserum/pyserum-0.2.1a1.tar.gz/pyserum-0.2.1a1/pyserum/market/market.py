"""Market module to interact with Serum DEX."""
from __future__ import annotations

import itertools
import logging
from typing import List

from solana.account import Account
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.rpc.types import RPCResponse, TxOpts
from solana.system_program import CreateAccountParams, create_account
from solana.sysvar import SYSVAR_RENT_PUBKEY
from solana.transaction import Transaction, TransactionInstruction
from spl.token.constants import ACCOUNT_LEN, TOKEN_PROGRAM_ID, WRAPPED_SOL_MINT  # type: ignore # TODO: Remove ignore.
from spl.token.instructions import CloseAccountParams  # type: ignore
from spl.token.instructions import InitializeAccountParams, close_account, initialize_account

import pyserum.instructions as instructions
import pyserum.market.types as t

from .._layouts.open_orders import OPEN_ORDERS_LAYOUT
from ..enums import OrderType, Side
from ..open_orders_account import OpenOrdersAccount, make_create_account_instruction
from ..utils import load_bytes_data
from ._internal.queue import decode_event_queue, decode_request_queue
from .orderbook import OrderBook
from .state import MarketState

LAMPORTS_PER_SOL = 1000000000


# pylint: disable=too-many-public-methods
class Market:
    """Represents a Serum Market."""

    logger = logging.getLogger("pyserum.market.Market")

    def __init__(
        self,
        conn: Client,
        market_state: MarketState,
    ) -> None:
        self._conn = conn
        self.state = market_state

    @staticmethod
    # pylint: disable=unused-argument
    def load(
        conn: Client,
        market_address: PublicKey,
        program_id: PublicKey = instructions.DEFAULT_DEX_PROGRAM_ID,
    ) -> Market:
        """Factory method to create a Market.

        :param conn: The connection that we use to load the data, created from `solana.rpc.api`.
        :param market_address: The market address that you want to connect to.
        :param program_id: The program id of the given market, it will use the default value if not provided.
        """
        market_state = MarketState.load(conn, market_address, program_id)
        return Market(conn, market_state)

    def support_srm_fee_discounts(self) -> bool:
        raise NotImplementedError("support_srm_fee_discounts not implemented")

    def find_fee_discount_keys(self, owner: PublicKey, cache_duration: int):
        raise NotImplementedError("find_fee_discount_keys not implemented")

    def find_best_fee_discount_key(self, owner: PublicKey, cache_duration: int):
        raise NotImplementedError("find_best_fee_discount_key not implemented")

    def find_open_orders_accounts_for_owner(self, owner_address: PublicKey) -> List[OpenOrdersAccount]:
        return OpenOrdersAccount.find_for_market_and_owner(
            self._conn, self.state.public_key(), owner_address, self.state.program_id()
        )

    def find_quote_token_accounts_for_owner(self, owner_address: PublicKey, include_unwrapped_sol: bool = False):
        raise NotImplementedError("find_quote_token_accounts_for_owner not implemented")

    def load_bids(self) -> OrderBook:
        """Load the bid order book"""
        bytes_data = load_bytes_data(self.state.bids(), self._conn)
        return OrderBook.from_bytes(self.state, bytes_data)

    def load_asks(self) -> OrderBook:
        """Load the ask order book."""
        bytes_data = load_bytes_data(self.state.asks(), self._conn)
        return OrderBook.from_bytes(self.state, bytes_data)

    def load_orders_for_owner(self, owner_address: PublicKey) -> List[t.Order]:
        """Load orders for owner."""
        bids = self.load_bids()
        asks = self.load_asks()
        open_orders_accounts = self.find_open_orders_accounts_for_owner(owner_address)
        if not open_orders_accounts:
            return []

        all_orders = itertools.chain(bids.orders(), asks.orders())
        open_orders_addresses = {str(o.address) for o in open_orders_accounts}
        orders = [o for o in all_orders if str(o.open_order_address) in open_orders_addresses]
        return orders

    def load_base_token_for_owner(self):
        raise NotImplementedError("load_base_token_for_owner not implemented")

    def load_event_queue(self) -> List[t.Event]:
        """Load the event queue which includes the fill item and out item. For any trades two fill items are added to
        the event queue. And in case of a trade, cancel or IOC order that missed, out items are added to the event
        queue.
        """
        bytes_data = load_bytes_data(self.state.event_queue(), self._conn)
        return decode_event_queue(bytes_data)

    def load_request_queue(self) -> List[t.Request]:
        bytes_data = load_bytes_data(self.state.request_queue(), self._conn)
        return decode_request_queue(bytes_data)

    def load_fills(self, limit=100) -> List[t.FilledOrder]:
        bytes_data = load_bytes_data(self.state.event_queue(), self._conn)
        events = decode_event_queue(bytes_data, limit)
        return [
            self.parse_fill_event(event)
            for event in events
            if event.event_flags.fill and event.native_quantity_paid > 0
        ]

    def parse_fill_event(self, event) -> t.FilledOrder:
        if event.event_flags.bid:
            side = Side.Buy
            price_before_fees = (
                event.native_quantity_released + event.native_fee_or_rebate
                if event.event_flags.maker
                else event.native_quantity_released - event.native_fee_or_rebate
            )
        else:
            side = Side.Sell
            price_before_fees = (
                event.native_quantity_released - event.native_fee_or_rebate
                if event.event_flags.maker
                else event.native_quantity_released + event.native_fee_or_rebate
            )

        price = (price_before_fees * self.state.base_spl_token_multiplier()) / (
            self.state.quote_spl_token_multiplier() * event.native_quantity_paid
        )
        size = event.native_quantity_paid / self.state.base_spl_token_multiplier()
        return t.FilledOrder(
            order_id=int.from_bytes(event.order_id, "little"),
            side=side,
            price=price,
            size=size,
            fee_cost=event.native_fee_or_rebate * (1 if event.event_flags.maker else -1),
        )

    def place_order(  # pylint: disable=too-many-arguments,too-many-locals
        self,
        payer: PublicKey,
        owner: Account,
        order_type: OrderType,
        side: Side,
        limit_price: int,
        max_quantity: int,
        client_id: int = 0,
        opts: TxOpts = TxOpts(),
    ) -> RPCResponse:  # TODO: Add open_orders_address_key param and fee_discount_pubkey
        transaction = Transaction()
        signers: List[Account] = [owner]
        open_order_accounts = self.find_open_orders_accounts_for_owner(owner.public_key())
        if not open_order_accounts:
            new_open_orders_account = Account()
            mbfre_resp = self._conn.get_minimum_balance_for_rent_exemption(OPEN_ORDERS_LAYOUT.sizeof())
            balanced_needed = mbfre_resp["result"]
            transaction.add(
                make_create_account_instruction(
                    owner.public_key(),
                    new_open_orders_account.public_key(),
                    balanced_needed,
                    self.state.program_id(),
                )
            )
            signers.append(new_open_orders_account)
            # TODO: Cache new_open_orders_account

        # TODO: Handle open_orders_address_key
        # TODO: Handle fee_discount_pubkey

        if payer == owner.public_key():
            raise ValueError("Invalid payer account")

        # TODO: add integration test for SOL wrapping.
        should_wrap_sol = (side == side.Buy and self.state.quote_mint() == WRAPPED_SOL_MINT) or (
            side == side.Sell and self.state.base_mint == WRAPPED_SOL_MINT
        )
        wrapped_sol_account = Account()
        if should_wrap_sol:
            transaction.add(
                create_account(
                    CreateAccountParams(
                        from_pubkey=owner.public_key(),
                        new_account_pubkey=wrapped_sol_account.public_key(),
                        lamports=Market._get_lamport_need_for_sol_wrapping(
                            limit_price, max_quantity, side, open_order_accounts
                        ),
                        space=ACCOUNT_LEN,
                        program_id=TOKEN_PROGRAM_ID,
                    )
                )
            )
            transaction.add(
                initialize_account(
                    InitializeAccountParams(
                        account=wrapped_sol_account.public_key(),
                        mint=WRAPPED_SOL_MINT,
                        owner=owner.public_key(),
                        program_id=SYSVAR_RENT_PUBKEY,
                    )
                )
            )

        transaction.add(
            self.make_place_order_instruction(
                wrapped_sol_account.public_key() if should_wrap_sol else payer,
                owner,
                order_type,
                side,
                limit_price,
                max_quantity,
                client_id,
                open_order_accounts[0].address if open_order_accounts else new_open_orders_account.public_key(),
            )
        )

        if should_wrap_sol:
            transaction.add(
                close_account(
                    CloseAccountParams(
                        account=wrapped_sol_account.public_key(),
                        owner=owner.public_key(),
                        dest=owner.public_key(),
                    )
                )
            )
        # TODO: extract `make_place_order_transaction`.
        return self._conn.send_transaction(transaction, *signers, opts=opts)

    @staticmethod
    def _get_lamport_need_for_sol_wrapping(
        price: int, size: int, side: Side, open_orders_accounts: List[OpenOrdersAccount]
    ) -> int:
        lamports = 0
        if side == Side.Buy:
            lamports = round(price * size * 1.01 * LAMPORTS_PER_SOL)
            if open_orders_accounts:
                lamports -= open_orders_accounts[0].quote_token_free
        else:
            lamports = round(size * LAMPORTS_PER_SOL)
            if open_orders_accounts:
                lamports -= open_orders_accounts[0].base_token_free

        return max(lamports, 0) + 10000000

    def make_place_order_instruction(  # pylint: disable=too-many-arguments
        self,
        payer: PublicKey,
        owner: Account,
        order_type: OrderType,
        side: Side,
        limit_price: int,
        max_quantity: int,
        client_id: int,
        open_order_account: PublicKey,
    ) -> TransactionInstruction:
        if self.state.base_size_number_to_lots(max_quantity) < 0:
            raise Exception("Size lot %d is too small" % max_quantity)
        if self.state.price_number_to_lots(limit_price) < 0:
            raise Exception("Price lot %d is too small" % limit_price)
        return instructions.new_order(
            instructions.NewOrderParams(
                market=self.state.public_key(),
                open_orders=open_order_account,
                payer=payer,
                owner=owner.public_key(),
                request_queue=self.state.request_queue(),
                base_vault=self.state.base_vault(),
                quote_vault=self.state.quote_vault(),
                side=side,
                limit_price=limit_price,
                max_quantity=max_quantity,
                order_type=order_type,
                client_id=client_id,
                program_id=self.state.program_id(),
            )
        )

    def cancel_order_by_client_id(
        self, owner: Account, open_orders_account: PublicKey, client_id: int, opts: TxOpts = TxOpts()
    ) -> RPCResponse:
        txs = Transaction().add(self.make_cancel_order_by_client_id_instruction(owner, open_orders_account, client_id))
        return self._conn.send_transaction(txs, owner, opts=opts)

    def make_cancel_order_by_client_id_instruction(
        self, owner: Account, open_orders_account: PublicKey, client_id: int
    ) -> TransactionInstruction:
        return instructions.cancel_order_by_client_id(
            instructions.CancelOrderByClientIDParams(
                market=self.state.public_key(),
                owner=owner.public_key(),
                open_orders=open_orders_account,
                request_queue=self.state.request_queue(),
                client_id=client_id,
                program_id=self.state.program_id(),
            )
        )

    def cancel_order(self, owner: Account, order: t.Order, opts: TxOpts = TxOpts()) -> RPCResponse:
        txn = Transaction().add(self.make_cancel_order_instruction(owner.public_key(), order))
        return self._conn.send_transaction(txn, owner, opts=opts)

    def match_orders(self, fee_payer: Account, limit: int, opts: TxOpts = TxOpts()) -> RPCResponse:
        txn = Transaction().add(self.make_match_orders_instruction(limit))
        return self._conn.send_transaction(txn, fee_payer, opts=opts)

    def make_cancel_order_instruction(self, owner: PublicKey, order: t.Order) -> TransactionInstruction:
        params = instructions.CancelOrderParams(
            market=self.state.public_key(),
            owner=owner,
            open_orders=order.open_order_address,
            request_queue=self.state.request_queue(),
            side=order.side,
            order_id=order.order_id,
            open_orders_slot=order.open_order_slot,
            program_id=self.state.program_id(),
        )
        return instructions.cancel_order(params)

    def make_match_orders_instruction(self, limit: int) -> TransactionInstruction:
        params = instructions.MatchOrdersParams(
            market=self.state.public_key(),
            request_queue=self.state.request_queue(),
            event_queue=self.state.event_queue(),
            bids=self.state.bids(),
            asks=self.state.asks(),
            base_vault=self.state.base_vault(),
            quote_vault=self.state.quote_vault(),
            limit=limit,
            program_id=self.state.program_id(),
        )
        return instructions.match_orders(params)

    def settle_funds(  # pylint: disable=too-many-arguments
        self,
        owner: Account,
        open_orders: OpenOrdersAccount,
        base_wallet: PublicKey,
        quote_wallet: PublicKey,  # TODO: add referrer_quote_wallet.
        opts: TxOpts = TxOpts(),
    ) -> RPCResponse:
        # TODO: Handle wrapped sol accounts
        if open_orders.owner != owner.public_key():
            raise Exception("Invalid open orders account")
        vault_signer = PublicKey.create_program_address(
            [bytes(self.state.public_key()), self.state.vault_signer_nonce().to_bytes(8, byteorder="little")],
            self.state.program_id(),
        )
        transaction = Transaction()
        transaction.add(self.make_settle_funds_instruction(open_orders, base_wallet, quote_wallet, vault_signer))
        return self._conn.send_transaction(transaction, owner, opts=opts)

    def make_settle_funds_instruction(
        self,
        open_orders_account: OpenOrdersAccount,
        base_wallet: PublicKey,
        quote_wallet: PublicKey,
        vault_signer: PublicKey,
    ) -> TransactionInstruction:
        if base_wallet == self.state.base_vault():
            raise ValueError("base_wallet should not be a vault address")
        if quote_wallet == self.state.quote_vault():
            raise ValueError("quote_wallet should not be a vault address")

        return instructions.settle_funds(
            instructions.SettleFundsParams(
                market=self.state.public_key(),
                open_orders=open_orders_account.address,
                owner=open_orders_account.owner,
                base_vault=self.state.base_vault(),
                quote_vault=self.state.quote_vault(),
                base_wallet=base_wallet,
                quote_wallet=quote_wallet,
                vault_signer=vault_signer,
                program_id=self.state.program_id(),
            )
        )
