# Mercury Fintech CI Demo - Live Test

🤖 **This PR triggers Nova CI-Rescue to fix financial calculation bugs**

## 🐛 Expected Failures

The tests should fail due to these financial bugs:

1. **Float precision loss** in `compute_fees()` 
2. **Wrong rounding strategy** (banker's vs HALF_UP)
3. **Missing validation** for zero amounts

## 🔧 Nova Should Fix

Nova will automatically:
- Replace float conversion with proper Decimal math
- Fix rounding to use HALF_UP instead of banker's rounding  
- Add proper validation to reject zero/negative amounts

## 📊 Watch the CI

Check the Actions tab to see Nova in action fixing fintech bugs! 🏦✨
