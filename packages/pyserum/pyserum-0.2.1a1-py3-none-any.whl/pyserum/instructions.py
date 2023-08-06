"""Serum Dex Instructions."""
from typing import Any, Dict, List, NamedTuple

from solana.publickey import PublicKey
from solana.sysvar import SYSVAR_RENT_PUBKEY
from solana.transaction import AccountMeta, TransactionInstruction
from solana.utils.validate import validate_instruction_keys, validate_instruction_type
from spl.token.constants import TOKEN_PROGRAM_ID  # type: ignore # TODO: Fix and remove ignore.

from ._layouts.instructions import INSTRUCTIONS_LAYOUT, InstructionType
from .enums import OrderType, Side

# V2
DEFAULT_DEX_PROGRAM_ID = PublicKey("EUqojwWA2rd19FZrzeBncJsm38Jm1hEhE3zsmX3bRc2o")


class InitializeMarketParams(NamedTuple):
    """Initalize market params."""

    market: PublicKey
    """"""
    request_queue: PublicKey
    """"""
    event_queue: PublicKey
    """"""
    bids: PublicKey
    """"""
    asks: PublicKey
    """"""
    base_vault: PublicKey
    """"""
    quote_vault: PublicKey
    """"""
    base_mint: PublicKey
    """"""
    quote_mint: PublicKey
    """"""
    base_lot_size: int
    """"""
    quote_lot_size: int
    """"""
    fee_rate_bps: int
    """"""
    vault_signer_nonce: int
    """"""
    quote_dust_threshold: int
    """"""
    program_id: PublicKey = DEFAULT_DEX_PROGRAM_ID


class NewOrderParams(NamedTuple):
    """New order params."""

    market: PublicKey
    """"""
    open_orders: PublicKey
    """"""
    payer: PublicKey
    """"""
    owner: PublicKey
    """"""
    request_queue: PublicKey
    """"""
    base_vault: PublicKey
    """"""
    quote_vault: PublicKey
    """"""
    side: Side
    """"""
    limit_price: int
    """"""
    max_quantity: int
    """"""
    order_type: OrderType
    """"""
    client_id: int = 0
    """"""
    program_id: PublicKey = DEFAULT_DEX_PROGRAM_ID
    """"""


class MatchOrdersParams(NamedTuple):
    """"Match order params."""

    market: PublicKey
    """"""
    request_queue: PublicKey
    """"""
    event_queue: PublicKey
    """"""
    bids: PublicKey
    """"""
    asks: PublicKey
    """"""
    base_vault: PublicKey
    """"""
    quote_vault: PublicKey
    """"""
    limit: int
    """"""
    program_id: PublicKey = DEFAULT_DEX_PROGRAM_ID
    """"""


class ConsumeEventsParams(NamedTuple):
    """Consume events params."""

    market: PublicKey
    """"""
    event_queue: PublicKey
    """"""
    open_orders_accounts: List[PublicKey]
    """"""
    limit: int
    """"""
    program_id: PublicKey = DEFAULT_DEX_PROGRAM_ID
    """"""


class CancelOrderParams(NamedTuple):
    """Cancel order params."""

    market: PublicKey
    """"""
    open_orders: PublicKey
    """"""
    owner: PublicKey
    """"""
    request_queue: PublicKey
    """"""
    side: Side
    """"""
    order_id: int
    """"""
    open_orders_slot: int
    """"""
    program_id: PublicKey = DEFAULT_DEX_PROGRAM_ID
    """"""


class CancelOrderByClientIDParams(NamedTuple):
    """Cancel order by client ID params."""

    market: PublicKey
    """"""
    open_orders: PublicKey
    """"""
    owner: PublicKey
    """"""
    request_queue: PublicKey
    """"""
    client_id: int
    """"""
    program_id: PublicKey = DEFAULT_DEX_PROGRAM_ID
    """"""


class SettleFundsParams(NamedTuple):
    """Settle fund params."""

    market: PublicKey
    """"""
    open_orders: PublicKey
    """"""
    owner: PublicKey
    """"""
    base_vault: PublicKey
    """"""
    quote_vault: PublicKey
    """"""
    base_wallet: PublicKey
    """"""
    quote_wallet: PublicKey
    """"""
    vault_signer: PublicKey
    """"""
    program_id: PublicKey = DEFAULT_DEX_PROGRAM_ID


def __parse_and_validate_instruction(instruction: TransactionInstruction, instruction_type: InstructionType) -> Any:
    instruction_type_to_length_map: Dict[InstructionType, int] = {
        InstructionType.InitializeMarket: 9,
        InstructionType.NewOrder: 9,
        InstructionType.MatchOrder: 7,
        InstructionType.ConsumeEvents: 2,
        InstructionType.CancelOrder: 4,
        InstructionType.CancelOrderByClientID: 4,
        InstructionType.SettleFunds: 9,
    }
    validate_instruction_keys(instruction, instruction_type_to_length_map[instruction_type])
    data = INSTRUCTIONS_LAYOUT.parse(instruction.data)
    validate_instruction_type(data, instruction_type)
    return data


