# Main paart where queries are written for regions table

import sqlite3

class RegionBase:

    def __init__(self, event, database, app):
        self.result = None
        self.final_region = None
        self.event = event
        self.db_connect = database
        self.app = app

    def region_search(self):
        r_name = self.event.name()
        r_code = self.event.region_code()
        l_code = self.event.local_code()
        if r_code is not None and r_name is None and l_code is None:
            self.result = self.db_connect.execute('SELECT * FROM region WHERE region_code LIKE ?;',
                                                  (r_code + '%',))

        elif r_code is None and r_name is not None and l_code is None:
            self.result = self.db_connect.execute('SELECT * FROM region WHERE name LIKE ?;',
                                                  (r_name + '%',))

        elif r_code is None and r_name is None and l_code is not None:
            self.result = self.db_connect.execute('SELECT * FROM region WHERE local_code LIKE  ?;',
                                                  (l_code + '%',))

        elif r_code is not None and r_name is not None and l_code is None:
            self.result = self.db_connect.execute(
                'SELECT * FROM region WHERE region_code LIKE  ? and name LIKE ?;',
                (r_code + '%', r_name + '%'))

        elif r_code is None and r_name is not None and l_code is not None:
            self.result = self.db_connect.execute(
                'SELECT * FROM region WHERE name LIKE ? and local_code LIKE ?;',
                (r_name + '%', l_code + '%'))

        elif r_code is not None and r_name is None and l_code is not None:
            self.result = self.db_connect.execute(
                'SELECT * FROM region WHERE region_code LIKE ? and local_code LIKE ?;',
                (r_code + '%', l_code + '%'))

        elif r_code is not None and r_name is not None and l_code is not None:
            self.result = self.db_connect.execute(
                'SELECT * FROM region WHERE region_code LIKE ? and local_code LIKE ? and name LIKE ?;',
                (r_code + '%', l_code + '%', r_name + '%'))

        self.result = self.result.fetchall()
        for i in range(len(self.result)):
            self.final_region = self.app.Region(self.result[i][0], self.result[i][1], self.result[i][2],
                                           self.result[i][3], self.result[i][4], self.result[i][5],
                                           self.result[i][6], self.result[i][7])
            yield self.app.RegionSearchResultEvent(self.final_region)

    def load_region(self):
        r_id = self.event.region_id()
        self.result = self.db_connect.execute('SELECT * FROM region WHERE region_id = ?;', (r_id,))
        self.result = self.result.fetchone()
        self.final_region = self.app.Region(self.result[0], self.result[1], self.result[2],
                                       self.result[3], self.result[4], self.result[5],
                                       self.result[6], self.result[7])
        yield self.app.RegionLoadedEvent(self.final_region)

    def new_region(self):
        try:
            r_name = self.event.region().name
            r_code = self.event.region().region_code
            l_code = self.event.region().local_code
            continent_id = self.event.region().continent_id
            country_id = self.event.region().country_id
            r_link = self.event.region().wikipedia_link
            r_key = self.event.region().keywords
            new_region_id = self.db_connect.execute('SELECT MAX(region_id) FROM region')
            new_region_id = new_region_id.fetchone()[0] + 1
            self.db_connect.execute(
                'INSERT INTO region(region_code, local_code, name, continent_id ,country_id ,wikipedia_link ,keywords) values(?,?,?,?,?,?,?);',
                (r_code, l_code, r_name, continent_id, country_id, r_link, r_key))
            self.result = self.app.Region(new_region_id, r_code, l_code, r_name, continent_id,
                                     country_id, r_link, r_key)
            yield self.app.RegionSavedEvent(self.result)

        except sqlite3.IntegrityError:
            yield self.app.SaveRegionFailedEvent("New Region couldn't be saved into the database ")

        except:
            yield self.app.SaveRegionFailedEvent("New Region couldn't be saved into the database ")

    def edit_region(self):
        try:
            r_code = self.final_region.region_code
            r_name = self.final_region.name
            self.result = self.db_connect.execute(
                'SELECT region_id FROM region WHERE region_code = ? and name = ?;',
                (r_code, r_name))
            self.result = self.result.fetchone()[0]
            r_name_new = self.event.region().name
            r_code_new = self.event.region().region_code
            l_code_new = self.event.region().local_code
            continent_id_new = self.event.region().continent_id
            country_id_new = self.event.region().country_id
            r_link_new = self.event.region().wikipedia_link
            r_key_new = self.event.region().keywords
            self.db_connect.execute(
                "UPDATE region SET region_code = ? , local_code = ?, name =?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ? WHERE region_id =?;",
                (r_code_new, l_code_new, r_name_new, continent_id_new, country_id_new, r_link_new,
                 r_key_new, self.result))
            ans = self.app.Region(self.result, r_code_new, l_code_new, r_name_new, continent_id_new,
                             country_id_new, r_link_new, r_key_new)
            yield self.app.RegionSavedEvent(ans)

        except sqlite3.IntegrityError:
            yield self.app.SaveRegionFailedEvent("Modified Region couldn't be saved into the database ")

        except:
            yield self.app.SaveRegionFailedEvent("Modified Region couldn't be saved into the database ")


