#==============================================================================
# Planet Max: Utility library file
#------------------------------------------------------------------------------
#add: forgaing+hunting, pastures,permissivity,
# 'frgWork''frgSource''pstWork''pstSource''prms'
#==============================================================================
# Constans
#------------------------------------------------------------------------------
biomes = { 
    "Sea":              {'color':'#2b53ff', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Rainforest":       {'color':'#005f11', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Monsoon":          {'color':'#008511', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Savannah":         {'color':'#8e852c', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Desert":           {'color':'#fefc01', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Cold desert":      {'color':'#C3D3EC', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Steppe":           {'color':'#c4a53b', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Subtropical":      {'color':'#BA6120', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Mediterranean":    {'color':'#D13A0F', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Marine":           {'color':'#86f4a2', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Humid":            {'color':'#25AB92', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Taiga":            {'color':'#9AB3AD', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Tundra":           {'color':'#B1C4C0', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Ice Caps":         {'color':'#bef9ff', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
    "Mountains":        {'color':'#656565', 'prmst': 0, 'agrWork':  0, 'agrSource':    0, 'frgWork':  0, 'frgSource':    0, 'pstrWork':  0, 'pstrSource':    0,'indWork':  0, 'indSource':    0},
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
def getResource(biome, resType, workForce, knowledge):
    "Returns produced resource of <resType> for respective <biome> and <workforce> density and <knowledge>"
    
    # Ak som neposlal ziadnu workforce, vysledok je 0 resources pri 0 efektivite a 0 unused workforce
    if workForce == 0: return (0, 0, 0)
    
    #--------------------------------------------------------------------------
    # Urcim skutocne vyuzitu pracovnu silu - je to maximalne vyuzitelna workoforce na biome
    #--------------------------------------------------------------------------
    maxForce    = getMaxWork(biome, resType)
    usedForce   = min(workForce, maxForce)
    
    # Urcim kolko workforce bolo alokovanych zbytocne a nebolo vyuzitych
    unUsedForce = workForce - usedForce
    
    #--------------------------------------------------------------------------
    # Vynos resource je pomerna cast USED workforce voci  max workforce krat miera znalosti
    #--------------------------------------------------------------------------
    res = getMaxResource(biome, resType) * (usedForce/maxForce) * knowledge
    
    #--------------------------------------------------------------------------
    # Efektivita je pomer vynosu a celkovej workforce (vratane nevyuzitej casti)
    #--------------------------------------------------------------------------
    eff = res / workForce
    
    return (res, eff, unUsedForce)

#------------------------------------------------------------------------------
def getMaxResource(biome, resType):
    "Returns maximum of resource can be harvested in the biome with respective biome"
    
    return biomes[biome][f'{resType}Source']
    
#------------------------------------------------------------------------------
def getMaxWork(biome, resType):
    "Returns maximum of workforce can be used in the biome with respective biome"
    
    return biomes[biome][f'{resType}Work']
    
#==============================================================================
# Color Functions
#------------------------------------------------------------------------------
def getBiomeColor(targetBiome):
    "Returns the colour of the biome" 
    
    for biome, info in biomes.items():
        if biome == targetBiome: return info['color']
        
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