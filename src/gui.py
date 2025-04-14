import tkinter as tk
from tkinter import ttk, messagebox
from src.database import DataBase, AlreadyExists, Unknown
from src.ranking import *

#=====================================================#
#======================== GUI ========================#
#=====================================================#

global comboBox_participants
comboBox_participants = []

global comboBox_categories
comboBox_categories = []

global comboBox_clubs
comboBox_clubs = []

global listBox_matches
listBox_matches = []

def refreshParticipantLists(db: DataBase):
    p = db.getParticipants()
    participants = [f"{row["id"]} - {row["prenom"]} {row["nom"]}" for row in p]
    for cbp in comboBox_participants:
        cbp["values"] = participants

def refreshClubLists(db: DataBase):
    c = db.getClubs()
    clubs = [f"{row["name"]}" for row in c]
    for cbc in comboBox_clubs:
        cbc["values"] = clubs

def refreshCategoryLists(db: DataBase):
    categories = db.getCategories()
    cat_list = [f"{row["name"]}" for row in categories]
    for cbc in comboBox_categories:
        cbc["value"] = cat_list

def GUI(db: DataBase):
    root = tk.Tk()
    root.title("Fechtschule manager")

    
    ManagerGUI(root,db)
    RankingGUI(root,db,40)


    refreshParticipantLists(db)
    refreshMatches(db)
    refreshCategoryLists(db)
    refreshClubLists(db)

    root.mainloop()



#=====================================================#
#==================== MANAGER GUI ====================#
#=====================================================#

def refreshMatches(db: DataBase, filtre=""):
    for l in listBox_matches:
        l.delete(0, tk.END)
        rencontres = db.getMatches()
        for row in rencontres:
            catname = db.getCategoryNameByID(row["categorie"])
            ligne = f"{row["date"][:16]} - {row["nom_combattant1"]} ({row["score1"]}) vs {row["nom_combattant2"]} ({row["score2"]}) [{catname}] - Arbitre: {row["nom_arbitre"]}, Assesseur: {row["nom_assesseur"]}"
            if filtre.lower() in ligne.lower():
                l.insert(tk.END, ligne)

def ManagerGUI(root: tk.Tk,db: DataBase):
    AddFrame(root,db,0,0)
    MatchesFrame(root,db,1,0)
    return

def MatchesFrame(root: tk.Tk,db: DataBase, row: int, column: int) :
    frame_matches = ttk.LabelFrame(root, text="Rencontres")
    frame_matches.grid(row=row, column=column, padx=10, pady=10, sticky="ew")
    AddMatchFrame(frame_matches,db,0,0)
    ShowMatchesFrame(frame_matches,db,0,1)

def AddFrame(root: tk.Tk,db: DataBase, row: int, column: int):
    frame_add = ttk.LabelFrame(root, text="Ajouter")
    frame_add.grid(row=row, column=column, padx=10, pady=10, sticky="ew")
    AddParticipantFrame(frame_add,db,0,0)
    AddCategoryFrame(frame_add,db,0,1)
    AddClubFrame(frame_add,db,0,2)


def AddParticipantFrame(root: tk.Tk,db: DataBase, row: int, column: int) :
    # Frame creation
    frame_participant = ttk.LabelFrame(root, text="Ajouter un participant")
    frame_participant.grid(row=row, column=column, padx=10, pady=10, sticky="ns")

    # Text input creation
    ttk.Label(frame_participant, text="Prénom").grid(row=0, column=0)
    entry_prenom = ttk.Entry(frame_participant)
    entry_prenom.grid(row=0, column=1)

    # Button creation (function and button)
    ttk.Label(frame_participant, text="Nom").grid(row=1, column=0)
    entry_nom = ttk.Entry(frame_participant)
    entry_nom.grid(row=1, column=1)


    # Club entry
    ttk.Label(frame_participant, text="Club").grid(row=2, column=0)
    combo_club = ttk.Combobox(frame_participant)
    combo_club.grid(row=2, column=1)
    comboBox_clubs.append(combo_club)

    def ajouter_participant():
        prenom = entry_prenom.get()
        nom = entry_nom.get()
        try:
            club = db.getClubIdByName(combo_club.get())
        except Unknown as e:
                messagebox.showinfo("Inconnu", str(e))
                return
        if prenom and nom and club:
            db.addParticipant(prenom,nom,club)
            entry_prenom.delete(0, tk.END)
            entry_nom.delete(0, tk.END)
            combo_club.delete(0, tk.END)
            refreshParticipantLists(db)
            refreshMatches(db)
        else:
            messagebox.showwarning("Champs manquants", "Veuillez remplir le prénom et le nom.")

    ttk.Button(frame_participant, text="Ajouter", command=ajouter_participant).grid(row=3, column=0, columnspan=2, pady=5)


