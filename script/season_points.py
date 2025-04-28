import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np

class SeasonPoints:
    
    def __init__(self, client):
        self.client = client
        self.collection = "races"
        self.constructor = ""
        
    def getConstructor(self):
        constructor = ""
        
        while(constructor == ""):
            constructor = input("Insert the constructor: ")
            if(constructor == ""):
                print("Unavalilable constructor, please check your input and try again!")
            
        self.constructor = constructor
        return True
        
    def plotData(self, years, points, constructor_name):
        x = np.array(years)
        y = np.array(points)
        plt.bar(x, y)
        plt.title(f"{constructor_name} points during seasons")
        plt.show()
        
    def query(self):
        self.getConstructor()
        print("Computing the result, please wait...\n", end="")
        
        pipeline = [
                    { "$lookup": {
                        "from": "constructor_standings",
                        "localField": "raceId",
                        "foreignField": "raceId",
                        "as": "constructor_standings",
                        }
                    },
                    { "$unwind": "$constructor_standings"
                    },
                    { "$lookup": {
                            "from": "constructors",
                            "foreignField": "constructorId",
                            "localField": "constructor_standings.constructorId",
                            "as": "constructor_info"
                        }
                    },
                    { "$match": {
                        "constructor_info.name": f"{self.constructor}"
                        }
                    },
                    { "$project": {
                        "_id": 0,
                        "raceId": 1,
                        "year": 1,
                        "round": 1,
                        "constructor_standings.points": 1,
                        "constructor_info.name": 1,
                        "constructor_info.constructorId": 1
                        }
                    },
                    { "$group": {
                        "_id": {
                            "year": "$year",
                            "name" : "$constructor_info.name"
                        },
                        "standings": {
                            "$push": {
                                "round": "$round",
                                "points": "$constructor_standings.points"
                            }
                        }
                        }                    
                    },
                    { "$project": {
                        "_id": 0,
                        "year": "$_id.year",
                        "points": {
                            "$max": "$standings.points"
                            }
                        }
                    }, 
                    
                    {"$sort": {"year": 1}}
                    ]
        
        result = self.client[self.collection].aggregate(pipeline)
        years = []
        points = []
        
        for elem in result:
            years.append(elem["year"])
            points.append(elem["points"])

        self.plotData(years, points, self.constructor)
        self.constructor = ""

        print("done!\n")
        