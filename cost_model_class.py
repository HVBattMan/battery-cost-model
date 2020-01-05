class CostModel:

    # Initializer:
    def __init__(self, cellInput, priceInput):
        self.cellInput = cellInput
        self.priceInput = priceInput
        # Put in a model ID somewhere???

    ## Section 1: Importing Cell Parameters
    # Now: define method to extract input parameters from input dictionaries
    def get_cellParameters(self):
        self.cellId = self.cellInput['cellId']
        self.cellName = self.cellInput['cellName']
        self.cellType = self.cellInput['cellType']
        self.npRatio = self.cellInput['npRatio']
        self.electrodeLength = self.cellInput['electrodeLength'] #cm
        self.electrodeWidth = self.cellInput['electrodeWidth'] #cm
        self.electrodeOneSidedArea = self.electrodeLength*self.electrodeWidth #cm
        
        self.catFormulaId = self.cellInput['catFormulaId'] #Chemical formula as dictionary
        self.catGravCapacity = self.cellInput['catGravCapacity'] #mAh/g
        self.catTotalLoading = self.cellInput['catTotalLoading'] #mg/cm^2
        self.catActiveFrac = self.cellInput['catActiveFrac']
        self.catBinderFrac = self.cellInput['catBinderFrac']
        self.catConductorFrac = self.cellInput['catConductorFrac']
    
        self.anGravCapacity = self.cellInput['anGravCapacity'] #mAh/g
        self.anActiveFrac = self.cellInput['anActiveFrac']
        self.anBinderFrac = self.cellInput['anBinderFrac']
        self.anConductorFrac = self.cellInput['anConductorFrac']

        self.alFoilThickness = self.cellInput['alFoilThickness'] #um
        self.cuFoilThickness = self.cellInput['cuFoilThickness'] #um

        self.elyte = self.cellInput['elyte']
        self.can = self.cellInput['can']
        self.separator = self.cellInput['separatorName']
        self.avgDischargeVoltage = self.cellInput['avgDischargeVoltage']


    ##################################################################################
    ## Section 2: Importing Price Data
    def get_prices(self):
        self.price_catActiveMaterial = self.priceInput['catActiveMaterial']
        self.price_catBinder = self.priceInput['catBinder']
        self.price_catConductor = self.priceInput['catConductor']

        self.price_anActiveMaterial = self.priceInput['anActiveMaterial']
        self.price_anBinder = self.priceInput['anBinder']
        self.price_anConductor = self.priceInput['anConductor']

        self.price_alFoil = self.priceInput['alFoil']
        self.price_cuFoil = self.priceInput['cuFoil']

        self.price_can = self.priceInput['can']
        self.price_separator = self.priceInput['sep']
        self.price_elyte = self.priceInput['elyte']

        self.price_cellManufacturing = self.priceInput['cellManufacturing']
        self.price_packIntegration = self.priceInput['packIntegration']

    ##################################################################################
    ## Section 3: Preliminary Calculations
    # Calculating total electrode material masses:
    def calc_allPreliminary(self):
        '''Calculates all preliminiary parameters necessary calculate costs.
        These parameters include electrode mass (total, active, conductor, binder),
        current collector masses, energy per cell, and cells per kWh.
        '''
        self.catTotalMass = (self.catTotalLoading*.001) * (2*self.electrodeOneSidedArea) #g
        self.catActiveMass = self.catTotalMass * self.catActiveFrac #g
        self.catCellCapacity = self.catActiveMass * self.catGravCapacity #mAh per cell
        self.anCellCapacity = self.npRatio * self.catCellCapacity #mah per cell
        self.anActiveMass = self.anCellCapacity / self.anGravCapacity #g
        self.anTotalMass = self.anActiveMass / self.anActiveFrac #g

        self.catBinderMass = self.catTotalMass * self.catBinderFrac
        self.catConductorMass = self.catTotalMass * self.catConductorFrac
        self.anBinderMass = self.anTotalMass * self.anBinderFrac
        self.anConductorMass = self.anTotalMass * self.anConductorFrac

        al_density = 2.70 #g/cm^3
        cu_density = 8.96 #g/cm^3
        self.mass_alFoil = self.electrodeOneSidedArea * (self.alFoilThickness/1e4) * al_density #g
        self.mass_cuFoil = self.electrodeOneSidedArea * (self.cuFoilThickness/1e4) * cu_density #g
        self.separatorLength = self.electrodeLength #cm

        '''Calculates the energy per cell (in Wh) given the cell capacity (in mAh)
        and average discharge voltage (in V). 
        Note that this uses cathode capacity for the calculation, given that the 
        cathode has a lower capacity than the anode (because the N-P ratio should 
        always be greater than 1).
        The parameter cellsPerKwh is number of cells required to have 1kWh of energy.
        '''
        self.cellEnergy = (self.catCellCapacity/1000) * self.avgDischargeVoltage
        self.cellsPerKwh = 1000/self.cellEnergy

    ##################################################################################
    ## Section 4: Cost Calculations
    # All cost calculations here are on a cost per cell basis.
    def calc_allCosts(self):
        self.cost_catActiveMaterial = (self.catActiveMass/1000) * self.price_catActiveMaterial
        self.cost_catBinder = (self.catBinderMass/1000) * self.price_catBinder
        self.cost_catConductor = (self.catConductorMass/1000) * self.price_catConductor

        self.cost_anActiveMaterial = (self.anActiveMass/1000) * self.price_anActiveMaterial
        self.cost_anBinder = (self.anBinderMass/1000) * self.price_anBinder
        self.cost_anConductor = (self.anConductorMass/1000) * self.price_anConductor

        self.cost_alFoil = (self.mass_alFoil/1000) * self.price_alFoil
        self.cost_cuFoil = (self.mass_cuFoil/1000) * self.price_cuFoil
        self.cost_can = self.price_can
        # To calculate separator cost:
        # First calculate price per cm of length
        # Divide by 500 for 500m per separtor roll, then by 100 for 100cm per m
        pricePerCm_separator = self.price_separator / (500 * 100)
        self.cost_separator = pricePerCm_separator * self.electrodeLength

        self.cost_elyte = self.price_elyte

        self.cost_cellManufacturing = self.price_cellManufacturing
        self.cost_packIntegration = self.price_packIntegration

    def return_allCosts_cellBasis(self):
        '''Returns cost of each component on a per cell basis.
        '''
        self.get_cellParameters()
        self.get_prices()
        self.calc_allPreliminary()
        self.calc_allCosts()
        return {
            "Cathode Active Material": self.cost_catActiveMaterial,
            "Cathode Binder": self.cost_catBinder,
            "Cathode Conductor": self.cost_catConductor,
            "Anode Active Material": self.cost_anActiveMaterial,
            "Anode Binder": self.cost_anBinder,
            "Anode Conductor": self.cost_anConductor,
            "Aluminum Foil": self.cost_alFoil,
            "Copper Foil": self.cost_cuFoil,
            "Can": self.cost_can,
            "Separator": self.cost_separator,
            "Electrolyte": self.cost_elyte,
            "Manufacturing": self.cost_cellManufacturing,
            "Pack Integration": self.cost_packIntegration
        }

    def return_allCosts_kwhBasis(self):
        '''Returns cost of each component on a per-kWh basis.

        This is calculated by multiplying each of the per-cell cost basis
        by the number of cells required to have 1kWh of energy.
        '''
        self.get_cellParameters()
        self.get_prices()
        self.calc_allPreliminary()
        self.calc_allCosts()
        return {
            "Cathode Active Material": self.cost_catActiveMaterial * self.cellsPerKwh,
            "Cathode Binder": self.cost_catBinder * self.cellsPerKwh,
            "Cathode Conductor": self.cost_catConductor * self.cellsPerKwh,
            "Anode Active Material": self.cost_anActiveMaterial * self.cellsPerKwh,
            "Anode Binder": self.cost_anBinder * self.cellsPerKwh,
            "Anode Conductor": self.cost_anConductor * self.cellsPerKwh,
            "Aluminum Foil": self.cost_alFoil * self.cellsPerKwh,
            "Copper Foil": self.cost_cuFoil * self.cellsPerKwh,
            "Can": self.cost_can * self.cellsPerKwh,
            "Separator": self.cost_separator * self.cellsPerKwh,
            "Electrolyte": self.cost_elyte * self.cellsPerKwh,
            "Manufacturing": self.cost_cellManufacturing * self.cellsPerKwh,
            "Pack Integration": self.cost_packIntegration * self.cellsPerKwh
        }