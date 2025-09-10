"""
Mercury-style fintech fee calculations with intentional bugs for Nova CI demo.

This module demonstrates common financial calculation bugs that Nova can fix:
1. Float precision issues in fee calculations
2. Incorrect rounding (banker's vs HALF_UP)
3. Missing validation for edge cases
"""

from decimal import Decimal, ROUND_HALF_UP


def compute_fees(
    amount_usd: Decimal, 
    is_international: bool, 
    interchange_bps: int, 
    fx_spread_bps: int = 0
) -> Decimal:
    """
    Compute total fees for a transaction.
    
    Args:
        amount_usd: Transaction amount in USD
        is_international: Whether this is an international transaction
        interchange_bps: Interchange fee in basis points (1 bps = 0.01%)
        fx_spread_bps: FX spread in basis points (for international only)
    
    Returns:
        Total fees rounded to cents using HALF_UP rounding
    """
    if amount_usd <= 0:
        raise ValueError("Amount must be positive")
    
    # BUG 1: Float precision loss - should stay in Decimal
    interchange_fee = Decimal(str(float(amount_usd) * interchange_bps / 10000))
    
    total_fees = interchange_fee
    
    if is_international:
        fx_spread = amount_usd * Decimal(fx_spread_bps) / Decimal('10000')
        total_fees += fx_spread
    
    # BUG 2: Using Python's round() which uses banker's rounding, not HALF_UP
    return Decimal(str(round(float(total_fees), 2)))


def settle_amount(
    amount_usd: Decimal, 
    is_international: bool, 
    interchange_bps: int, 
    fx_spread_bps: int = 0
) -> Decimal:
    """
    Calculate the net settlement amount after fees.
    
    Args:
        amount_usd: Transaction amount in USD
        is_international: Whether this is an international transaction  
        interchange_bps: Interchange fee in basis points
        fx_spread_bps: FX spread in basis points (for international only)
    
    Returns:
        Net amount after fees, rounded to cents
    """
    # BUG 3: Missing validation - should reject zero/negative amounts
    if amount_usd == 0:
        return Decimal('0.00')
    
    fees = compute_fees(amount_usd, is_international, interchange_bps, fx_spread_bps)
    net_amount = amount_usd - fees
    
    return net_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
