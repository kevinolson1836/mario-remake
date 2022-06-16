import json
   
# Opening JSON file
f = open('leaderboards/leaderboard.json',)
   
# returns JSON object as 
# a dictionary
data = json.load(f)
f.close()   
# Iterating through the json
# list
data["first"][0]["score"] = 0
data["second"][0]["score"] = 0
data["third"][0]["score"] = 0
data["fourth"][0]["score"] = 0
data["fith"][0]["score"] = 0

data["first"][0]["name"] = "NULL"
data["second"][0]["name"] = "NULL"
data["third"][0]["name"] = "NULL"
data["fourth"][0]["name"] = "NULL"
data["fith"][0]["name"] = "NULL"

json_object = json.dumps(data, indent = 4)
print(json_object)

with open("leaderboards/leaderboard.json", "w") as outfile:
    json.dump(data, outfile)
    # Closing file
    outfile.close()
