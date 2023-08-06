import pandas as pd
import requests
from datapungibea import generalSettings 
from datapungibea import drivers

#TODO: improve delegation (want name of methods - getDatasetlis - to be _get... or be all in a loadedDrivers class etc.  These shouldn't be 
#      easy for user access)
# only initialize a driver if it's being called

class delegator(object):
    def __init__(self):
        self._lastCalledDriver = ''
        
    def __getattr__(self, called_method):

        self._lastCalledMethod = called_method

        def __raise_standard_exception():
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, called_method))
        
        def wrapper(*args, **kwargs):
            delegation_config = getattr(self, 'DELEGATED_METHODS', None)
            if not isinstance(delegation_config, dict):
                __raise_standard_exception()
            
            for delegate_object_str, delegated_methods in delegation_config.items():
                if called_method in delegated_methods:
                    break
            else:
                __raise_standard_error()
            
            delegate_object = getattr(self, delegate_object_str, None)
            
            self._lastCalledDriver = delegate_object #NOTE: could use this to track all loaded data etc.  For now, will only use 

            return(getattr(delegate_object, called_method)(*args, **kwargs))
    
        return(wrapper)


class data(delegator):
    '''
       the purpose of this class is to provide an environment where the shared data needed to establish a connection is loaded
       and to be a one stop shop of listing all available drivers.  
       :param connectionParameters: a dictionary with at least 'key', and 'url'
         {'key': 'your key', 'description': 'BEA data', 'url': 'https://apps.bea.gov/api/data/'} 
       :param userSettings: settings saved in the packge pointing to a json containing the connection parameters 
    '''
    DELEGATED_METHODS = {
        'getDatasetlist'             : ['datasetlist'],
        'getGetParameterList'        : ['getParameterList'],
        'getGetParameterValues'      : ['getParameterValues'],
        'getNIPA'                    : ['NIPA'],
        'getMNE'                     : ['MNE'],
        'getFixedAssets'             : ['fixedAssets'],
        'getITA'                     : ['ITA'],
        'getIIP'                     : ['IIP'],
        'getGDPbyIndustry'           : ['GDPbyIndustry'],  
        'getRegionalIncome'          : ['RegionalIncome'],  #deprecated, use Regional instead
        'getRegionalProduct'         : ['RegionalProduct'], #deprecated, use Regional instead
        'getInputOutput'             : ['InputOutput'],
        'getUnderlyingGDPbyIndustry' : ['UnderlyingGDPbyIndustry'],
        'getIntlServTrade'           : ['IntlServTrade'],
        'getRegional'                : ['Regional'],
        'getNIPAVintageTables'       : ['NIPAVintageTables'],
        'getNIPAVintage'             : ['NIPAVintage'],
        'getNIPASummary'             : ['NIPASummary'],
    }
    def __init__(self,connectionParameters = {}, userSettings = {}):
        self.__connectInfo = generalSettings.getGeneralSettings(connectionParameters = connectionParameters, userSettings = userSettings ) #TODO: inherit this, all drivers as well
        self._metadata = self.__connectInfo.packageMetadata
        self._help     = self.__connectInfo.datasourceOverview
        #load drivers:
        loadInfo = {'baseRequest' : self.__connectInfo.baseRequest, 'connectionParameters' : self.__connectInfo.connectionParameters}
        self.getDatasetlist                = drivers.getDatasetlist(**loadInfo)
        self.getGetParameterList           = drivers.getGetParameterList(**loadInfo)
        self.getGetParameterValues         = drivers.getGetParameterValues(**loadInfo)
        self.getNIPA                       = drivers.getNIPA(**loadInfo)
        self.getMNE                        = drivers.getMNE(**loadInfo)
        self.getFixedAssets                = drivers.getFixedAssets(**loadInfo)
        self.getITA                        = drivers.getITA(**loadInfo)
        self.getIIP                        = drivers.getIIP(**loadInfo)
        self.getGDPbyIndustry              = drivers.getGDPbyIndustry(**loadInfo)
        self.getRegionalIncome             = drivers.getRegionalIncome(**loadInfo)
        self.getRegionalProduct            = drivers.getRegionalProduct(**loadInfo)
        self.getInputOutput                = drivers.getInputOutput(**loadInfo)
        self.getUnderlyingGDPbyIndustry    = drivers.getUnderlyingGDPbyIndustry(**loadInfo)
        self.getIntlServTrade              = drivers.getIntlServTrade(**loadInfo)
        self.getRegional                   = drivers.getRegional(**loadInfo)
        self.getNIPAVintageTables          = drivers.getNIPAVintageTables(**loadInfo)
        self.getNIPAVintage                = drivers.getNIPAVintage(**loadInfo)
        self.getNIPASummary                = drivers.getNIPASummary(**loadInfo)
        #TODO: improve loading the drivers 
    
    def __str__(self):
        print(pd.DataFrame.from_dict(self.DELEGATED_METHODS,orient='index',columns=['Shortcut to Driver']))
        return('\nList of drivers and their shortcuts')

    def _clipcode(self):
        try:
            self._lastCalledDriver.clipcode()
        except:
            print('Get data using a driver first, eg: data.NIPA("T10101", verbose = True)')
    
    def _docDriver(self,driverName):
        '''
          Given the delegated method name, get the __doc__ of its class.  
          eg: _docDriver('NIPA') 
          returns the __doc__ of getNIPA.NIPA
        '''
        parentName = list(self.DELEGATED_METHODS.keys())[list(self.DELEGATED_METHODS.values()).index([driverName])]
        outhelp = getattr(getattr(self,parentName ),driverName).__doc__
        return(outhelp)
        




