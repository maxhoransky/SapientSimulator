#==============================================================================
# Planet Max: Utility library file
#------------------------------------------------------------------------------

#==============================================================================
# Constans - 1 tile is around 400 000 km*km
# Colour - 
# Permissivity - 
# typeWork - Maximal density of work force a tile cna absorb - ppl/km
# typeSource - The amount of resources a biome cna produce - resorurces/km
#------------------------------------------------------------------------------
biomes = { 
    "Sea":              {'color':'#2b53ff', 'prmst':   1, 'frgWork':    0, 'frgSource':    1, 'agrWork':   1, 'agrSource':    1, 'pstrWork':   1, 'pstrSource':    1,'indWork':   1, 'indSource':    1},
    "Rainforest":       {'color':'#005f11', 'prmst':   1, 'frgWork': 0.35, 'frgSource':    1, 'agrWork':  50, 'agrSource':  150, 'pstrWork':   1, 'pstrSource':    1,'indWork':  30, 'indSource':   60},
    "Monsoon":          {'color':'#008511', 'prmst':   1, 'frgWork': 0.05, 'frgSource':    1, 'agrWork': 180, 'agrSource': 2000, 'pstrWork': 150, 'pstrSource': 1300,'indWork': 100, 'indSource':  450},
    "Savannah":         {'color':'#8e852c', 'prmst':   1, 'frgWork': 0.95, 'frgSource':    1, 'agrWork': 120, 'agrSource': 1000, 'pstrWork':   1, 'pstrSource':    1,'indWork': 150, 'indSource':  450},
    "Desert":           {'color':'#fefc01', 'prmst':   1, 'frgWork': 0.36, 'frgSource':    1, 'agrWork':  90, 'agrSource':  250, 'pstrWork':   1, 'pstrSource':    1,'indWork': 160, 'indSource':  500},
    "Cold desert":      {'color':'#C3D3EC', 'prmst':   1, 'frgWork':    1, 'frgSource':    1, 'agrWork':   1, 'agrSource':    1, 'pstrWork':   1, 'pstrSource':    1,'indWork':  70, 'indSource':   90},
    "Steppe":           {'color':'#c4a53b', 'prmst':   1, 'frgWork':    1, 'frgSource':    1, 'agrWork': 140, 'agrSource': 1200, 'pstrWork':   1, 'pstrSource':    1,'indWork': 150, 'indSource':  450},
    "Subtropical":      {'color':'#BA6120', 'prmst':   1, 'frgWork':    1, 'frgSource':    1, 'agrWork':   1, 'agrSource':    1, 'pstrWork':   1, 'pstrSource':    1,'indWork':   1, 'indSource':    1},
    "Mediterranean":    {'color':'#D13A0F', 'prmst':   1, 'frgWork':    1, 'frgSource':    1, 'agrWork': 180, 'agrSource': 2000, 'pstrWork':   1, 'pstrSource':    1,'indWork': 150, 'indSource':  450},
    "Marine":           {'color':'#86f4a2', 'prmst':   1, 'frgWork':    1, 'frgSource': 1000, 'agrWork':  50, 'agrSource':  150, 'pstrWork': 100, 'pstrSource':  900,'indWork': 250, 'indSource': 3000},
    "Humid":            {'color':'#25AB92', 'prmst':   1, 'frgWork':    1, 'frgSource': 1550, 'agrWork':  20, 'agrSource':   70, 'pstrWork':  50, 'pstrSource':  400,'indWork': 300, 'indSource': 4000},
    "Taiga":            {'color':'#9AB3AD', 'prmst':   1, 'frgWork':    1, 'frgSource': 1325, 'agrWork':  20, 'agrSource':   50, 'pstrWork':   1, 'pstrSource':    1,'indWork': 200, 'indSource': 1250},
    "Tundra":           {'color':'#B1C4C0', 'prmst':   1, 'frgWork':    1, 'frgSource': 1325, 'agrWork':  30, 'agrSource':   80, 'pstrWork':   1, 'pstrSource':    1,'indWork': 250, 'indSource': 2500},
    "Ice Caps":         {'color':'#bef9ff', 'prmst':   1, 'frgWork':    1, 'frgSource':  750, 'agrWork':   1, 'agrSource':    1, 'pstrWork':   1, 'pstrSource':    1,'indWork':  50, 'indSource':  300},
    "Mountains":        {'color':'#656565', 'prmst':   1, 'frgWork':    1, 'frgSource':    1, 'agrWork': 115, 'agrSource':    1, 'pstrWork':   1, 'pstrSource':    1,'indWork': 350, 'indSource': 5000},
}