def decode_initialize_market(instruction: TransactionInstruction) -> InitializeMarketParams:
    """Decode an instialize market instruction and retrieve the instruction params."""
    data = __parse_and_validate_instruction(instruction, InstructionType.InitializeMarket)
    return InitializeMarketParams(
        market=instruction.keys[0].pubkey,
        request_queue=instruction.keys[1].pubkey,
        event_queue=instruction.keys[2].pubkey,
        bids=instruction.keys[3].pubkey,
        asks=instruction.keys[4].pubkey,
        base_vault=instruction.keys[5].pubkey,
        quote_vault=instruction.keys[6].pubkey,
        base_mint=instruction.keys[7].pubkey,
        quote_mint=instruction.keys[8].pubkey,
        base_lot_size=data.args.base_lot_size,
        quote_lot_size=data.args.quote_lot_size,
        fee_rate_bps=data.args.fee_rate_bps,
        vault_signer_nonce=data.args.vault_signer_nonce,
        quote_dust_threshold=data.args.quote_dust_threshold,
        program_id=instruction.program_id,
    )


def decode_new_order(instruction: TransactionInstruction) -> NewOrderParams:
    data = __parse_and_validate_instruction(instruction, InstructionType.NewOrder)
    return NewOrderParams(
        market=instruction.keys[0].pubkey,
        open_orders=instruction.keys[1].pubkey,
        request_queue=instruction.keys[2].pubkey,
        payer=instruction.keys[3].pubkey,
        owner=instruction.keys[4].pubkey,
        base_vault=instruction.keys[5].pubkey,
        quote_vault=instruction.keys[6].pubkey,
        side=data.args.side,
        limit_price=data.args.limit_price,
        max_quantity=data.args.max_quantity,
        order_type=data.args.order_type,
        client_id=data.args.client_id,
    )


def decode_match_orders(instruction: TransactionInstruction) -> MatchOrdersParams:
    """Decode a match orders instruction and retrieve the instruction params."""
    data = __parse_and_validate_instruction(instruction, InstructionType.MatchOrder)
    return MatchOrdersParams(
        market=instruction.keys[0].pubkey,
        request_queue=instruction.keys[1].pubkey,
        event_queue=instruction.keys[2].pubkey,
        bids=instruction.keys[3].pubkey,
        asks=instruction.keys[4].pubkey,
        base_vault=instruction.keys[5].pubkey,
        quote_vault=instruction.keys[6].pubkey,
        limit=data.args.limit,
    )


def decode_consume_events(instruction: TransactionInstruction) -> ConsumeEventsParams:
    """Decode a consume events instruction and retrieve the instruction params."""
    data = __parse_and_validate_instruction(instruction, InstructionType.ConsumeEvents)
    return ConsumeEventsParams(
        open_orders_accounts=[a_m.pubkey for a_m in instruction.keys[:-2]],
        market=instruction.keys[-2].pubkey,
        event_queue=instruction.keys[-1].pubkey,
        limit=data.args.limit,
    )


def decode_cancel_order(instruction: TransactionInstruction) -> CancelOrderParams:
    data = __parse_and_validate_instruction(instruction, InstructionType.CancelOrder)
    return CancelOrderParams(
        market=instruction.keys[0].pubkey,
        open_orders=instruction.keys[1].pubkey,
        request_queue=instruction.keys[2].pubkey,
        owner=instruction.keys[3].pubkey,
        side=Side(data.args.side),
        order_id=int.from_bytes(data.args.order_id, "little"),
        open_orders_slot=data.args.open_orders_slot,
    )


def decode_settle_funds(instruction: TransactionInstruction) -> SettleFundsParams:
    # data = __parse_and_validate_instruction(instruction, InstructionType.SettleFunds)
    return SettleFundsParams(
        market=instruction.keys[0].pubkey,
        open_orders=instruction.keys[1].pubkey,
        owner=instruction.keys[2].pubkey,
        base_vault=instruction.keys[3].pubkey,
        quote_vault=instruction.keys[4].pubkey,
        base_wallet=instruction.keys[5].pubkey,
        quote_wallet=instruction.keys[6].pubkey,
        vault_signer=instruction.keys[7].pubkey,
    )


def decode_cancel_order_by_client_id(instruction: TransactionInstruction) -> CancelOrderByClientIDParams:
    data = __parse_and_validate_instruction(instruction, InstructionType.CancelOrderByClientID)
    return CancelOrderByClientIDParams(
        market=instruction.keys[0].pubkey,
        open_orders=instruction.keys[1].pubkey,
        request_queue=instruction.keys[2].pubkey,
        owner=instruction.keys[3].pubkey,
        client_id=data.args.client_id,
    )


