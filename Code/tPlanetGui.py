#==============================================================================
# class for MaxPlanet GUI
#------------------------------------------------------------------------------
import tkinter            as tk
import planet_lib         as lib

from   tkinter            import (ttk, font, messagebox, filedialog, scrolledtext, END)
import tkinter as tk

#==============================================================================
# package's constants
#------------------------------------------------------------------------------
_WIN            = '1680x1050'
_DPI            = 100

_WIDTH_MAX      = 250
_PADX           = 7
_PADY           = 9

#==============================================================================
# class TPlanetGui
#------------------------------------------------------------------------------
class TPlanetGui(tk.Tk):
    
    #==========================================================================
    # Static variables & methods
    #--------------------------------------------------------------------------

    #==========================================================================
    # Constructor & utilities
    #--------------------------------------------------------------------------
    def __init__(self, journal, planet):
        "Creates and shows GUI for MaxPlanet"

        journal.I( 'TPlanetGui constructor...')
        
        #----------------------------------------------------------------------
        #iniciatizazia tk.Tk
        #----------------------------------------------------------------------
        super().__init__()
        self.user    = 'max'
        self.version = '0.01'

        #----------------------------------------------------------------------
        # Internal data
        #----------------------------------------------------------------------
        self.journal   = journal
        self.planet    = planet              # Objekt Planeta
        self.lblTiles  = {}                  # Zoznam tiles {lblTile: tile}
        
        self.tab_selected = 0                # Vybrany tab EDIT/TRIBE/SIMUL
        self.state        = 'STOP'           # Stav simulacie RUNNIG/STOP
        self.period       = 0                # Perioda s ktorou prave pracujem
        self.denMax       = 10               # Maximalna suhrnna density na vsetkych tiles pre danu periodu
        self.knowMax      = 3                # Maximalna suma knowledge per srcType na vsetkych tiles pre danu periodu
        
        self.lblTileSelected = None          # lblTile s ktorou pracujem
        self.str_show   = tk.StringVar()     # Show BIOM/TRIBES/POPULATION/KNOWLEDGE/PREFERENCES
        self.str_tribe  = tk.StringVar()     # Tribe s ktorym pracujem na Tile
        self.str_dens   = tk.StringVar()     # Hustota polpulacie ktoru chcem nastavit na Tile
        self.str_period = tk.StringVar()     # Show BIOM/TRIBES/POPULATION/KNOWLEDGE/PREFERENCES
        self.str_period.trace('w', self.periodChanged)

        #----------------------------------------------------------------------
        # Initialisation
        #----------------------------------------------------------------------
        self.show()   # Initial drawing

        self.journal.O( 'TPlanetGui created for Object {}'.format(self.title))

    #==========================================================================
    # GUI methods
    #--------------------------------------------------------------------------
    def show(self):
        "Shows Max Planet GUI"
        
        self.journal.I( f'TPlanetGui{self.title}.show' )
        
        #----------------------------------------------------------------------
        # Nastavenia root window
        #----------------------------------------------------------------------
        self.geometry('1435x740')
        self.minsize(1050,400)
        self.title(self.planet.name)
