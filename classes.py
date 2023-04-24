import pygame
import random

class Button():   
    def __init__(self, btn_type, text, x, y, width, height, font):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text_color = "Black"
        self.font = font
        self.btn_type = btn_type

        if btn_type == 1: 
            self.image = pygame.image.load(r"graphics\UI\Button_01.png").convert_alpha()
            self.pressed_image = pygame.image.load(r"graphics\UI\Button_01_Pressed.png").convert_alpha()
        elif btn_type == 2: 
            self.image = pygame.image.load(r"graphics\UI\Button_02.png").convert_alpha()
            self.pressed_image = pygame.image.load(r"graphics\UI\Button_02_Pressed.png").convert_alpha()
    
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.pressed_image = pygame.transform.scale(self.pressed_image, (self.width, self.height))
        self.phase = 0
        self.phase_add = 0.1
        self.pressed = False

        
    def draw_button(self, surface):
        imgtodraw = self.pressed_image if self.pressed else self.image
        self.rect = imgtodraw.get_rect(center=(self.x, self.y + self.phase))
        surface.blit(imgtodraw, self.rect)
        text = self.font.render(self.text, False, self.text_color)
        surface.blit(text, (self.x - text.get_width() / 2, self.y - text.get_height() / 2 - 5 + self.phase ))
        
        #floating animation
        self.phase += self.phase_add
        if self.phase >= 5: 
            self.phase_add = -0.1
        if self.phase <= 0.0: 
            self.phase_add = 0.1
            
class Background():
    def __init__(self, surface, WINDOW_WIDTH, WINDOW_HEIGHT):
        super().__init__()
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.surface = surface
        self.background = pygame.image.load("graphics\Sky_Blue.jpg").convert()
        self.background = pygame.transform.scale(self.background, (self.WINDOW_WIDTH,WINDOW_HEIGHT - 60))
        self.bg_left =pygame.Rect(0, 0, self.WINDOW_WIDTH, self.WINDOW_HEIGHT - 60)
        self.bg_right = pygame.Rect(self.WINDOW_WIDTH, 0, self.WINDOW_WIDTH, WINDOW_HEIGHT)
        self.ground = pygame.image.load("graphics\Ground.jpg").convert()
        self.ground_left = pygame.Rect(0, self.WINDOW_HEIGHT - 60, WINDOW_WIDTH, 60)
        self.ground_right = pygame.Rect(self.WINDOW_WIDTH, self.WINDOW_HEIGHT - 60, self.WINDOW_WIDTH, 60)
        self.scroll_speed = 2
        self.x = 0
    
    def scroll_background(self, game_speed):
        if self.background and self.ground:
            self.x -= self.scroll_speed * game_speed
            if self.x <= -self.WINDOW_WIDTH: self.x = 0
            
            self.surface.blit(self.background, self.bg_left.move(self.x, 0))
            self.surface.blit(self.background, self.bg_right.move(self.x, 0))
            self.surface.blit(self.ground, self.ground_left.move(self.x, 0))
            self.surface.blit(self.ground, self.ground_right.move(self.x, 0))
            
class Obstacle(pygame.sprite.Sprite):
    def __init__ (self, type, surface, WINDOW_WIDTH, WINDOW_HEIGHT, game_speed):
        super().__init__()
        self.game_speed = game_speed
        self.surface = surface
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        
        if type == "fly":
            self.sprite_size = (60,30)
            self.speed = 0.25 * game_speed
            fly_frame_1 = pygame.image.load("graphics\Fly\Fly_01.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics\Fly\Fly_02.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = self.WINDOW_HEIGHT - 160
        
        elif type == "slime":
            self.sprite_size = (60,30)
            self.speed = 0.1 * game_speed
            slime_frame_1 = pygame.image.load("graphics\Slime\Slime_01.png").convert_alpha()
            slime_frame_2 = pygame.image.load("graphics\Slime\Slime_02.png").convert_alpha()
            self.frames = [slime_frame_1, slime_frame_2]
            y_pos = self.WINDOW_HEIGHT - 60
            
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], self.sprite_size)
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (self.WINDOW_WIDTH + random.randint(500, 900), y_pos))
        
    def animation_state(self):
        self.animation_index += self.speed
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= random.randint(3, 5) * self.game_speed
        self.destroy()
        
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
            
class Player(pygame.sprite.Sprite):
    def __init__(self, surface, WINDOW_WIDTH, WINDOW_HEIGHT):
        super().__init__()
        self.surface = surface
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        
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
        self.rect = self.image.get_rect(midbottom = (125, self.WINDOW_HEIGHT - 60))
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
        if self.rect.bottom >= self.WINDOW_HEIGHT - 60: self.rect.bottom = self.WINDOW_HEIGHT - 60
    
    def animation_state(self, game_speed):
        if self.rect.bottom < self.WINDOW_HEIGHT - 60:
            self.image = self.player_jump
        else:
            self.player_index += 0.1 * game_speed
            if self.player_index >= len(self.player_walks): self.player_index = 0
            self.image = self.player_walks[int(self.player_index)] 
            
    def update(self, game_speed):
        self.player_input()
        self.apply_gravity()
        self.animation_state(game_speed)