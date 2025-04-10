from src.database import DataBase



import math

def truncate_float(value: float, decimals: int = 2) -> float:
    factor = 10.0 ** decimals
    return math.trunc(value * factor) / factor



def rankingByFeshtschuleScore(db: DataBase, cat: str = "all"): #Score final = (PV_totaux / Nb_combats) × log(Nb_combats + 1)
    participants=db.getParticipants()
    matches=db.getMatches()

    results = []

    for p in participants :
        id = p["id"]
        lifePoints = 0
        nbMatches = 0
        for r in matches :
            if cat!= "all" and db.getCategoryNameByID(r["categorie"])!= cat : 
                continue
            if(r["id_combattant1"] == id) :
                lifePoints = lifePoints + r["score1"]
                nbMatches = nbMatches + 1
                
            if(r["id_combattant2"] == id) :
                lifePoints = lifePoints + r["score2"]
                nbMatches = nbMatches + 1

        score = 0
        if(nbMatches > 0 ) : 
            score = (lifePoints / nbMatches) * math.log(nbMatches + 1)
            res = {"id": id, "name": p["prenom"] + ' ' + p["nom"], "score": truncate_float(score)}
            results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results

# - Le premier critère est d'afficher les combattants ayant le plus de participation en tant que combattant à des rencontres

def rankingByParticipationAsFencer(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    matches=db.getMatches()

    results = []

    for p in participants :
        id = p["id"]
        nbMatches = 0
        for r in matches :
            if cat!= "all" and db.getCategoryNameByID(r["categorie"])!= cat : 
                continue
            if(r["id_combattant1"] == id or r["id_combattant2"] == id) :
                nbMatches = nbMatches + 1
        if(nbMatches > 0 ) : 
            res = {"id": id, "name": p["prenom"] + ' ' + p["nom"], "score": nbMatches}
            results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results


# - Le second critère est pareil mais pour l'arbitre (en mélangeant assesseur et arbitre)

def rankingByParticipationInRefereeing(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    matches=db.getMatches()

    results = []

    for p in participants :
        id = p["id"]
        nbMatches = 0
        for r in matches :
            if cat!= "all" and db.getCategoryNameByID(r["categorie"])!= cat : 
                continue
            if(r["id_arbitre"] == id or r["id_assesseur"] == id) :
                nbMatches = nbMatches + 1
        if(nbMatches > 0 ) : 
            res = {"id": id, "name": p["prenom"] + ' ' + p["nom"], "score": nbMatches}
            results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results


# - Ensuite le critère suivant est le total des points obtenus à la fin d'une rencontre.

def rankingByTotalLifePoints(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    matches=db.getMatches()

    results = []

    for p in participants :
        id = p["id"]
        lifePoints = 0
        nbMatches = 0
        for r in matches :
            if cat!= "all" and db.getCategoryNameByID(r["categorie"])!= cat : 
                continue
            if(r["id_combattant1"] == id) :
                lifePoints = lifePoints + r["score1"]
                nbMatches = nbMatches + 1
                
            if(r["id_combattant2"] == id) :
                lifePoints = lifePoints + r["score2"]
                nbMatches = nbMatches + 1

        if(nbMatches > 0 ) : 
            res = {"id": id, "name": p["prenom"] + ' ' + p["nom"], "score": lifePoints}
            results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results

# - Ensuite, le critère suivant est le ratio entre le le total de point et le nombre de rencontre

def rankingByRatioTotalLifePointsToRencontres(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    matches=db.getMatches()

    results = []

    for p in participants :
        id = p["id"]
        lifePoints = 0
        nbMatches = 0
        for r in matches :
            if cat!= "all" and db.getCategoryNameByID(r["categorie"])!= cat : 
                continue
            if(r["id_combattant1"] == id) :
                lifePoints = lifePoints + r["score1"]
                nbMatches = nbMatches + 1
                
            if(r["id_combattant2"] == id) :
                lifePoints = lifePoints + r["score2"]
                nbMatches = nbMatches + 1

        ratio = 0
        if(nbMatches > 0 ) : 
            ratio = lifePoints / nbMatches
            res = {"id": id, "name": p["prenom"] + ' ' + p["nom"], "score": truncate_float(ratio)}
            results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results


# - Le critère suivant et le ratio victoire/défaite (sachant que le score 0 vaut une défaite, et le score > 0 une victoire)
def rankingByRatioVictoryToDefeat(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    matches=db.getMatches()

    results = []

    for p in participants :
        id = p["id"]
        victories = 0
        nbMatches = 0
        for r in matches :
            if cat!= "all" and db.getCategoryNameByID(r["categorie"])!= cat : 
                continue
            if(r["id_combattant1"] == id) :
                nbMatches = nbMatches + 1
                if(r["score1"] > 0):
                    victories = victories + 1
                
                
            if(r["id_combattant2"] == id) :
                nbMatches = nbMatches + 1
                if(r["score2"] > 0):
                    victories = victories + 1

        ratio = 0
        if(nbMatches > 0 ) : 
            ratio = victories / nbMatches
            res = {"id": id, "name": p["prenom"] + ' ' + p["nom"], "score": truncate_float(ratio*100,1)}
            results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results





def rankingByClubMeanLifePoints(db: DataBase, cat: str = "all"):
    clubs=db.getClubs()
    matches=db.getMatches()

    results = []

    for c in clubs :
        id = c["id"]
        lifePoints = 0
        nbMatches = 0
        for r in matches :
            if cat!= "all" and db.getCategoryNameByID(r["categorie"])!= cat : 
                continue
            if(db.getClubIdByParticipantId(r["id_combattant1"]) == id) :
                lifePoints = lifePoints + r["score1"]
                nbMatches = nbMatches + 1
                
            if(db.getClubIdByParticipantId(r["id_combattant2"]) == id) :
                lifePoints = lifePoints + r["score2"]
                nbMatches = nbMatches + 1

        ratio = 0
        if(nbMatches > 0 ) : 
            ratio = lifePoints / nbMatches
            res = {"id": id, "name": c["name"], "score": truncate_float(ratio)}
            results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results