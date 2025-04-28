import pymongo as mongo
import matplotlib.pyplot as plt

class SeasonPoints:
    
    #     db.races.aggregate([{$lookup: {from: "constructor_standings", localField: "raceId", foreignField: "raceId", as: "constructor_standings"}}, {$unwind: "$constructor_standings"}, {$lookup: {from: "constructors", foreignField: "constructorId", localField: "constructor_standings.constructorId", as: "constructor_info"}}, {$match: {"constructor_info.name": "Ferrari"}}, {$project: {_id: 0, raceId: 1, year: 1, name: 1, round: 1, "constructor_standings.points": 1, "constructor_info.name": 1, "constructor_info.constructorId": 1}}, {$group: {_id: {year: "$year", name: "$constructor_info.name"}, "standings": {$push: {round: "$round", points: "$constructor_standings.points"}}}}, {$project: {_id: 0, year: "$_id.year", points: {$max: "$standings.points"}}}, {$sort: {year: 1}}])

    
    def __init__(self, client):
        self.client = client
        self.collection = "races"
        
    def query(constructor):
        if(constructor == ""):
            return None
        else:
            pass