#        self.icon_path = resource_path('ikona.ico')
#        self.iconbitmap(self.icon_path)

        #----------------------------------------------------------------------
        # Nastavenia style
        #----------------------------------------------------------------------
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.layout('Custom.TNotebook', []) # copy of TNotebook
        self.style.configure('Treeview', bakcground='silver', foreground='black', rowheight=15, fieldbackground='grey' )
        self.style.map('Treeview', background=[('selected','green')] )

        #----------------------------------------------------------------------
        # Frames for Status bar, Tools, Common a Map
        #----------------------------------------------------------------------
        self.statusBarShow()
        self.frame_map = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        self.frame_map.pack(side='left', fill='both')
        self.CommonsShow()
        self.toolsShow()

        #----------------------------------------------------------------------
        # Vytvorenie mapy
        #----------------------------------------------------------------------
        self.mapCreate()
            
        self.journal.O( f'TPlanetGui{self.title}.show: End' )

    #==========================================================================
    # Common gauges
    #--------------------------------------------------------------------------
    def CommonsShow(self):
       
        frm = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        frm.pack(side='top', anchor='n', fill='x')
       
        frm.columnconfigure(0, weight=1)
        frm.columnconfigure(1, weight=1)
       
        frm.rowconfigure   ( 0, weight=1)
        frm.rowconfigure   ( 1, weight=1)
        frm.rowconfigure   ( 2, weight=1)
        frm.rowconfigure   ( 3, weight=1)
        frm.rowconfigure   ( 4, weight=1)
        frm.rowconfigure   ( 5, weight=1)

        #----------------------------------------------------------------------
        # Period, Show, Load & Save Buttons
        #----------------------------------------------------------------------
        lbl_period = ttk.Label(frm, relief=tk.FLAT, text='I will edit Period:' )
        lbl_period.grid(row=0, column=0, sticky='ws', padx=_PADX, pady=_PADY)

        self.str_period.set(self.period)
        spin_period = ttk.Spinbox(frm, from_=0, to=99999, textvariable=self.str_period, width=3)
        spin_period.grid(row=0, column=1, sticky='w', padx=_PADX, pady=_PADY)

        #----------------------------------------------------------------------
        lbl_show = ttk.Label(frm, relief=tk.FLAT, text='I will show on map:' )
        lbl_show.grid(row=1, column=0, sticky='ws', padx=_PADX, pady=_PADY)

        self.str_show.set('BIOM')
        cb_show = ttk.Combobox(frm, textvariable=self.str_show)
        cb_show['values'] = ['BIOM','TRIBES', 'POPULATION', 'KNOWLEDGE','PREFERENCES']
        cb_show['state'] = 'readonly'
        cb_show.bind('<<ComboboxSelected>>', self.showChanged)
        cb_show.grid(row=1, column=1, sticky='nw', padx=_PADX, pady=_PADY)

        #----------------------------------------------------------------------
        btn_load = ttk.Button(frm, text='Load Planet', command=self.load)
        btn_load.grid(row=0, column=3, sticky='nwe', padx=_PADX, pady=_PADY)
        
        btn_save = ttk.Button(frm, text='Save Planet', command=self.save)
        btn_save.grid(row=1, column=3, sticky='nwe', padx=_PADX, pady=_PADY)
        
        #----------------------------------------------------------------------
        # Seelected Tile
        #----------------------------------------------------------------------
        self.lbl_tile = ttk.Label(frm, relief=tk.FLAT, text='Tile' )
        self.lbl_tile.grid(row=3, column=0, columnspan=6, sticky='w', padx=_PADX, pady=_PADY)

        #----------------------------------------------------------------------
        # Selected Tribe
        #----------------------------------------------------------------------
        lbl_trb = ttk.Label(frm, relief=tk.FLAT, text='Available Tribes:' )
        lbl_trb.grid(row=4, column=0, sticky='ws', padx=_PADX, pady=_PADY)

        self.cb_trb = ttk.Combobox(frm, textvariable=self.str_tribe)
        self.cb_trb['values'] = list(lib.tribes.keys())
        self.cb_trb['state']  = 'readonly'
        self.cb_trb.bind('<<ComboboxSelected>>', self.tribeChanged)
        self.cb_trb.grid(row=4, column=1, sticky='wn', padx=_PADX, pady=_PADY)

    #--------------------------------------------------------------------------
    def periodChanged(self, widget, blank, mode):
        
        if self.str_period.get() != '': tmpPeriod = int(self.str_period.get())
        else                          : tmpPeriod = 0
        
        # Ak nastala zmena periody
        if tmpPeriod != self.period:
            
            self.period = tmpPeriod
        
            # Ak je perioda vacsia ako maximalna perioda v historii planety
            if self.period > self.planet.getMaxPeriod():
                self.period = self.planet.getMaxPeriod()
                self.str_period.set(self.period)
                
            # Vykreslim zmenenu periodu
            self.setStatus(f'Selected period is {self.period}')
            self.mapShow()
        
    #--------------------------------------------------------------------------
    def showChanged(self, event):
        
        self.setStatus(f'Selected show is {self.str_show.get()}')
        self.mapShow()
        self.showTileOptions()
        
    #--------------------------------------------------------------------------
    def load(self):
        
        #----------------------------------------------------------------------
        # Zistim, kam mam zapisat
        #----------------------------------------------------------------------
        fileName = filedialog.askopenfilename(
            title      = 'Metadata file',
            initialdir = self.planet.fName,
            filetypes  = (('json files', '*.json'), ('All files', '*.*'))
            )
 
        if fileName == '': return
        
        #----------------------------------------------------------------------
        # Nacitanie metadat
        #----------------------------------------------------------------------
        self.setStatus(f'Loading planet from {fileName}')
        self.period = 0
        
        self.planet.fName = fileName
        self.planet.load()
        self.denMax  = self.planet.getMaxDensity  (self.period)
        self.knowMax = self.planet.getMaxKnowledge(self.period)

        self.mapCreate()
        self.str_period.set(0)
         
    #--------------------------------------------------------------------------
    def save(self):
        
        #----------------------------------------------------------------------
        # Zistim, kam mam zapisat
        #----------------------------------------------------------------------
        fileName = filedialog.asksaveasfile( mode='w', defaultextension=".json", initialfile = self.planet.fName)

        if fileName is None: return
        
        #----------------------------------------------------------------------
        # Nacitanie metadat
        #----------------------------------------------------------------------
        self.setStatus(f'Saving planet into {fileName.name}')
        self.planet.fName = fileName.name
        self.planet.save()
         
    #--------------------------------------------------------------------------
    def tribeChanged(self, event):
        
        self.journal.M(f'tribeChanged: Selected Tribe is {self.str_tribe.get()}')
        self.setStatus(f'Selected Tribe is {self.str_tribe.get()}')
        self.mapShow()
        self.showTileOptions()

        self.str_dens.set('')
        tribe = self.getSelectedTribe()
        if tribe is not None: self.str_dens.set(tribe['density'])

    #==========================================================================
    # Pravy panel pre nastroje
    #--------------------------------------------------------------------------
    def toolsShow(self):
       
        frame_tool = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        frame_tool.pack(side='right', anchor='e', expand=True, fill='both')
       
        #----------------------------------------------------------------------
        # TABS as ttk.Notebook
        #----------------------------------------------------------------------
       
        self.tabs = ttk.Notebook(frame_tool, style='TNotebook')
        self.tabs.pack(expand=True, fill='both')
        self.tabs.enable_traversal()
       
        # Vytkreslenie jednotlivych tabs
        self.tabEditShow()
        self.tabSimulShow()
        self.tabTribeShow()
   
        self.tabs.bind('<<NotebookTabChanged>>', self.tabChanged)
        self.tabs.select(self.tab_selected)
       
    #--------------------------------------------------------------------------
    def tabChanged(self, event):
       
        self.tabSelected = self.tabs.index("current")
