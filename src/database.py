import sqlite3
import datetime
import csv

class DataBase :

    def __init__(self):
        self.conn = sqlite3.connect("tournoi.db")
        self.cursor = self.conn.cursor()

        # == Tables creation if they don't exist ==
        with self.conn:
        # "Participants" data base
            self.conn.execute(""" 
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                prenom TEXT
            )
            """)

            # "Rencontres" data base
            self.conn.execute("""
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

    def __del__(self):
        self.conn.close() # Closes the connection when the object is no longer referenced

#region Methods - Add queries
    def addParticipant(self, prenom: str, nom: str):
        with self.conn:
            self.conn.execute("INSERT INTO participants (prenom, nom) VALUES (?, ?)", (prenom, nom))

    def addRencontre(self, id1: int, id2: int, arbitre: int, assesseur: int,cat: str, s1: int, s2: int):
        with self.conn:
            self.cursor.execute("""
                INSERT INTO rencontres (combattant1, combattant2, arbitre, assesseur, categorie, score1, score2, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (id1, id2, arbitre, assesseur, cat, s1, s2, datetime.datetime.now().isoformat()))
#endregion

#region Methods - Getters
    def getParticipants(self):
        self.cursor.execute("SELECT id, prenom, nom FROM participants ORDER BY nom")
        res = self.cursor.fetchall()

        # Convert the result of the sql query into a dictionary
        colonnes = ["id", "prenom", "nom"]
        participants = [dict(zip(colonnes, row)) for row in res]

        return participants
   
    
    
    def getRencontres(self):
        self.cursor.execute("""
        SELECT r.id, p1.id, p1.prenom || ' ' || p1.nom, p2.id, p2.prenom || ' ' || p2.nom,
               arb.id, arb.prenom || ' ' || arb.nom, ass.id, ass.prenom || ' ' || ass.nom,
               r.score1, r.score2, r.categorie, r.date
        FROM rencontres r
        JOIN participants p1 ON r.combattant1 = p1.id
        JOIN participants p2 ON r.combattant2 = p2.id
        JOIN participants arb ON r.arbitre = arb.id
        JOIN participants ass ON r.assesseur = ass.id
        ORDER BY r.date DESC
        """)
        res = self.cursor.fetchall()

        # Convert the result of the sql query into a dictionary
        colonnes = [
        "id_rencontre", 
        "id_combattant1", "nom_combattant1",
        "id_combattant2", "nom_combattant2",
        "id_arbitre", "nom_arbitre",
        "id_assesseur", "nom_assesseur",
        "score1", "score2", "categorie", "date"
        ]
        rencontres = [dict(zip(colonnes, row)) for row in res]
        return rencontres
#endregion

    
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
            for row in self.cursor.fetchall():
                writer.writerow([row[7], row[0], row[4], row[1], row[5], row[6], row[2], row[3]])