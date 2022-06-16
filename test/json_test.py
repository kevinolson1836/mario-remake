import json
   
# Opening JSON file
f = open('leaderboard.json',)
   
# returns JSON object as 
# a dictionary
data = json.load(f)
   
# Iterating through the json
# list
print(data["first"])
print(data["second"])
print(data["third"])
print(data["fourth"])
print(data["fith"])
print()
data["first"][0]["score"] = 1
print(data["first"][0]["score"])
# data["first"]["name"] = "test"

# for i in data:
#     print(i)
   

with open("json_write.json", "w") as outfile:
    json.dump(data, outfile)
# Closing file
f.close()