#        self.refresh()

    #--------------------------------------------------------------------------
    def tabEditShow(self):
       
        #----------------------------------------------------------------------
        # Vytvorim frame a skonfigurujem grid
        #----------------------------------------------------------------------
        frm = ttk.Frame(self.tabs)

        frm.columnconfigure( 0, weight=1)
        frm.columnconfigure( 1, weight=1)
        frm.columnconfigure( 2, weight=1)
        frm.columnconfigure( 3, weight=1)
        frm.columnconfigure( 4, weight=1)
        frm.columnconfigure( 5, weight=1)
       
        frm.rowconfigure   ( 0, weight=1)
        frm.rowconfigure   ( 1, weight=1)
        frm.rowconfigure   ( 2, weight=1)
        frm.rowconfigure   ( 3, weight=10)
 
        # Vlozim frame do Tabs       
        self.tabs.add(frm, text='Edit Planet')
 
        #----------------------------------------------------------------------
        # Generate new geography
        #----------------------------------------------------------------------
        lbl_gen1 = ttk.Label(frm, relief=tk.FLAT, text='New Planet for')
        lbl_gen1.grid(row=0, column=0, sticky='w', padx=_PADX, pady=_PADY)
       
        self.str_rows = tk.StringVar(value=self.planet.rows)
        spin_rows = ttk.Spinbox(frm, from_=5, to=90, textvariable=self.str_rows, width=3)
        spin_rows.grid(row=0, column=1, sticky='w', padx=_PADX, pady=_PADY)
       
        lbl_gen2 = ttk.Label(frm, relief=tk.FLAT, text='rows  and' )
        lbl_gen2.grid(row=0, column=2, sticky='w', padx=_PADX, pady=_PADY)

        self.str_cols = tk.StringVar(value=self.planet.cols)
        spin_cols = ttk.Spinbox(frm, from_=5, to=90, textvariable=self.str_cols, width=3)
        spin_cols.grid(row=0, column=3, sticky='w', padx=_PADX, pady=_PADY)
       
        lbl_gen3 = ttk.Label(frm, relief=tk.FLAT, text='columns' )
        lbl_gen3.grid(row=0, column=4, padx=_PADX, pady=_PADY)

        btn_gen = ttk.Button(frm, text='Generate now', command=self.generate)
        btn_gen.grid(row=0, column=5, sticky='we', padx=_PADX, pady=_PADY)
        
        separator1 = ttk.Separator(frm, orient='horizontal')
        separator1.grid(row=1, column=0, columnspan=6, sticky='we', padx=_PADX, pady=_PADY)       
        
        #----------------------------------------------------------------------
        # Edit Tribes on the Tile
        #----------------------------------------------------------------------

        lbl_dens = ttk.Label(frm, relief=tk.FLAT, text="I will set Tribe's density" )
        lbl_dens.grid(row=2, column=0, sticky='nw', padx=_PADX, pady=_PADY)

        spin_dens = ttk.Spinbox(frm, from_=0, to=5000, textvariable=self.str_dens, width=3)
        spin_dens.grid(row=2, column=1, sticky='nwe', padx=_PADX, pady=_PADY)

        btn_trbSet = ttk.Button(frm, text='Set tribe in the Tile', command=self.setTribe)
        btn_trbSet.grid(row=2, column=5, sticky='nwe', padx=_PADX, pady=_PADY)
        
        #----------------------------------------------------------------------
        self.st_tile = scrolledtext.ScrolledText(frm, wrap="none", width=100, height=15)
        self.st_tile.grid(row=3, column=0, columnspan=6, sticky='nwes')

        st_scrollbar = ttk.Scrollbar(self.st_tile, orient='horizontal', command=self.st_tile.xview)
        self.st_tile["xscrollcommand"] = st_scrollbar.set
        st_scrollbar.pack(side="bottom", fill="x", expand=False)

    #--------------------------------------------------------------------------
    def generate(self):

        self.planet.generate( int(self.str_rows.get()), int(self.str_cols.get()) )
        self.denMax  = self.planet.getMaxDensity  (self.period)
        self.knowMax = self.planet.getMaxKnowledge(self.period)
        self.mapCreate()
        
    #--------------------------------------------------------------------------
    def setTribe(self):
        
        #----------------------------------------------------------------------
        # Skontrolujem ci je vybrana Tile
        #----------------------------------------------------------------------
        if self.lblTileSelected is None: self.setStatus('Tile was not selected')
        else:
            #------------------------------------------------------------------
            # Skontrolujem vhodnost biomu Tile
            #------------------------------------------------------------------
            tileObj  = self.lblTiles[self.lblTileSelected]
            
            if tileObj.height==0: self.setStatus('I can not set tribe into sea')
            else:
                #--------------------------------------------------------------
                # Skontrolujem ci je vybrany tribe
                #--------------------------------------------------------------
                tribeObj = self.getSelectedTribe()

                if tribeObj is None: self.setStatus('Tribe was not selected')
                else: 
                    tribeObj['density'] = round(float(self.str_dens.get()),2)
                    self.denMax  = self.planet.getMaxDensity  (self.period)
                    self.knowMax = self.planet.getMaxKnowledge(self.period)
                    self.mapShow()
                    self.showTileOptions()
            
    #--------------------------------------------------------------------------
    def tabSimulShow(self):
       
        #----------------------------------------------------------------------
        # Vytvorim frame a skonfigurujem grid
        #----------------------------------------------------------------------
        frm = ttk.Frame(self.tabs)

        frm.columnconfigure( 0, weight=1)
        frm.columnconfigure( 1, weight=1)
        frm.columnconfigure( 2, weight=1)
       
        frm.rowconfigure   (0, weight=1)
        frm.rowconfigure   (1, weight=1)
        frm.rowconfigure   (2, weight=1)
 
        # Vlozim frame do Tabs       
        self.tabs.add(frm, text='Simulation')
 
        #----------------------------------------------------------------------
        # Reset, SimOne, Start/Stop
        #----------------------------------------------------------------------
        btn_simRest = ttk.Button(frm, text='Reset Simulation to period', command=self.simReset)
        btn_simRest.grid(row=0, column=0, sticky='we', padx=_PADX, pady=_PADY)
        
        btn_simOne = ttk.Button(frm, text='Simulate one period', command=self.simOne)
        btn_simOne.grid(row=0, column=1, sticky='we', padx=_PADX, pady=_PADY)
        
        self.btn_simSS = ttk.Button(frm, text='Simulation start', command=self.simStart)
        self.btn_simSS.grid(row=0, column=2, sticky='we', padx=_PADX, pady=_PADY)
        
        separator1 = ttk.Separator(frm, orient='horizontal')
        separator1.grid(row=1, column=0, columnspan=3, sticky='we', padx=_PADX, pady=_PADY)       
        
    #--------------------------------------------------------------------------
    def simReset(self):
        
        pass
    
    #--------------------------------------------------------------------------
    def simOne(self):
        
        self.simPeriod()
            
    #--------------------------------------------------------------------------
    def simStart(self):
        
        self.state = 'RUNNING'
        self.btn_simSS.configure(text='Simulation stop', command=self.simStop)
        
        # Naplanujem prvy krok simulacie
        self.after(1, self.simPeriod)
            
    #--------------------------------------------------------------------------
    def simStop(self):
        
        self.state = 'STOP'
        self.btn_simSS.configure(text='Simulation start', command=self.simStart)
    
    #--------------------------------------------------------------------------
    def simPeriod(self):
        
        self.journal.M(f'simPeriod: period is {self.period}')

        self.period += 1
        self.planet.simPeriod(self.period)
        self.str_period.set(self.period)
        self.mapShow()

        # Ak bezi simulacia, naplanujem dalsi krok
        if self.state == 'RUNNING':
            self.after(700, self.simPeriod)
        
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    #--------------------------------------------------------------------------
    def tabTribeShow(self):
       
        #----------------------------------------------------------------------
        # Vytvorim frame a skonfigurujem grid
        #----------------------------------------------------------------------
        frm = ttk.Frame(self.tabs)

        frm.columnconfigure( 0, weight=1)
        frm.columnconfigure( 1, weight=1)
        frm.columnconfigure( 2, weight=1)
        frm.columnconfigure( 3, weight=1)
        frm.columnconfigure( 4, weight=1)
        frm.columnconfigure( 5, weight=1)
        frm.columnconfigure( 6, weight=1)
        frm.columnconfigure( 7, weight=1)
        frm.columnconfigure( 8, weight=1)
        frm.columnconfigure( 9, weight=1)
       
        frm.rowconfigure   (0, weight=1)
        frm.rowconfigure   (1, weight=1)
        frm.rowconfigure   (2, weight=1)
        frm.rowconfigure   (3, weight=1)
        frm.rowconfigure   (4, weight=1)
        frm.rowconfigure   (5, weight=1)
        frm.rowconfigure   (6, weight=1)
        frm.rowconfigure   (7, weight=1)
        frm.rowconfigure   (8, weight=1)
 
        # Vlozim frame do Tabs       
        self.tabs.add(frm, text='Tribes')

    #==========================================================================
    # Lavy panel pre mapu
    #--------------------------------------------------------------------------
    def mapCreate(self):
       
        #----------------------------------------------------------------------
        # Odstranim existujuce lblTiles
        #----------------------------------------------------------------------
        for lblTile, tile in self.lblTiles.items():
            lblTile.destroy()

        self.lblTiles.clear()
        
        #----------------------------------------------------------------------
        # Re-Konfiguracia gridu podla rows * cols
        #----------------------------------------------------------------------
        self.frame_map.grid_forget()
        
        for row in range(self.planet.rows):
            self.frame_map.rowconfigure(row, weight=1)
      
        for col in range(self.planet.cols):
            self.frame_map.columnconfigure(col, weight=1)
            
        #----------------------------------------------------------------------
        # Vytvorenie rows * cols tiles
        #----------------------------------------------------------------------
        for row in range(self.planet.rows):
            for col in range(self.planet.cols):
                
                # Zistim ktora Tile je na pozicii row, col
                tile    = self.planet.getTile(row, col)

                # Vytvorim label na zobrazenie Tile
                lblTile = ttk.Label(self.frame_map, relief=tk.RAISED, text=self.tileText(row, col), cursor='hand2')
                lblTile.configure(background='white')
                lblTile.bind( '<Button-1>', self.tileLeftClick)
                lblTile.bind( '<Button-3>', self.tileRightClick)
                lblTile.grid(row=row, column=col, sticky='nwse')
                
                # Ulozim si vazbu {lblTile: Tile}
                self.lblTiles[lblTile] = tile

        #----------------------------------------------------------------------
        # Vytvorim Menu pre click on Tile / nastavenie height
        #----------------------------------------------------------------------
        self.tileMenu = tk.Menu(self, tearoff = 0)
        
        for h in range(0, 3100, 200):
            self.tileMenu.add_command(label =f"Height :   {str(h).ljust(5)}", command=lambda t=str(h): self.tileHeight(t))

        #----------------------------------------------------------------------
        # Vycistenie selected premennych
        #----------------------------------------------------------------------
        self.lblTileSelected = None
        
        #----------------------------------------------------------------------
        # Vykreslenie mapy
        #----------------------------------------------------------------------
        self.mapShow()
        self.showTileOptions()
                 
    #--------------------------------------------------------------------------
    def mapShow(self):
       
        self.denMax  = self.planet.getMaxDensity  (self.period)
        self.knowMax = self.planet.getMaxKnowledge(self.period)

        #----------------------------------------------------------------------
        # Prejdem vsetky lblTile v lblTiles
        #----------------------------------------------------------------------
        for lblTile, tile in self.lblTiles.items():
                
            # Zistim vlastnosti Tile na pozicii row, col
            bcColor = self.tileColor(tile)
            
            # Vykreslim label na zobrazenie Tile
            lblTile.configure(background=bcColor)
            
    #--------------------------------------------------------------------------
    def showTileOptions(self):
        
        # Vycistenie option
        self.setStatus('showTileOptions')
        self.lbl_tile['text'] = 'No Tile was selected'
        
        #----------------------------------------------------------------------
        # Kontrola ci je vybrana Tile
        #----------------------------------------------------------------------
        if self.lblTileSelected is None: return
        tile = self.lblTiles[self.lblTileSelected]
        
        #----------------------------------------------------------------------
        # Vypis podla typu SHOW
        #----------------------------------------------------------------------
        msg =  self.tileLabel(tile)
        self.lbl_tile['text'] = msg
        self.setStatus(msg)
        
        self.st_tile.delete("1.0", "end")
        for line in tile.info()['msg']:
            self.st_tile.insert(END, line + '\n')
        
    #--------------------------------------------------------------------------
    def tileLeftClick(self, event):
        
        #----------------------------------------------------------------------
        # Zistim podla eventu, na ktoru lblTile som vlastne clickol
        #----------------------------------------------------------------------
        self.lblTileSelected = event.widget
        
        # Zobraz vlastnosti Tile
        self.showTileOptions()
        self.tribeChanged(event)
        
    #--------------------------------------------------------------------------
    def tileRightClick(self, event):
        
        #----------------------------------------------------------------------
        # Zistim podla eventu, na ktoru lblTile som vlastne clickol
        #----------------------------------------------------------------------
        self.lblTileSelected = event.widget
        tile   = self.lblTiles[self.lblTileSelected]
        self.setStatus(f'tileRightClick: {self.lblTileSelected} => {tile.tileId} with height {tile.height}')
        
        # Zobraz vlastnosti Tile
        self.showTileOptions()

        #nakoniec otvor popup menu pre nastavenie height
        try    : self.tileMenu.tk_popup(event.x_root, event.y_root)
        finally: self.tileMenu.grab_release()

    #--------------------------------------------------------------------------
    def tileHeight(self, heightStr):
        
        height = int(heightStr)
        
        # Ziskam tile, ktora je spojena s touto lblTile
        tile   = self.lblTiles[self.lblTileSelected]
        row    = tile.row
        col    = tile.col
        
        self.setStatus(f'tileHeight: {height} for tileId = {tile.tileId}')
        
        # Nastavim vysku tile
        tile.height = height

        # Updatnem na obrazovke lblTile
        self.lblTileSelected.configure( background = self.tileColor(tile)    )
        self.lblTileSelected.configure( text       = self.tileText(row, col) )
        
    #--------------------------------------------------------------------------
    def tileTribes(self):
        
        pass
        
    #==========================================================================
    # Status bar
    #--------------------------------------------------------------------------
    def statusBarShow(self):
       
        frame_status_bar = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        frame_status_bar.pack(side='bottom', anchor='s', fill='x')
       
        frame_status_bar.columnconfigure(0, weight=5)
        frame_status_bar.columnconfigure(1, weight=1)
        frame_status_bar.columnconfigure(2, weight=1)
       
        self.str_status_bar = tk.StringVar(value = 'str_status_bar')
       
        status_bar_txt = ttk.Label(frame_status_bar, relief=tk.RAISED, textvariable=self.str_status_bar)
        status_bar_txt.grid(row = 0, column = 0, sticky = 'we' )
       
        status_bar_ver = ttk.Label(frame_status_bar, relief=tk.RAISED, text=f'(c) SIQO v. {self.version}')
        status_bar_ver.grid(row = 0, column = 2, padx = 3 ,sticky = 'we')

        #----------------------------------------------------------------------
        # URL Menu
        #----------------------------------------------------------------------
