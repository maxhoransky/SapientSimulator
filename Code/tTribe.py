#==============================================================================
# Siqo class TTribe
#------------------------------------------------------------------------------
# from   dwm_calendar         import DWM_Calendar

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_SEP   = 50*''

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# TTribe
#------------------------------------------------------------------------------
class TTribe:

    #==========================================================================
    # Static variables & methods
    #--------------------------------------------------------------------------
    journal = None   # Globalny journal
    tribes  = {}     # Zoznam vsetkych tribes  {tribeId: tribeObj}

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, tribeId):
        "Calls constructor of TTribe and initialise it with empty data"

        self.journal.I('TTribe.constructor')
        
        self.tribeId    = tribeId     # ID tribe
        
        # Zaradim novu tile do zoznamu tiles
        self.tribes[self.tribeId] = self

        self.journal.O(f'{self.tileId}.constructor: done')
        
    #--------------------------------------------------------------------------
    def __str__(self):
        "Prints info about this Tile"

        toRet = ''
        for line in self.info()['out']: toRet += line +'\n'

        return toRet

    #==========================================================================
    # Reports for users
    #--------------------------------------------------------------------------
    def info(self):
        "Returns info about the Tile"

        msg = []
        msg.append(f'Tile ID   :{self.tileId}'   )
        msg.append(f'height    :{self.height}'   )
        msg.append(f'row       :{self.row}'   )
        msg.append(f'col       :{self.col}'   )
        msg.append(_SEP)
        msg.append('Neighbours:')

        for neighObj in self.neighs:
            msg.append(f'{neighObj.tileId}    :{neighObj.height}'   )
            
        return {'res':'OK', 'msg':msg}

    #==========================================================================
    # API for GUI
    #--------------------------------------------------------------------------
    def reset(self):
        "Resets state of Tile into begining state"
    
        self.journal.I(f'{self.tileId}.reset:')
        
        # Ak existuje nejaka historia, zrusim ju do zakladneho stavu
        if len(self.history) > 0:
            begState = self.history[0]
            self.history.clear()
            self.history.append(begState)
        
        self.journal.O(f'{self.tileId}.reset: done')
        
    #--------------------------------------------------------------------------
    
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
        
    #==========================================================================
    # Persistency methods
    #--------------------------------------------------------------------------
    def toJson(self):
        "Creates json representation of this tile"

        self.journal.I(f'{self.tileId}.toJson:')
        
        self.journal.O(f'{self.tileId}.toJson: done')
        
    #--------------------------------------------------------------------------
    def fromJson(self, json):
        "Updates tile from json structure"

        self.journal.I(f'{self.tileId}.fromJson:')
        
        self.journal.O(f'{self.tileId}.fromJson: done')
        
        
#------------------------------------------------------------------------------
print('TTribe ver 0.01')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------