#------------------------------------------------------------------------------
tribes = { 
        'Hunters'   : {'color'      : {'red':0,    'green':0,    'blue':1   }, 
                       'preference' : {'frg':0.42, 'agr'  :0.30, 'pstr':0.05, 'ind':0.02, 'sci':0.01, 'rlg':0.01, 'war':0.15, 'trd':0.02, 'dpl':0.01},
                       'knowledge'  : {'frg':0.28, 'agr'  :0.25, 'pstr':0.15, 'ind':0.10, 'sci':0.01, 'rlg':0.01, 'war':0.20, 'trd':0.9 , 'dpl':0.01},
                        },
       
        'Fishermen' : {'color'      : {'red':0,    'green':1,    'blue':0   }, 
                       'preference' : {'frg':0.48, 'agr'  :0.02, 'pstr':0.02, 'ind':0.06, 'sci':0.01, 'rlg':0.01, 'war':0.30, 'trd':0.9, 'dpl':0.01},
                       'knowledge'  : {'frg':0.43, 'agr'  :0.10, 'pstr':0.10, 'ind':0.10, 'sci':0.01, 'rlg':0.01, 'war':0.10, 'trd':0.9, 'dpl':0.01},
                        },
        
        'Nomads'    : {'color'      : {'red':1,    'green':0,    'blue':0   }, 
                       'preference' : {'frg':0.68, 'agr'  :0.02, 'pstr':0.05, 'ind':0.03, 'sci':0.01, 'rlg':0.01, 'war':0.05, 'trd':0.18, 'dpl':0.01},
                       'knowledge'  : {'frg':0.68, 'agr'  :0.10, 'pstr':0.10, 'ind':0.10, 'sci':0.01, 'rlg':0.01, 'war':0.10, 'trd':0.19, 'dpl':0.01},
                        },
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
    
        mix[0] += tribeDens * (tribe['preference']['war'] + tribe['preference']['trd'] + tribe['preference']['dpl'])  /2  # Channel RED   = Interaction
        mix[1] += tribeDens * (tribe['preference']['frg'] + tribe['preference']['agr'] + tribe['preference']['pstr']) /2  # Channel GREEN = Food
        mix[2] += tribeDens * (tribe['preference']['ind'] + tribe['preference']['sci'] + tribe['preference']['rlg'])  /2  # Channel BLUE  = Society
        
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
        
            mix[0] += tribe['knowledge']['war'] + tribe['knowledge']['trd'] + tribe['knowledge']['dpl']  # Channel RED   = Interaction
            mix[1] += tribe['knowledge']['frg'] + tribe['knowledge']['agr'] + tribe['knowledge']['pstr'] # Channel GREEN = Food
            mix[2] += tribe['knowledge']['ind'] + tribe['knowledge']['sci'] + tribe['knowledge']['rlg']  # Channel BLUE  = Society
        
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
        
            mix[0] += tribe['preference']['war'] + tribe['preference']['trd'] + tribe['preference']['dpl']  # Channel RED   = Interaction
            mix[1] += tribe['preference']['frg'] + tribe['preference']['agr'] + tribe['preference']['pstr'] # Channel GREEN = Food
            mix[2] += tribe['preference']['ind'] + tribe['preference']['sci'] + tribe['preference']['rlg']  # Channel BLUE  = Society
            
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
