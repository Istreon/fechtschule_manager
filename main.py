import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime
import csv
import threading

# --- Base de donnees ---
conn = sqlite3.connect("tournoi.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT,
    prenom TEXT
)
""")

c.execute("""
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

conn.commit()

# --- Données ---
CATEGORIES = ["Épée", "Sabre", "Rapière", "Autre"]

# --- GUI ---
root = tk.Tk()
root.title("Gestion de Tournoi")

# Frame pour ajouter un participant
frame_participant = ttk.LabelFrame(root, text="Ajouter un participant")
frame_participant.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

ttk.Label(frame_participant, text="Prénom").grid(row=0, column=0)
entry_prenom = ttk.Entry(frame_participant)
entry_prenom.grid(row=0, column=1)

ttk.Label(frame_participant, text="Nom").grid(row=1, column=0)
entry_nom = ttk.Entry(frame_participant)
entry_nom.grid(row=1, column=1)

def ajouter_participant():
    prenom = entry_prenom.get()
    nom = entry_nom.get()
    if prenom and nom:
        c.execute("INSERT INTO participants (prenom, nom) VALUES (?, ?)", (prenom, nom))
        conn.commit()
        entry_prenom.delete(0, tk.END)
        entry_nom.delete(0, tk.END)
        rafraichir_listes()
        rafraichir_rencontres()
    else:
        messagebox.showwarning("Champs manquants", "Veuillez remplir le prénom et le nom.")

ttk.Button(frame_participant, text="Ajouter", command=ajouter_participant).grid(row=2, column=0, columnspan=2, pady=5)

# Frame pour enregistrer une rencontre
frame_rencontre = ttk.LabelFrame(root, text="Enregistrer une rencontre")
frame_rencontre.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

combattant1_var = tk.StringVar()
combattant2_var = tk.StringVar()
arbitre_var = tk.StringVar()
assesseur_var = tk.StringVar()
categorie_var = tk.StringVar(value=CATEGORIES[0])
score1_var = tk.IntVar(value=0)
score2_var = tk.IntVar(value=0)

def filtrer_listes(*args):
    selection = set()
    for var in [combattant1_var, combattant2_var, arbitre_var, assesseur_var]:
        try:
            selection.add(int(var.get().split(" - ")[0]))
        except:
            pass

    c.execute("SELECT id, prenom, nom FROM participants")
    participants = c.fetchall()
    liste = [f"{id} - {prenom} {nom}" for id, prenom, nom in participants if id not in selection or f"{id} - {prenom} {nom}" == combattant1_var.get() or f"{id} - {prenom} {nom}" == combattant2_var.get() or f"{id} - {prenom} {nom}" == arbitre_var.get() or f"{id} - {prenom} {nom}" == assesseur_var.get()]

    combo_combattant1["values"] = liste
    combo_combattant2["values"] = liste
    combo_arbitre["values"] = liste
    combo_assesseur["values"] = liste

ttk.Label(frame_rencontre, text="Combattant 1").grid(row=0, column=0)
combo_combattant1 = ttk.Combobox(frame_rencontre, textvariable=combattant1_var)
combo_combattant1.grid(row=0, column=1)

ttk.Label(frame_rencontre, text="Combattant 2").grid(row=1, column=0)
combo_combattant2 = ttk.Combobox(frame_rencontre, textvariable=combattant2_var)
combo_combattant2.grid(row=1, column=1)

ttk.Label(frame_rencontre, text="Arbitre").grid(row=2, column=0)
combo_arbitre = ttk.Combobox(frame_rencontre, textvariable=arbitre_var)
combo_arbitre.grid(row=2, column=1)

ttk.Label(frame_rencontre, text="Assesseur").grid(row=3, column=0)
combo_assesseur = ttk.Combobox(frame_rencontre, textvariable=assesseur_var)
combo_assesseur.grid(row=3, column=1)

for var in [combattant1_var, combattant2_var, arbitre_var, assesseur_var]:
    var.trace_add("write", filtrer_listes)

ttk.Label(frame_rencontre, text="Catégorie").grid(row=4, column=0)
combo_categorie = ttk.Combobox(frame_rencontre, textvariable=categorie_var, values=CATEGORIES)
combo_categorie.grid(row=4, column=1)

ttk.Label(frame_rencontre, text="Score Combattant 1").grid(row=5, column=0)
spin_score1 = ttk.Spinbox(frame_rencontre, from_=0, to=6, textvariable=score1_var)
spin_score1.grid(row=5, column=1)

