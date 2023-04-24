import pygame
from sys import exit
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_sprite_size = (85,85)
        player_walk1 = pygame.image.load("graphics\Char\Char_Walk_01.png").convert_alpha()
        player_walk2 = pygame.image.load("graphics\Char\Char_Walk_02.png").convert_alpha()
    
        self.player_jump = pygame.image.load("graphics\Char\Char_Jump.png").convert_alpha()
        self.player_jump = pygame.transform.scale(self.player_jump, player_sprite_size)
        self.player_walks = [player_walk1, player_walk2]
        self.player_index = 0
        
        for i in range(len(self.player_walks)):
            self.player_walks[i] = pygame.transform.scale(self.player_walks[i], player_sprite_size)
        
        self.image = self.player_walks[self.player_index]
        self.image = pygame.transform.scale(self.image, player_sprite_size)
        self.rect = self.image.get_rect(midbottom = (125, WINDOW_HEIGHT - 60))
        self.gravity = 0
        
        self.jump_sound_01 = pygame.mixer.Sound("audio\Jump_01.wav")
        self.jump_sound_02 = pygame.mixer.Sound("audio\Jump_02.wav")
        self.jump_sound_01.set_volume(0.15)
        self.jump_sound_02.set_volume(0.15)
        self.jump_sound_played = False
        self.jump_sound_start_time = 0
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -15
            
            sound_to_play = random.choice([self.jump_sound_01, self.jump_sound_02])
            if not self.jump_sound_played:
                sound_to_play.play()
                self.jump_sound_played = True
                self.jump_sound_start_time = pygame.time.get_ticks()
            
            else:
                sound_dur = sound_to_play.get_length() * 1000
                current_time = pygame.time.get_ticks()
                if self.jump_sound_played and current_time-self.jump_sound_start_time >= sound_dur: self.jump_sound_played = False
            
    def apply_gravity(self):
        self.gravity += 0.5
        self.rect.y += self.gravity
        if self.rect.bottom >= WINDOW_HEIGHT - 60: self.rect.bottom = WINDOW_HEIGHT - 60
    
    def animation_state(self):
        if self.rect.bottom < WINDOW_HEIGHT - 60:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walks): self.player_index = 0
            self.image = self.player_walks[int(self.player_index)] 
            
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        
class Obstacle(pygame.sprite.Sprite):
    def __init__ (self, type):
        super().__init__()
        
        if type == "fly":
            self.sprite_size = (60,30)
            self.speed = 0.25
            fly_frame_1 = pygame.image.load("graphics\Fly\Fly_01.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics\Fly\Fly_02.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = WINDOW_HEIGHT - 160
        
        elif type == "slime":
            self.sprite_size = (60,30)
            self.speed = 0.1
            slime_frame_1 = pygame.image.load("graphics\Slime\Slime_01.png").convert_alpha()
            slime_frame_2 = pygame.image.load("graphics\Slime\Slime_02.png").convert_alpha()
            self.frames = [slime_frame_1, slime_frame_2]
            y_pos = WINDOW_HEIGHT - 60
            
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], self.sprite_size)
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH + random.randint(500, 900), y_pos))
        
    def animation_state(self):
        self.animation_index += self.speed
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= random.randint(3, 5)
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Background():
    def __init__(self):
        super().__init__()
        
        self.background = pygame.image.load("graphics\Sky_Blue.jpg").convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH,WINDOW_HEIGHT - 60))
        self.bg_left =pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT - 60)
        self.bg_right = pygame.Rect(WINDOW_WIDTH, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.ground = pygame.image.load("graphics\Ground.jpg").convert()
        self.ground_left = pygame.Rect(0, WINDOW_HEIGHT - 60, WINDOW_WIDTH, 60)
        self.ground_right = pygame.Rect(WINDOW_WIDTH, WINDOW_HEIGHT - 60, WINDOW_WIDTH, 60)
        self.scroll_speed = 2
        self.x = 0
    
    def scroll_background(self):
        if self.background and self.ground:
            self.x -= self.scroll_speed
            if self.x <= -WINDOW_WIDTH: self.x = 0
            
            screen.blit(self.background, self.bg_left.move(self.x, 0))
            screen.blit(self.background, self.bg_right.move(self.x, 0))
            screen.blit(self.ground, self.ground_left.move(self.x, 0))
            screen.blit(self.ground, self.ground_right.move(self.x, 0))

            
                                    
def display_score():
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
start_time = 0
score = 0

pygame.init() #Initialize PyGame (A must)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) #Set Window Resolution
pygame.display.set_caption("Runner") #Set Window Title
clock = pygame.time.Clock() #Create a call object

#background = pygame.image.load("graphics\Sky_Blue.jpg").convert()
#background = pygame.transform.scale(background, (WINDOW_WIDTH,WINDOW_HEIGHT - 60))
background = Background()

ground = pygame.image.load("graphics\Ground.jpg").convert()
ground = pygame.transform.scale(ground, (800, 60))

small_font_20 = pygame.font.Font("font\Pixeled.ttf", 20)
big_font_30 = pygame.font.Font("font\Pixeled.ttf", 30)

#Title screen Text
titlescreen_textsurface = big_font_30.render("Runner Game", False, "Black")
titlescreen_text_rect = titlescreen_textsurface.get_rect(center=(WINDOW_WIDTH / 2, 50))
titlescreen_pressSPACE_textsurface = small_font_20.render("Press Space to Start", False, "darkgrey")
titlescreen_pressSPACE_rect = titlescreen_pressSPACE_textsurface.get_rect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))

#Background Music
BGM = pygame.mixer.Sound("audio\Lines of Code.mp3").play(loops=-1)
BGM.set_volume(0.35)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2500)

while True:
    #Handle Quit Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if game_active:                    
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(random.choice(["fly", "fly", "slime", "slime"])))

        else:
            #Input Key If the Game wasn't active
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000) - start_time
        
    
        
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
        
        screen.blit(ground, (0,WINDOW_HEIGHT - 60))
        player_gravity = 0
        
        if (not score == 0):
            score_text = small_font_20.render(f"Your Score: {score}", False, "Black")
            score_text_rect = score_text.get_rect(center = (WINDOW_WIDTH / 2, 100))
            screen.blit(score_text, score_text_rect)
        
        screen.blit(titlescreen_textsurface, titlescreen_text_rect)
        screen.blit(titlescreen_pressSPACE_textsurface, titlescreen_pressSPACE_rect)

    #Update the Display
    pygame.display.update()
    clock.tick(MAX_FRAMERATE) #Set Game's Max Framerate