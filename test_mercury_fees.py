"""
Comprehensive test suite for Mercury fintech fee calculations.

These tests will FAIL due to the intentional bugs in mercury_fees.py:
1. Rounding bug: Should use HALF_UP, but uses banker's rounding
2. Float precision bug: Loses precision in fee calculations  
3. Validation bug: Allows zero amounts when it shouldn't

Nova CI-Rescue will automatically fix these bugs to make tests pass.
"""

import pytest
from decimal import Decimal
from mercury_fees import compute_fees, settle_amount


def test_domestic_fee_and_settlement_rounding():
    """Test domestic transaction with rounding edge case."""
    amount = Decimal('12.50')
    interchange_bps = 100  # 1%
    
    # 12.50 * 0.01 = 0.125 -> should round UP to 0.13 (HALF_UP)
    expected_fee = Decimal('0.13')
    actual_fee = compute_fees(amount, False, interchange_bps)
    
    assert actual_fee == expected_fee, f"Fee should be {expected_fee}, got {actual_fee}"
    
    # Settlement should be 12.50 - 0.13 = 12.37
    expected_settlement = Decimal('12.37')
    actual_settlement = settle_amount(amount, False, interchange_bps)
    
    assert actual_settlement == expected_settlement


def test_international_adds_fx_spread():
    """Test international transaction includes FX spread."""
    amount = Decimal('100.00')
    interchange_bps = 150  # 1.5%
    fx_spread_bps = 50     # 0.5%
    
    # Interchange: 100 * 0.015 = 1.50
    # FX spread: 100 * 0.005 = 0.50  
    # Total: 1.50 + 0.50 = 2.00
    expected_fee = Decimal('2.00')
    actual_fee = compute_fees(amount, True, interchange_bps, fx_spread_bps)
    
    assert actual_fee == expected_fee
    
    # Settlement: 100.00 - 2.00 = 98.00
    expected_settlement = Decimal('98.00')
    actual_settlement = settle_amount(amount, True, interchange_bps, fx_spread_bps)
    
    assert actual_settlement == expected_settlement


def test_small_amounts_exact_cents():
    """Test small amounts maintain precision."""
    amount = Decimal('0.99')
    interchange_bps = 290  # 2.9%
    
    # 0.99 * 0.029 = 0.02871 -> rounds to 0.03
    expected_fee = Decimal('0.03')
    actual_fee = compute_fees(amount, False, interchange_bps)
    
    assert actual_fee == expected_fee


def test_negative_or_zero_amount_rejected():
    """Test that zero and negative amounts are properly rejected."""
    
    # Zero amount should raise ValueError
    with pytest.raises(ValueError, match="Amount must be positive"):
        compute_fees(Decimal('0.00'), False, 100)
    
    with pytest.raises(ValueError, match="Amount must be positive"):
        settle_amount(Decimal('0.00'), False, 100)
    
    # Negative amount should raise ValueError  
    with pytest.raises(ValueError, match="Amount must be positive"):
        compute_fees(Decimal('-10.00'), False, 100)
    
    with pytest.raises(ValueError, match="Amount must be positive"):
        settle_amount(Decimal('-10.00'), False, 100)


def test_precision_edge_cases():
    """Test precision with large amounts and high basis points."""
    amount = Decimal('999999.99')
    interchange_bps = 150  # 1.5%
    
    # Should maintain precision: 999999.99 * 0.015 = 14999.99985 -> 15000.00
    expected_fee = Decimal('15000.00')
    actual_fee = compute_fees(amount, False, interchange_bps)
    
    assert actual_fee == expected_fee
    
    # Settlement precision
    expected_settlement = Decimal('984999.99')  # 999999.99 - 15000.00
    actual_settlement = settle_amount(amount, False, interchange_bps)
    
    assert actual_settlement == expected_settlement
