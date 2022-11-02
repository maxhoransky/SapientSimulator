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
_KNOW_LIMIT      = 0.3   # Hranica pozornosti, pri ktorej sa knowledge zvysuje
_KNOW_DECAY      = 0.95  # Koeficient zabudania knowledge ak jej tribe nevenuje pozornost
_KNOW_MIN        = 0.1   # Minimalna hodnota znalosti uplnych divochov

_PREF_UNUS_LIMIT =   5   # Ak je unused workforce vyssia ako tato hranica, zapricini zmenu preferencii
_PREF_BY_UNUS    = 0.1   # Zmena preferncie podla unused workforce pre biom
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
        
            agrSum = 0
            indSum = 0
            warSum = 0
            
            # Prejdem vsetky tribe na tile pre konkretnu periodu
            for tribe in tile.history[period]['tribes'].values():
                agrSum += tribe['knowledge']['agr']
                indSum += tribe['knowledge']['ind']
                warSum += tribe['knowledge']['war']
                
            if agrSum > knowMax: knowMax = agrSum
            if indSum > knowMax: knowMax = indSum
            if warSum > knowMax: knowMax = warSum

        return knowMax
    
    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, tileId, height=0):
        "Calls constructor of TTile and initialise it with empty data"

        self.journal.I('TTile.constructor')
        
        self.tileId     = tileId          # ID tile
        self.row        = 0               # Pozicia tile - riadok
        self.col        = 0               # Pozicia tile - stlpec
        self.neighs     = []              # Zoznam geografickych susedov tile [tileObj]

        self.height     = height          # Priemerna vyska tile nad morom
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
        msg.append(f'height    :{self.height}'   )
        msg.append(f'row       :{self.row}'   )
        msg.append(f'col       :{self.col}'   )
        msg.append(_SEP)
        msg.append('Neighbours:')

        for neighObj in self.neighs:
            msg.append(f'{neighObj.tileId}    :{neighObj.height}'   )
            
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
    def getPeriodPopStr(self, period):
        "Returns string describing population with different preferences in this Tile"
        
        tribes = self.getPeriod(period)['tribes']
        
        agr = 0
        ind = 0
        war = 0
        
        #----------------------------------------------------------------------
        # Spocitam jednotlive druhy populacie
        #----------------------------------------------------------------------
        for tribeObj in tribes.values(): 
            
            agr += tribeObj['density'] * tribeObj['preference']['agr']
            ind += tribeObj['density'] * tribeObj['preference']['ind']
            war += tribeObj['density'] * tribeObj['preference']['war']
                
        if (agr+ind+war) == 0: toRet = 'No tribe here'
        else                 : toRet = f"Population agr:{round(agr, 2)} ind:{round(ind, 2)} war:{round(war, 2)}"
    
        return toRet
    
    #--------------------------------------------------------------------------
    def getPeriodKnwStr(self, period):
        "Returns string describing knowledge in this Tile"
        
        tribes = self.getPeriod(period)['tribes']
        
        toRet = 'Knowledge:'
        for tribeId, tribeObj in tribes.items():
            if tribeObj['density']>0:
                toRet += f" {tribeId}: agr={round(tribeObj['knowledge']['agr'], 2)}, ind={round(tribeObj['knowledge']['ind'], 2)}, war={round(tribeObj['knowledge']['war'], 2)}"
 
        if toRet=='Knowledge:': toRet = 'No tribe here'
        
        return toRet
    
    #--------------------------------------------------------------------------
    def getPeriodPrfStr(self, period):
        "Returns string describing preferences in this Tile"
        
        tribes = self.getPeriod(period)['tribes']
        
        toRet = 'Preferences:'
        for tribeId, tribeObj in tribes.items(): 
            if tribeObj['density']>0:
                toRet += f" {tribeId}: agr={round(tribeObj['preference']['agr'], 2)}, ind={round(tribeObj['preference']['ind'], 2)}, war={round(tribeObj['preference']['war'], 2)}"
 
        if toRet=='Preferences:': toRet = 'No tribe here'
        
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
            resrs = {'agr':0, 'ind':0, 'war':0}
            effs  = {'agr':0, 'ind':0, 'war':0}
            unus  = {'agr':0, 'ind':0, 'war':0}

            #------------------------------------------------------------------
            # Zber AGR resources - zlomok podla pomeru density Tribe voci celkovej densite na Tile
            #------------------------------------------------------------------
            (res, eff, unu) = lib.getResource( self.height, resType='agr', workForce=dens*prefs['agr'], knowledge=knows['agr'] )
            
            resrs['agr'] = res
            effs ['agr'] = eff
            unus ['agr'] = unu

            #------------------------------------------------------------------
            # Zber IND resources - zlomok podla pomeru density Tribe voci celkovej densite na Tile
            #------------------------------------------------------------------
            (res, eff, unu) = lib.getResource( self.height, resType='ind', workForce=dens*prefs['ind'], knowledge=knows['ind'] )
            resrs['ind'] = res
            effs ['ind'] = eff
            unus ['ind'] = unu

            #------------------------------------------------------------------
            # Nakupovanie zvysnych AGR za zvysne IND vyrobky a 
            # Lupenie WAR zdrojov od inych tribes
            #------------------------------------------------------------------



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
            resrTot = tribeObj['resrs']['agr'] + tribeObj['resrs']['ind'] + tribeObj['resrs']['war']
            
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
                if neighTile.height > 0:
                
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
                know = self.knowledgeChange(tribeObj, 'agr')
                simPeriodTribe['knowledge']['agr'] = know
            
                know = self.knowledgeChange(tribeObj, 'ind')
                simPeriodTribe['knowledge']['ind'] = know
            
                know = self.knowledgeChange(tribeObj, 'war')
                simPeriodTribe['knowledge']['war'] = know
        
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
                if unus['agr'] > _PREF_UNUS_LIMIT: prefs['agr'] -= _PREF_BY_UNUS
                if unus['ind'] > _PREF_UNUS_LIMIT: prefs['ind'] -= _PREF_BY_UNUS
            
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
                
                simPeriodTribe['preference']['agr'] = prefs['agr']
                simPeriodTribe['preference']['ind'] = prefs['ind']
            
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
            
        if attention > _KNOW_LIMIT: toRet = tribeObj['knowledge'][resType] * _KNOW_GROWTH
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
        data['height' ] = self.height   # Priemerna vyska tile nad morom
        data['row'    ] = self.row      # Pozicia tile - riadok
        data['col'    ] = self.col      # Pozicia tile - stlpec
        data['history'] = self.history  # Historia tile [{'agrState':agrState, 'tribes':tribes}]
        
        self.journal.O(f'{self.tileId}.toJson: done')
        
        return data
        
    #--------------------------------------------------------------------------
    def fromJson(self, data):
        "Updates tile from json structure"

        self.journal.I(f'{self.tileId}.fromJson:')
        
        self.height  = data['height' ]
        
        if 'history' in data.keys() and len(data['history'])>0: 
            self.history = data['history']
        
        self.journal.O(f'{self.tileId}.fromJson: done')
        
#------------------------------------------------------------------------------
print('TTile ver 1.01')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------