import sqlite3
import datetime
import csv

class DataBase :

    def __init__(self):
        self.conn = sqlite3.connect("tournoi.db")
        self.cursor = self.conn.cursor()

        # == Tables creation if they don't exist ==
        with self.conn:
            # Club data base
            self.conn.execute(""" 
            CREATE TABLE IF NOT EXISTS clubs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
            """)

            # "Participants" data base
            self.conn.execute(""" 
            CREATE TABLE IF NOT EXISTS participants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                prenom TEXT,
                club INTEGER
            )
            """)
                    

            # Fighting style categories data base
            self.conn.execute(""" 
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
            """)

            # "Matches" data base
            self.conn.execute("""
            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                combattant1 INTEGER,
                combattant2 INTEGER,
                arbitre INTEGER,
                assesseur INTEGER,
                categorie INTEGER,
                score1 INTEGER,
                score2 INTEGER,
                date TEXT
            )
            """)

    def __del__(self):
        self.conn.close() # Closes the connection when the object is no longer referenced

#region Methods - Add queries
    def addClub(self, name: str):
        try:
            with self.conn:
                self.conn.execute("INSERT INTO clubs (name) VALUES (?)", (name,))
        except sqlite3.IntegrityError:
            raise AlreadyExists(f"Le club '{name}' existe déjà.")
    
    def addParticipant(self, firstname: str, lastname: str, clubID: int):
        with self.conn:
            self.conn.execute("INSERT INTO participants (prenom, nom, club) VALUES (?, ?, ?)", (firstname, lastname, clubID))

    def addCategory(self, name: str):
        try:
            with self.conn:
                self.conn.execute("INSERT INTO categories (name) VALUES (?)", (name,))
        except sqlite3.IntegrityError:
            raise AlreadyExists(f"Le style '{name}' existe déjà.")

    def addMatch(self, id1: int, id2: int, arbitre: int, assesseur: int,cat: str, s1: int, s2: int):
        with self.conn:
            self.cursor.execute("""
                INSERT INTO matches (combattant1, combattant2, arbitre, assesseur, categorie, score1, score2, date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (id1, id2, arbitre, assesseur, cat, s1, s2, datetime.datetime.now().isoformat()))
#endregion

#region Methods - Getters
    def getClubs(self):
        self.cursor.execute("SELECT id, name FROM clubs ORDER BY name")
        res = self.cursor.fetchall()

        # Convert the result of the sql query into a dictionary
        colonnes = ["id", "name"]
        clubs = [dict(zip(colonnes, row)) for row in res]

        return clubs
    
    def getClubIdByName(self,name: str):
        self.cursor.execute("SELECT id FROM clubs WHERE name = ?", (name,))
        res = self.cursor.fetchone()

        if res:
            return res[0]
        else:
            raise Unknown(f"Le club '{name}' n'existe pas.")
        
    def getClubIdByParticipantId(self,pId: int):
        self.cursor.execute("SELECT c.id FROM clubs c JOIN participants p ON c.id = p.club WHERE p.id = ?", (pId,))
        res = self.cursor.fetchone()

        if res:
            return res[0]
        else:
            raise Unknown(f"L'id de participant '{pId}' n'existe pas.")
    
    def getParticipants(self):
        self.cursor.execute("SELECT id, prenom, nom, club FROM participants ORDER BY nom")
        res = self.cursor.fetchall()

        # Convert the result of the sql query into a dictionary
        colonnes = ["id", "prenom", "nom","club"]
        participants = [dict(zip(colonnes, row)) for row in res]

        return participants
   

    def getCategories(self):
        self.cursor.execute("SELECT id, name FROM categories ORDER BY name")
        res = self.cursor.fetchall()

        # Convert the result of the sql query into a dictionary
        colonnes = ["id", "name"]
        categories = [dict(zip(colonnes, row)) for row in res]

        return categories
    
    def getCategoryIdByName(self,name: str):
        self.cursor.execute("SELECT id FROM categories WHERE name = ?", (name,))
        res = self.cursor.fetchone()

        if res:
            return res[0]
        else:
            raise Unknown(f"Le style '{name}' n'existe pas.")
        
    def getCategoryNameByID(self,id: int):
        self.cursor.execute("SELECT name FROM categories WHERE id = ?", (id,))
        res = self.cursor.fetchone()

        if res:
            return res[0]
        else:
            raise Unknown(f"Le style ayant pour id '{id}' n'existe pas.")
    
    
    def getMatches(self):
        self.cursor.execute("""
        SELECT r.id, p1.id, p1.prenom || ' ' || p1.nom, p2.id, p2.prenom || ' ' || p2.nom,
               arb.id, arb.prenom || ' ' || arb.nom, ass.id, ass.prenom || ' ' || ass.nom,
               r.score1, r.score2, r.categorie, r.date
        FROM matches r
        JOIN participants p1 ON r.combattant1 = p1.id
        JOIN participants p2 ON r.combattant2 = p2.id
        JOIN participants arb ON r.arbitre = arb.id
        JOIN participants ass ON r.assesseur = ass.id
        ORDER BY r.date DESC
        """)
        res = self.cursor.fetchall()

        # Convert the result of the sql query into a dictionary
        colonnes = [
        "id_match", 
        "id_combattant1", "nom_combattant1",
        "id_combattant2", "nom_combattant2",
        "id_arbitre", "nom_arbitre",
        "id_assesseur", "nom_assesseur",
        "score1", "score2", "categorie", "date"
        ]
        matches = [dict(zip(colonnes, row)) for row in res]
        return matches
#endregion

    
    def exporter_csv(self):
        with open("matches.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Combattant 1", "Score 1", "Combattant 2", "Score 2", "Catégorie", "Arbitre", "Assesseur"])
            self.cursor.execute("""
                SELECT p1.prenom || ' ' || p1.nom, p2.prenom || ' ' || p2.nom,
                    arb.prenom || ' ' || arb.nom, ass.prenom || ' ' || ass.nom,
                    r.score1, r.score2, r.categorie, r.date
                FROM matches r
                JOIN participants p1 ON r.combattant1 = p1.id
                JOIN participants p2 ON r.combattant2 = p2.id
                JOIN participants arb ON r.arbitre = arb.id
                JOIN participants ass ON r.assesseur = ass.id
            """)
            for row in self.cursor.fetchall():
                writer.writerow([row[7], row[0], row[4], row[1], row[5], row[6], row[2], row[3]])



class AlreadyExists(Exception):
    pass

class Unknown(Exception):
    pass