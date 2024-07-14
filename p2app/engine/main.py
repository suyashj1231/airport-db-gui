# p2app/engine/main.py

# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that  build

import sqlite3
import p2app.events.__init__ as app
from p2app.engine.database_cases_module import DataBase as dcm
from p2app.engine.continent_db_cases import ContinentBase as contibase
from p2app.engine.country_db_cases import CountryBase as countrybase
from p2app.engine.region_db_cases import RegionBase as regbase

class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.db_connect = None
        self.result = None
        self.dcm = dcm(None, None)
        self.cb = contibase(None, None, None)
        self.cyb = countrybase(None, None, None)
        self.rb = regbase(None, None, None)
    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""

# DATABASE CASES
# Quit pressed from Menu
        try:
            if type(event) == app.QuitInitiatedEvent:
                self.dcm = dcm(app, event)
                yield from self.dcm.end_app_event()

    # Connects to Database and opens it
            elif type(event) == app.OpenDatabaseEvent:
                # Connects to Database and opens it
                try:
                    self.db_connect = sqlite3.connect(event.path())
                    self.db_connect.execute("PRAGMA foreign_keys = ON;")
                    yield app.DatabaseOpenedEvent(event.path())
                except:
                    yield app.DatabaseOpenFailedEvent("Databased didn't open")

    # Close the current database, pressed from Menu
            elif type(event) == app.CloseDatabaseEvent:
                self.dcm = dcm(app, event)
                yield from self.dcm.close_db()


    # CONTINENT DATABASE CASES
    # Search for Continent using continent code and name fields
            elif type(event) == app.StartContinentSearchEvent:
                self.cb = contibase(event, self.db_connect, app)
                yield from self.cb.continent_search()

    # Loads a Continent info
            elif type(event) == app.LoadContinentEvent:
                self.cb = contibase(event, self.db_connect, app)
                yield from self.cb.load_continent()

    # Saves a new Continent into the database
            elif type(event) == app.SaveNewContinentEvent:
                self.cb = contibase(event, self.db_connect, app)
                yield from self.cb.new_continent()

    # Saves a modified Continent into the database
            elif type(event) == app.SaveContinentEvent:
                self.cb.event = event
                yield from self.cb.edit_continent()

    # COUNTRY DATABASE CASES
    # Search for Country using Country code and Name fields
            elif type(event) == app.StartCountrySearchEvent:
                self.cyb = countrybase(event,self.db_connect,app)
                yield from self.cyb.country_search()

    # Loads a Country info
            elif type(event) == app.LoadCountryEvent:  # Loads a Country info
                self.cyb = countrybase(event,self.db_connect,app)
                yield from self.cyb.load_country()

    # Saves a new Country into the database
            elif type(event) == app.SaveNewCountryEvent:
                self.cyb = countrybase(event,self.db_connect,app)
                yield from self.cyb.new_country()

    # Saves a modified Country into the database
            elif type(event) == app.SaveCountryEvent:
                self.cyb.event = event
                yield from self.cyb.edit_country()

    # REGION DATABASE CASES
    # Search for Region using Region code, Region Name and Local Code fields
            elif type(event) == app.StartRegionSearchEvent:
                self.rb = regbase(event,self.db_connect,app)
                yield from self.rb.region_search()

    # Loads a Region info
            elif type(event) == app.LoadRegionEvent:
                self.rb = regbase(event, self.db_connect, app)
                yield from self.rb.load_region()

    # Saves a new Region into the database
            elif type(event) == app.SaveNewRegionEvent:
                self.rb = regbase(event, self.db_connect, app)
                yield from self.rb.new_region()

    # Saves a modified Region into the database
            elif type(event) == app.SaveRegionEvent:
                self.rb.event = event
                yield from self.rb.edit_region()

        except:
             yield app.ErrorEvent("Unknown error occurred!!!")
