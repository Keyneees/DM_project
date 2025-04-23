# imports
import pymongo as mongo
import matplotlib.pyplot as plt

# global
ADDR = "mongodb://127.0.0.1:27017/"
DB = "f1"
COLLECTION = "Ferrari_standings_2018_differences"
QUERY = {}

# db call
client = mongo.MongoClient(ADDR)
db = client[DB]

# main
if __name__ == "__main__":
	db_list = client.list_database_names()
	
	if(DB in db_list):
		print(f"'{DB}' in list of database names")
	
	doc = db[COLLECTION]
	stats = []
 
	for elem in doc.find():
		stats.append({"round": elem["round"], "difference": elem["points_difference"]})		
  		  
	stats.sort(key=lambda x: x["round"])
	print(stats)
 
	rounds = [elem["round"] for elem in stats]
	points = [elem["difference"] for elem in stats]
 
	plt.plot(rounds, points, color="red")
	plt.title("Ferrari 2018 drivers standings differences")
	plt.show()