def initialize_market(params: InitializeMarketParams) -> TransactionInstruction:
    """Generate a transaction instruction to initialize a Serum market."""
    return TransactionInstruction(
        keys=[
            AccountMeta(pubkey=params.market, is_signer=False, is_writable=False),
            AccountMeta(pubkey=params.request_queue, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.event_queue, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.bids, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.asks, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.base_vault, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.quote_vault, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.base_mint, is_signer=False, is_writable=False),
            AccountMeta(pubkey=params.quote_mint, is_signer=False, is_writable=False),
        ],
        program_id=params.program_id,
        data=INSTRUCTIONS_LAYOUT.build(
            dict(
                instruction_type=InstructionType.InitializeMarket,
                args=dict(
                    base_lot_size=params.base_lot_size,
                    quote_lot_size=params.quote_lot_size,
                    fee_rate_bps=params.fee_rate_bps,
                    vault_signer_nonce=params.vault_signer_nonce,
                    quote_dust_threshold=params.quote_dust_threshold,
                ),
            ),
        ),
    )


def new_order(params: NewOrderParams) -> TransactionInstruction:
    """Generate a transaction instruction to place new order."""
    return TransactionInstruction(
        keys=[
            AccountMeta(pubkey=params.market, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.open_orders, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.request_queue, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.payer, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.owner, is_signer=True, is_writable=False),
            AccountMeta(pubkey=params.base_vault, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.quote_vault, is_signer=False, is_writable=True),
            AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
            AccountMeta(pubkey=SYSVAR_RENT_PUBKEY, is_signer=False, is_writable=False),
        ],
        program_id=params.program_id,
        data=INSTRUCTIONS_LAYOUT.build(
            dict(
                instruction_type=InstructionType.NewOrder,
                args=dict(
                    side=params.side,
                    limit_price=params.limit_price,
                    max_quantity=params.max_quantity,
                    order_type=params.order_type,
                    client_id=params.client_id,
                ),
            )
        ),
    )


def match_orders(params: MatchOrdersParams) -> TransactionInstruction:
    """Generate a transaction instruction to match order."""
    return TransactionInstruction(
        keys=[
            AccountMeta(pubkey=params.market, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.request_queue, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.event_queue, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.bids, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.asks, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.base_vault, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.quote_vault, is_signer=False, is_writable=True),
        ],
        program_id=params.program_id,
        data=INSTRUCTIONS_LAYOUT.build(
            dict(instruction_type=InstructionType.MatchOrder, args=dict(limit=params.limit))
        ),
    )


def consume_events(params: ConsumeEventsParams) -> TransactionInstruction:
    """Generate a transaction instruction to consume market events."""
    keys = [
        AccountMeta(pubkey=pubkey, is_signer=False, is_writable=True)
        for pubkey in params.open_orders_accounts + [params.market, params.event_queue]
    ]
    return TransactionInstruction(
        keys=keys,
        program_id=params.program_id,
        data=INSTRUCTIONS_LAYOUT.build(
            dict(instruction_type=InstructionType.ConsumeEvents, args=dict(limit=params.limit))
        ),
    )


def cancel_order(params: CancelOrderParams) -> TransactionInstruction:
    """Generate a transaction instruction to cancel order."""
    return TransactionInstruction(
        keys=[
            AccountMeta(pubkey=params.market, is_signer=False, is_writable=False),
            AccountMeta(pubkey=params.open_orders, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.request_queue, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.owner, is_signer=True, is_writable=False),
        ],
        program_id=params.program_id,
        data=INSTRUCTIONS_LAYOUT.build(
            dict(
                instruction_type=InstructionType.CancelOrder,
                args=dict(
                    side=params.side,
                    order_id=params.order_id.to_bytes(16, byteorder="little"),
                    open_orders=bytes(params.open_orders),
                    open_orders_slot=params.open_orders_slot,
                ),
            )
        ),
    )


def settle_funds(params: SettleFundsParams) -> TransactionInstruction:
    """Generate a transaction instruction to settle fund."""
    return TransactionInstruction(
        keys=[
            AccountMeta(pubkey=params.market, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.open_orders, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.owner, is_signer=True, is_writable=False),
            AccountMeta(pubkey=params.base_vault, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.quote_vault, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.base_wallet, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.quote_wallet, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.vault_signer, is_signer=False, is_writable=False),
            AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        ],
        program_id=params.program_id,
        data=INSTRUCTIONS_LAYOUT.build(dict(instruction_type=InstructionType.SettleFunds, args=dict())),
    )


def cancel_order_by_client_id(params: CancelOrderByClientIDParams) -> TransactionInstruction:
    """Generate a transaction instruction to cancel order by client id."""
    return TransactionInstruction(
        keys=[
            AccountMeta(pubkey=params.market, is_signer=False, is_writable=False),
            AccountMeta(pubkey=params.open_orders, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.request_queue, is_signer=False, is_writable=True),
            AccountMeta(pubkey=params.owner, is_signer=True, is_writable=False),
        ],
        program_id=params.program_id,
        data=INSTRUCTIONS_LAYOUT.build(
            dict(
                instruction_type=InstructionType.CancelOrderByClientID,
                args=dict(
                    client_id=params.client_id,
                ),
            )
        ),
    )
