import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np

class PitStopsQuery:
    def __init__(self, db):
        self.db=db
        
    def plotting(self,results):
        pitStops=[]
        pointsScored=[]
        rounds=[]
        constructors=[]
        
        for result in results:
            round=result["gp"]
            if round not in rounds:
                rounds.append(round)
            
            constructor=result["constructor"]
            if constructor not in constructors:
                constructors.append(constructor)
            
            pitStops.append(result["totalPitStop"])
            pointsScored.append(result["totalPoints"])
        
        i = 0
        size = len(constructors)

        for round in rounds:
            # Crea figura e assi principali
            fig, ax1 = plt.subplots(figsize=(10, 6))
            ax2 = ax1.twinx()

            # Asse X (nomi team)
            xaxis = np.arange(len(constructors))  # posizioni per le barre

            # Dati Y
            yaxis1 = np.array(pointsScored[i * size: (i + 1) * size])
            yaxis2 = np.array(pitStops[i * size: (i + 1) * size])

            # Barre affiancate
            width = 0.4
            ax1.bar(xaxis - width/2, yaxis1, width, color='blue', alpha=0.6, label='Points')
            ax2.bar(xaxis + width/2, yaxis2, width, color='red', alpha=0.6, label='Pit Stops')

            # Etichette e titoli
            ax1.set_title(f"Round: {round}")
            ax1.set_xlabel("Constructors")
            ax1.set_ylabel("Points", color='blue')
            ax2.set_ylabel("Number of Pit Stops", color='red')

            ax1.set_xticks(xaxis)
            ax1.set_xticklabels(constructors, rotation=45)

            ax1.tick_params(axis='y', colors='blue')
            ax2.tick_params(axis='y', colors='red')

            plt.tight_layout()
            plt.show()
            i += 1
    
    def query(self):
        chosen=False
        while not chosen:
            print("Choose a season from 1950 to 2024")
            season=input("Insert the season: ")
            if season.isnumeric():
                season=int(season)
                if season>1949 and season<2025:
                    chosen=True
                else:
                    print("Wrong season selected")
            else:
                print("Wrong input inserted")
            
            collection=self.db["results"]
            
            pipeline=[{"$lookup":{
                            "from":"races", 
                            "foreignField":"raceId", 
                            "localField":"raceId", 
                            "as":"season"}
                       },
                      {"$unwind":"$season"},
                      {"$match":{"season.year":season}},
                      {"$lookup":{
                          "from":"pit_stops",
                          "let":{
                              "driver":"$driverId",
                              "race":"$raceId"},
                          "pipeline":[{"$match":{"$expr":{"$and":[{"$eq":["$$driver","$driverId"]},{"$eq":["$$race","$raceId"]}]}}},
                                      {"$count":"num_pitstops"}],
                          "as":"pit_stop"}
                       },
                      {"$lookup":{
                          "from":"constructors", 
                          "foreignField":"constructorId", 
                          "localField":"constructorId", 
                          "as":"constructorInfo"}
                       },
                      {"$project":{
                          "_id":0,
                          "constructorName":"$constructorInfo.name",
                          "round":"$season.round",
                          "gp":"$season.name",
                          "pitStops":{"$cond":{"if":{"$gt":[{"$size":"$pit_stop"},0]},
                                               "then":{"$arrayElemAt":["$pit_stop.num_pitstops",0]},
                                               "else":0}}, 
                          "points":1}
                       },
                      {"$group":{
                          "_id":{"constructor":"$constructorName","round":"$round"},
                          "totalPitStop":{"$sum":"$pitStops"}, 
                          "totalPoints":{"$sum":"$points"}, 
                          "gp":{"$first":"$gp"}}
                       },
                      {"$project":{
                          "_id":0,
                          "constructor":{"$first":"$_id.constructor"},
                          "round":"$_id.round",
                          "totalPitStop":1, 
                          "totalPoints":1,
                          "gp":1}
                       },
                      {"$sort":{
                          "round":1,
                          "constructor":1
                      }}
                     ]
            
            results=collection.aggregate(pipeline)
            self.plotting(results)