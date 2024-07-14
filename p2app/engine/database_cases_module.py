class DataBase:

    def __init__(self,app, event):
        self.app = app
        self.event = event
    def end_app_event(self):
        yield self.app.EndApplicationEvent()

    def close_db(self):
            # Close the current database, pressed from Menu
                yield self.app.DatabaseClosedEvent()

