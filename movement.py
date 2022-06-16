# things to add
    # left right jump, collition, animation

import pygame
import platforms
import sprite_sheet_class as ss
import background
from pygame.locals import *
import time

class movement():
    def __init__(self, screen, left_right_speed, location, player_image_width, player_image_height,
                player_right_sheet, player_left_sheet, player_still_sheet, background_image,
                player_image, plat_list, player_rect, clock, fps, bg_img_file, player_height):
        self.screen = screen
        self.bg_img_file = bg_img_file
        self.left_right_speed = left_right_speed
        self.momentum = 0
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.jump_number = 0
        self.can_jump = True
        self.location = location
        self.plat_list = plat_list
        self.start_plat = platforms.platform("start", self.screen, 0, 800, 2000, 0)
        self.player_frame_count = 0
        self.player_max_frame_count = 3 
        self.player_image_width = player_image_width
        self.player_image_height = player_image_height
        self.frame_delay = 3
        self.frame_count = 0
        self.prev_time = 0
        self.player_right_sheet = player_right_sheet
        self.player_left_sheet = player_left_sheet
        self.player_still_sheet = player_still_sheet
        self.direction = ""
        self.player_rect = player_rect
        self.player_rect.x = self.location[0]
        self.player_rect.y = self.location[1]
        self.background_image = background_image    # background image
        self.background_rect = background.background(self.bg_img_file, [0,0]) # background rect
        self.player_image = player_image            # player image
        self.clock = clock  
        self.fps = fps
        self.player_image_height = player_image_height

    def move(self, debug=False, plat_list=None, player_rect=None, location=None, background_rect=None, score=None, return_score=False):
        # sets player pos

        self.score = 0
        if plat_list != None:
            self.plat_list = plat_list
        if player_rect != None:
            self.player_rect = player_rect
        if location != None:
            self.location = location
        if background_rect != None:
            self.background_rect = background_rect
        # if score != None:
        #     self.score = score
        
        self.player_rect.x = self.location[0]
        self.player_rect.y = self.location[1]
        if debug:
            print("********start movement debug********")
            print("\tplayer starting lcoation AND starting rect [x,y]: ", self.location)

        # blit backgrounf img
        self.screen.blit(self.background_rect.image, self.background_rect.rect)
        
        # set player animation
        if self.direction == "right":
            self.screen.blit(self.player_right_sheet.animate(self.player_frame_count), self.location)    
        elif self.direction == "left":
            self.screen.blit(self.player_left_sheet.animate(self.player_frame_count), self.location)     
        else:
            self.screen.blit(self.player_still_sheet.animate(1), self.location) 
        if debug:
            print("\tcurrent direction: ", self.direction)
        
        # check if player colided with a platform
        for x in range(len(self.plat_list)):
            if self.player_rect.colliderect(self.plat_list[x].rect):
                # debug info
                self.score = self.plat_list[x].score()
                if debug:
                    print(f"\tplayer collided with {self.plat_list[x].get_name()}, debug info: ")
                    print('\t' + str(self.plat_list[x].print_debug()))
                self.momentum = 0
                # self.score = self.plat_list[x].score()
                if self.location[1] >  self.plat_list[x].ypos - self.player_image_height-100:
                    # print("dedede;v;lS", self.location)
                    self.location[1] = self.plat_list[x].ypos - self.player_image_height-127 
                    floatting = True
                    self.momentum = 0
                    self.can_jump = True
                else:
                    floaing = False
                self.can_jump = True
                if self.plat_list[x].name == "toliet":
                    if debug:
                        print("\tplayer hit toliet rect, exiting start loop.")
                    return ("next")
            else:
                if x == 0:
                    # if player bottom of screen end game
                    if self.player_rect.y > 1000 + self.player_image_height - 110:
                        gameover = True
                        if debug:
                            print("\tplayer fell off map, ending game.")
                        return(-1)
                    # else make player fall
                    else:
                        self.momentum += 1    
             
        self.location[1] += self.momentum   
        if debug:
            print("\tplayer y location updated, new value: ", self.location[1])

        # move player right
        if self.moving_right == True:
            self.location[0] += self.left_right_speed
            if debug:
                print("\tplayer moving right")

        # move player left 
        if self.moving_left == True:
            self.location[0] -= self.left_right_speed
            if debug:   
                print("\tplayer moving left")
            
        # jumping locgic
        if self.jumping == True:
            if self.jump_number < 0:
                self.jumping = False
                self.can_jump = False
            else: 
                self.can_jump = False
                self.jump_number -= 1
            if self.can_jump:
                self.jump_number = self.jump_count
            self.location[1] -= 100
            self.momentum = -15
            if debug:
                print("\tplayer jumped")

        # key management  
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # quit game
                if event.key == K_ESCAPE:
                    if debug:
                        print("\tplayer quit game with ESC key")
                    exit()
                # move right
                if event.key == K_RIGHT or event.key == K_d:
                    self.moving_right = True
                # move left
                if event.key == K_LEFT or event.key == K_a:
                    self.moving_left = True
                # jump
                if event.key == K_SPACE or event.key == K_UP or event.key == K_w:
                    if self.can_jump:
                        self.can_jump = False
                        self.jumping = True           

            # keys stopped being pressed
            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    self.moving_right = False
                if event.key == K_LEFT or event.key == K_a:
                    self.moving_left = False
                if event.key == K_SPACE:
                    self.jumping = False

        if self.moving_right == True:
            self.direction = "right"
            if self.frame_delay < self.frame_count - self.prev_time:
                self.prev_time = self.frame_count 
                self.player_frame_count +=1
            # self.player_frame_count += 1
            if self.player_frame_count >= self.player_max_frame_count:
                self.player_frame_count = 0

        elif self.moving_left == True:
            self.direction = "left"
            if self.frame_delay < self.frame_count - self.prev_time:
                self.prev_time = self.frame_count 
                self.player_frame_count +=1
            # self.player_frame_count += 1
            if self.player_frame_count >= self.player_max_frame_count:
                self.player_frame_count = 0
        else:
            self.direction = ""
            self.player_frame_count = 0
        if debug:
            print("\tcurrent animation frame: ", self.player_frame_count)

        # pygame.display.update()
        self.clock.tick()
        self.frame_count += 1
        self.fps = self.clock.get_fps()
        self.player_rect.x = self.location[0]
        self.player_rect.y = self.location[1]
        if debug:
            print("\tupdated clock, frame count, fps and player location. ending vars are: ")
            print("\t\t frame count: ", self.frame_count)
            print("\t\tfps: ", self.fps)
            print("\t\tplayer location AND player_rect [x,y]: ", self.location)
            print("********end movement debug********", end='\n\n\n\n\n')
        return(self.score)

    def update_backround_img(self, img, file_location):
        self.background_image = img    # background image
        self.background_rect = background.background(file_location, [0,0]) # background rect
    
    def current_direction(self):
        if (self.moving_right == True):
            return("right")
        elif (self.moving_left == True):
            return("left")
        else:
            return