ttk.Label(frame_rencontre, text="Score Combattant 2").grid(row=6, column=0)
spin_score2 = ttk.Spinbox(frame_rencontre, from_=0, to=6, textvariable=score2_var)
spin_score2.grid(row=6, column=1)

def enregistrer_rencontre():
    try:
        id1 = int(combattant1_var.get().split(" - ")[0])
        id2 = int(combattant2_var.get().split(" - ")[0])
        arbitre = int(arbitre_var.get().split(" - ")[0])
        assesseur = int(assesseur_var.get().split(" - ")[0])
        cat = categorie_var.get()
        s1 = score1_var.get()
        s2 = score2_var.get()

        ids = [id1, id2, arbitre, assesseur]
        if len(set(ids)) < 4:
            messagebox.showerror("Erreur", "Un participant ne peut apparaître qu'une seule fois dans une rencontre.")
            return

        if s1 != 0 and s2 != 0:
            messagebox.showerror("Erreur", "Un seul score peut être non nul !")
            return

        c.execute("""
            INSERT INTO rencontres (combattant1, combattant2, arbitre, assesseur, categorie, score1, score2, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id1, id2, arbitre, assesseur, cat, s1, s2, datetime.datetime.now().isoformat()))
        conn.commit()
        messagebox.showinfo("Succès", "Rencontre enregistrée !")
        rafraichir_rencontres()
    except Exception as e:
        messagebox.showerror("Erreur", str(e))

ttk.Button(frame_rencontre, text="Enregistrer", command=enregistrer_rencontre).grid(row=7, column=0, columnspan=2, pady=5)

# Frame pour afficher les rencontres
frame_liste = ttk.LabelFrame(root, text="Rencontres enregistrées")
frame_liste.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

entry_recherche = ttk.Entry(frame_liste)
entry_recherche.pack(pady=5)

liste_rencontres = tk.Listbox(frame_liste, width=100)
liste_rencontres.pack(padx=5, pady=5)

def rafraichir_rencontres(filtre=""):
    liste_rencontres.delete(0, tk.END)
    c.execute("""
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
    for row in c.fetchall():
        ligne = f"{row[8][:16]} - {row[1]} ({row[5]}) vs {row[2]} ({row[6]}) [{row[7]}] - Arbitre: {row[3]}, Assesseur: {row[4]}"
        if filtre.lower() in ligne.lower():
            liste_rencontres.insert(tk.END, ligne)

def rechercher_rencontres(event):
    texte = entry_recherche.get()
    rafraichir_rencontres(texte)

entry_recherche.bind("<KeyRelease>", rechercher_rencontres)

def exporter_csv():
    with open("rencontres.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Combattant 1", "Score 1", "Combattant 2", "Score 2", "Catégorie", "Arbitre", "Assesseur"])
        c.execute("""
            SELECT p1.prenom || ' ' || p1.nom, p2.prenom || ' ' || p2.nom,
                   arb.prenom || ' ' || arb.nom, ass.prenom || ' ' || ass.nom,
                   r.score1, r.score2, r.categorie, r.date
            FROM rencontres r
            JOIN participants p1 ON r.combattant1 = p1.id
            JOIN participants p2 ON r.combattant2 = p2.id
            JOIN participants arb ON r.arbitre = arb.id
            JOIN participants ass ON r.assesseur = ass.id
        """)
        for row in c.fetchall():
            writer.writerow([row[7], row[0], row[4], row[1], row[5], row[6], row[2], row[3]])
    messagebox.showinfo("Export", "Export CSV terminé : rencontres.csv")

ttk.Button(frame_liste, text="Exporter en CSV", command=exporter_csv).pack(pady=5)

# Mise à jour des listes déroulantes

def rafraichir_listes():
    c.execute("SELECT id, prenom, nom FROM participants")
    participants = [f"{row[0]} - {row[1]} {row[2]}" for row in c.fetchall()]
    combo_combattant1["values"] = participants
    combo_combattant2["values"] = participants
    combo_arbitre["values"] = participants
    combo_assesseur["values"] = participants

rafraichir_listes()
rafraichir_rencontres()

# Sauvegarde automatique

def sauvegarde_auto():
    conn.commit()
    root.after(30000, sauvegarde_auto)  # toutes les 30 secondes

sauvegarde_auto()

root.mainloop()

conn.close()