#        self.rcm_url = tk.Menu(self, tearoff = 0)

#        self.rcm_url.add_command(label=_URLS[0], command=lambda: self.changeUrl(_URLS[0]) )
#        self.rcm_url.add_command(label=_URLS[1], command=lambda: self.changeUrl(_URLS[1]) )
      
    #--------------------------------------------------------------------------
    def setStatus(self, mess):
       
        self.str_status_bar.set(mess)
 
    #==========================================================================
    # Internal methods
    #--------------------------------------------------------------------------
    def tileColor(self, tile):
        
        # Ak je to more, zobrazim more
        if tile.height==0: return lib.getBiomColor(0)
        
        # Ak je to pevnina, zobrazim zelanu agregaciu zo zelanej historie tribes
        show   = self.str_show.get()
        tribes = tile.history[self.period]['tribes']
                
        if   show == 'BIOM'       : bcColor = lib.getBiomColor  (tile.height)
        elif show == 'TRIBES'     : bcColor = lib.getTribesColor(tribes, self.denMax )
        elif show == 'POPULATION' : bcColor = lib.getPopulColor (tribes, self.denMax )
        elif show == 'KNOWLEDGE'  : bcColor = lib.getKnowlColor (tribes, self.knowMax)
        elif show == 'PREFERENCES': bcColor = lib.getPrefsColor (tribes)
        else                      : bcColor = 'black'

        return bcColor
    
    #--------------------------------------------------------------------------
    def tileLabel(self, tile):
        
        # Ak je to more, zobrazim more
        if tile.height==0: return 'This is a sea'
        
        # Ak je to pevnina, zobrazim zelanu agregaciu zo zelanej historie tribes
        show = self.str_show.get()
                
        if   show == 'BIOM'       : lbl = tile.getPeriodTrbStr(self.period)
        elif show == 'TRIBES'     : lbl = tile.getPeriodTrbStr(self.period)
        elif show == 'POPULATION' : lbl = tile.getPeriodPopStr(self.period)
        elif show == 'KNOWLEDGE'  : lbl = tile.getPeriodKnwStr(self.period)
        elif show == 'PREFERENCES': lbl = tile.getPeriodPrfStr(self.period)
        else                      : lbl = 'Unknown show option'

        return f'{tile.tileId} [{tile.height}m n.m.] : {lbl}'
    
    #--------------------------------------------------------------------------
    def tileText(self, row, col):
        
        return '     '
