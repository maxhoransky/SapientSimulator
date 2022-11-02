#==============================================================================
# :main file
#------------------------------------------------------------------------------
from siqo_journal     import SiqoJournal
from tPlanet          import TPlanet
from tPlanetGui       import TPlanetGui

#==============================================================================
# package's constants
#------------------------------------------------------------------------------

#==============================================================================
# package's tools
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
if __name__ =='__main__':
  
    journal = SiqoJournal('MaxPlanet', debug=2)
    journal.I( 'Main loop' )
    
    # Vytvorim testovaciu Planetu
    tp = TPlanet(journal, 'TestPlanet')
    tp.generate(20, 20)
    
    # Vytvorim GUI
    gui = TPlanetGui(journal, tp)
    gui.mainloop()       # Start listening for events
    
    journal.O('Main end')
    
#==============================================================================
#                              END OF FILE
#------------------------------------------------------------------------------
