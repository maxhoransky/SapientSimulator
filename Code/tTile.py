#==============================================================================
# Siqo class TTile
#------------------------------------------------------------------------------
import planet_lib    as lib

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
_STRES_EMIG      = 0.2   # Koeficient emigracie kvoli stresu

_KNOW_GROWTH     = 1.10  # Koeficient zvysenia knowledge ak jej tribe venuje pozornost
_KNOW_GROWTH_SCI = 0.05  # How much does science help speed up research
_KNOW_LIMIT      = 0.3   # Hranica pozornosti, pri ktorej sa knowledge zvysuje
_KNOW_DECAY      = 0.95  # Koeficient zabudania knowledge ak jej tribe nevenuje pozornost
_KNOW_MIN        = 0.1   # Minimalna hodnota znalosti uplnych divochov

_PREF_UNUS_LIMIT =   5   # Ak je unused workforce vyssia ako tato hranica, zapricini zmenu preferencii
_PREF_BY_UNUS    = 0.1   # Zmena preferncie podla unused workforce pre biome
_PREF_BY_EFF     = 0.1   # Zmena preferencie podla efektivity vyuzitia pracovnej sily (preferencie)
_PREF_MIN        = 0.05  # Minimalna hodnota preferencie pre resType

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
    def simPeriod(self, period):
        "Simulates respective period for this Tile based on previous period values"
        
        self.journal.I(f'{self.tileId}.simPeriod: period {period}')
        
        #----------------------------------------------------------------------
        # Vyberiem z historie predchadzajucu periodu a inicializujem simulovanu periodu
        #----------------------------------------------------------------------
        lastPeriod = self.getPeriod(period-1)
        simPeriod  = self.getPeriod(period  )
        
        #----------------------------------------------------------------------
        # Vyriesim zber resurces vratane trades podla stavu v lastPeriod
        #----------------------------------------------------------------------
        self.getResource(lastPeriod)
        
        #----------------------------------------------------------------------
        # Vyriesim ubytok/prirastok populacie na zaklade ziskanych resources a emigracie
        #----------------------------------------------------------------------
        self.evaluateDensity(lastPeriod, simPeriod)
 
        #----------------------------------------------------------------------
        # Vyriesim zmenu knowledge/preferenci Tribe 
        #----------------------------------------------------------------------
        self.changePrefsAndKnowledge(lastPeriod, simPeriod)
        
        self.journal.O(f'{self.tileId}.simPeriod: done')

    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def getResource(self, lastPeriod):
        "Evaluates resources per Tribe based on preferences including trade and war"

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

            '''
            #------------------------------------------------------------------
            # Gaining RLG resources - 
            #------------------------------------------------------------------
            (res, eff, unu) = lib.getResource( self.biome, resType='ind', workForce=dens*prefs['ind'], knowledge=knows['ind'] )
            resrs['ind'] = res
            effs ['ind'] = eff
            unus ['ind'] = unu

            #------------------------------------------------------------------
            # Stealing WAR resources - 
            #------------------------------------------------------------------
            (res, eff, unu) = lib.getResource( self.biome, resType='ind', workForce=dens*prefs['ind'], knowledge=knows['ind'] )
            resrs['ind'] = res
            effs ['ind'] = eff
            unus ['ind'] = unu

            #------------------------------------------------------------------
            # Trading TRD resources - 
            #------------------------------------------------------------------
            (res, eff, unu) = lib.getResource( self.biome, resType='ind', workForce=dens*prefs['ind'], knowledge=knows['ind'] )
            resrs['ind'] = res
            effs ['ind'] = eff
            unus ['ind'] = unu

            #------------------------------------------------------------------
            # Zber DPL resources - 
            #------------------------------------------------------------------
            (res, eff, unu) = lib.getResource( self.biome, resType='ind', workForce=dens*prefs['ind'], knowledge=knows['ind'] )
            resrs['ind'] = res
            effs ['ind'] = eff
            unus ['ind'] = unu
            '''
            #------------------------------------------------------------------
            # Zapisem priebezne vypocty o ziskanych resources a efektivite do lastPeriod Tile
            #------------------------------------------------------------------
            tribeObj['resrs'] = resrs
            tribeObj['unus' ] = unus
            tribeObj['effs' ] = effs
            
        #----------------------------------------------------------------------
        self.journal.O()

    #--------------------------------------------------------------------------
    def evaluateDensity(self, lastPeriod, simPeriod):
        "Evaluates population density per Tribe based on earned resources and emigration"

        self.journal.I(f'{self.tileId}.evaluateDensity:')
        period = lastPeriod['period']+1
        
        #----------------------------------------------------------------------
        # Vyhodnotim zmeny populacie pre vsetky Tribes na Tile
        #----------------------------------------------------------------------
        for tribeId, tribeObj in lastPeriod['tribes'].items():

            # Vstupne hodnoty
            resrTot = tribeObj['resrs']['frg'] + tribeObj['resrs']['agr'] + tribeObj['resrs']['pstr'] + tribeObj['resrs']['ind'] + tribeObj['resrs']['sci'] + tribeObj['resrs']['rlg'] + tribeObj['resrs']['war'] + tribeObj['resrs']['trd'] + tribeObj['resrs']['dpl']
            
            # Zacinam simulaciu s povodnym obyvatelstvom z predchadzajucej periody
            densSim = tribeObj['density']

            #------------------------------------------------------------------
            # Opravim populaciu o prirodzeny prirastok
            #------------------------------------------------------------------
            densGrowth = _DENS_GROWTH * densSim
            densSim   += densGrowth

            #------------------------------------------------------------------
            # Ubytok populacie nasledkom nedostatku zdrojov 1 res per 1 clovek/km2
            #------------------------------------------------------------------
            if densSim > resrTot: 
                
                # Zistim, kolko populcie zomrie lebo nema zdroje kvoli wojne
                densWar   = 0
                
                # Zistim, kolko populcie zomrie lebo nema vyprodukovane zdroje
                densHunger = densSim - resrTot
                
                # Miera stresu je pomer zomretej populacie voci povodnej populacii
                strsTot = _STRES_MIN + ((densWar+densHunger) / densSim)
                if strsTot > _STRES_MAX: strsTot = _STRES_MAX
                
                # Zostane zit len tolko ludi kolko ma zdroje
                densSim   = resrTot
                
            else:
                strsTot    = _STRES_MIN
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
                                  'stres'     : strsTot
                                  }
            #------------------------------------------------------------------
            # Ak tribe prezil, zapisem ho do simulovanej periody s densSim
            #------------------------------------------------------------------
            if densSim > 0:
                
                simPeriodTribe = self.getPeriodTribe(period, tribeId, tribeObj)
                simPeriodTribe['density'] += densSim
                
            #------------------------------------------------------------------
        self.journal.O()

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
                know = self.knowledgeChange(tribeObj, 'frg')
                simPeriodTribe['knowledge']['frg'] = know
                
                know = self.knowledgeChange(tribeObj, 'agr')
                simPeriodTribe['knowledge']['agr'] = know

                know = self.knowledgeChange(tribeObj, 'pstr')
                simPeriodTribe['knowledge']['pstr'] = know

                know = self.knowledgeChange(tribeObj, 'ind')
                simPeriodTribe['knowledge']['ind'] = know

                know = self.knowledgeChange(tribeObj, 'sci')
                simPeriodTribe['knowledge']['sci'] = know

                know = self.knowledgeChange(tribeObj, 'rlg')
                simPeriodTribe['knowledge']['rlg'] = know

                know = self.knowledgeChange(tribeObj, 'war')
                simPeriodTribe['knowledge']['war'] = know
                
                know = self.knowledgeChange(tribeObj, 'trd')
                simPeriodTribe['knowledge']['trd'] = know

                know = self.knowledgeChange(tribeObj, 'dpl')
                simPeriodTribe['knowledge']['dpl'] = know

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
                if unus['sci'] > _PREF_UNUS_LIMIT: prefs['sci'] -= _PREF_BY_UNUS  
                if unus['rlg'] > _PREF_UNUS_LIMIT: prefs['rlg'] -= _PREF_BY_UNUS  
                if unus['war'] > _PREF_UNUS_LIMIT: prefs['war'] -= _PREF_BY_UNUS
                if unus['trd'] > _PREF_UNUS_LIMIT: prefs['trd'] -= _PREF_BY_UNUS
                if unus['dpl'] > _PREF_UNUS_LIMIT: prefs['dpl'] -= _PREF_BY_UNUS            
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
        
        toRet = 0
        attention = tribeObj['preference'][resType]
            
        if attention > _KNOW_LIMIT: toRet = tribeObj['knowledge'][resType] * _KNOW_GROWTH * (((tribeObj['density'] + 0.9) * (tribeObj['preference']['sci'] + 0.9) * (tribeObj['knowledge']['sci'] + 0.9) * _KNOW_GROWTH_SCI) + 1)
        else                      : toRet = tribeObj['knowledge'][resType] * _KNOW_DECAY
            
        # Znalosti nemozu klesnut pod zakladne minimum
        if toRet < _KNOW_MIN: toRet = _KNOW_MIN
        
        # Znalosti nemozu byt vyssie ako 1 (=100%)
        if toRet > 1: toRet = 1

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
        data['biome' ]  = self.biome   # Priemerna vyska tile nad morom
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