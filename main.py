 
import pygame
from pygame.locals import *
import random
import time
import sys
from  vars import *

# todo:
    # collect mangos for extra points? 5 mangos = bonus game?
    # fix randomly floating on top of a plat
    # hit box with the bird does not work
    # add some rats to go with the voice line
    # score board persistent over time. maybe use a database
    # add leaderboard function at the end of the game 
    # add a real story line to game, some sort of toleit in a lab 

# debug stuff
debug = False
if len(sys.argv) > 1:
    if sys.argv[1] == "debug":
        debug = True
        print("debug enabled")

# start screeen with instructions 
start_loop = 1
while start_loop != "next":
    # return 1 when nothing. 0, momentum, move left, move right when in toleit hitbox
    if debug:
        start_loop = start_inst.move(debug=True)
    else:
        start_loop = start_inst.move()


# remove toleit and instruction rect from list
# number of platforms and first platform
plat_list = []
count = 0
start_plat = platforms.platform("start", screen, 0, 700, screen_size[0], plat_width)
plat_list.append(start_plat)

# intro over, clean up intro bits
pygame.mixer.Sound.stop(intro)
pygame.mixer.Sound.play(poopy_water)

# move player to starting location
location = [200,200]

inst = movement_control.update_backround_img(background1, "img/sewer.png")
# main game loop
while loop:
    # game over code 
    if gameover == True:
        if (first_time_game_over_loop):

            # sleep and play death sound
            time.sleep(1)
            first_time_game_over_loop = 0

        # play death sound here
        if (gameover_screen.loop(screen, score) == 1 ):
            pass
        else:
            # start new game
            # cancle game overloop and movement 
            gameover = False
            first_time_game_over_loop = 1
            movement_control = movement.movement(screen, left_right_speed, location, 
                player_image_width, player_image_width, player_right_sheet, 
                player_left_sheet, player_still_sheet, start_background, 
                player_image, plat_list, player_rect, clock, fps, "img/start.png", player_image_height)


            #update payer location
            location = [200, 0]
            player_rect = pygame.Rect(location[0], location[1], player_image_width, player_image_height)

            # clear plats and init starting plat again
            plat_list = []
            count = 0
            start_plat = platforms.platform("start", screen, 0, 700, screen_size[0], plat_width)
            plat_list.append(start_plat)

            # clear bird
            bird_list = []

            # clear tank and tank bullet
            tank_x = 1800
            tank_y = 100
            bullet_color = [255,0,0]
            del tank
            import tank # idk why i need this here, prob cuz the 'del tank'
            tank = tank.tank(screen, tank_image, bullet_image, tank_x, tank_y)
            prev_bullet_time = 10
            tank.init_bullet(bullet_color)
            score = 0
            
    else:
        # print debug info
        if debug == True:
            # move player to top left for debugging
            location[0] = 1
            location[1] = 1
            player_rect.x = location[0]
            player_rect.y = location[1]
            print("****************START OF DEBUG**********")
            print("current FPS: ", end='')
            print(clock.get_fps())
            print("current frame: ", end='')
            print(frame_count)

        # random chance to play a voice line
        if random.randint(rand_voice_line_start,rand_voice_line_end) == voice_line_1:
            pygame.mixer.Sound.play(check_out_the_pipes)
            rand_voice_line_end += rand_voice_line_end

        # update the score
        score_surface = myfont.render("score:  " + str(score), False, score_color)
        
        # draw player and tank images
        if direction == "right":
            screen.blit(player_right_sheet.animate(player_frame_count), location)    
        elif direction == "left":
            screen.blit(player_left_sheet.animate(player_frame_count), location)     
        else:
            screen.blit(player_still_sheet.animate(1), location)   
        if debug:
            sc= movement_control.move(debug, plat_list, player_rect, location, background1, score, return_score=True)
        else:
            sc = movement_control.move(debug, plat_list, player_rect, location, background1, score, return_score=True)
        if type(sc) is int and sc == 1:
            score += sc
        if sc == -1:
            gameover = True

        if (movement_control.current_direction() == "left"):
            player_rect.update(location[0]+40,location[1]+20,player_image_width-40, player_image_height+5)

        elif (movement_control.current_direction() == "right"):
            player_rect.update(location[0]+10,location[1]+20,player_image_width-40, player_image_height+5)

        else:
            player_rect.update(location[0]+20,location[1]+20,player_image_width-30, player_image_height+5)


        # draw player hitbox
        if debug:
            pygame.draw.rect(screen, (255,120,200),player_rect)

        # score 
        screen.blit(score_surface,(score_location))

        # tank movement for bouncing
        tank.move(tank_move_speed)

        # tank.init_bullet()
        if random.randint(rand_bullet_time_start, rand_bullet_time_end) < frame_count - prev_bullet_time:
            if fps != 0: 
                prev_bullet_time = frame_count + (fps * 2)
                tank.init_bullet(bullet_color)

        # end game if collided with bulet from tank
        if player_rect.colliderect(tank.bullet_rect):
            print("player rect: ", player_rect)
            print("bullet location: ", tank.bullet_rect)
            gameover = True
            if debug == True:
                    print(f"player collieded with BULLET:")
                    tank.print_debug()
                    print("player location: " + str(location))
                    gameover = False
        tank.move_bullet(20)

        # randomly make new bird 
        xbird = new_bird.random_timed_bird(bird_rand_location_start, bird_rand_location_end, frame_count, prev_bird_time, fps)
        if xbird != 0:
            prev_bird_time = frame_count + fps
            bird_list.append(xbird)

        # draw and move all birds
        for x in bird_list:
            x.move(bird_move_speed)
            x.draw()
            # gameover if collieded with bird
            if player_rect.colliderect(x.get_bird_location()):
                if debug == True:
                    print(f"player collieded with BIRD:")
                    x.print_debug()
                    print("player location: " + str(location))
                gameover = True

        # every random_plat_time  make new platform
        if random.randint(rand_plat_time_start, rand_plat_time_end ) < frame_count - prev_plat_time: 
            prev_plat_time = frame_count + fps
            count += 1
            plat = platforms.platform(count, screen, screen_size[0], random.randint(plat_x_rand, plat_y_rand), plat_len, plat_width)
            plat.draw()
            plat_list.append(plat)
            
        # move all platforms with for loop
        for x in range(len(plat_list)):
            plat_list[x].move(random.randint(plat_giggle_start, plat_giggle_end))
            plat_list[x].draw()
            # print(plat_list)

    if debug == True:
        # print("player momentum: " + str(momentum))
        print("****************END OF DEBUG**********",end="\n\n\n\n\n")
        # move player to top left for debugging 
        location[0] = 1
        location[1] = 1
        player_rect.x = location[0]
        player_rect.y = location[1]
    
    pygame.display.update()
    clock.tick()
    frame_count += 1
    fps = clock.get_fps()

pygame.quit()