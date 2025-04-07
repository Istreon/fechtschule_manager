import tkinter as tk
from tkinter import ttk
from src.database import DataBase
from src.ranking import *

def ManagerGUI(root: tk.Tk,db: DataBase):
    return







#region Methods - ranking related
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



global cat_filter
cat_filter = "all" 

def RankingGUI(root: tk.Tk,db: DataBase, categories: list[str], width: int=40) :
    # Ranking related frames 
    win_ranking = tk.Toplevel(root)
    win_ranking.title("Classement")

    frame_filter = ttk.LabelFrame(win_ranking, text="Filtre")
    frame_filter.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    categories.insert(0, "all")
    
    def on_categorie_change(event):
        global cat_filter
        cat_filter = combo_categories.get()

    ttk.Label(frame_filter, text="Categorie").grid(row=0, column=0)
    combo_categories = ttk.Combobox(frame_filter, values=categories)
    combo_categories.set("all")
    combo_categories.grid(row=0, column=1)
    combo_categories.bind("<<ComboboxSelected>>", on_categorie_change)

    frame_ranking_1 = ttk.LabelFrame(win_ranking, text="Classement participation")
    frame_ranking_1.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    list_ranking_1= tk.Listbox(frame_ranking_1, width=width, height=30)
    list_ranking_1.pack(padx=5, pady=5)


    frame_ranking_2 = ttk.LabelFrame(win_ranking, text="Classement arbitrage")
    frame_ranking_2.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
    list_ranking_2= tk.Listbox(frame_ranking_2, width=width, height=30)
    list_ranking_2.pack(padx=5, pady=5)


    frame_ranking_3 = ttk.LabelFrame(win_ranking, text="Classement points de vie")
    frame_ranking_3.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
    list_ranking_3= tk.Listbox(frame_ranking_3, width=width, height=30)
    list_ranking_3.pack(padx=5, pady=5)


    frame_ranking_4 = ttk.LabelFrame(win_ranking, text="Classement ratio vie/rencontres")
    frame_ranking_4.grid(row=1, column=3, padx=10, pady=10, sticky="ew")
    list_ranking_4= tk.Listbox(frame_ranking_4, width=width, height=30)
    list_ranking_4.pack(padx=5, pady=5)

    frame_ranking_5 = ttk.LabelFrame(win_ranking, text="Classement ratio victoire/défaite")
    frame_ranking_5.grid(row=1, column=4, padx=10, pady=10, sticky="ew")
    list_ranking_5= tk.Listbox(frame_ranking_5, width=width, height=30)
    list_ranking_5.pack(padx=5, pady=5)


    def autoRefresh():
        global cat_filter
        refreshRanking(list_ranking_1, rankingByParticipationAsFencer(db,cat_filter))
        refreshRanking(list_ranking_2, rankingByParticipationInRefereeing(db,cat_filter))
        refreshRanking(list_ranking_3, rankingByTotalLifePoints(db,cat_filter))
        refreshRanking(list_ranking_4, rankingByRatioTotalLifePointsToRencontres(db,cat_filter))
        refreshRanking(list_ranking_5, rankingByRatioVictoryToDefeat(db,cat_filter))
        win_ranking.after(2000, autoRefresh)  # toutes les 2 secondes

    autoRefresh()  # Lancer la boucle
#endregion