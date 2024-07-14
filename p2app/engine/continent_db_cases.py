# Main paart where queries are written for continent table

import sqlite3

class ContinentBase:

    def __init__(self, event, database, app):
        self.result = None
        self.final_continent = None
        self.event = event
        self.db_connect = database
        self.app = app


    def continent_search(self):
        c_name = self.event.name()
        c_code = self.event.continent_code()

        if c_code is not None and c_name is not None:  # when both fields have values
            self.result = self.db_connect.execute('SELECT * FROM continent WHERE continent_code LIKE ? AND name LIKE ?;',(c_code + '%', c_name + '%'))

        elif c_code is None and c_name is not None:  # when continent code is empty
            self.result = self.db_connect.execute('SELECT * FROM continent WHERE name LIKE ?;',(c_name + '%',))

        elif c_code is not None and c_name is None:  # when continent name is empty
            self.result = self.db_connect.execute('SELECT * FROM continent WHERE continent_code LIKE ?;', (c_code + '%',))

        self.result = self.result.fetchall()  # fetch all results of query
        for i in range(len(self.result)):
            self.final_continent = self.app.Continent(self.result[i][0], self.result[i][1], self.result[i][2])
            yield self.app.ContinentSearchResultEvent(self.final_continent)


    def load_continent(self):
        c_id = self.event.continent_id()
        self.result = self.db_connect.execute('SELECT * FROM continent WHERE continent_id = ?;', (c_id,))
        self.result = self.result.fetchone()
        self.final_continent = self.app.Continent(self.result[0], self.result[1], self.result[2])
        yield self.app.ContinentLoadedEvent(self.final_continent)


    def new_continent(self):
        try:
            c_name = self.event.continent().name
            c_code = self.event.continent().continent_code
            new_continent_id = self.db_connect.execute('SELECT MAX(continent_id) FROM continent')
            new_continent_id = new_continent_id.fetchone()  # Fetches from SQLite object
            new_continent_id = new_continent_id[0] + 1
            self.db_connect.execute('INSERT INTO continent(continent_code, name) values(?, ?);',
                                    (c_code, c_name))
            self.result = self.app.Continent(new_continent_id, c_code, c_name)
            yield self.app.ContinentSavedEvent(self.result)
        except sqlite3.IntegrityError:
            yield self.app.SaveContinentFailedEvent(
                "New Continent couldn't be saved into the database")
        except:
            yield self.app.SaveContinentFailedEvent("New Continent couldn't be saved into the database")


    def edit_continent(self):
        try:
            c_name = self.final_continent.name
            c_code = self.final_continent.continent_code
            self.result = self.db_connect.execute(
                "SELECT continent_id FROM continent WHERE continent_code =? and name=? ;",
                (c_code, c_name))
            self.result = self.result.fetchone()[0]
            c_code_new = self.event.continent().continent_code  # gets the new continent code and name
            c_name_new = self.event.continent().name
            self.db_connect.execute(
                "UPDATE  continent SET continent_code =?, name =? WHERE continent_id =?;",
                (c_code_new, c_name_new, self.result))
            ans = self.app.Continent(self.result, c_code_new, c_name_new)  # submits it to database
            yield self.app.ContinentSavedEvent(ans)

        except sqlite3.IntegrityError:
            yield self.app.SaveContinentFailedEvent(
                "Modified Continent couldn't be saved into the database")
        except :
            yield self.app.SaveContinentFailedEvent(
                "Modified Continent couldn't be saved into the database")


