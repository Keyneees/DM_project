import matplotlib.pyplot as plt
import numpy as np

class PilotPoints:
    def __init__(self, db):
        self.db=db
        self.collection=self.db["drivers"]
        
    def plotting(self, results, pilot):
        constructors=[]
        avgPoints=[]
        
        for result in results:
            constructors.append(result["constructor"])
            avgPoints.append(result["avgPoints"])
            
        plt.title(f"Average points of {pilot} per constructors")
        xaxis=np.array(constructors)
        yaxis=np.array(avgPoints)
        plt.bar(xaxis, yaxis)
        plt.show()
        
    def query(self):
        chosen=False
        while not chosen:
            print("Choose a pilot")
            name=input("Name: ")
            surname=input("Surname: ")
            
            driver=self.collection.find({"forename":name, "surname":surname})
            if driver=="":
                print(f"Pilot {name} {surname} is not present. Please try again")
            else:
                chosen=True
        
        pipeline=[{"$match": 
                    {"forename": name, 
                     "surname": surname}}, 
                  {"$lookup": { 
                        "from": "results", 
                        "localField": "driverId", 
                        "foreignField": "driverId", 
                        "as": "results" } }, 
                  {"$unwind": "$results" }, 
                  {"$project": { 
                        "_id": 0, 
                        "driverId": 1, 
                        "forename": 1, 
                        "surname": 1, 
                        "constructorId": "$results.constructorId", 
                        "points": { "$toDouble": "$results.points" } } 
                   }, 
                  { "$group": { 
                      "_id": { "driverId": "$driverId", "constructorId": "$constructorId" }, 
                      "name": { "$first": "$forename" }, 
                      "surname": { "$first": "$surname" }, 
                      "avgPoints": { "$avg": "$points" } } 
                   }, 
                  { "$lookup": { 
                      "from": "constructors", 
                      "let": { "cid": "$_id.constructorId" }, 
                      "pipeline": [ 
                          {"$match": { "$expr": { "$eq": ["$constructorId", "$$cid"] } } },
                          {"$project": { "_id": 0, "name": 1 } } 
                         ], 
                      "as": "constructor" } 
                   }, 
                  {"$project": { 
                      "name": 1, 
                      "surname": 1, 
                      "constructor": {"$arrayElemAt": ["$constructor.name", 0] }, 
                      "avgPoints": 1 } 
                   }
                  ]
        results=self.collection.aggregate(pipeline)
        pilot=name + " " + surname
        self.plotting(results, pilot)