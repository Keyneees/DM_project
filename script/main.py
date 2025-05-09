# imports
import pymongo as mongo
import getpass

from season_points import SeasonPoints
from champion_victory import ChampionVictoriesQuery
from scoreboard_season import ScoreboardSeason
from pit_stops import PitStopsQuery
from pilots_point import PilotPoints

# global
SRV_CONNECTION = "mongodb+srv://"
CLUSTER_HOST ="cluster0.mqgq6xr.mongodb.net/"
DB = "f1"

# main
if __name__ == "__main__":
	print("     _______    ____                      ____")
	print("    /  ____/ __/   /                     /_/_/\____")
	print("   / /___   /__   /     __     __       /_/_/_/_/_/")
	print("  /  ____/    /  /     /  \   /  \     /_/_/_/_/_/")
	print(" /  /      __/  /__   /   /  /--<     /     \_/_/")
	print("/__/      /_______/  /___/  /___/    /\n")
	print("==================================================")
	print("|| Welcome to 'Data Management project:F1 Data' ||")
	print("==================================================\n")
	print("Please enter username and password to connect to the database")
	connected=False

	while not connected:
		username=input("Username: ")
		password=getpass.getpass("Password: ")
		try:
			client=mongo.MongoClient(SRV_CONNECTION+username+":"+password+"@"+CLUSTER_HOST)
			print("Connection successful")
			connected=True
		except:
			print("Connection failed, please try again")
   
	try:
		db_list = client.list_database_names()
	except Exception as e:
		print("Error during connection, gracefully terminating...")
		exit(1)
  
	if(DB in db_list):
		print(f"{DB} available")
	else:
		print(f"{DB} not available")
		client.close()
		exit(1)

	db=client[DB]

	exit=False
	while not exit:
		passed=False
		while not passed:
      
			print("\n Insert one of the following number to choose an action:")
			print("   1 - Given a season, show how the constrcutors leaderboard changes")
			print("   2 - For all the seasons, show the number of victories of the champion of the world (either driver or constructor)")
			print("   3 - Given a constructor, show the points scored in all the seasons it partecipated")
			print("   4 - Given a season, show for each weekend the number of pit stops done and the points scored by each constrcutor")
			print("   5 - Given a pilot, show the average points scored per race per constructor for which he has run")
			print("   6 - Exit")
			print()
			
			number=input("Insert number: ")
			if number.isnumeric():
				number=int(number)
				if number>0 and number<7:
					passed=True
				else:
					print("Wrong number inserted")
			else:
				print("Wrong input")
    
		match number:
			case 1:
				print(" > Given a season, show how the constrcutors leaderboard changes")
				query_1  = ScoreboardSeason(db)
				query_1.query()
    
			case 2:
				print(" > For all the seasons, show the number of victories of the champion of the world (either driver or constructor)")
				query_2=ChampionVictoriesQuery(db)
				query_2.query()
    
			case 3:
				print(" > Given a constructor, show the points scored in all the seasons it partecipated")
				query_3 = SeasonPoints(db)
				query_3.query()
    
			case 4:
				print(" > Given a season, show for each weekend the number of pit stops done and the points scored by each constrcutor")
				query_4=PitStopsQuery(db)
				query_4.query()
			case 5:
				print(" > Given a pilot, show the average points scored per race per constructor for which he has run")
				query_5=PilotPoints(db)
				query_5.query()
			case _:
				print("Closing the connection")
				client.close()
				exit=True