#==============================================================================
# Planet Max: Utility library file
#------------------------------------------------------------------------------

#==============================================================================
# Constans
#------------------------------------------------------------------------------
bioms = { 
       0: {'color':'#4faed0', 'agrWork':  0, 'agrSource':    0, 'indWork':  0, 'indSource':    0},
       
     100: {'color':'#66ff33', 'agrWork':170, 'agrSource': 1800, 'indWork':110, 'indSource':  400},
     200: {'color':'#5ceb2e', 'agrWork':180, 'agrSource': 2000, 'indWork':150, 'indSource':  450},
     300: {'color':'#52d629', 'agrWork':185, 'agrSource': 1900, 'indWork':180, 'indSource':  500},
     400: {'color':'#47c224', 'agrWork':175, 'agrSource': 1800, 'indWork':200, 'indSource':  600},
     500: {'color':'#38a31c', 'agrWork':120, 'agrSource': 1300, 'indWork':210, 'indSource':  800},
     600: {'color':'#298514', 'agrWork':100, 'agrSource': 1000, 'indWork':230, 'indSource': 1200},
     700: {'color':'#1a660d', 'agrWork':100, 'agrSource':  900, 'indWork':250, 'indSource': 3000},
     800: {'color':'#0a4705', 'agrWork':100, 'agrSource':  800, 'indWork':270, 'indSource': 4000},
     900: {'color':'#003300', 'agrWork':100, 'agrSource':  750, 'indWork':300, 'indSource': 4500},
     
    1000: {'color':'#333300', 'agrWork':110, 'agrSource':  700, 'indWork':310, 'indSource': 4700},
    1100: {'color':'#423300', 'agrWork':120, 'agrSource':  650, 'indWork':300, 'indSource': 4200},
    1200: {'color':'#523300', 'agrWork':130, 'agrSource':  600, 'indWork':290, 'indSource': 3700},
    1300: {'color':'#613300', 'agrWork':130, 'agrSource':  550, 'indWork':250, 'indSource': 2600},
    1400: {'color':'#803300', 'agrWork':120, 'agrSource':  500, 'indWork':220, 'indSource': 1400},
    1500: {'color':'#8f3300', 'agrWork':115, 'agrSource':  450, 'indWork':210, 'indSource': 1100},
    1600: {'color':'#9e3300', 'agrWork':110, 'agrSource':  400, 'indWork':200, 'indSource':  900},
    1700: {'color':'#ad3300', 'agrWork':100, 'agrSource':  370, 'indWork':190, 'indSource':  800},
    1800: {'color':'#bd3300', 'agrWork': 90, 'agrSource':  330, 'indWork':180, 'indSource':  700},
    1900: {'color':'#cc3300', 'agrWork': 95, 'agrSource':  300, 'indWork':170, 'indSource':  600},
    
    2000: {'color':'#d1470f', 'agrWork': 90, 'agrSource':  250, 'indWork':160, 'indSource':  500},
    2100: {'color':'#d6591d', 'agrWork': 80, 'agrSource':  200, 'indWork':150, 'indSource':  450},
    2200: {'color':'#da6c2b', 'agrWork': 50, 'agrSource':  150, 'indWork':140, 'indSource':  400},
    2300: {'color':'#df7e38', 'agrWork': 20, 'agrSource':  100, 'indWork':130, 'indSource':  370},
    2400: {'color':'#e8a354', 'agrWork': 20, 'agrSource':   50, 'indWork':120, 'indSource':  330},
    2500: {'color':'#edb562', 'agrWork':  0, 'agrSource':    0, 'indWork':110, 'indSource':  300},
    2600: {'color':'#f1c870', 'agrWork':  0, 'agrSource':    0, 'indWork':100, 'indSource':  250},
    2700: {'color':'#f6da7d', 'agrWork':  0, 'agrSource':    0, 'indWork': 90, 'indSource':  200},
    2800: {'color':'#faed8b', 'agrWork':  0, 'agrSource':    0, 'indWork': 90, 'indSource':  150},
    2900: {'color':'#ffff99', 'agrWork':  0, 'agrSource':    0, 'indWork': 90, 'indSource':  100},
    
    3000: {'color':'#ffffff', 'agrWork':  0, 'agrSource':    0, 'indWork':  0, 'indSource':    0}
}

