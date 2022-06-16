# from curses import KEY_ENTER
# from tkinter.tix import Select
from vars import *

class gameover_screen():
    def __init__(self, screen, font, leaderboard, score_surface):
        # init gameover vars 
        self.screen = screen
        self.gameover_background = background.background('img/gameover_background.jpg', [0,0])
        self.font = font 
        self.debug = debug
        self.Selection = 0
        self.enter = False
        self.return_val = 1
        self.leaderboard_board = leaderboard
        self.enter_delay = True
        self. waiting = True
        self.firt_time = True
        self.score_surface = score_surface
        self.lb = self.leaderboard_board.return_leaderboard_data()

    def render_text(self):

        # surfaces with normal non selected color
        surface1 = self.font.render("RETRY", False, (54,33,5))
        surface2 = self.font.render("LEADERBOARDS", False, (54,33,5))
        surface3 = self.font.render("QUIT", False, (54,33,5))

        # surfaces with selected color
        surface1_1 = self.font.render("RETRY", False, (154,133,15))
        surface2_2 = self.font.render("LEADERBOARDS", False, (154,133,15))
        surface3_3 = self.font.render("QUIT", False, (154,133,15))

        # check for keys being pressed
        for event in pygame.event.get():
            if event.type == KEYDOWN:

                # quit game
                if event.key == K_ESCAPE:
                    exit()

                # UP pressed
                if event.key == K_UP or event.key == K_w:
                    self.up = True
                    self.Selection = self.Selection - 1
                
                # DOWN pressed
                if event.key == K_DOWN or event.key == K_s:
                    self.down = True
                    self.Selection = self.Selection + 1
                
                # ENTER pressed
                if event.key == K_RETURN and self.enter_delay == True:
                    self.enter = True
                    self.enter_delay = False
            
            # keys stopped being pressed
            if event.type == KEYUP:
                
                # UP unpressed
                if event.key == K_UP or event.key == K_w:
                    self.up = False
                
                # DOWN unpressed
                if event.key == K_DOWN or event.key == K_s:
                    self.down = False
                
                # ENTER unpressed
                if event.key == K_RETURN:
                    self.enter = False
                    self.enter_delay = True
                   
        # retry selected
        if (self.Selection % 3 == 0):
            self.screen.blit(surface1_1, [760,320])
            self.screen.blit(surface2, [500,460])
            self.screen.blit(surface3, [800,600])
            print("dedededededededededededededed")
            print(self.score)
            self.firt_time = True
            if (self.enter == True):
                # retry 
                print("[qekro bqe=rokb ")
                self.return_val = 0
                self.enter = False
                self.first_time = True

        # leaderboards selected
        elif (self.Selection % 3 == 1):
            if (self.enter == False):
                self.screen.blit(surface1, [760,320])
                self.screen.blit(surface2_2, [500,460])
                self.screen.blit(surface3, [800,600])
            elif (self.enter == True):
                self.waiting = True
                self.screen.blit(self.gameover_background.image, self.gameover_background.rect)

                score_surface = self.font.render("score:  " + str(self.score), False, [255,255,0])
                self.screen.blit(score_surface, (600,0))
                # leaderboards
                # print(self.leaderboard_board.print_data())
                # print(self.leaderboard_board.print_data())
                # self.leaderboard_board.read_leaderbard()
                
                # print(self.leaderboard_board.print_data())
                if (self.firt_time == True):
                    self.leaderboard_board.read_leaderbard()
                    name = self.get_player_name()
                    self.leaderboard_board.update_leaderboard( [self.score, name] )
                    self.leaderboard_board.write_new_score()
                    self.firt_time = False
                    self.lb = self.leaderboard_board.return_leaderboard_data()

                offset = 0
                for key, value in self.lb.items():  
                    surface_string = (f"{key}: ".ljust(9) + f"{value[0].get('score')} " + f" {value[0].get('name')}")
                    leaderboard_surface = self.font.render(surface_string, False, (54,33,5))
                    self.screen.blit(leaderboard_surface, [500,400 + offset])
                    offset = offset + 100
                pygame.display.update()
                # time.sleep(0.5)   
                while(self.waiting == True):    
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                exit()
                            if event.key == K_RETURN or event.key == K_SPACE:
                                self.enter = False
                                self.waiting = False
                                # self.Selection = self.Selection - 1
                                # break
                self.screen.blit(surface1_1, [760,320])
                self.screen.blit(surface2, [500,460])
                self.screen.blit(surface3, [800,600])
                pygame.display.update()
        
        # quit selected
        elif (self.Selection % 3 == 2):
            self.screen.blit(surface1, [760,320])
            self.screen.blit(surface2, [500,460])
            self.screen.blit(surface3_3, [800,600])
            if (self.enter == True):
                # quit
                exit()

    # main loop, return 0 when want to run main loop again
    def loop(self, screen, score):
        self.score = score
        screen.blit(self.gameover_background.image, self.gameover_background.rect)
        self.render_text()
        score_surface = self.font.render("score:  " + str(score), False, [255,255,0])
        self.screen.blit(score_surface, (600,0))
        if (self.return_val == 0):
            self.return_val = 1
            return(0)
        else:
            return(1)

    def get_player_name(self):
        return("kevin")