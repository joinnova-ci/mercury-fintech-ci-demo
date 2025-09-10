# Mercury Fintech Demo - Nova CI-Rescue

🏦 **Fintech fee calculation bugs fixed automatically by Nova CI-Rescue**

This repository demonstrates Nova's ability to fix subtle financial calculation bugs that are common in fintech applications.

## 🐛 Intentional Bugs

The `mercury_fees.py` module contains three realistic financial bugs:

1. **Float Precision Loss** 💸
   - Uses `float()` conversion in fee calculations
   - Causes precision errors in financial math
   - Should use `Decimal` throughout

2. **Wrong Rounding Strategy** 🎯
   - Uses Python's `round()` (banker's rounding)
   - Financial systems typically need `HALF_UP` rounding
   - Affects fee calculations at 0.5 cent boundaries

3. **Missing Validation** 🚫
   - Allows zero amounts in `settle_amount()`
   - Should reject zero/negative amounts consistently
   - Creates security/business logic gaps

## 🧪 Test Suite

Comprehensive tests in `test_mercury_fees.py` verify:
- ✅ Proper rounding behavior (HALF_UP)
- ✅ International transaction FX spreads
- ✅ Small amount precision handling
- ✅ Zero/negative amount rejection
- ✅ Large amount precision maintenance

## 🤖 Nova CI Integration

When you create a PR with failing tests, Nova will:

1. **Analyze** the financial calculation failures
2. **Fix** the precision, rounding, and validation bugs
3. **Verify** all tests pass with the fixes
4. **Create** a reviewable PR with the corrected code

## 🚀 Try It Yourself

```bash
# Clone and test locally
git clone <this-repo>
cd mercury-fintech-ci-demo

# Install dependencies
pip install pytest

# See the failing tests
pytest -v

# Let Nova fix them
pip install nova-ci-rescue
export OPENAI_API_KEY="your-key"
nova fix --ci "pytest -v"
```

## 📊 Expected Results

**Before Nova:**
```
FAILED test_mercury_fees.py::test_domestic_fee_and_settlement_rounding
FAILED test_mercury_fees.py::test_negative_or_zero_amount_rejected  
FAILED test_mercury_fees.py::test_precision_edge_cases
```

**After Nova:**
```
✅ test_mercury_fees.py::test_domestic_fee_and_settlement_rounding PASSED
✅ test_mercury_fees.py::test_international_adds_fx_spread PASSED
✅ test_mercury_fees.py::test_small_amounts_exact_cents PASSED  
✅ test_mercury_fees.py::test_negative_or_zero_amount_rejected PASSED
✅ test_mercury_fees.py::test_precision_edge_cases PASSED
```

## 💡 Why This Matters

Financial bugs can be costly:
- **Precision errors** → Revenue leakage or compliance issues
- **Wrong rounding** → Inconsistent fee calculations  
- **Missing validation** → Security vulnerabilities

Nova catches and fixes these automatically, ensuring your fintech code is robust and compliant.

---

**Powered by [Nova CI-Rescue](https://github.com/joinnova-ci/nova-ci-rescue)** 🚀
