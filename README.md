# Discounted Cash Flow Analysis
A program to build a DCF model, with the ultimate goal of offering the ability to perform DCFs simultaneously on a given set of tickers.

The DCF class is intentionally designed to be highly modular, but require very minimal interation on the part of the user.
Yes the whole thing could have been built out in a single function, but due to the high senstivity of each parameter in the model, this style on constrction
allows for easy debugging and modification.

Bellow are a series of example inputs from AAPL, index 0 represents time period 1 and so on.
cashFlowFromOperationsT = [81266000, 66231000, 64225000, 77434000] # Cash Flow Statemenet line item
capExT = [-11247000, -12734000, -12451000, -13313000] # Capital Expeditures: Cash Flow Statement line item
netIncomeT = [53394000, 45687000, 48351000, 59531000] # Income
totalRevenueT = [233715000, 215639000, 229234000, 265595000, 257310000, 269680000]

Note last two values in totalRevenueT are analyst projections in this case, this isn't great and 
I'm looking to elimate the need for outside analyst ratings

```python
cashFlowFromOperationsT = [81266000, 66231000, 64225000, 77434000] # Cash Flow Statemenet line item
capExT = [-11247000, -12734000, -12451000, -13313000] # Capital Expeditures: Cash Flow Statement line item
netIncomeT = [53394000, 45687000, 48351000, 59531000] # Income
totalRevenueT = [233715000, 215639000, 229234000, 265595000, 257310000, 269680000]

testDCF = DiscountedCashFlow(cashFlowFromOperationsT, capExT, netIncomeT, totalRevenueT, 8.4/100, 2.5/100, 4601075)
testDCF.buildModel()

#This is the value you're after
print(testDCF.fairStockPrice)
```