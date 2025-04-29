import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

class PitStopsQuery:
    def __init__(self, db):
        self.db=db
        
    def plotting(self,results):
        pitStops=[]
        pointsScored=[]
        rounds=[]
        constructors=[]
        
        for result in results:
            round=result["round"]
            if round not in rounds:
                rounds.append(round)
            
            constructor=result["constructor"]
            if constructor not in constructors:
                constructors.append(constructor)
            
            pitStops.append(result["totalPitStop"])
            pointsScored.append(result["totalPoints"])
    
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
                      {"$project":{
                          "_id":0,
                          "constructorId":1,
                          "round":"$season.round",
                          "pitStops":{"$cond":{"if":{"$gt":[{"$size":"$pit_stop"},0]},
                                               "then":{"$arrayElemAt":["$pit_stop.num_pitstops",0]},
                                               "else":0}}, 
                          "points":1}
                       },
                      {"$group":{
                          "_id":{"constructor":"$constructorId","round":"$round"},
                          "totalPitStop":{"$sum":"$pitStops"}, 
                          "totalPoints":{"$sum":"$points"}}
                       },
                      {"$project":{
                          "_id":0,
                          "constructor":"$_id.constructor",
                          "round":"$_id.round",
                          "totalPitStop":1, 
                          "totalPoints":1}
                       },
                      {"$sort":{
                          "round":1,
                          "constructor":1
                      }}
                      ]
            
            results=collection.aggregate(pipeline)
            self.plotting(results)