#==============================================================================
# Siqo class TTile
#------------------------------------------------------------------------------
import planet_lib    as lib
import random

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_SEP   = 50*''

#==============================================================================
# package's variables
#------------------------------------------------------------------------------
_DENS_GROWTH     = 0.2   # Koeficient prirodzeneho prirastku populacie

_STRES_MIN       = 0.1   # Zakladna miera stresu populacie
_STRES_MAX       = 0.8   # Maximalna miera stresu populacie
_RLG_STRESS_AVERT= 0.2   # Koeficient znizovania stresu kvoli nabozenstvu
_STRES_EMIG      = 0.2   # Koeficient emigracie kvoli stresu

_STRES_WAR       = 0.8   # Koeficient stresu zo smrti vojakov
_STRES_WAR_END   = 0.7   # Koeficient ako velmi zvacsuje stres sancu zrusit vojnu

_DISP_MAX        = 10.0 # Maximum possible Disposition
_DISP_TREND_MAX  = 0.2  # Maximalna a minimalana hodnota trendu
_DISP_DIPL       = 1.4  # Koeficient zvysovania dispozicie pomocou diplomacie
_DISP_STRESS     = 0.6  # Koeficient znizovania dispozicie kvoli stresu

_KNOW_GROWTH     = 1.05  # Koeficient zvysenia knowledge ak jej tribe venuje pozornostS
_KNOW_GROWTH_SCI = 0.05  # How much does science help speed up research
_KNOW_LIMIT      = 0.3   # Hranica pozornosti, pri ktorej sa knowledge zvysuje
_KNOW_DECAY      = 0.95  # Koeficient zabudania knowledge ak jej tribe nevenuje pozornost
_KNOW_MIN        = 0.1   # Minimalna hodnota znalosti uplnych divochov

_PREF_UNUS_LIMIT =   5   # Ak je unused workforce vyssia ako tato hranica, zapricini zmenu preferencii
_PREF_BY_UNUS    = 0.1   # Zmena preferncie podla unused workforce pre biome
_PREF_BY_EFF     = 0.1   # Zmena preferencie podla efektivity vyuzitia pracovnej sily (preferencie)
_PREF_MIN        = 0.05  # Minimalna hodnota preferencie pre resType

_WAR_RSRS_EFF    = 0.6   # Efektivita kolko zdrojov ziska vyherna armada
_WAR_KILL_EFF    = 0.4   # Efektivita  o kolko sa znizi densita po vojne

