import matplotlib.pyplot as plt
import numpy as np

class ScoreboardSeason:
    def __init__(self, db):
        self.db = db
        self.collection = "races"
        self.season = ""
        
    def getSeason(self):
        while(self.season == ""):
            self.season = input("Insert the year of the season: ")
            
            if(self.season == ""):
                print("Please, check your input and try again!")
            else:
                self.season = int(self.season)
        
    def plotData(self, year, constructors):
        plt.title(f"Global scoreboard - season {year}")
        legend = []
        
        for elem in constructors:
            y = np.array(constructors[elem])
            plt.plot(y)
            legend.append(elem)

        plt.legend(legend)
        
    def query(self):
        self.getSeason()
        print("Computing the result, please wait...", end="")
        
        # db.races.aggregate([{$match: {year: 2012}}, {$lookup: {from: "constructor_standings", localField: "raceId", foreignField: "raceId", as: "constructor_standings" }}, {$unwind: "$constructor_standings"}, {$lookup: {from: "constructors", foreignField: "constructorId", localField: "constructor_standings.constructorId", as: "constructor_info"}}, {$project: {_id: 0, round: 1, name: 1, "constructor_name": "$constructor_info.name", "constructor_points": "$constructor_standings.points"}}, {$group: {_id: "$round", standings: {$push: {name: "$constructor_name", points: "$constructor_points"}}}}, {$sort: {_id: 1}}])

        
        pipeline = [
                    { "$match": {
                        "year": self.season
                        }
                    },
                    {"$lookup": {
                        "from": "constructor_standings",
                        "localField": "raceId",
                        "foreignField": "raceId",
                        "as": "constructor_standings"
                        }
                    },
                    { "$unwind": "$constructor_standings"},
                    { "$lookup":{
                        "from": "constructors",
                        "localField": "constructor_standings.constructorId",
                        "foreignField": "constructorId",
                        "as": "constructor_info"    
                        }
                    },
                    { "$project": {
                        "_id": 0,
                         "round": 1,
                         "name": 1,
                         "constructor_name": "$constructor_info.name",
                         "constructor_points": "$constructor_standings.points"
                        }
                    },
                    { "$group": {
                        "_id": "$round",
                        "standings": {
                            "$push": {
                                "name": {"$first": "$constructor_name"},
                                "points": "$constructor_points"
                                }
                            }
                        }
                    }, 
                    {"$sort": {"_id": 1}}
                    ]
        
        result = self.db[self.collection].aggregate(pipeline)
        constructors = {}
                
        for elem in result:

            if(len(constructors) == 0):
                for tuple in elem["standings"]:
                    constructors[tuple["name"]] =  []
                    
            for res in elem["standings"]:
                if(res["name"] not in constructors):
                    constructors[res["name"]] = [res["points"]]
                else:
                    constructors[res["name"]].append(res["points"])

        self.plotData(self.season, constructors)
        self.season = ""
        
        print("done!\n")