if __name__ == '__main__':
    #TODO TODO: Need to test MNE
    #TODO: harmonize the names - use the same as listed in the datasetlist, include the function entry names in the example below
    #TODO: transform this into tests
    
    d = data()
    print(d)

    #METADATA Functions:
    #print(d.datasetlist(verbose=True)['code'])
    #print(d.getParameterList('FixedAssets',verbose=True))   
    #print(d.getParameterValues('NIPA','Year',verbose=True))

    #print(d.NIPA('T10101',verbose=True)['code'])
    #print(d.NIPA('T10101'))
    #print(d.fixedAssets('FAAt101','X'))

    #print(d.ITA('BalCurrAcct','Brazil','A','2010'))

    #print(d.IIP(TypeOfInvestment='DebtSecAssets',Component='All',Frequency='All',Year='All'))    #NOTE: for IIP, either use All years of All TypeOfInvestment            
    #print(d.IIP('All','All','All','2010'))              

    #print(d.GDPbyIndustry('211','1','A','2018'))

    #RegionalIncome and RegionalOutput were deprecated - use Regional instead.
    #d.getRegionalIncome.RegionalIncome()
    #d.getRegionalProduct.RegionalProduct()

    #print(d.InputOutput(TableID='56',Year='2010'))                       
    #print(d.InputOutput('All','All'))                       
    #print(d.UnderlyingGDPbyIndustry('ALL','ALL','A','ALL',verbose=True)) #NOTE: PDF and query of getParameterValues say Frequency = Q, but actually it's A TODO: email BEA
    #print(d.IntlServTrade('ALL','ALL','ALL','AllCountries','All')) 
    
    #print(d.Regional('00000','1','SAGDP5N', '2015,2016')) 

    #print('Regional data test')
    #print(d.Regional('00000','1','SAGDP5N', 'All')) 
    #print(d.NIPAVintageTables())
    print(d.NIPA('T10101'))
    #print(d._docDriver('NIPA'))
    #print(d._docDriver('NIPASummary'))
    #print(d.NIPASummary('2018','Q'))
    #v = d.NIPAVintage(tableName = 'T10206', releaseDate = '2018-08-08')
    #print('table')
    #v = d.NIPAVintage(tableName = 'T10101', Title = 'Section 1',year = '2018', quarter ='Q1',vintage='Second')
    #print(v)