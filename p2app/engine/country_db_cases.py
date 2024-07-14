# Main paart where queries are written for country table
import sqlite3

class CountryBase:

    def __init__(self, event, database, app):
        self.result = None
        self.final_country = None
        self.event = event
        self.db_connect = database
        self.app = app

    def country_search(self):
        c_name = self.event.name()
        c_code = self.event.country_code()
        if c_code is not None and c_name is not None:  # when both fields have values
            self.result = self.db_connect.execute(
                'SELECT * FROM country WHERE country_code LIKE ? AND name LIKE ?;',
                (c_code + '%', c_name + '%'))

        elif c_code is None and c_name is not None:  # when both fields have values
            self.result = self.db_connect.execute('SELECT * FROM country WHERE name LIKE ?;',
                                                  (c_name + '%',))

        elif c_code is not None and c_name is None:  # when both fields have values
            self.result = self.db_connect.execute(
                'SELECT * FROM country WHERE country_code LIKE ?;', (c_code + '%',))

        self.result = self.result.fetchall()
        for i in range(len(self.result)):
            self.final_country = self.app.Country(self.result[i][0], self.result[i][1],
                                             self.result[i][2], self.result[i][3],
                                             self.result[i][4], self.result[i][5])
            yield self.app.CountrySearchResultEvent(self.final_country)

    def load_country(self):
        c_id = self.event.country_id()
        self.result = self.db_connect.execute('SELECT * FROM country WHERE country_id = ?;',
                                              (c_id,))
        self.result = self.result.fetchone()
        self.final_country = self.app.Country(self.result[0], self.result[1], self.result[2],
                                         self.result[3], self.result[4], self.result[5])
        yield self.app.CountryLoadedEvent(self.final_country)

    def new_country(self):
        try:
            c_name = self.event.country().name
            c_code = self.event.country().country_code
            c_id = self.event.country().continent_id
            c_link = self.event.country().wikipedia_link
            c_key = self.event.country().keywords
            new_country_id = self.db_connect.execute(
                'SELECT MAX(country_id) FROM country')  # GETS to end of content id
            new_country_id = new_country_id.fetchone()  # Fetches from SQLite object
            new_country_id = new_country_id[0] + 1
            self.db_connect.execute(
                'INSERT INTO country(country_code, name, continent_id, wikipedia_link, keywords ) values(?, ?, ?, ?, ?);',
                (c_code, c_name, c_id, c_link, c_key))
            self.result = self.app.Country(new_country_id, c_code, c_name, c_id, c_link, c_key)
            yield self.app.CountrySavedEvent(self.result)

        except sqlite3.IntegrityError:
            yield self.app.SaveCountryFailedEvent("New Country couldn't be saved into the database")

        except:
            yield self.app.SaveCountryFailedEvent("New Country couldn't be saved into the database")

    def edit_country(self):
        try:
            c_name = self.final_country.name
            c_code = self.final_country.country_code
            self.result = self.db_connect.execute(
                "SELECT country_id FROM country WHERE country_code =? and name=?;",
                (c_code, c_name))
            self.result = self.result.fetchone()[0]
            c_code_new = self.event.country().country_code
            c_name_new = self.event.country().name
            c_id_new = self.event.country().continent_id
            c_link_new = self.event.country().wikipedia_link
            c_key_new = self.event.country().keywords
            self.db_connect.execute(
                "UPDATE country SET country_code =?, name =?, continent_id=?, wikipedia_link=?, keywords=? WHERE country_id = ?;",
                (c_code_new, c_name_new, c_id_new, c_link_new, c_key_new, self.result))
            ans = self.app.Country(self.result, c_code_new, c_name_new, c_id_new, c_link_new, c_key_new)
            yield self.app.CountrySavedEvent(ans)

        except sqlite3.IntegrityError:
            yield self.app.SaveCountryFailedEvent("Modified Country couldn't be saved into the database")

        except:
            yield self.app.SaveCountryFailedEvent("Modified Country couldn't be saved into the database")
