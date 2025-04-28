# imports
import pymongo as mongo
import matplotlib.pyplot as plt

# global
SRV_CONNECTION = "mongodb+srv://"
CLUSTER_HOST ="cluster0.mqgq6xr.mongodb.net/"
DB = "f1"

# main
if __name__ == "__main__":
	print("Welcome to 'Data Management project:F1 Data'")
	print("Please enter username and password to connect to the database")
	connected=False

	while not connected:
		username=input("username: ")
		password=input("Password: ")
		try:
			client=mongo.MongoClient(SRV_CONNECTION+username+":"+password+"@"+CLUSTER_HOST)
			print("Connection successful")
			connected=True
		except:
			print("Connection failed, please try again")
		
	db_list=client.list_database_names()
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
			print("Insert one of the following number to choose an action:")
			print("1 - Given a season, show how the constrcutors leaderboard changes")
			print("2 - For all the seasons, show the number of victories of the champion of the world (either driver or constructor)")
			print("3 - Given a constructor, show the points scored in all the seasons it partecipated")
			print("4 - Given a season, show for each weekend the number of pit stops done and the points scored by each constrcutor")
			print("5 - Exit")
			
			number=input("Insert number:")
			if number.isnumeric():
				number=int(number)
				if number>0 and number<6:
					passed=True
				else:
					print("Wrong number inserted")
			else:
				print("Wrong input")
    
		match number:
			case 1:
				print("Given a season, show how the constrcutors leaderboard changes")
			case 2:
				print("For all the seasons, show the number of victories of the champion of the world (either driver or constructor)")
			case 3:
				print("Given a constructor, show the points scored in all the seasons it partecipated")
			case 4:
				print("Given a season, show for each weekend the number of pit stops done and the points scored by each constrcutor")
			case _:
				print("Closing the connection")
				client.close()
				exit=True