#==============================================================================
# TTile
#------------------------------------------------------------------------------
class TTile:

    #==========================================================================
    # Static variables & methods
    #--------------------------------------------------------------------------
    journal    = None        # Globalny journal
    tiles      = {}          # Zoznam vsetkych tiles  {tileId: tileObj}

    #--------------------------------------------------------------------------
    @staticmethod
    def getDenMax(period):
        "Returns global maximum of population desnsity in the Tile"
        
        denMax = 0
        
        # Prejdem vsetky tiles
        for tile in TTile.tiles.values():
        
            tileSum = 0
            
            # Prejdem vsetky tribe na tile pre konkretnu periodu
            for tribe in tile.history[period]['tribes'].values():
                tileSum += tribe['density']
                
            if tileSum > denMax: denMax = tileSum

        return denMax
    
    #--------------------------------------------------------------------------
    @staticmethod
    def getKnowMax(period):
        "Returns global maximum of knowledge in the Tile"
        
        knowMax = 0
        
        # Prejdem vsetky tiles
        for tile in TTile.tiles.values():
        
            tileKnwSum = 0
            
            # Prejdem vsetky tribe na tile pre konkretnu periodu
            for tribe in tile.history[period]['tribes'].values():
                tileKnwSum += sum(tribe['knowledge'].values())

            if tileKnwSum > knowMax: knowMax = tileKnwSum

        return knowMax
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, tileId, biome="Sea"):
        "Calls constructor of TTile and initialise it with empty data"

        self.journal.I('TTile.constructor')
        
        self.tileId     = tileId          # ID tile
        self.row        = 0               # Pozicia tile - riadok
        self.col        = 0               # Pozicia tile - stlpec
        self.neighs     = []              # Zoznam geografickych susedov tile [tileObj]

        self.biome      = biome          # Biome of the tile
        self.history    = [{'period':0, 'densTot':0, 'tribes':{}}] # Historia tile
        
        # Zaradim novu tile do zoznamu tiles
        self.tiles[self.tileId] = self

        self.journal.O(f'{self.tileId}.constructor: done')
        
    #--------------------------------------------------------------------------
    def __str__(self):
        "Prints info about this Tile"

        toRet = ''
        for line in self.info()['msg']: toRet += line +'\n'

        return toRet

    #==========================================================================
    # Reports for users
    #--------------------------------------------------------------------------
    def info(self):
        "Returns info about this Tile"

        msg = []
        msg.append(f'Tile ID   :{self.tileId}'   )
        msg.append(f'biome    :{self.biome}'   )
        msg.append(f'row       :{self.row}'   )
        msg.append(f'col       :{self.col}'   )
        msg.append(_SEP)
        msg.append('Neighbours:')

        for neighObj in self.neighs:
            msg.append(f'{neighObj.tileId}    :{neighObj.biome}'   )
            
        for actPer in self.history:
            
            msg.append(f"Period = {actPer['period']}")
            
            for tribeId, tribeObj in actPer['tribes'].items():
                
                if tribeObj['density'] > 0:
                
                    dens = round(tribeObj['density'], 1)
                    prefs = lib.dRound(tribeObj['preference'], 2)
                    knows = lib.dRound(tribeObj['knowledge' ], 2)
                 
                    if 'resrs' in tribeObj.keys() : resrs  = lib.dRound(tribeObj['resrs' ], 2)
                    else                          : resrs  = {}
                
                    if 'unus'  in tribeObj.keys() : unus   = lib.dRound(tribeObj['unus'  ], 2)
                    else                          : unus   = {}
                
                    if 'effs'  in tribeObj.keys() : effs   = lib.dRound(tribeObj['effs'  ], 2)
                    else                          : effs   = {}
                
                    if 'denses' in tribeObj.keys(): denses = lib.dRound(tribeObj['denses'], 2)
                    else                          : denses = {}
                
                    msg.append(f"{tribeId.ljust(12)}: prefs={prefs} knowledge={knows} density={dens} resrs={resrs} unus={unus} effs={effs} denses={denses}")
            
        return {'res':'OK', 'msg':msg}

    #==========================================================================
    # API for GUI
    #--------------------------------------------------------------------------
    def clear(self):
        "Clear history of this Tile"
    
        self.journal.I(f'{self.tileId}.clear:')
        
        self.history.clear()
        self.history.append( {'period':0, 'densTot':0, 'tribes':{}} )
        
        self.journal.O(f'{self.tileId}.clear: done')
        
    #--------------------------------------------------------------------------
    def reset(self):
        "Resets history of this Tile into state in period 0"
    
        self.journal.I(f'{self.tileId}.reset:')
        
        # Vratim historiu ju do zakladneho stavu
        begState = self.history[0]
        self.history.clear()
        self.history.append(begState)
        
        self.journal.O(f'{self.tileId}.reset: done')
        
    #--------------------------------------------------------------------------
    def getPeriodTrbStr(self, period):
        "Returns string describing tribes in this Tile"
        
        tribes = self.getPeriod(period)['tribes']
        
        toRet = 'Density:'
        for tribeId, tribeObj in tribes.items(): 
            if tribeObj['density']>0:
                toRet += f" {tribeId}:{round(tribeObj['density'], 2)}"
    
        if toRet=='Density:': toRet = 'No tribe here'
        
        return toRet
    
    #--------------------------------------------------------------------------
    def getPeriodPopStr(self, period, short):
        "Returns string describing population with different preferences in this Tile"
        
        tribes = self.getPeriod(period)['tribes']
        
        frg = 0
        agr = 0
        pstr= 0
        ind = 0
        sci = 0
        rlg = 0
        war = 0
        trd = 0
        dpl = 0

        #----------------------------------------------------------------------
        # Spocitam jednotlive druhy populacie
        #----------------------------------------------------------------------
        for tribeObj in tribes.values(): 
            
            frg += tribeObj['density'] * tribeObj['preference']['frg']
            agr += tribeObj['density'] * tribeObj['preference']['agr']
            pstr+= tribeObj['density'] * tribeObj['preference']['pstr']
            ind += tribeObj['density'] * tribeObj['preference']['ind']
            sci += tribeObj['density'] * tribeObj['preference']['sci']
            rlg += tribeObj['density'] * tribeObj['preference']['rlg']
            war += tribeObj['density'] * tribeObj['preference']['war']
            trd += tribeObj['density'] * tribeObj['preference']['trd']
            dpl += tribeObj['density'] * tribeObj['preference']['dpl']
            
        if (frg+agr+pstr+ind+sci+rlg+war+trd+dpl) == 0: toRet = 'No tribe here'
        elif short == False: 
            toRet = f"Total population consists of people focusing on:\nForage:{round(frg, 2)} Agriculture:{round(agr, 2)} Cattle:{round(pstr, 2)}\nIndustry:{round(ind, 2)} Science:{round(sci, 2)} Religion:{round(rlg, 2)}\nWar:{round(war, 2)} Trade:{round(trd, 2)} Diplomacy:{round(dpl, 2)}"
        elif short == True:
            toRet = f"People focusing on: Food:{round(frg + agr + pstr, 2)}, Development:{round(ind + sci + rlg, 2)}, Interaction:{round(war + trd + dpl, 2)}"
        return toRet

    #--------------------------------------------------------------------------
    def getPeriodKnwStr(self, period, short):
        "Returns string describing knowledge in this Tile"
        
        tribes = self.getPeriod(period)['tribes']
        
        if short == False:
            toRet = 'The amount of knowledge each tribe in this tile posseses:'
            for tribeId, tribeObj in tribes.items():
                if tribeObj['density']>0:
                    toRet += f"\n{tribeId}:\nForage={round(tribeObj['knowledge']['frg'], 2)}, Agriculture={round(tribeObj['knowledge']['agr'], 2)}, Cattle={round(tribeObj['knowledge']['pstr'], 2)}\nIndustry={round(tribeObj['knowledge']['ind'], 2)}, Science={round(tribeObj['knowledge']['sci'], 2)}, Religion={round(tribeObj['knowledge']['rlg'], 2)}\nWar={round(tribeObj['knowledge']['war'], 2)}, Trade={round(tribeObj['knowledge']['trd'], 2)}, Diplomacy={round(tribeObj['knowledge']['dpl'], 2)}\n---------------------------------------------------------"
            
            if toRet=='The amount of knowledge each tribe in this tile posseses:': toRet = 'No tribe here'
        
        elif short == True:
            fodKnw = 0
            devKnw = 0
            intKnw = 0

            for tribeId, tribeObj in tribes.items():
                if tribeObj['density']>0:
                    fodKnw += tribeObj['knowledge']['frg'] + tribeObj['knowledge']['agr'] + tribeObj['knowledge']['pstr']
                    devKnw += tribeObj['knowledge']['ind'] + tribeObj['knowledge']['sci'] + tribeObj['knowledge']['rlg']
                    intKnw += tribeObj['knowledge']['war'] + tribeObj['knowledge']['trd'] + tribeObj['knowledge']['dpl']
            
            if fodKnw + devKnw + intKnw == 0 : toRet = 'No tribe here'
            else : toRet = f"Knowledge in tile: Food:{round(fodKnw,2)}, Development:{round(devKnw,2)}, Interaction:{round(intKnw,2)}"
        return toRet
    
    #--------------------------------------------------------------------------
    def getPeriodPrfStr(self, period, short):
        "Returns string describing preferences in this Tile"
        
        tribes = self.getPeriod(period)['tribes']
        
        if short == False:
            toRet = 'Preferences tribes in this tile have about resources:'
            for tribeId, tribeObj in tribes.items(): 
                if tribeObj['density']>0:
                    toRet += f"\n{tribeId}:\nForage={round(tribeObj['preference']['frg'], 2)}, Agriculture={round(tribeObj['preference']['agr'], 2)}, Cattle={round(tribeObj['preference']['pstr'], 2)}\nIndustry={round(tribeObj['preference']['ind'], 2)}, Science={round(tribeObj['preference']['sci'], 2)}, Religion={round(tribeObj['preference']['rlg'], 2)}\nWar={round(tribeObj['preference']['war'], 2)}, Trade={round(tribeObj['preference']['trd'], 2)}, Diplomacy={round(tribeObj['preference']['dpl'], 2)}\n---------------------------------------------------------"
    
            if toRet=='Preferences tribes in this tile have about resources:': toRet = 'No tribe here'
        
        elif short == True:
            fodPrf = 0
            devPrf = 0
            intPrf = 0

            for tribeId, tribeObj in tribes.items():
                if tribeObj['density']>0:
                    fodPrf += tribeObj['preference']['frg'] + tribeObj['preference']['agr'] + tribeObj['preference']['pstr']
                    devPrf += tribeObj['preference']['ind'] + tribeObj['preference']['sci'] + tribeObj['preference']['rlg']
                    intPrf += tribeObj['preference']['war'] + tribeObj['preference']['trd'] + tribeObj['preference']['dpl']
            
            if fodPrf + devPrf + intPrf == 0 : toRet = 'No tribe here'
            else : toRet = f"Preference in tile: Food:{round(fodPrf,2)}, Development:{round(devPrf,2)}, Interaction:{round(intPrf,2)}"
        return toRet
    
    #--------------------------------------------------------------------------
    def getPeriodDispText(self, period):
        "Returns list describing Dispo between all pairs of Tribes in this Tile"
        
        toRet = []
        tribes = self.getPeriod(period)['tribes']
        
        #----------------------------------------------------------------------
        # Prejdem cez vsetky tribe na Tile
        #----------------------------------------------------------------------
        for tribeId, tribeObj in tribes.items(): 
            
            if tribeObj['density']>0:
                
                toRet.append(f"Tribe {tribeId:15} ({tribeObj['density']:06.3})")
                
                #--------------------------------------------------------------
                # Prejdem vsetkych adversaries                
                #--------------------------------------------------------------
                if 'disp' in tribeObj.keys():
                    
                    for advId, advObj in tribeObj['disp'].items(): 
                        dispString = f"     Relations - {advId:15}: Disp = {advObj['disp']:06.3} | Trend = {advObj['trend']:06.3}"

                        if tribeObj['wars'][advId] == True:
                            dispString += f" | War = Y"
                        else:
                            dispString += f" | War = N"

                        if tribeObj['trades'][advId] == True:
                            dispString += f" | Trade = Y"
                        else:
                            dispString += f" | Trade = N"

                        toRet.append(dispString)
                        
                        
                        
                    toRet.append("----------------------------------------------------")
            
        return toRet

    #--------------------------------------------------------------------------
    def simPeriod(self, period):
        "Simulates respective period for this Tile based on previous period values"
        
        self.journal.I(f'{self.tileId}.simPeriod: period {period}')
        
        #----------------------------------------------------------------------
        # Vyberiem z historie predchadzajucu periodu a inicializujem simulovanu periodu
        #----------------------------------------------------------------------
        lastPeriod = self.getPeriod(period-1)
        simPeriod  = self.getPeriod(period  )
        
        #----------------------------------------------------------------------
        # Vyriesim zber resurces vratane trades a war podla stavu v lastPeriod
        #----------------------------------------------------------------------
        self.getResource(lastPeriod)

        #----------------------------------------------------------------------
        # Vyriesim ubytok/prirastok populacie na zaklade ziskanych resources a emigracie
        #----------------------------------------------------------------------
        self.evaluateDensity(lastPeriod, simPeriod)

        self.evaluateDisposition(lastPeriod, simPeriod)

        #----------------------------------------------------------------------
        # Vyriesim zmenu knowledge/preferenci Tribe 
        #----------------------------------------------------------------------
        self.changePrefsAndKnowledge(lastPeriod, simPeriod)

        self.journal.O(f'{self.tileId}.simPeriod: done')

    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def getResource(self, lastPeriod):
        "Evaluates resources per Tribe based on preferences"

        self.journal.I(f'{self.tileId}.getResource:')
        
        #----------------------------------------------------------------------
        # Zber AGR urody a IND vyrobkov jednotlivymi tribe
        #----------------------------------------------------------------------
        for tribeId, tribeObj in lastPeriod['tribes'].items():
            
            # Vlastnosti tribe
            dens  = tribeObj['density'   ]
            prefs = tribeObj['preference']
            knows = tribeObj['knowledge' ]
            
            # Pripravim si nove prazdne resources, efektivitu a unused workforce
            resrs = {'frg':0, 'agr':0, 'pstr':0, 'ind':0, 'sci':0, 'rlg':0, 'war':0, 'trd':0, 'dpl':0}
            effs  = {'frg':0, 'agr':0, 'pstr':0, 'ind':0, 'sci':0, 'rlg':0, 'war':0, 'trd':0, 'dpl':0}
            unus  = {'frg':0, 'agr':0, 'pstr':0, 'ind':0, 'sci':0, 'rlg':0, 'war':0, 'trd':0, 'dpl':0}
            
            #------------------------------------------------------------------
            # Zber FRG resources - zlomok podla pomeru density Tribe voci celkovej densite na Tile
            #------------------------------------------------------------------
            (res, eff, unu) = lib.getResource( self.biome, resType='frg', workForce=dens*prefs['frg'], knowledge=knows['frg'] )
            
            resrs['frg'] = res
            effs ['frg'] = eff
            unus ['frg'] = unu
            
            #------------------------------------------------------------------
            # Zber AGR resources - zlomok podla pomeru density Tribe voci celkovej densite na Tile
            #------------------------------------------------------------------
            (res, eff, unu) = lib.getResource( self.biome, resType='agr', workForce=dens*prefs['agr'], knowledge=knows['agr'] )
            
            resrs['agr'] = res
            effs ['agr'] = eff
            unus ['agr'] = unu

            #------------------------------------------------------------------
            # Zber PSTR resources - zlomok podla pomeru density Tribe voci celkovej densite na Tile
            #------------------------------------------------------------------
            (res, eff, unu) = lib.getResource( self.biome, resType='pstr', workForce=dens*prefs['pstr'], knowledge=knows['pstr'] )
            
            resrs['pstr'] = res
            effs ['pstr'] = eff
            unus ['pstr'] = unu
            
            #------------------------------------------------------------------
            # Zber IND resources - zlomok podla pomeru density Tribe voci celkovej densite na Tile
            #------------------------------------------------------------------
            (res, eff, unu) = lib.getResource( self.biome, resType='ind', workForce=dens*prefs['ind'], knowledge=knows['ind'] )
            resrs['ind'] = res
            effs ['ind'] = eff
            unus ['ind'] = unu

            #------------------------------------------------------------------
            # Zapisem priebezne vypocty o ziskanych resources a efektivite do lastPeriod Tile
            #------------------------------------------------------------------
            tribeObj['resrs'] = resrs
            tribeObj['unus' ] = unus
            tribeObj['effs' ] = effs
            
        #----------------------------------------------------------------------
        self.journal.O()
    
    #--------------------------------------------------------------------------
    def getTradeResource(self, lastPeriod):
        "Evaluates resources per Tribe based on war state"
        #----------------------------------------------------------------------
        # Vyhodnotim zmeny pre vsetky Tribes na Tile ktore maju nenulovu densitu
        # disposition_between_two_populations_on_a_tile  = time * (diplomacy_pick_one_at_random + random_trend - stress)
        #----------------------------------------------------------------------
        dispositionPairs = []
        usedIDs = []
        
        tribeWarEffs = {}

        for tribeId, tribeObj in lastPeriod['tribes'].items():
            if tribeObj['density'] > 0:
                usedIDs.append(tribeId)
                for recTribeId, recTribeObj in lastPeriod['tribes'].items():
                    if recTribeId not in usedIDs and recTribeObj['density'] > 0:
                        pairTuple = (tribeId, recTribeId)
                        dispositionPairs.append(pairTuple)
        if dispositionPairs != []:
            for pair in dispositionPairs:
                if pair[1] in lastPeriod['tribes'][pair[0]]['disp'] and lastPeriod['tribes'][pair[0]]['wars'][pair[1]] == True:

                    armySize = [lastPeriod['tribes'][pair[0]]['density'] * lastPeriod['tribes'][pair[0]]['preference']['war'], lastPeriod['tribes'][pair[1]]['density'] * lastPeriod['tribes'][pair[1]]['preference']['war']]
                    armyPower = [armySize[0] * (lastPeriod['tribes'][pair[0]]['knowledge']['war'] + 1), armySize[1] * (lastPeriod['tribes'][pair[1]]['knowledge']['war'] + 1)]

                    #print(armySize, armyPower)
                    if armyPower[0] > armyPower [1]:
                        ResrsGained = (armyPower[0] - armyPower[1]) * _WAR_RSRS_EFF
                        lastPeriod['tribes'][pair[0]]['resrs']['war'] += ResrsGained
                        lastPeriod['tribes'][pair[1]]['resrs']['war'] -= ResrsGained
                        tribeWarEffs[pair[0]][0] += ResrsGained / (armySize[0] - armySize[1])
                        tribeWarEffs[pair[1]][0] += 1 / (ResrsGained / (armySize[0] - armySize[1]))

                    elif armyPower[1] > armyPower [0]:
                        ResrsGained = (armyPower[1] - armyPower[0]) * _WAR_RSRS_EFF
                        lastPeriod['tribes'][pair[1]]['resrs']['war'] += ResrsGained
                        lastPeriod['tribes'][pair[0]]['resrs']['war'] -= ResrsGained
                        tribeWarEffs[pair[1]][0] += ResrsGained / (armySize[1] - armySize[0])
                        tribeWarEffs[pair[0]][0] += 1 / (ResrsGained / (armySize[1] - armySize[0]))

                    tribeWarEffs[pair[0]][1] += 1
                    tribeWarEffs[pair[1]][1] += 1
                        
        for tribeId, tribeEff in tribeWarEffs.items():
            lastPeriod['tribes'][tribeId]['effs']['war'] = tribeEff[0] / tribeEff[1]

        #----------------------------------------------------------------------
        self.journal.O()
    
    #--------------------------------------------------------------------------
    def evaluateDensity(self, lastPeriod, simPeriod):
        "Evaluates population density per Tribe based on earned resources and emigration"

        self.journal.I(f'{self.tileId}.evaluateDensity:')
        period = lastPeriod['period']+1

        #----------------------------------------------------------------------
        # Pripravim pocty ludi co zomru z vojny na 0
        #----------------------------------------------------------------------
        tribeWarDeaths = {}
        for tribeId in lastPeriod['tribes'].keys():
            tribeWarDeaths[tribeId] = 0
        #----------------------------------------------------------------------
        # Vyhodnotim kolko ludi zomrie vo vojnach
        #----------------------------------------------------------------------
        dispositionPairs = []
        usedIDs = []

        tribeWarEffs = {}

        for tribeId, tribeObj in lastPeriod['tribes'].items():
            if tribeObj['density'] > 0:
                usedIDs.append(tribeId)
                for recTribeId, recTribeObj in lastPeriod['tribes'].items():
                    if recTribeId not in usedIDs and recTribeObj['density'] > 0:
                        pairTuple = (tribeId, recTribeId)
                        dispositionPairs.append(pairTuple)
        if dispositionPairs != []:
            for pair in dispositionPairs:
                if pair[1] in lastPeriod['tribes'][pair[0]]['disp'] and lastPeriod['tribes'][pair[0]]['wars'][pair[1]] == True:
                    armySize = [lastPeriod['tribes'][pair[0]]['density'] * lastPeriod['tribes'][pair[0]]['preference']['war'], lastPeriod['tribes'][pair[1]]['density'] * lastPeriod['tribes'][pair[1]]['preference']['war']]
                    armyPower = [armySize[0] * (lastPeriod['tribes'][pair[0]]['knowledge']['war'] + 1), armySize[1] * (lastPeriod['tribes'][pair[1]]['knowledge']['war'] + 1)]
                    #print(armySize, armyPower)
                    if armyPower[0] > armyPower [1]:
                        # Vyhercovia vojny zoberu zdroje porazenim
                        ResrsGained = (armyPower[0] - armyPower[1]) * _WAR_RSRS_EFF
                        lastPeriod['tribes'][pair[0]]['resrs']['war'] += ResrsGained
                        lastPeriod['tribes'][pair[1]]['resrs']['war'] -= ResrsGained
                        tribeWarEffs[pair[0]][0] += ResrsGained / (armySize[0] - armySize[1])
                        tribeWarEffs[pair[1]][0] += 1 / (ResrsGained / (armySize[0] - armySize[1]))
                        # Vyhercovia vojny zabiju porazenych
                        tribeWarDeaths[pair[1]] = (armyPower[1] - armyPower[0]) / (lastPeriod['tribes'][pair[1]]['knowledge']['war'] + 1) * _WAR_KILL_EFF * -1

                    elif armyPower[1] > armyPower [0]:
                        # Vyhercovia vojny zoberu zdroje porazenim
                        ResrsGained = (armyPower[1] - armyPower[0]) * _WAR_RSRS_EFF
                        lastPeriod['tribes'][pair[1]]['resrs']['war'] += ResrsGained
                        lastPeriod['tribes'][pair[0]]['resrs']['war'] -= ResrsGained
                        tribeWarEffs[pair[1]][0] += ResrsGained / (armySize[1] - armySize[0])
                        tribeWarEffs[pair[0]][0] += 1 / (ResrsGained / (armySize[1] - armySize[0]))
                        # Vyhercovia vojny zabiju porazenych
                        tribeWarDeaths[pair[0]] = (armyPower[0] - armyPower[1]) / (lastPeriod['tribes'][pair[0]]['knowledge']['war'] + 1) * _WAR_KILL_EFF * -1
                    
                    tribeWarEffs[pair[0]][1] += 1
                    tribeWarEffs[pair[1]][1] += 1

            #print(tribeWarDeaths)


        for tribeId, tribeEff in tribeWarEffs.items():
            lastPeriod['tribes'][tribeId]['effs']['war'] = tribeEff[0] / tribeEff[1]
            
        #----------------------------------------------------------------------

        #----------------------------------------------------------------------
        # Vyhodnotim zmeny populacie pre vsetky Tribes na Tile
        #----------------------------------------------------------------------
        for tribeId, tribeObj in lastPeriod['tribes'].items():
            
            # Vstupne hodnoty
            resrTot = tribeObj['resrs']['frg'] + tribeObj['resrs']['agr'] + tribeObj['resrs']['pstr'] +  tribeObj['resrs']['ind'] + tribeObj['resrs']['trd'] + tribeObj['resrs']['war']

            # Zacinam simulaciu s povodnym obyvatelstvom z predchadzajucej periody
            densSim = tribeObj['density']

            #------------------------------------------------------------------
            # Opravim populaciu o prirodzeny prirastok
            #------------------------------------------------------------------
            densGrowth = _DENS_GROWTH * densSim
            densSim   += densGrowth

            #------------------------------------------------------------------
            # Ubytok populacie nasledkom vojny
            #------------------------------------------------------------------
            densSim -= tribeWarDeaths[tribeId]

            #------------------------------------------------------------------
            # Ubytok populacie nasledkom nedostatku zdrojov 1 res per 1 clovek/km2
            #------------------------------------------------------------------
            if densSim > resrTot: 
                
                # Zistim, kolko populcie zomrie  kvoli vojne
                densWar   = tribeWarDeaths[tribeId] * _STRES_WAR
                
                # Zistim, kolko populcie zomrie lebo nema vyprodukovane zdroje
                densHunger = densSim - resrTot
                
                # Miera stresu je pomer zomretej populacie voci povodnej populacii
                strsTot = (_STRES_MIN + ((densWar+densHunger) / densSim))  / ((1 + (tribeObj['prefs']['rlg'] * tribeObj['know']['rlg'])) * _RLG_STRESS_AVERT)

                if strsTot > _STRES_MAX: strsTot = _STRES_MAX
                
                # Miera hladu je pomer hladom zomretej populacie voci povodnej populacii
                hungerTotal = (densHunger / densSim)

                # Zostane zit len tolko ludi kolko ma zdroje
                densSim   = resrTot
                    
            else:
                strsTot    = _STRES_MIN
                hungerTotal = 0
                densHunger = 0
                densWar    = 0
                
            #------------------------------------------------------------------
            # Emigracia do vsetkych susednych Tiles
            #------------------------------------------------------------------
            densEmig = 0
            for neighTile in self.neighs:
                
                #--------------------------------------------------------------
                # Ak susedna Tile nie je more
                #--------------------------------------------------------------
                if neighTile.biome != "Sea":
                
                    #----------------------------------------------------------
                    #Hustota tohto Tribeu u susedov v last period
                    #----------------------------------------------------------
                    densNeigh = neighTile.getPeriodDens(period-1, tribeId)
                
                    #----------------------------------------------------------
                    # Ak je u nas vacsia densita naseho Tribe ako u susedov
                    #----------------------------------------------------------
                    if densSim > densNeigh: 
                    
                        #------------------------------------------------------
                        # Emigracia do susedneho tribe
                        #------------------------------------------------------
                        emig      = _STRES_EMIG * strsTot * (densSim-densNeigh)
                        densEmig += emig
                    
                        #------------------------------------------------------
                        # Ziskam vlastnosti svojho tribe v susednej Tile
                        #------------------------------------------------------
                        neighTribe = neighTile.getPeriodTribe(period, tribeId, tribeObj)

                        #------------------------------------------------------
                        # Pridam emigrovanych do susednej Tile v sim period
                        #------------------------------------------------------
                        neighTribe['density'] += emig

            #------------------------------------------------------------------
            # Ubytok populacie nasledkom celkove emigracie
            #------------------------------------------------------------------
            densSim -= densEmig

            #------------------------------------------------------------------
            # Zapisem priebezne vypocty do lastPeriod
            #------------------------------------------------------------------
            
            tribeObj['denses'] = {'densSim'   : densSim   ,
                                  'densGrowth': densGrowth,
                                  'densHunger': densHunger,
                                  'densWar'   : densWar   ,
                                  'densEmig'  : densEmig  ,
                                  'stres'     : strsTot   ,
                                  'hunger'    : hungerTotal
                                  }
            #------------------------------------------------------------------
            # Ak tribe prezil, zapisem ho do simulovanej periody s densSim
            #------------------------------------------------------------------
            if densSim > 0:
                
                simPeriodTribe = self.getPeriodTribe(period, tribeId, tribeObj)
                simPeriodTribe['density'] += densSim

            print(tribeObj['denses']['stres'])

        #------------------------------------------------------------------
        self.journal.O()

    #--------------------------------------------------------------------------
    def evaluateDisposition(self, lastPeriod, simPeriod):
        #----------------------------------------------------------------------
        # Vyhodnotim zmeny pre vsetky Tribes na Tile ktore maju nenulovu densitu
        # disposition_between_two_populations_on_a_tile  = time * (diplomacy_pick_one_at_random + random_trend - stress)
        #----------------------------------------------------------------------
        dispositionPairs = []
        usedIDs = []

        for tribeId, tribeObj in lastPeriod['tribes'].items():
            if tribeObj['denses']['densSim'] > 0:
                usedIDs.append(tribeId)
                for recTribeId, recTribeObj in lastPeriod['tribes'].items():
                    if recTribeId not in usedIDs and recTribeObj['denses']['densSim'] > 0:
                        pairTuple = (tribeId, recTribeId)
                        dispositionPairs.append(pairTuple)
        if dispositionPairs != []:
            for pair in dispositionPairs:
                if pair[1] not in lastPeriod['tribes'][pair[0]]['disp']:
                    lastDisp = {'disp':0,'trend': random.uniform(-_DISP_TREND_MAX, _DISP_TREND_MAX)}
                    lastWar = False
                    lastTrade = False
                    # Creates a Tuple, first int is 0 and is the base disposition
                    # The second int should be random from -1 to 1 and is the random trend
                else:
                    lastDisp = lastPeriod['tribes'][pair[0]]['disp'][pair[1]]
                    lastWar = lastPeriod['tribes'][pair[0]]['wars'][pair[1]]
                    lastTrade = lastPeriod['tribes'][pair[0]]['trades'][pair[1]]
                
                # Change disposition by the random trend
                #print("Start - " + str(lastDisp['disp']) )
                lastDisp['disp'] += lastDisp['trend']
                #print("Rand - " + str(lastDisp['disp'])  )
                # Change disposition by the stress of both tribes
                lastDisp['disp'] -= lastPeriod['tribes'][pair[0]]['denses']['stres'] * _DISP_STRESS
                lastDisp['disp'] -= lastPeriod['tribes'][pair[1]]['denses']['stres'] * _DISP_STRESS
                #print("Stress - "+ str(lastDisp['disp'])  )
                # Change disposition by the diplomacy of one of the two tribes
                baseDisp = lastDisp['disp']
                randTribe = random.randint(0, 1)
                lastDisp['disp'] += ((1 + lastPeriod['tribes'][pair[randTribe]]['preference']['dpl']) * (1 + lastPeriod['tribes'][pair[randTribe]]['knowledge']['dpl']) - 1) * _DISP_DIPL

                #print("Dipl - "+ str(lastDisp['disp']) + '\n')

                if lastDisp['disp'] > _DISP_MAX:
                    lastDisp['disp'] = _DISP_MAX
                if lastDisp['disp'] < _DISP_MAX * -1:
                    lastDisp['disp'] = _DISP_MAX * -1

                simPeriod['tribes'][pair[0]]['disp'][pair[1]] = lastDisp
                simPeriod['tribes'][pair[1]]['disp'][pair[0]] = lastDisp

                lastWar = self.evaluateWarEvent(lastPeriod, simPeriod, lastDisp['disp'], lastWar, (lastPeriod['tribes'][pair[0]]['denses']['stres'] + lastPeriod['tribes'][pair[1]]['denses']['stres']) / 2)
                lastTrade = self.evaluateTradeEvent(lastPeriod, simPeriod, lastDisp['disp'], lastTrade)

                simPeriod['tribes'][pair[0]]['wars'][pair[1]] = lastWar
                simPeriod['tribes'][pair[1]]['wars'][pair[0]] = lastWar
                simPeriod['tribes'][pair[0]]['trades'][pair[1]] = lastTrade
                simPeriod['tribes'][pair[1]]['trades'][pair[0]] = lastTrade
                
                #print("-----------------------------------------------------------\n", lastPeriod['tribes'][pair[0]]['effs'])
                lastPeriod['tribes'][pair[0]]['effs']['dpl'] = lastDisp['disp'] / (lastPeriod['tribes'][pair[0]]['denses']['densSim'] * lastPeriod['tribes'][pair[0]]['preference']['dpl'])
                lastPeriod['tribes'][pair[1]]['effs']['dpl'] = lastDisp['disp'] / (lastPeriod['tribes'][pair[1]]['denses']['densSim'] * lastPeriod['tribes'][pair[1]]['preference']['dpl'])
                #print(lastPeriod['tribes'][pair[0]]['effs'])

                lastPeriod['tribes'][pair[0]]['preference']['dpl'] *= (baseDisp/(1 + lastPeriod['tribes'][pair[0]]['preference']['war'])) + 1
                lastPeriod['tribes'][pair[1]]['preference']['dpl'] *= (baseDisp/(1 + lastPeriod['tribes'][pair[1]]['preference']['war'])) + 1

                #effs['sci'] = knowGain / (tribeObj['denses']['densSim'] * prefs['sci'])
                #prefs['sci'] *= (knowBaseGain/(1 + prefs['rlg'])) + 1

                
        #------------------------------------------------------------------     
        self.journal.O()
    
    #--------------------------------------------------------------------------
    def evaluateWarEvent(self, lastPeriod, simPeriod, disp, lastWar, stres):
        if lastWar == False:
            if disp < 0:
                chance = lib.power(disp * -1)
                randomVal = random.uniform(0, 1)
                if chance > randomVal:
                    lastWar = True

        elif lastWar == True:
            if disp > 0:
                chance = lib.power(disp)
                randomVal = random.uniform(0, 1)
                if chance > randomVal:
                    lastWar = False
            elif stres > 0.5:
                chance = lib.power((stres - 0.5) * 33.333333 * _STRES_WAR_END)
                randomVal = random.uniform(0, 1)
                if chance > randomVal:
                    lastWar = False

        return lastWar
        
    #--------------------------------------------------------------------------
    def evaluateTradeEvent(self, lastPeriod, simPeriod ,disp, lastTrade):
        if lastTrade == False:
            if disp > 0:
                chance = lib.power(disp)
                randomVal = random.uniform(0, 1)
                if chance > randomVal:
                    lastTrade = True

        elif lastTrade == True:
            if disp < 0:
                chance = lib.power(disp * -1)
                randomVal = random.uniform(0, 1)
                if chance > randomVal:
                    lastTrade = False
        
        return lastTrade

    #--------------------------------------------------------------------------
    def changePrefsAndKnowledge(self, lastPeriod, simPeriod):
        "Evaluates changes in preferences and knowledge"
        
        #----------------------------------------------------------------------
        # Vyhodnotim zmeny pre vsetky Tribes na Tile ktore maju nenulovu densitu
        #----------------------------------------------------------------------
        for tribeId, tribeObj in lastPeriod['tribes'].items():

            if tribeObj['denses']['densSim'] > 0:
                
                #--------------------------------------------------------------
                # Zizkam cielovu periodu pre tribId kam budem zapisovat vysledky
                #--------------------------------------------------------------
                simPeriodTribe = simPeriod['tribes'][tribeId]

                #--------------------------------------------------------------
                # Zmena knowledge podla miery preferencii = pozornosti, ktory tribe venoval oblasti
                #--------------------------------------------------------------
                knowBaseGain = 0
                knowGain = 0

                know = self.knowledgeChange(tribeObj, 'frg')          
                simPeriodTribe['knowledge']['frg'] = know[0]
                knowBaseGain += know[1]
                knowGain += know[2]

                know = self.knowledgeChange(tribeObj, 'agr')
                simPeriodTribe['knowledge']['agr'] = know[0]
                knowBaseGain += know[1]
                knowGain += know[2]

                know = self.knowledgeChange(tribeObj, 'pstr')
                simPeriodTribe['knowledge']['pstr'] = know[0]
                knowBaseGain += know[1]
                knowGain += know[2]

                know = self.knowledgeChange(tribeObj, 'ind')
                simPeriodTribe['knowledge']['ind'] = know[0]
                knowBaseGain += know[1]
                knowGain += know[2]

                know = self.knowledgeChange(tribeObj, 'sci')
                simPeriodTribe['knowledge']['sci'] = know[0]
                knowBaseGain += know[1]
                knowGain += know[2]

                know = self.knowledgeChange(tribeObj, 'rlg')
                simPeriodTribe['knowledge']['rlg'] = know[0]
                knowBaseGain += know[1]
                knowGain += know[2]

                know = self.knowledgeChange(tribeObj, 'war')
                simPeriodTribe['knowledge']['war'] = know[0]
                knowBaseGain += know[1]
                knowGain += know[2]
                
                know = self.knowledgeChange(tribeObj, 'trd')
                simPeriodTribe['knowledge']['trd'] = know[0]
                knowBaseGain += know[1]
                knowGain += know[2]

                know = self.knowledgeChange(tribeObj, 'dpl')
                simPeriodTribe['knowledge']['dpl'] = know[0]
                knowBaseGain += know[1]
                knowGain += know[2]
                
                #--------------------------------------------------------------
                # Preberanie knowledge od vyspelejsich tribe
                #--------------------------------------------------------------
                
                #--------------------------------------------------------------
                # Zmena preferencii tribe
                #--------------------------------------------------------------
                
                prefs = dict(tribeObj['preference'])
                
                #--------------------------------------------------------------
                # Znizenie preferencie ak nevyuziva vsetku alokovanu workForce
                #--------------------------------------------------------------
                unus  = tribeObj['unus']

                if unus['frg'] > _PREF_UNUS_LIMIT: prefs['frg'] -= _PREF_BY_UNUS
                if unus['pstr']> _PREF_UNUS_LIMIT: prefs['pstr']-= _PREF_BY_UNUS
                if unus['agr'] > _PREF_UNUS_LIMIT: prefs['agr'] -= _PREF_BY_UNUS
                if unus['ind'] > _PREF_UNUS_LIMIT: prefs['ind'] -= _PREF_BY_UNUS     

                #--------------------------------------------------------------
                # Zvysovanie produkcie jedla a znizovanie  kôli nedostatku
                #--------------------------------------------------------------
                
                prefs['frg']  *= tribeObj['denses']['hunger'] + 1
                prefs['pstr'] *= tribeObj['denses']['hunger'] + 1
                prefs['agr']  *= tribeObj['denses']['hunger'] + 1
                
                #--------------------------------------------------------------
                # Zvysovanie nabozenstva kvoli stresu
                #--------------------------------------------------------------
                prefs['rlg'] *= tribeObj['denses']['stres'] + 1
                
                #--------------------------------------------------------------
                # Zvysovanie vedy kvoli vyzkumu
                #--------------------------------------------------------------
                prefs['sci'] *= (knowBaseGain/(1 + prefs['rlg'])) + 1
                tribeObj['effs']['sci'] = knowGain/knowBaseGain

                #--------------------------------------------------------------
                # Zvysenie preferencii pre resource type s maximalnou efektivitou
                #--------------------------------------------------------------
                
                effs = tribeObj['effs']

                # Zotriedim efektivitu zostupne
                effs = lib.dSort(effs, reverse=True)
                
                # Zvysim preferencie maximalnej efektivity
                rank = 1
                for srcType, eff in effs.items():
                    if rank == 1: prefs[srcType] += _PREF_BY_EFF
                    rank += 1

                #--------------------------------------------------------------
                # Normujem preferencie tak aby ich sucet bol 1 a zapisem do simulovanej periody
                #--------------------------------------------------------------
                for resType, pref in prefs.items():
                   if pref < _PREF_MIN: prefs[resType] = _PREF_MIN
                
                prefs = lib.normSumDic(prefs)
                
                simPeriodTribe['preference']['frg'] = prefs['frg']
                simPeriodTribe['preference']['agr'] = prefs['agr']
                simPeriodTribe['preference']['pstr']= prefs['pstr']
                simPeriodTribe['preference']['ind'] = prefs['ind']
                simPeriodTribe['preference']['sci'] = prefs['sci']
                simPeriodTribe['preference']['rlg'] = prefs['rlg']
                simPeriodTribe['preference']['war'] = prefs['war']
                simPeriodTribe['preference']['trd'] = prefs['trd']
                simPeriodTribe['preference']['dpl'] = prefs['dpl']
            
            #------------------------------------------------------------------
            # Koniec podmienky na nenulovu densitu
            #------------------------------------------------------------------

        self.journal.O()

    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #==========================================================================
    # Tile tools pre zadanu periodu
    #--------------------------------------------------------------------------
    def getPeriod(self, period):
        "Returns data of the history period if exists in this Tile, creates empty if does not exists"
        
        # Ak je to prave nasledujuca perioda v historii, vytvorim ju
        if period == len(self.history): 
            self.history.append({ 'period':period, 'tribes':{} })

        return self.history[period]
        
    #--------------------------------------------------------------------------
    def getPeriodTribe(self, period, tribeId, tribeFrom):
        "Returns data of the tribe for respective period in this Tile, if tribe does not exists cretes it based on <tribeFrom>"
        
        actPeriod = self.getPeriod(period)
        
        #----------------------------------------------------------------------
        # Ak tribe neexistuje, doplnim ho podla KOPIE tribe z ktoreho pochadzam
        #----------------------------------------------------------------------
        if tribeId not in actPeriod['tribes'].keys(): 
            
            actPeriod['tribes'][tribeId] = {}
            
            actPeriod['tribes'][tribeId]['density'   ] = 0
            actPeriod['tribes'][tribeId]['color'     ] = dict(tribeFrom['color'     ])
            actPeriod['tribes'][tribeId]['preference'] = dict(tribeFrom['preference'])
            actPeriod['tribes'][tribeId]['knowledge' ] = dict(tribeFrom['knowledge' ])
            actPeriod['tribes'][tribeId]['resrs'     ] = {}
            actPeriod['tribes'][tribeId]['denses'    ] = {}
            actPeriod['tribes'][tribeId]['disp'      ] = {}
            actPeriod['tribes'][tribeId]['wars'      ] = {}
            actPeriod['tribes'][tribeId]['trades'    ] = {}

        #----------------------------------------------------------------------
        return actPeriod['tribes'][tribeId]
        
    #==========================================================================
    # Work with the density of the population
    #--------------------------------------------------------------------------
    def getPeriodDensTot(self, period):
        "Returns total density on this Tile for respective period"
        
        toRet = 0
        
        actPeriod = self.getPeriod(period)
        
        for tribeObj in actPeriod['tribes'].values():
            toRet += tribeObj['density']
        
        return toRet
        
    #--------------------------------------------------------------------------
    def getPeriodDens(self, period, tribeId):
        "Returns density of tribeId on this Tile for respective period"
        
        actPeriod = self.getPeriod(period)
        
        if tribeId in actPeriod['tribes']: toRet = actPeriod['tribes'][tribeId]['density']
        else                             : toRet = 0

        return toRet
        
    #==========================================================================
    # Work with the knowledge
    #--------------------------------------------------------------------------
    def knowledgeChange(self, tribeObj, resType):
        "Evaluates changes in the knowledge and preference for respective tribe and resource type"
        
        toRet = [0, 0, 0]
        attention = tribeObj['preference'][resType]

        if attention > _KNOW_LIMIT:
            toRet[1] = tribeObj['knowledge'][resType] * _KNOW_GROWTH
            toRet[0] = tribeObj['knowledge'][resType] * _KNOW_GROWTH * (((tribeObj['density'] * tribeObj['preference']['sci'] + 0.9) * (tribeObj['knowledge']['sci'] + 0.9) * _KNOW_GROWTH_SCI) + 1)
        else : 
            toRet[1] = tribeObj['knowledge'][resType] * _KNOW_DECAY
            toRet[0] = tribeObj['knowledge'][resType] * _KNOW_DECAY
            
        # Znalosti nemozu klesnut pod zakladne minimum
        if toRet[0] < _KNOW_MIN:
            toRet[0] = _KNOW_MIN
        
        # Znalosti nemozu byt vyssie ako 1 (=100%)
        if toRet[0] > 1:
            toRet[0] = 1

        toRet[1] = toRet[1] - tribeObj['knowledge'][resType]
        toRet[2] = toRet[0] - tribeObj['knowledge'][resType]

        return toRet

    #==========================================================================
    # Work with the preferences
    #--------------------------------------------------------------------------

    #==========================================================================
    # Persistency methods
    #--------------------------------------------------------------------------
    def toJson(self):
        "Creates json representation of this tile"

        self.journal.I(f'{self.tileId}.toJson:')
        
        data = {}
        
        data['tileId' ] = self.tileId   # ID tile
        data['biome' ]  = self.biome    # Priemerna vyska tile nad morom
        data['row'    ] = self.row      # Pozicia tile - riadok
        data['col'    ] = self.col      # Pozicia tile - stlpec
        data['history'] = self.history  # Historia tile [{'agrState':agrState, 'tribes':tribes}]
        
        self.journal.O(f'{self.tileId}.toJson: done')
        
        return data
        
    #--------------------------------------------------------------------------
    def fromJson(self, data):
        "Updates tile from json structure"

        self.journal.I(f'{self.tileId}.fromJson:')
        
        self.biome  = data['biome' ]
        
        if 'history' in data.keys() and len(data['history'])>0: 
            self.history = data['history']
        
        self.journal.O(f'{self.tileId}.fromJson: done')
        
#------------------------------------------------------------------------------
print('TTile ver 1.01')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------