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
        self.revenueGrowthRate = 0 # our deteremined revenue growth rate
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

        # function calls to build out the model automatically
        self.calculateFCFE()
        self.calculateFCFEtoNetIncome()
        self.calculateRevenueGrowthRate()
        self.calculateNetIncomeMargins()
        self.projectRevenueGrowth()
        self.projectNetIncome()
        self.projectFCFE()
        self.calculateTerminalValue()
        self.calculatePresentValueOfFCFE()
        self.getValue()


    def calculateFCFE(self): # Calculate Free Cash Flow to Equity
        for ce, cffo in zip(self.capEx, self.cashFlowFromOperations):
            self.freeCashFlowToEquity.append(cffo+ce)

    def calculateFCFEtoNetIncome(self):
        for ni, fcfe in zip(self.netIncome, self.freeCashFlowToEquity):
            self.fcfeToNetIncome.append(fcfe/ni) # potentiall truncate / round this
        self.projectedFCFERate = min(self.fcfeToNetIncome) # ADJUST -- set to min for testing, explore other values such as average

    def calculateRevenueGrowthRate(self):
        # self.totalRevenue = totalRevenue
        growthRates = []
        for i in range(len(self.totalRevenue)-1):
            growthRates.append((self.totalRevenue[i+1]-self.totalRevenue[i])/self.totalRevenue[i])
        self.revenueGrowthRate = sum(growthRates) / len(growthRates) #REMOVE -- this is for testing

    def projectRevenueGrowth(self):
        # this whole function needs to be adjusted for automation
        self.projectedRevenue.append(self.totalRevenue[-2])
        self.projectedRevenue.append(self.totalRevenue[-1])
        self.projectedRevenue.append(self.projectedRevenue[1]*(1+self.revenueGrowthRate))
        self.projectedRevenue.append(self.projectedRevenue[2] * (1 + self.revenueGrowthRate))


    def calculateNetIncomeMargins(self):
        for ni, tr in zip(self.netIncome, self.totalRevenue):
            self.netIncomeMargins.append(ni / tr)
        self.netIncomeMarginsAverage = sum(self.netIncomeMargins) / len(self.netIncomeMargins)  # - 0.00884798731206756 REMOVE, this is for testing

    def projectNetIncome(self):
        for pr in self.projectedRevenue:
            self.projectedNetIncome.append(pr*self.netIncomeMarginsAverage)

    def projectFCFE(self):
        for pni in self.projectedNetIncome:
            self.projectedFCFE.append(pni*self.projectedFCFERate)

    def calculateTerminalValue(self):
        self.terminalValue = (self.projectedFCFE[-1]*(1+self.perpetualGrowthRate))/(self.requiredRateOfReturn-self.perpetualGrowthRate)

    def calculatePresentValueOfFCFE(self):
        i = 1
        discountFactors = []
        for fcfe in self.projectedFCFE:
            discountFactors.append((1+self.requiredRateOfReturn)**i)
            i += 1

        for fcfe, df in zip(self.projectedFCFE, discountFactors):
            self.presentValueOfFCFE.append(fcfe/df)

        # calculate the pv for terminal value and append
        self.presentValueOfFCFE.append(self.terminalValue/discountFactors[-1])

    def getValue(self):
        self.currentEstimatedValue = sum(self.presentValueOfFCFE)
        self.fairStockPrice = self.currentEstimatedValue / self.sharesOutstanding