#------------------------------------------------------------------------------
tribes = { 
       'Green Men'  : {'color'     : {'red':0,   'green':1,    'blue':0   }, 
                       'preference': {'agr':0.9, 'ind'  :0.05, 'war' :0.05},
                       'knowledge' : {'agr':0.1, 'ind'  :0.1,  'war' :0.1 },
                      },
       
       'Blue Indy'  : {'color'     : {'red':0,    'green':0,    'blue':1   }, 
                       'preference': {'agr':0.05, 'ind'  :0.9,  'war' :0.05},
                       'knowledge' : {'agr':0.1,  'ind'  :0.1,  'war' :0.1 },
                      },
       
       'Red Wariors': {'color'     : {'red':1,    'green':0,    'blue':0   }, 
                       'preference': {'agr':0.05, 'ind'  :0.05, 'war' :0.9 },
                       'knowledge' : {'agr':0.1,  'ind'  :0.1,  'war' :0.1 },
                      }
}

#==============================================================================
# Resource harvesting Functions
#------------------------------------------------------------------------------
def getResource(height, resType, workForce, knowledge):
    "Returns produced resource of <resType> for respective <height> and <workforce> density and <knowledge>"
    
    # Ak som neposlal ziadnu workforce, vysledok je 0 resources pri 0 efektivite a 0 unused workforce
    if workForce == 0: return (0, 0, 0)
    
    #--------------------------------------------------------------------------
    # Urcim skutocne vyuzitu pracovnu silu - je to maximalne vyuzitelna workoforce na biome
    #--------------------------------------------------------------------------
    maxForce    = getMaxWork(height, resType)
    usedForce   = min(workForce, maxForce)
    
    # Urcim kolko workforce bolo alokovanych zbytocne a nebolo vyuzitych
    unUsedForce = workForce - usedForce
    
    #--------------------------------------------------------------------------
    # Vynos resource je pomerna cast USED workforce voci  max workforce krat miera znalosti
    #--------------------------------------------------------------------------
    res = getMaxResource(height, resType) * (usedForce/maxForce) * knowledge
    
    #--------------------------------------------------------------------------
    # Efektivita je pomer vynosu a celkovej workforce (vratane nevyuzitej casti)
    #--------------------------------------------------------------------------
    eff = res / workForce
    
    return (res, eff, unUsedForce)

#------------------------------------------------------------------------------
def getMaxResource(height, resType):
    "Returns maximum of resource can be harvested in the biom with respective height"
    
    return bioms[height][f'{resType}Source']
    
#------------------------------------------------------------------------------
def getMaxWork(height, resType):
    "Returns maximum of workforce can be used in the biom with respective height"
    
    return bioms[height][f'{resType}Work']
    
#==============================================================================
# Color Functions
#------------------------------------------------------------------------------
def getBiomColor(height):
    "Returns of the biom" 
    
    for h, rec in bioms.items():
        if h >= height: return rec['color']
        
    # Ak nemam definovanu vysku
    return '#000000'

#------------------------------------------------------------------------------
def getTribesColor(tribes, denMax):
    "Returns color of the Tile based on density of different Tribes"
    
    # Ziskam mix color z populacii vsetkych Tribes
    mix = [0, 0, 0]
    
    for tribe in tribes.values():
        
        tribeDens = tribe['density']
    
        mix[0] += (tribe['color']['red'  ] * tribeDens)
        mix[1] += (tribe['color']['green'] * tribeDens)
        mix[2] += (tribe['color']['blue' ] * tribeDens)
        
    # Normalizujem mix na globalny denMax
    mix = normMax(mix, maxVal=denMax, norma=255)
    
    return rgbToHex(mix[0], mix[1], mix[2])

#------------------------------------------------------------------------------
def getPopulColor(tribes, denMax):
    "Returns color of the tile based on density of different prefferences"
    
    # Ziskam mix color z populacii vsetkych Tribes
    mix = [0, 0, 0]
    
    for tribe in tribes.values():
        
        tribeDens = tribe['density']
    
        mix[0] += tribeDens * tribe['preference']['war']    # Channel RED   = war
        mix[1] += tribeDens * tribe['preference']['agr']    # Channel GREEN = agr
        mix[2] += tribeDens * tribe['preference']['ind']    # Channel BLUE  = ind
        
    # Normalizujem mix na globalny denMax
    mix = normMax(mix, maxVal=denMax, norma=255)
    
    return rgbToHex(mix[0], mix[1], mix[2])

