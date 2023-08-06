import datapungibea as dpbea 
import time
import pandas as pd
import os


def executeCode(stringIn):
    '''
      auxiliary function for tests: get the requests code as a string and try to execute it.
    '''
    try:
        exec(stringIn+'\n')      #exec('print("hi")') #
        return(dict( codeRun = True, codeOutput = locals()['df_output']   ))   #try to output the dataframe called df_output
    except:
        try:
            exec(stringIn)  #if no dataframe called output, try to see it at least can exec the code
            return(dict(codeRun = True, codeOutput = pd.DataFrame([])))
        except:
            return(dict(codeRun = False, codeOutput = pd.DataFrame([])))

# start  the driver - used by all tests
def startDriver(cmdopt):
    if not cmdopt == "":
        connectionParameters = {"key": cmdopt, "url": "https://apps.bea.gov/api/data/"}
    else:
        connectionParameters = {}
    dataBea = dpbea.data(connectionParameters)
    return(dataBea)    

# content of test_sample.py
def test_startDriver(cmdopt):
    dataBea = startDriver(cmdopt)
    assert dataBea

def test_datasetlist(cmdopt):
    '''
      test the datasetlist BEA dataset
    '''
    dataBea = dataBea = startDriver(cmdopt)
    driver   = dataBea.datasetlist(verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200               #test if connection was stablished
    assert not driver['dataFrame'].empty                      #cleaned up output is not empty
    assert execCode['codeRun']                                #try to execute the code.
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  
    #print('datasetlist driver is working (Request OK, data cleaned, can run code snippet, snippet agrees with request)!')

def test_getParameterList(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.getParameterList('FixedAssets',verbose=True)  
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']                   #try to execute the code.
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  

def test_getParameterValues(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.getParameterValues('NIPA','Year',verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']                   #try to execute the code.
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  

def test_NIPA(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.NIPA('T10101','Q','2010',verbose=True,includeIndentations=False)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']                   #try to execute the code.
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  

def test_fixedAssets(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.fixedAssets('FAAt101','2013',verbose=True)   #try all years 
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']           #try to execute the code.   
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  

def test_ITA(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.ITA('BalCurrAcct','Brazil','A','2010',verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']            #try to execute the code.   
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the      

def test_IIP(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.IIP(TypeOfInvestment='DebtSecAssets',Component='All',Frequency='All',Year='2010',verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']        #try to execute the code.       
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the      

def test_GDPbyIndustry(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.GDPbyIndustry('211','1','A','2018',verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']          #try to execute the code.   
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the          

def test_InputOutput(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.InputOutput(TableID='56',Year='2010',verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']            #try to execute the code.       
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  

def test_UnderlyingGDPbyIndustry(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.UnderlyingGDPbyIndustry('ALL','ALL','A','2014',verbose=True)   #try all years and check line 40788
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']           #try to execute the code.       
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  

def test_IntlServTrade(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.IntlServTrade('ALL','ALL','ALL','AllCountries','All',verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']          #try to execute the code.       
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the  

def test_IntlServTrade(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.IntlServTrade('ALL','ALL','ALL','AllCountries','All',verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']         #try to execute the code.       

def test_Regional(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.Regional('00000','1','SAGDP5N', 'All',verbose=True)
    execCode = executeCode(driver['code']) 
    assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'].empty         #cleaned up output is not empty
    assert execCode['codeRun']           #try to execute the code.       
    assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the      

def test_NIPASummary(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.NIPASummary('2012','Q',verbose=True)
    #execCode = executeCode(driver['code']) 
    #assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'][0].empty         #cleaned up output is not empty  
    #assert execCode['codeRun']           #try to execute the code.       
    #assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the      

def test_NIPAVintage(cmdopt):
    dataBea = startDriver(cmdopt)
    driver = dataBea.NIPAVintage(tableName = 'T10101', Title = 'Section 1',year = '2018', quarter ='Q1',vintage='Second',verbose = True)
    execCode = executeCode(driver['code']) 
    #assert driver['request'].status_code == 200  #test if connection was stablished
    assert not driver['dataFrame'][0].empty         #cleaned up output is not empty
    #assert execCode['codeRun']           #try to execute the code.       
    #assert execCode['codeOutput'].equals(driver['dataFrame']) #test if the output of the code equals the output of the      


if __name__ == '__main__':
    test_answer('')
    #test_IIP()
    #test_datasetlist()
    #test_getParameterList()
    #test_getParameterValues()
    #test_NIPA()
    #test_fixedAssets()