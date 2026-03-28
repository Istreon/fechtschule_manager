from src.database import *
from src.ranking import *


def exporter_matches_csv(db: DataBase):
    with open("matches.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Combattant 1", "Score 1", "Combattant 2", "Score 2", "Catégorie", "Arbitre", "Assesseur"])
        matches = db.getMatches()
        for row in matches:
            writer.writerow([row["date"], row["nom_combattant1"], row["score1"], row["nom_combattant2"], row["score2"], row["categorie"], row["nom_arbitre"], row["nom_assesseur"]])


def export_ranking(db: DataBase) :
     with open("ranking.csv", "w", newline="", encoding="utf-8") as f:
        categories = db.getCategories()
        main_ranking = rankingByFechtschuleScore(db)  
        categories_ranking = []
        for c in categories :
            ranking = rankingByFechtschuleScore(db,c["name"])  
            if len(ranking) > 0 :
                categories_ranking.append((c["name"],ranking))
        writer = csv.writer(f)
        head = ["Participant", "Toutes armes confondues"]
        for cr in categories_ranking :
            head.append(cr[0])
        writer.writerow(head)

        for mr in main_ranking:
            row =  [mr["name"], mr["score"]]
            for cr in categories_ranking :
                score = next((item["score"] for item in cr[1] if int(item["id"]) == int(mr["id"])), None)
                row.append(score)
            writer.writerow(row)


def export_summary(db: DataBase) :
    with open("summary.txt", "w", newline="", encoding="utf-8") as f:
        # Participants, clubs and matches count  
        f.write("=====================")        
        f.write("COMPTE RENDU GENERAL")
        f.write("=====================")
        f.write('\n')
        f.write("Lors de ce tournoi, ")  
        f.write(str(db.get_participants_count()))
        f.write(" participants provenant de ")
        f.write(str(db.get_clubs_count()))
        f.write(" clubs différents se sont affrontés au cours de ")
        f.write(str(db.get_matches_count()))  
        f.write(" duels.")  
        f.write('\n')

        citation_count = 3


        # Refereeing ranking
        f.write("\n\nParticipants ayant le plus de participation à l'arbitrage (")
        f.write(str(citation_count))
        f.write(" premiers, ordre décroissant)\n")
        referees = rankingByParticipationInRefereeing(db)
        max = min(citation_count,len(referees))
        for i in range(max) :
            k = max - 1 - i
            f.write(str(k+1))
            f.write("- ")
            f.write(referees[k]["name"])
            f.write(" (avec ")
            f.write(str(referees[k]["score"]))
            f.write(" participations)")
            f.write("\n")
        


        # Gala's fight
        f.write('\n\n')
        f.write("=====================")        
        f.write("COMBATS DE GALA")
        f.write("=====================")
        f.write("\n")
        f.write("Nombre de combats par catégorie d'armes (max 4), et combattants pour le gala :\n")
        cat_matches_count = rankingCategoriesByMatchesCount(db)
        max = min(4,len(cat_matches_count))
        for i in range(max) :
            k = max - 1 - i
            cat_scores = rankingByFechtschuleScore(db,cat_matches_count[k]["name"])
            if cat_matches_count[k]["score"] == 0 :
                continue
            if len(cat_scores) < 2 :
                continue
            f.write(str(k+1))
            f.write("- ")
            f.write(cat_matches_count[k]["name"])
            f.write(" (avec ")
            f.write(str(cat_matches_count[k]["score"]))
            f.write(" combats)")
            f.write("--> ")

            for j in range(2) :
                f.write(cat_scores[j]["name"])
                f.write(" (")
                f.write(str(cat_scores[j]["score"]))
                f.write(") ")
            f.write("\n")








        f.write('\n\n')
        f.write("=====================")        
        f.write("CLASSEMENT FINAL")
        f.write("=====================")
        f.write("\n")

        # Clubs ranking
        f.write("Classement des clubs par point de vie moyen :\n")
        clubs_mean_life_points = rankingByClubMeanLifePoints(db)
        for i in range(len(clubs_mean_life_points)) :
            k = len(clubs_mean_life_points) - 1 - i
            f.write(str(k+1))
            f.write("- ")
            f.write(clubs_mean_life_points[k]["name"])
            f.write(" (avec en moyenne ")
            f.write(str(clubs_mean_life_points[k]["score"]))
            f.write(" points de vie)")
            f.write("\n")



        # Clubs ranking
        f.write("\n\nClassement général des duellistes (pv/nbCombats * log(nbCombats + 1)) :\n")
        general_ranking = rankingByFechtschuleScore(db)
        count = 1
        lastDiffPos = 1
        lastDiff = -1
        for g in general_ranking :
            pos = count
            if(g["score"] == lastDiff):
                pos = lastDiffPos
            else :
                lastDiffPos = count
            f.write(str(pos))
            f.write("- ")
            f.write(g["name"])
            f.write(" (avec un score de ")
            f.write(str(g["score"]))
            f.write(")")
            f.write("\n")
            count = count + 1
            lastDiff = g["score"]



           