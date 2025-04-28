import matplotlib.pyplot as plot
import numpy as np

plot.ion()

class ChampionVictoriesQuery:
    def __init__(self, db):
        self.db=db
    
    def plotter(self, results):
        seasons=[]
        points=[]
        for result in results:
            seasons.append(result["year"])
            points.append(int(result["wins"]))
            
        xaxis=np.array(seasons)
        yaxis=np.array(points)
        plot.bar(xaxis, yaxis)
        plot.show()
        
    def query(self):
        chosen=False
        while not chosen:
            print("Choose the champion of the world:")
            print("1 - Driver")
            print("2 - Construtor")
            number=input("Number selected: ")
            if number.isnumeric():
                number=int(number)
                if number == 1 or number == 2:
                    chosen=True
                else:
                    print("Wrong number selected")
            else:
                print("Wrong input")
        
        if number==1:
            CHAMPION_COLLECTION="driver_standings"
        else:
            CHAMPION_COLLECTION="constructor_standings"
            
        collection=self.db["races"]
        
        pipeline=[{"$group":{
                    "_id":"$year",
                    "lastRound":{"$max":"$round"}
                    }
                   },
                  {"$lookup":{
                      "from":"races",
                      "let":{"year":"$_id",
                             "round":"$lastRound"},
                      "pipeline":[{"$match":{"$expr":{"$and":[{"$eq":["$year","$$year"]},{"$eq":["$round","$$round"]}]}}},
                                  {"$project":{"raceId":1,"year":1}}
                                 ],
                      "as":"lastRace"}
                   },
                  {"$unwind":"$lastRace"},
                  {"$lookup":{
                      "from":CHAMPION_COLLECTION,
                      "localField":"lastRace.raceId",
                      "foreignField":"raceId",
                      "as":"standing"}
                   },
                  {"$unwind":"$standing"},
                  {"$match":{"standing.position":1}},
                  {"$lookup":{
                      "from":"drivers",
                      "localField":"standing.driverId",
                      "foreignField":"driverId",
                      "as":"driver"}
                   },
                  {"$unwind":"$driver"},
                  {"$project":{
                      "_id":0,
                      "year":"$_id",
                      "driverId":"$standing.driverId",
                      "wins":"$standing.wins",
                      "name":"$driver.forename",
                      "surname":"$driver.surname"}
                   },
                  {"$sort":{"year":1}}
                 ]
        
        results=collection.aggregate(pipeline)
        self.plotter(results)