class DiscountedCashFlow:
    def __init__(self,cashFlowFromOperations, capEx, netIncome, totalRevenue, requiredRateOfReturn, perpetualGrowthRate, sharesOutstanding):
        # variables to instantiate the class
        self.cashFlowFromOperations = cashFlowFromOperations
        self.capEx = capEx
        self.netIncome = netIncome
        self.totalRevenue = totalRevenue
        self.requiredRateOfReturn = requiredRateOfReturn  # This could be CAPM or WACC or some other number depending on your investment goals
        self.perpetualGrowthRate = perpetualGrowthRate
        self.sharesOutstanding = sharesOutstanding

        # variables to hold key information across methods
        self.freeCashFlowToEquity = [] # cash flow from operations - capEx
        self.fcfeToNetIncome = [] # free cash flow to equity / net income (represented as a percent value)
        self.revenueGrowthRate = 0 # our determined revenue growth rate
        self.projectedRevenue = []
        self.projectedFCFERate = 0 # Note FCFE --> "Free Cash Flow to Equity"
        self.projectedFCFE = []
        self.netIncomeMargins = []
        self.netIncomeMarginsAverage = 0
        self.projectedNetIncome = []
        self.presentValueOfFCFE = []
        self.terminalValue = 0
        self.currentEstimatedValue = 0  # "Today's Value"
        self.fairStockPrice = 0  # "Fair Value of Equity" on a per share basis


    def calculateFCFE(self): # Calculate Free Cash Flow to Equity
        for ce, cffo in zip(self.capEx, self.cashFlowFromOperations):
            self.freeCashFlowToEquity.append(cffo+ce)

    def calculateFCFEtoNetIncome(self, nonZeroMin):
        for ni, fcfe in zip(self.netIncome, self.freeCashFlowToEquity):
            self.fcfeToNetIncome.append(round(fcfe/ni, 2))
        # whether or not to use the non zero min or the average
        if nonZeroMin:
            self.projectedFCFERate = round(min(i for i in self.fcfeToNetIncome if i > 0), 2)
        else:
            self.projectedFCFERate = round(sum(self.fcfeToNetIncome) / len(self.fcfeToNetIncome), 2)

    def calculateRevenueGrowthRate(self):
        # self.totalRevenue = totalRevenue
        growthRates = []
        for i in range(len(self.totalRevenue)-1):
            growthRates.append((self.totalRevenue[i+1]-self.totalRevenue[i])/self.totalRevenue[i])
        self.revenueGrowthRate = round(sum(growthRates) / len(growthRates), 2)

    def projectRevenueGrowth(self, withAnalyst):
        # If analyst projections are used ### NOTE: Only the last two values may be analyst projections ###
        if withAnalyst:
            self.projectedRevenue.append(self.totalRevenue[-2])
            self.projectedRevenue.append(self.totalRevenue[-1])
            self.projectedRevenue.append(round(self.projectedRevenue[1]*(1+self.revenueGrowthRate)))
            self.projectedRevenue.append(round(self.projectedRevenue[2] * (1 + self.revenueGrowthRate)))
        # If analyst projections are not used
        else:
            self.projectedRevenue.append(round(self.totalRevenue[-1] * (1 + self.revenueGrowthRate)))
            for i in range(3):
                self.projectedRevenue.append(round(self.projectedRevenue[i] * (1 + self.revenueGrowthRate)))

    def calculateNetIncomeMargins(self):
        for ni, tr in zip(self.netIncome, self.totalRevenue):
            self.netIncomeMargins.append(round(ni/tr, 2))
        self.netIncomeMarginsAverage = round(sum(self.netIncomeMargins) / len(self.netIncomeMargins), 2)

    def projectNetIncome(self):
        for pr in self.projectedRevenue:
            self.projectedNetIncome.append(round(pr*self.netIncomeMarginsAverage))

    def projectFCFE(self):
        for pni in self.projectedNetIncome:
            self.projectedFCFE.append(round(pni*self.projectedFCFERate))

    def calculateTerminalValue(self):
        self.terminalValue = round((self.projectedFCFE[-1]*(1+self.perpetualGrowthRate))/(self.requiredRateOfReturn-self.perpetualGrowthRate))

    def calculatePresentValueOfFCFE(self):
        i = 1
        discountFactors = []
        for fcfe in self.projectedFCFE:
            discountFactors.append((1+self.requiredRateOfReturn)**i)
            i += 1

        for fcfe, df in zip(self.projectedFCFE, discountFactors):
            self.presentValueOfFCFE.append(round(fcfe/df))

        # calculate the pv for terminal value and append
        self.presentValueOfFCFE.append(round(self.terminalValue/discountFactors[-1]))

    def getValue(self):
        self.currentEstimatedValue = sum(self.presentValueOfFCFE)
        self.fairStockPrice = round(self.currentEstimatedValue / self.sharesOutstanding, 2)

    # function calls to build out the model automatically
    def buildModel(self, fcfcToNetIncomeMin=True, analystProjections=True):
        self.calculateFCFE()
        self.calculateFCFEtoNetIncome(fcfcToNetIncomeMin) # False to use average over non zero min
        self.calculateRevenueGrowthRate()
        self.calculateNetIncomeMargins()
        self.projectRevenueGrowth(analystProjections) # True to use analyst projections
        self.projectNetIncome()
        self.projectFCFE()
        self.calculateTerminalValue()
        self.calculatePresentValueOfFCFE()
        self.getValue()





