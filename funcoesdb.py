import sqlite3


class Database:
    def __init__(self):
        self.connect = sqlite3.connect('snakegame.db')
        self.cursor = self.connect.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS recordes 
                               (nome varchar(10), pontuacao int NOT NULL)""")

    def insert_record(self, name, points):
        try:
            self.cursor.execute(f"""INSERT INTO recordes 
                                    (nome, pontuacao)
                                    VALUES
                                    ('{name}', '{points}')""")
        except:
            pass
        finally:
            self.connect.commit()

    def show_records(self):
        data = None
        try:
            data = self.cursor.execute("""SELECT * FROM recordes ORDER BY pontuacao DESC""").fetchall()
        except:
            pass
        finally:
            self.connect.commit()
        return data

    def endconnection(self):
        self.cursor.close()

    def erasetable(self):
        self.cursor.execute("DELETE FROM recordes")