#------------------------------------------------------------------------------
def getKnowlColor(tribes, knowMax):
    "Returns color of the tile based on knowledge ratios"
    
    # Ziskam mix color z knowledges vsetkych Tribes
    mix = [0, 0, 0]
    
    for tribe in tribes.values():
        
        if tribe['density']>0:
        
            mix[0] += tribe['knowledge']['war']    # Channel RED   = war
            mix[1] += tribe['knowledge']['agr']    # Channel GREEN = agr
            mix[2] += tribe['knowledge']['ind']    # Channel BLUE  = ind
        
    # Normalizujem mix na globalny strop
    mix = normMax(mix, maxVal=knowMax, norma=255)
    
    if mix[0]>255 or mix[1]>255 or mix[2]>255:
        print(f'{knowMax} for {tribes}')
    
    return rgbToHex(mix[0], mix[1], mix[2])

#------------------------------------------------------------------------------
def getPrefsColor(tribes):
    "Returns color of the tile based on preferences ratios"
    
    # Ziskam mix color z preferences vsetkych Tribes
    mix    = [0, 0, 0]
    
    for tribe in tribes.values():
        
        if tribe['density']>0:
        
            mix[0] += tribe['preference']['war']    # Channel RED   = war
            mix[1] += tribe['preference']['agr']    # Channel GREEN = agr
            mix[2] += tribe['preference']['ind']    # Channel BLUE  = ind
            
    # Normalizujem mix na sumu vsetkych preferencii na tomto tile
    mix = normSum(mix, norma=255)
    
    if mix[0]>255 or mix[1]>255 or mix[2]>255:
        print(f'getPrefsColor for {tribes}')
    
    return rgbToHex(mix[0], mix[1], mix[2])

#------------------------------------------------------------------------------
def rgbToHex(r, g, b):
    
    return '#{:02X}{:02X}{:02X}'.format( round(r),round(g), round(b) )
   
#==============================================================================
# Math utilities
#------------------------------------------------------------------------------
def normMax(lst, maxVal, norma=1):
    "Normuje hodnoty listu aby maximalna hodnota <maxVal> bola <norma>"
    
    toRet = []

    # Nomralizujem na normu
    if maxVal > 0: 
        for i in range(len(lst)): toRet.append( lst[i] / maxVal * norma )
        
    else: toRet = list(lst)
    
    return toRet
    
#------------------------------------------------------------------------------
def normSum(lst, norma=1):
    "Normuje hodnoty listu aby suma hodnot bola <norma>"
    
    # Ziskam celkovu sumu mixu
    suma = 0
    for val in lst: suma += val
    
    # Ak je suma 0, vratim kopiu listu
    if suma==0: return list(lst)
    
    toRet = []

    # Normalizacia na normu
    for i in range(len(lst)): toRet.append( lst[i] / suma * norma )
    
    return toRet

#------------------------------------------------------------------------------
def normSumDic(dic, norma=1):
    "Normuje hodnoty dictionary aby suma values bola <norma>"
    
    toRet = {}

    # Ziskam list of values
    lst = [x for x in dic.values()]
    
    # Normujem list
    lst = normSum(lst, norma)
    
    # Updatnem dic na normovane values
    i = 0
    for key in dic.keys():
        
        toRet[key] = lst[i]
        i += 1
    
    return toRet

#==============================================================================
# Dict utilities
#------------------------------------------------------------------------------
def dSort(dic, reverse=False, key1=None):
    "Sorts dictionary by value. Secondary key is optional"
    
    if key1 is None: toRet = dict(sorted(dic.items(), key=lambda x: x[1],       reverse=reverse))
    else           : toRet = dict(sorted(dic.items(), key=lambda x: x[1][key1], reverse=reverse))
    
    return toRet

#------------------------------------------------------------------------------
def dRound(dic, precision=2, key1=None):
    "Rounds values in dictionary"
    
    toRet = {}
    
    for key, val in dic.items():
        toRet[key] = round(val, precision)
    
    return toRet

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------