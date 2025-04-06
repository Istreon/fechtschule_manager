from src.database import DataBase

# - Le premier critère est d'afficher les combattants ayant le plus de participation en tant que combattant à des rencontres

def rankingByParticipationAsFencer(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    rencontres=db.getRencontres()

    results = []

    for p in participants :
        p[0] #Id
        nbRecontres = 0
        for r in rencontres :
            if cat!= "all" and r[11]!= cat : 
                continue
            if(r[1] == p[0] or r[3] == p[0]) :
                nbRecontres = nbRecontres + 1
        res = {"id": p[0], "prenom": p[1], "nom": p[2], "score": nbRecontres}
        results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results


# - Le second critère est pareil mais pour l'arbitre (en mélangeant assesseur et arbitre)

def rankingByParticipationInRefereeing(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    rencontres=db.getRencontres()

    results = []

    for p in participants :
        p[0] #Id
        nbRecontres = 0
        for r in rencontres :
            if cat!= "all" and r[11]!= cat : 
                continue
            if(r[5] == p[0] or r[7] == p[0]) :
                nbRecontres = nbRecontres + 1
        res = {"id": p[0], "prenom": p[1], "nom": p[2], "score": nbRecontres}
        results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results


# - Ensuite le critère suivant est le total des points obtenus à la fin d'une rencontre.

def rankingByTotalLifePoints(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    rencontres=db.getRencontres()

    results = []

    for p in participants :
        p[0] #Id
        lifePoints = 0
        for r in rencontres :
            if cat!= "all" and r[11]!= cat : 
                continue
            if(r[1] == p[0]) :
                lifePoints = lifePoints + r[9]
                
            if(r[3] == p[0]) :
                lifePoints = lifePoints + r[10]

        res = {"id": p[0], "prenom": p[1], "nom": p[2], "score": lifePoints}
        results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results

# - Ensuite, le critère suivant est le ratio entre le le total de point et le nombre de rencontre

def rankingByRatioTotalLifePointsToRencontres(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    rencontres=db.getRencontres()

    results = []

    for p in participants :
        p[0] #Id
        lifePoints = 0
        nbRecontres = 0
        for r in rencontres :
            if cat!= "all" and r[11]!= cat : 
                continue
            if(r[1] == p[0]) :
                lifePoints = lifePoints + r[9]
                nbRecontres = nbRecontres + 1
                
            if(r[3] == p[0]) :
                lifePoints = lifePoints + r[10]
                nbRecontres = nbRecontres + 1

        ratio = 0
        if(nbRecontres > 0 ) : 
            ratio = lifePoints / nbRecontres

        res = {"id": p[0], "prenom": p[1], "nom": p[2], "score": ratio}
        results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results


# - Le critère suivant et le ratio victoire/défaite (sachant que le score 0 vaut une défaite, et le score > 0 une victoire)
def rankingByRatioVictoryToDefeat(db: DataBase, cat: str = "all"):
    participants=db.getParticipants()
    rencontres=db.getRencontres()

    results = []

    for p in participants :
        p[0] #Id
        victories = 0
        nbRecontres = 0
        for r in rencontres :
            if cat!= "all" and r[11]!= cat : 
                continue
            if(r[1] == p[0]) :
                nbRecontres = nbRecontres + 1
                if(r[9] > 0):
                    victories = victories + 1
                
                
            if(r[3] == p[0]) :
                nbRecontres = nbRecontres + 1
                if(r[10] > 0):
                    victories = victories + 1

        ratio = 0
        if(nbRecontres > 0 ) : 
            ratio = victories / nbRecontres

        res = {"id": p[0], "prenom": p[1], "nom": p[2], "score": ratio}
        results.append(res)

    sorted_results = sorted(results, key=lambda x: x["score"], reverse=True)

    return sorted_results