def AddCategoryFrame(root: tk.Tk,db: DataBase, row: int, column: int):
    # Frame creation
    frame_category = ttk.LabelFrame(root, text="Ajouter un style de combat")
    frame_category.grid(row=row, column=column, padx=10, pady=10, sticky="ns")

    # Text input creation
    ttk.Label(frame_category, text="Nom").grid(row=0, column=0)
    entry_catname = ttk.Entry(frame_category)
    entry_catname.grid(row=0, column=1)

    # Button creation (function and button)
    def addCategory():
        catName = entry_catname.get()
        if catName :
            try:
                db.addCategory(catName)
            except AlreadyExists as e:
                messagebox.showinfo("Doublon", str(e))
            entry_catname.delete(0, tk.END)
            refreshCategoryLists(db)
        else:
            messagebox.showwarning("Champs manquants", "Veuillez remplir le nom.")

    ttk.Button(frame_category, text="Ajouter", command=addCategory).grid(row=1, column=0, columnspan=2, pady=5)

def AddClubFrame(root: tk.Tk,db: DataBase, row: int, column: int):
    # Frame creation
    frame_club = ttk.LabelFrame(root, text="Ajouter un club")
    frame_club.grid(row=row, column=column, padx=10, pady=10, sticky="ns")

    # Text input creation
    ttk.Label(frame_club, text="Nom").grid(row=0, column=0)
    entry_clubname = ttk.Entry(frame_club)
    entry_clubname.grid(row=0, column=1)

    # Button creation (function and button)
    def addClub():
        clubName = entry_clubname.get()
        if clubName :
            try:
                db.addClub(clubName)
            except AlreadyExists as e:
                messagebox.showinfo("Doublon", str(e))
            entry_clubname.delete(0, tk.END)
            refreshClubLists(db)
        else:
            messagebox.showwarning("Champs manquants", "Veuillez remplir le nom.")

    ttk.Button(frame_club, text="Ajouter", command=addClub).grid(row=1, column=0, columnspan=2, pady=5)


def AddMatchFrame(root: tk.Tk,db: DataBase, row: int, column: int):
    # Frame creation
    frame_rencontre = ttk.LabelFrame(root, text="Enregistrer une rencontre")
    frame_rencontre.grid(row=row, column=column, padx=10, pady=10,sticky="ns")

    # Participants entries
    requiredParticipants = ["Combattant 1","Combattant 2","Arbitre","Assesseur"]
    i = 0
    for s in requiredParticipants :
        ttk.Label(frame_rencontre, text=s).grid(row=i, column=0)
        combo = ttk.Combobox(frame_rencontre, textvariable=tk.StringVar())
        combo.grid(row=i, column=1)
        comboBox_participants.append(combo)
        i = i + 1

    # Category entry
    categorie_var = tk.StringVar(value="")
    ttk.Label(frame_rencontre, text="Catégorie").grid(row=4, column=0)
    combo_categorie = ttk.Combobox(frame_rencontre, textvariable=categorie_var)
    combo_categorie.grid(row=4, column=1)
    comboBox_categories.append(combo_categorie)
    # Score entries
    score1_var = tk.IntVar(value=0)
    ttk.Label(frame_rencontre, text="Point de vie Combattant 1").grid(row=5, column=0)
    spin_score1 = ttk.Spinbox(frame_rencontre, from_=0, to=6, textvariable=score1_var)
    spin_score1.grid(row=5, column=1)

    score2_var = tk.IntVar(value=0)
    ttk.Label(frame_rencontre, text="Point de vie Combattant 2").grid(row=6, column=0)
    spin_score2 = ttk.Spinbox(frame_rencontre, from_=0, to=6, textvariable=score2_var)
    spin_score2.grid(row=6, column=1)

    def registerMatch():
        try:
            id1 = int(comboBox_participants[0].get().split(" - ")[0])
            id2 = int(comboBox_participants[1].get().split(" - ")[0])
            arbitre = int(comboBox_participants[2].get().split(" - ")[0])
            assesseur = int(comboBox_participants[3].get().split(" - ")[0])
            cat = categorie_var.get()
            s1 = score1_var.get()
            s2 = score2_var.get()

            ids = [id1, id2, arbitre, assesseur]
            if len(set(ids)) < 4:
                messagebox.showerror("Erreur", "Un participant ne peut apparaître qu'une seule fois dans une rencontre.")
                return
            
            if len(cat) < 1:
                messagebox.showerror("Erreur", "Un style de combat doit être sélectionné.")
                return

            if s1 != 0 and s2 != 0:
                messagebox.showerror("Erreur", "Un seul score peut être non nul !")
                return
            
            db.addMatch(id1, id2, arbitre, assesseur, db.getCategoryIdByName(cat), s1, s2)
            messagebox.showinfo("Succès", "Rencontre enregistrée !")
            refreshMatches(db)
        except Exception as e:
            messagebox.showerror("Erreur", str(e))

    ttk.Button(frame_rencontre, text="Enregistrer", command=registerMatch).grid(row=7, column=0, columnspan=2, pady=5)



