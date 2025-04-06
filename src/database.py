import sqlite3
import datetime
import csv

class DataBase :

    def __init__(self):
        self.conn = sqlite3.connect("tournoi.db")
        self.cursor = self.conn.cursor()

        # == Tables creation if they don't exist ==

        # "Participants" data base
        self.cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            prenom TEXT
        )
        """)

        # "Rencontres" data base
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS rencontres (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            combattant1 INTEGER,
            combattant2 INTEGER,
            arbitre INTEGER,
            assesseur INTEGER,
            categorie TEXT,
            score1 INTEGER,
            score2 INTEGER,
            date TEXT
        )
        """)

        self.conn.commit()

    def __del__(self):
        self.close()
    
    def addParticipant(self, prenom: str, nom: str):
        self.cursor.execute("INSERT INTO participants (prenom, nom) VALUES (?, ?)", (prenom, nom))
        self.conn.commit()

    def getParticipants(self):
        self.cursor.execute("SELECT id, prenom, nom FROM participants ORDER BY nom")
        return self.cursor.fetchall()
    

    def addRencontre(self, id1: int, id2: int, arbitre: int, assesseur: int,cat: str, s1: int, s2: int):
        self.cursor.execute("""
            INSERT INTO rencontres (combattant1, combattant2, arbitre, assesseur, categorie, score1, score2, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id1, id2, arbitre, assesseur, cat, s1, s2, datetime.datetime.now().isoformat()))
        self.conn.commit()

    def getRencontres(self):
        self.cursor.execute("""
        SELECT r.id, p1.prenom || ' ' || p1.nom, p2.prenom || ' ' || p2.nom,
               arb.prenom || ' ' || arb.nom, ass.prenom || ' ' || ass.nom,
               r.score1, r.score2, r.categorie, r.date
        FROM rencontres r
        JOIN participants p1 ON r.combattant1 = p1.id
        JOIN participants p2 ON r.combattant2 = p2.id
        JOIN participants arb ON r.arbitre = arb.id
        JOIN participants ass ON r.assesseur = ass.id
        ORDER BY r.date DESC
        """)
        return self.cursor.fetchall()
    
    def exporter_csv(self):
        with open("rencontres.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Combattant 1", "Score 1", "Combattant 2", "Score 2", "Catégorie", "Arbitre", "Assesseur"])
            self.cursor.execute("""
                SELECT p1.prenom || ' ' || p1.nom, p2.prenom || ' ' || p2.nom,
                    arb.prenom || ' ' || arb.nom, ass.prenom || ' ' || ass.nom,
                    r.score1, r.score2, r.categorie, r.date
                FROM rencontres r
                JOIN participants p1 ON r.combattant1 = p1.id
                JOIN participants p2 ON r.combattant2 = p2.id
                JOIN participants arb ON r.arbitre = arb.id
                JOIN participants ass ON r.assesseur = ass.id
            """)
            for row in self.cursos.fetchall():
                writer.writerow([row[7], row[0], row[4], row[1], row[5], row[6], row[2], row[3]])

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()