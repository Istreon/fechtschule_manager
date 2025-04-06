from src.database import DataBase

# - Le premier critère est d'afficher les combattants ayant le plus de participation en tant que combattant à des rencontres

def rankingByParticipationAsFencer(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    rencontres=db.getRencontres()

    results = []

    for p in participants :
        id = p["id"]
        nbRecontres = 0
        for r in rencontres :
            if cat!= "all" and r["categorie"]!= cat : 
                continue
            if(r["id_combattant1"] == id or r["id_combattant2"] == id) :
                nbRecontres = nbRecontres + 1
        res = {"id": id, "prenom": p["prenom"], "nom": p["nom"], "score": nbRecontres}
        results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results


# - Le second critère est pareil mais pour l'arbitre (en mélangeant assesseur et arbitre)

def rankingByParticipationInRefereeing(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    rencontres=db.getRencontres()

    results = []

    for p in participants :
        id = p["id"]
        nbRecontres = 0
        for r in rencontres :
            if cat!= "all" and r["categorie"]!= cat : 
                continue
            if(r["id_arbitre"] == id or r["id_assesseur"] == id) :
                nbRecontres = nbRecontres + 1
        res = {"id": id, "prenom": p["prenom"], "nom": p["nom"], "score": nbRecontres}
        results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results


# - Ensuite le critère suivant est le total des points obtenus à la fin d'une rencontre.

def rankingByTotalLifePoints(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    rencontres=db.getRencontres()

    results = []

    for p in participants :
        id = p["id"]
        lifePoints = 0
        for r in rencontres :
            if cat!= "all" and r["categorie"]!= cat : 
                continue
            if(r["id_combattant1"] == id) :
                lifePoints = lifePoints + r["score1"]
                
            if(r["id_combattant2"] == id) :
                lifePoints = lifePoints + r["score2"]

        res = {"id": id, "prenom": p["prenom"], "nom": p["nom"], "score": lifePoints}
        results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results

# - Ensuite, le critère suivant est le ratio entre le le total de point et le nombre de rencontre

def rankingByRatioTotalLifePointsToRencontres(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    rencontres=db.getRencontres()

    results = []

    for p in participants :
        id = p["id"]
        lifePoints = 0
        nbRecontres = 0
        for r in rencontres :
            if cat!= "all" and r["categorie"]!= cat : 
                continue
            if(r["id_combattant1"] == id) :
                lifePoints = lifePoints + r["score1"]
                nbRecontres = nbRecontres + 1
                
            if(r["id_combattant2"] == id) :
                lifePoints = lifePoints + r["score2"]
                nbRecontres = nbRecontres + 1

        ratio = 0
        if(nbRecontres > 0 ) : 
            ratio = lifePoints / nbRecontres

        res = {"id": id, "prenom": p["prenom"], "nom": p["nom"], "score": ratio}
        results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results


# - Le critère suivant et le ratio victoire/défaite (sachant que le score 0 vaut une défaite, et le score > 0 une victoire)
def rankingByRatioVictoryToDefeat(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    rencontres=db.getRencontres()

    results = []

    for p in participants :
        id = p["id"]
        victories = 0
        nbRecontres = 0
        for r in rencontres :
            if cat!= "all" and r["categorie"]!= cat : 
                continue
            if(r["id_combattant1"] == id) :
                nbRecontres = nbRecontres + 1
                if(r["score1"] > 0):
                    victories = victories + 1
                
                
            if(r["id_combattant2"] == id) :
                nbRecontres = nbRecontres + 1
                if(r["score2"] > 0):
                    victories = victories + 1

        ratio = 0
        if(nbRecontres > 0 ) : 
            ratio = victories / nbRecontres

        res = {"id": id, "prenom": p["prenom"], "nom": p["nom"], "score": ratio}
        results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results