def ShowMatchesFrame(root: tk.Tk,db: DataBase, row: int, column: int):
    frame_liste = ttk.LabelFrame(root, text="Rencontres enregistrées")
    frame_liste.grid(row=row, column=column, padx=10, pady=10, sticky="ew")

    entry_recherche = ttk.Entry(frame_liste)
    entry_recherche.pack(pady=5)

    listMatches = tk.Listbox(frame_liste, width=150)
    listMatches.pack(padx=5, pady=5)

    listBox_matches.append(listMatches)
    def searchMatches(event):
        texte = entry_recherche.get()
        refreshMatches(listMatches,texte)

    entry_recherche.bind("<KeyRelease>", searchMatches)

    def exporter_csv():
        db.exporter_csv()
        messagebox.showinfo("Export", "Export CSV terminé : rencontres.csv")

    ttk.Button(frame_liste, text="Exporter en CSV", command=exporter_csv).pack(pady=5)

#region Methods - ranking related

#=====================================================#
#==================== RANKING GUI ====================#
#=====================================================#

def refreshRanking(listbox: tk.Listbox, data: dict):
        listbox.delete(0, tk.END)
        count = 1
        lastDiffPos = 1
        lastDiff = -1
        for d in data:
            pos = count
            if(d["score"] == lastDiff):
                pos = lastDiffPos
            else :
                lastDiffPos = count
            listbox.insert(tk.END, f"{pos} -- {d["name"]} ({d["score"]})")
            count = count + 1
            lastDiff = d["score"]


def RankingGUI(root: tk.Tk,db: DataBase, width: int=40) :
    # Create a separate windows from root
    win_ranking = tk.Toplevel(root)
    win_ranking.title("Classement")

    # Create a frame for filtering
    frame_filter = ttk.LabelFrame(win_ranking, text="Filtre")
    frame_filter.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    # Create a filter for fighting style category using a combobox
    categories = db.getCategories()
    cat_names = [cat["name"] for cat in categories]
    cat_names.insert(0, "all") # Add a category "all" to check global ranking

    global cat_filter
    cat_filter = cat_names[0]
    
    def on_categorie_change(event):
        global cat_filter
        cat_filter = combo_categories.get()

    ttk.Label(frame_filter, text="Categorie").grid(row=0, column=0)
    combo_categories = ttk.Combobox(frame_filter, values=cat_names)
    combo_categories.set("all")
    combo_categories.grid(row=0, column=1)
    combo_categories.bind("<<ComboboxSelected>>", on_categorie_change)


    #kjsdnvjvn
    frame_categoryMatches = ttk.LabelFrame(win_ranking, text="Nombre de combats par catégorie")
    frame_categoryMatches.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

    list_categoryMatches = tk.Listbox(frame_categoryMatches, width=width, height=10)
    list_categoryMatches.pack(padx=5, pady=5)


    # Create frames with listboxes showing results
    rankingFrames = []
    rankingListboxes = []

    # Define frame name and the ranking function that will be used
    rankings = [
    ("Classement individuel : Feshtschule score", rankingByFeshtschuleScore),
    ("Classement participation", rankingByParticipationAsFencer),
    ("Classement arbitrage", rankingByParticipationInRefereeing),
    ("Classement club : moyenne points de vie", rankingByClubMeanLifePoints),
    ("Classement points de vie", rankingByTotalLifePoints),
    ("Classement ratio victoire/défaite", rankingByRatioVictoryToDefeat),
    ]

    for i in range(len(rankings)):
        label, _ = rankings[i]

        frame_ranking = ttk.LabelFrame(win_ranking, text=label)
        frame_ranking.grid(row=1, column=i, padx=10, pady=10, sticky="ew")
        rankingFrames.append(frame_ranking)
        list_ranking= tk.Listbox(frame_ranking, width=width, height=30)
        list_ranking.pack(padx=5, pady=5)
        rankingListboxes.append(list_ranking)

    def autoRefresh():
        global cat_filter
        for i in range(len(rankings)):
            _ , func = rankings[i]
            refreshRanking(rankingListboxes[i], func(db,cat_filter))
        refreshRanking(list_categoryMatches, rankingCategoriesByMatchesCount(db))
        win_ranking.after(2000, autoRefresh)  # toutes les 2 secondes

    autoRefresh()  # Lancer la boucle
#endregion