import pygame
from sys import exit
import random
from math import sin, pi
import webbrowser
from classes import Button, Background, Obstacle, Player
               
def display_score():
    if game_active:
        current_time = int(pygame.time.get_ticks() / 1000) * 2 - start_time
        score_surface = small_font_20.render(f"Score: {current_time}", False, (64, 64, 64))
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH / 2,25))
        screen.blit(score_surface, score_rect)
        
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True
        
MAX_FRAMERATE = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
game_active = False
iscredit_menu_showed = False
start_time = 0
score = 0

pygame.init() #Initialize PyGame (A must)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #Set Window Resolution
pygame.display.set_caption("Runner") #Set Window Title
clock = pygame.time.Clock() #Create a call object

bg = pygame.image.load("graphics\Sky_Blue.jpg").convert()
bg = pygame.transform.scale(bg, (WINDOW_WIDTH,WINDOW_HEIGHT - 60))
background = Background(screen, WINDOW_WIDTH, WINDOW_HEIGHT)

ground = pygame.image.load("graphics\Ground.jpg").convert()
ground = pygame.transform.scale(ground, (800, 60))

small_font_20 = pygame.font.Font("font\Pixeled.ttf", 20)
small_font_14 = pygame.font.Font("font\Pixeled.ttf", 14)
big_font_30 = pygame.font.Font("font\Pixeled.ttf", 30)

#Title screen Text
titlescreen_textsurface = big_font_30.render("Runner Game", False, "Black")
titlescreen_text_rect = titlescreen_textsurface.get_rect(center=(WINDOW_WIDTH / 2, 50))

#Credit Text
credit_text_title = big_font_30.render("Credit", False, "Black")
credit_text = small_font_14.render("Made by Steward Melvin Tang with love", False, "Black")
credit_text2 = small_font_14.render("Uses PyGame library, Trevor Lentz's Music,", False, "Black")
credit_text3 = small_font_14.render("and  Clear Code's Youtube Video", False, "Black")

#Background Music
BGM = pygame.mixer.Sound("audio\Lines of Code.mp3").play(loops=-1)
BGM.set_volume(0.35)

pressed_sound = pygame.mixer.Sound(r"audio\button_press.wav")
pressed_sound.set_volume(0.25)
clicked_sound = pygame.mixer.Sound(r"audio\button_click.wav")
clicked_sound.set_volume(0.25)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player(screen, WINDOW_WIDTH, WINDOW_HEIGHT))

obstacle_group = pygame.sprite.Group()

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2500)

menu_button1 = Button(1, "Play", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 40, 200, 64, small_font_20)
menu_button2 = Button(2, "i", 30, WINDOW_HEIGHT - 40, 65, 65, small_font_20)
menu_button3 = Button(1, "Exit", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 105, 200, 64, small_font_20)

credit_button1 = Button(2, "X", 30, 35, 65, 65, small_font_20)
credit_button2 = Button(1, "Github", WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100, 200, 64, small_font_14)
menu_buttons = [menu_button1, menu_button2, menu_button3]
credit_buttons = [credit_button1, credit_button2]

while True:
    #Handle Quit Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:                    
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(["fly", "fly", "slime", "slime"]), screen, WINDOW_WIDTH, WINDOW_HEIGHT))

        else:
            mouse_pos = pygame.mouse.get_pos()
            
            if iscredit_menu_showed:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in credit_buttons:
                        if button.rect.collidepoint(event.pos):
                            button.pressed = True
                            
                            pressed_sound.play()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if credit_button1.rect.collidepoint(event.pos):
                        game_active = False
                        iscredit_menu_showed = False
                        clicked_sound.play()
                    if credit_button2.rect.collidepoint(event.pos):
                        webbrowser.open("https://github.com/StewardMelvinTang/Runner_Game")
                        clicked_sound.play()
                    
                    for menu_button in menu_buttons:
                        menu_button.pressed = False
                    for credit_button in credit_buttons:
                        credit_button.pressed = False                          
                        
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in menu_buttons:
                        if button.rect.collidepoint(event.pos):
                            button.pressed = True
                            pressed_sound.play()
                    
                if event.type == pygame.MOUSEBUTTONUP:
                    if menu_button1.rect.collidepoint(event.pos):
                        #Button Play is Clicked
                        game_active = True
                        start_time = int(pygame.time.get_ticks() / 1000) * 2 - start_time
                        clicked_sound.play()
                        
                    if menu_button2.rect.collidepoint(event.pos):
                        #Button Credit is Clicked
                        game_active = False
                        iscredit_menu_showed = True
                        clicked_sound.play()
                        
                    if menu_button3.rect.collidepoint(event.pos):
                        clicked_sound.play()
                        #Quit Game is Clicked
                        pygame.quit()
                        exit()                
                                
                    for menu_button in menu_buttons:
                        menu_button.pressed = False
                    for credit_button in credit_buttons:
                        credit_button.pressed = False            
                    
        
    
        
    if game_active:
        background.scroll_background()
    
        score = display_score()
        
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()
        
        game_active = collision_sprite()

    else:
        #Intro / Mainmenu Screen
        screen.blit(bg, (0,0))
        screen.blit(ground, (0,WINDOW_HEIGHT - 60))
        player_gravity = 0
        
        if iscredit_menu_showed:
            for button in credit_buttons:
                button.draw_button(screen)
            
            screen.blit(credit_text_title, (WINDOW_WIDTH / 2 - credit_text_title.get_width() / 2 , -10))
            screen.blit(credit_text, (WINDOW_WIDTH / 2 - credit_text.get_width() / 2 , 100))
            screen.blit(credit_text2, (WINDOW_WIDTH / 2 - credit_text2.get_width() / 2 , 160))
            screen.blit(credit_text3, (WINDOW_WIDTH / 2 - credit_text3.get_width() / 2 , 200))
            
        else:
            if (not score == 0):
                score_text = small_font_20.render(f"Your Score: {score}", False, "Black")
                score_text_rect = score_text.get_rect(center = (WINDOW_WIDTH / 2, 100))
                screen.blit(score_text, score_text_rect)
                
            for button in menu_buttons:
                button.draw_button(screen)
            
            screen.blit(titlescreen_textsurface, titlescreen_text_rect)


    #Update the Display
    pygame.display.update()
    clock.tick(MAX_FRAMERATE) #Set Game's Max Framerate