#        return f'{str(row).rjust(2)}x{str(col).rjust(2)}'
        
    #--------------------------------------------------------------------------
    def getSelectedTribe(self):
        
        #----------------------------------------------------------------------
        # Kontrola vybranej Tile
        #----------------------------------------------------------------------
        if self.lblTileSelected is None: return None
        else:
            #------------------------------------------------------------------
            # Kontrola vybraneho tribe
            #------------------------------------------------------------------
            tileObj  = self.lblTiles[self.lblTileSelected]
            tribeId  = self.str_tribe.get()
        
            if tribeId is None or tribeId=='' : return None
            else: 
                # Vytvorim na mape novy tribe podla vzoru v library
                tribeObj = tileObj.getPeriodTribe(self.period, tribeId, lib.tribes[tribeId])

        #----------------------------------------------------------------------
        self.journal.M(f'getSelectedTribe: tileId={tileObj.tileId}, period={self.period}, tribeId={tribeId}')
        return tribeObj
        
    #==========================================================================
    # Utility
    #--------------------------------------------------------------------------
    def treeWhere(self, tree, event):
       
        row   = ''
        val   = ''
        col   = ''
        colid = ''
       
        iid = tree.identify_row(event.y)
      
        # presun focus a selection sem ak nie je vybraný iaden riadok
        if iid and len(tree.selection()) == 0:
            tree.focus(iid)
            tree.selection_set(iid)
         
        if tree.identify_region(event.x,event.y) == 'heading':
            hd    = tree.identify_column(event.x)
            colid = int(tree.identify_column(event.x)[1:]) - 1
            val   = tree.heading(hd, 'text')
           
        elif tree.identify_region(event.x,event.y) == 'cell':
            curItem = tree.focus()
            val   = tree.item(curItem, 'values')
            colid = int(tree.identify_column(event.x)[1:]) - 1
           
            row   = val
            val   = val[colid]
            hd    = tree.identify_column(event.x)
            col   = tree.heading(hd, 'text')
           
        return {'row':row, 'col':col, 'val':val, 'colNum':colid}
       
    #--------------------------------------------------------------------------
    def datToTab(self, dat, tree):
       
        #----------------------------------------------------------------------
        # Zadefinujem stlpce podla nazvov atributov v dat[0]
        #----------------------------------------------------------------------
        tree["columns"] = dat[0]
        
        #----------------------------------------------------------------------
        # Ziskam maximalne sirky stlpcov
        #----------------------------------------------------------------------
        maxW = [0 for col in dat[0]]
       
        for row in dat:
            
            i = 0
            for col in row:
                
                if (col is not None): w = len(str(col))
                else                : w = 0
               
                if w>maxW[i] and w<_WIDTH_MAX: maxW[i] = w
                i += 1
       
        #----------------------------------------------------------------------
        # Zadefinujem vlastnosti stlpcov
        #----------------------------------------------------------------------
        i = 0
        for col in tree["columns"]:
            
            tree.column(col, width=(8*maxW[i])+10, minwidth=30)
            i += 1
       
        #----------------------------------------------------------------------
        # Zadefinujem nazvy stlpcov
        #----------------------------------------------------------------------
        for h in dat[0]:
            tree.heading(h, text=h, anchor='w')
       
        #----------------------------------------------------------------------
        # Vlozim udaje do riadkov
        #----------------------------------------------------------------------
        for row in dat[1:]:
            tree.insert('', tk.END, values=row, tags=['TableCell'])
           
        tree['show'] = 'headings'
        tree.tag_configure('TableCell', font=font.nametofont('TkFixedFont'))
       
    #--------------------------------------------------------------------------
    def treeClear(self, tree):
       
        for i in tree.get_children():
            tree.delete(i)
           
    #--------------------------------------------------------------------------
    def treeExpand(self, tree, parent=''):
       
        tree.item(parent, open=True)
        for child in tree.get_children(parent):
            self.treeExpand(tree, child)
           
    #--------------------------------------------------------------------------
    def datToTree(self, dat, tree, rootId=None, maxId=0):
       
        if rootId is None: tree.tag_configure('TreeCell', font=font.nametofont('TkFixedFont'))
        localPos = 0
       
        #----------------------------------------------------------------------
        # Prejdem vsetky polozky dictionary
        #----------------------------------------------------------------------
        for key, val in dat.items():
           
            maxId += 1
 
            #------------------------------------------------------------------
            # Ak je item dictionary, potom rekurzia
            if type(val)==dict:
                
                tree.insert('', tk.END, text=f'[{key}]', iid=maxId, open=True, tags=['TreeCell'])
                if rootId is not None: tree.move(maxId, rootId, localPos)
               
                maxId  = self.datToTree(val, tree, maxId, maxId)
           
            #------------------------------------------------------------------
            # Ak je item list
            elif type(val)==list:
                
                tree.insert('', tk.END, text=f'[{key}]', iid=maxId, open=True, tags=['TreeCell'])
                listRoot = maxId
                if rootId is not None: tree.move(listRoot, rootId, localPos)
 
                # Vlozim list po riadkoch
                listPos = 0
                for row in val:
                   
                    maxId   += 1
                    tree.insert('', tk.END, text=f'{str(row)}', iid=maxId, open=True, tags=['TreeCell'])
                    tree.move(maxId, listRoot, listPos)
                    listPos += 1
           
            #------------------------------------------------------------------
            # Trivialna polozka
            else:
                key = str(key).ljust(12)
               
                # Vlozim do stromu
                tree.insert('', tk.END, text=f'{key}: {str(val)}', iid=maxId, open=True, tags=['TreeCell'])
               
                # Ak som v podstrome, presuniem pod rootId
                if rootId is not None: tree.move(maxId, rootId, localPos)
               
            #------------------------------------------------------------------
            # Zvysenie lokalnej pozicie
            localPos += 1
               
        return maxId
       
    #--------------------------------------------------------------------------

#------------------------------------------------------------------------------
print('Max Planet GUI ver 0.30')

#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
