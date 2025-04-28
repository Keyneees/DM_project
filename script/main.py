# imports
import pymongo as mongo
import matplotlib.pyplot as plt

# global
ADDR = "mongodb://127.0.0.1:27017/"
DB = "f1"
COLLECTION = "constructors"
QUERY = {}
PIPELINE = []

# db call
client = mongo.MongoClient(ADDR)
db = client[DB]

# main
if __name__ == "__main__":
	db_list = client.list_database_names()
 
	if(DB in db_list):
		print(f"{DB} in list")

	collection = db[COLLECTION]
 
	PIPELINE = [{"$lookup": {
					"from": "constructor_standings",
					"foreignField": "constructorId",
					"localField": "constructorId",
					"as": "standings"
				}}, 
				{"$lookup": {
                  	"from": "races",
                  	"foreignField": "raceId",
					"localField": "standings.raceId",
					"as": "standings.race_info"
				}},
				{"$match": {
					"standings.race_info.year": 2020
				}}, 
    			{"$project":{
					"_id": 0,
					"name": 1,
					"nationality": 1,
					"standings.points": 1,
					"standings.position": 1,
					"standings.race_info.name": 1,
					"standings.race_info.round": 1
				}}]

	res = collection.aggregate(PIPELINE)

	for elem in res:
		print(f"{elem}\n")
