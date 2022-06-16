import json

class Leaderboard ():

    # init some vars 
    def __init__(self, leaderboard_file):
        self.leaderboard_file = leaderboard_file 
        self.top_5 = [ [0 , "NULL"], [0 , "NULL"], [0 , "NULL"], [0 , "NULL"], [0 , "NULL"] ] 
        
    # update leader board
    def update_leaderboard (self, score):
        # change score into a dict. too lazy to update score globaly
        score = {
            "score": int(score[0]),
            "name": score[1]
        }

        # update score to first palce
        if (score.get("score") > int(self.top_5["first"][0]["score"])):
            self.top_5["fith"][0] = self.top_5["fourth"][0]
            self.top_5["fourth"][0] = self.top_5["third"][0]
            self.top_5["third"][0] = self.top_5["second"][0]
            self.top_5["second"][0] = self.top_5["first"][0]
            self.top_5["first"][0] = score
            return()

        # update score to second palce
        elif (score.get("score") > int(self.top_5["second"][0]["score"])):
            self.top_5["fith"][0] = self.top_5["fourth"][0]
            self.top_5["fourth"][0] = self.top_5["third"][0]
            self.top_5["third"][0] = self.top_5["second"][0]
            self.top_5["second"][0] = score
            return()


        # update score to third palce
        elif (score.get("score") > int(self.top_5["third"][0]["score"])):
            self.top_5["fith"][0] = self.top_5["fourth"][0]
            self.top_5["fourth"][0] = self.top_5["third"][0]
            self.top_5["third"][0] = score
            return()

        # update score to forth palce
        elif (score.get("score") > int(self.top_5["fourth"][0]["score"])):
            self.top_5["fith"][0] = self.top_5["fourth"][0] 
            self.top_5["fourth"][0] = score
            return()

        # update score to fith palce
        elif (score.get("score") > int(self.top_5["fith"][0]["score"])):
            self.top_5["fith"][0] = score
            return()

    # read the 5 lines in leader board file
    def read_leaderbard (self):
        f = open('leaderboards/leaderboard.json',)
        self.top_5 = json.load(f)
        f.close()

    # writes new score data to leaderboards
    def write_new_score(self):
        with open("leaderboards/leaderboard.json", "w") as outfile:
            json.dump(self.top_5, outfile)
        outfile.close()

    # print scoreboard data
    def print_data(self):
        # Serializing json 
        json_object = json.dumps(self.top_5, indent = 4)
        print(json_object)

    def return_leaderboard_data(self):
        return(self.top_5)