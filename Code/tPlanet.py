#==============================================================================
# Siqo class TPlanet
#------------------------------------------------------------------------------
import siqo_general  as     gen
from   tTile         import TTile

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

#==============================================================================
# package's variables
#------------------------------------------------------------------------------

#==============================================================================
# TPlanet
#------------------------------------------------------------------------------
class TPlanet:

    #==========================================================================
    # Static variables & methods
    #--------------------------------------------------------------------------

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, name):
        "Calls constructor of TPlanet and initialise it with empty data"

        journal.I('TPlanet.constructor')
        
        # Nastavenie journal-u projektu
        self.journal    = journal     # Odkaz na globalny journal
        TTile.journal   = journal
        
        # Prepojim evidenciu Tiles
        self.tiles      = TTile.tiles # Geografia planety  {tileId: tileObj}

        # Nastavenie vlastnosti planety
        self.name       = name               # Nazov planety
        self.fName      = 'TestPlanet.json'  # Nazov suboru pre perzistenciu planetu
        self.rows       = 0                  # Pocet riadkov rastra planety
        self.cols       = 0                  # Pocet stlpcov rastra planety

        self.journal.O(f'{self.name}.constructor: done')
        
    #--------------------------------------------------------------------------
    def __str__(self):
        "Prints info about this Planet"

        toRet = ''
        for line in self.info()['msg']: toRet += line +'\n'

        return toRet

    #==========================================================================
    # Reports for users
    #--------------------------------------------------------------------------
    def info(self):
        "Returns info about the Planet"

        msg = []
        msg.append(f'Planet name :{self.name}'       )
        msg.append(f'File name   :{self.fName}'      )
        msg.append(f'rows        :{self.rows}'       )
        msg.append(f'cols        :{self.cols}'       )
        msg.append(f'tiles       :{len(self.tiles)}' )
        msg.append(f'Max period  :{self.getMaxPeriod()}')

        return {'res':'OK', 'msg':msg}

    #==========================================================================
    # API for GUI
    #--------------------------------------------------------------------------
    def clear(self):
        "Clears all Planet's data"
    
        self.journal.I(f'{self.name}.clear:')
        
        self.rows   = 0
        self.cols   = 0
        
        for tile in self.tiles.values(): tile.clear()
        
        self.journal.O(f'{self.name}.clear: done')
        
    #--------------------------------------------------------------------------
    def reset(self):
        "Resets state of Planet into begining state"
    
        self.journal.I(f'{self.name}.reset:')
        for tile in self.tiles.values(): tile.reset()
        self.journal.O(f'{self.name}.reset: done')
        
    #--------------------------------------------------------------------------
    def generate(self, rows, cols):
        "Creates new void Planet"
    
        self.journal.I(f'{self.name}.generate: New planet {rows} * {cols}')
        
        #----------------------------------------------------------------------
        # Zrusim existujucu planetu
        #----------------------------------------------------------------------
        self.clear()
        
        #----------------------------------------------------------------------
        # Najprv vytvorim vsetky tiles        
        #----------------------------------------------------------------------
        self.rows = rows
        self.cols = cols
        
        for r in range(self.rows):
            for c in range(self.cols):
                tileObj     = TTile( self.getTileId(r, c) )
                tileObj.row = r
                tileObj.col = c

        #----------------------------------------------------------------------
        # Potom nastavim vsetkym tiles ich susedov
        #----------------------------------------------------------------------
        for tileId, tileObj in self.tiles.items():
                
                neighs = self.getNeighbours(tileId)
                tileObj.neighs = neighs
        
        self.journal.O(f'{self.name}.generate: done')
    
    #--------------------------------------------------------------------------
    def simReset(self, period):

        self.journal.I(f'{self.name}.simReset: period = {period}')
        
        
        self.journal.O(f'{self.name}.simReset: done')

    #--------------------------------------------------------------------------
    def simPeriod(self, period):
        "Simulates new period for all tiles"
        
        #----------------------------------------------------------------------
        # Skontrolujem vstupne pomienky
        #----------------------------------------------------------------------
        if period < 1                    : return 'Period is lower than 0, command is denied'
        if period > self.getMaxPeriod()+1: return 'Period is too high, command is denied'
        
        #----------------------------------------------------------------------
        self.journal.I(f'{self.name}.simPeriod: Period is {period}')

        #----------------------------------------------------------------------
        # Vykonam simulaciu postupne vo vsetkych tiles
        #----------------------------------------------------------------------
        for tileObj in self.tiles.values():
            tileObj.simPeriod(period)
        
        self.journal.O(f'{self.name}.simPeriod: done')

    #--------------------------------------------------------------------------
    def getMaxPeriod(self):
        "Returns max available period in history"
        
        key   = list(self.tiles.keys())[0]
        toRet = len(self.tiles[key].history) - 1
        
        self.journal.M(f'{self.name}.getMaxPeriod: is {toRet}')
        
        return toRet
        
    #--------------------------------------------------------------------------
    def getMaxDensity(self, period):
        "Returns max sum of densities per Tile for all Tiles in respective period"

        toRet = TTile.getDenMax(period)
        self.journal.O(f'{self.name}.getMaxDensity: for period {period} is {toRet}')
        
        return toRet
        
    #--------------------------------------------------------------------------
    def getMaxKnowledge(self, period):
        "Returns max sum of knowledge per sourcetype  for all Tiles in respective period"

        toRet = TTile.getKnowMax(period)
        self.journal.O(f'{self.name}.getMaxKnowledge: for period {period} is {toRet}')
        
        return toRet
        
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def getTile(self, row, col):
        "Returns Tile for respective row, col"
        
        tileId = self.getTileId(row, col)
        
        if tileId in self.tiles.keys(): return self.tiles[tileId]
        else:
            self.journal.M(f'{self.name}.getTile: Tile ID {tileId} does not exists')
            return None
        
    #--------------------------------------------------------------------------
    def getTileId(self, row, col):
        "Returns tileID for respective row, col"
        
        return f'Tile {row}, {col}'
        
    #--------------------------------------------------------------------------
    def getNeighbours(self, tileId):
        "Returns neighbours [tileObj] for tile with respective ID"
        
        toRet = []
        
        #----------------------------------------------------------------------
        # Ziskam poziciu row, col pre tileID
        #----------------------------------------------------------------------
        tile = self.tiles[tileId]
        row = tile.row
        col = tile.col
        
        #----------------------------------------------------------------------
        # Urcim susedov
        #----------------------------------------------------------------------
        for dr in range(-1,2):
            for dc in range(-1,2):
                
                neighId = self.getTileId( (row+dr)%self.rows, (col+dc)%self.cols )  
                
                # Ak to nie je ID mna, potom je to sused a vlozim ho do zoznamu susedov
                if neighId != tileId: toRet.append(self.tiles[neighId])
                
        return toRet
        
    #==========================================================================
    # Persistency methods
    #--------------------------------------------------------------------------
    def save(self):
        "Saves planet into disk file"

        self.journal.I(f'{self.name}.save:')
        
        #----------------------------------------------------------------------
        # Vyrobim json na ulozenie
        #----------------------------------------------------------------------
        data = {}
        
        data['rows'  ] = self.rows
        data['cols'  ] = self.cols
        
        for tileId, tileObj in self.tiles.items():
            data[tileId] = tileObj.toJson()
        
        #----------------------------------------------------------------------
        # Zapisem json na disk
        #----------------------------------------------------------------------
        gen.dumpJson(self.journal, self.fName, data)
        
        self.journal.O(f'{self.name}.save: done')
        
    #--------------------------------------------------------------------------
    def load(self):
        "Loads planet from disk file"

        self.journal.I(f'{self.name}.load:')
        
        #----------------------------------------------------------------------
        # Nacitam json z disku
        #----------------------------------------------------------------------
        data = gen.loadJson(self.journal, self.fName)
        
        #----------------------------------------------------------------------
        # Vygenerujem cistu planetu rows*cols
        #----------------------------------------------------------------------
        self.generate(data['rows'], data['cols'])
        
        #----------------------------------------------------------------------
        # Updatnem parametre tiles podla data
        #----------------------------------------------------------------------
        for tileId, tileObj in self.tiles.items():
            tileObj.fromJson( data[tileId] )
        
        self.journal.O(f'{self.name}.load: done')
        
#------------------------------------------------------------------------------
print('TPlanet ver 1.01')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------