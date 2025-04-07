import tkinter as tk
from tkinter import ttk
from src.database import DataBase
from src.ranking import *


global comboBox_participants
comboBox_participants = []

global comboBox_categories
comboBox_categories = []


def ManagerGUI(root: tk.Tk,db: DataBase):
    return



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
            listbox.insert(tk.END, f"{pos} -- {d["prenom"]} {d["nom"]} ({d["score"]})")
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


    # Create frames with listboxes showing results
    rankingFrames = []
    rankingListboxes = []

    # Define frame name and the ranking function that will be used
    rankings = [
    ("Classement participation", rankingByParticipationAsFencer),
    ("Classement arbitrage", rankingByParticipationInRefereeing),
    ("Classement points de vie", rankingByTotalLifePoints),
    ("Classement ratio vie/rencontres", rankingByRatioTotalLifePointsToRencontres),
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
        win_ranking.after(2000, autoRefresh)  # toutes les 2 secondes

    autoRefresh()  # Lancer la boucle
#endregion