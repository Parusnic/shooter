#Создай собственный Шутер!

from random import randint
from pygame import *

font.init()

SCREEN_SIZE = (1920, 1080)
SPRITE_SIZE = 60


class GameSprite(sprite.Sprite):
    def __init__ (self, image_name, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (SPRITE_SIZE, SPRITE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < SCREEN_SIZE[0] - SPRITE_SIZE:
            self.rect.x += self.speed     
        self.reset()

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= SCREEN_SIZE[1]:
            self.rect.y = 0
            self.rect.x = randint(0, SCREEN_SIZE[0] - SPRITE_SIZE)
            # Увеличить счетчик пропущеных на 1
            missed_counter.count += 1
            missed_counter.render_text()


class Counter:
    def __init__(self, x, y, text):
        self.pos = (x, y)
        self.text = text
        self.count = 0
    
    def render_text(self, text_color=(255, 255, 255), text_size=30, font_name='Verdana'):
        f = font.SysFont(font_name, text_size)
        self.image = f.render(self.text + str(self.count), True, text_color)
    
    def update(self):
        window.blit(self.image, self.pos)

missed_counter = Counter(10, 10, 'Количество пропущенных: ')
missed_counter.render_text()

player = Player('rocket.png', SCREEN_SIZE[0] // 2, SCREEN_SIZE[1]-SPRITE_SIZE, 5)
enemies = sprite.Group()

for i in range(5):
    enemies.add(Enemy('ufo.png', randint(0, SCREEN_SIZE[0] - SPRITE_SIZE), 0, randint(1, 3)))


window = display.set_mode(SCREEN_SIZE)
display.set_caption('Shooter')
background = transform.scale(
        image.load('galaxy.jpg'),
        SCREEN_SIZE
)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.05)
mixer.music.play()


game = True
clock = time.Clock()
FPS = 60
while game:
    clock.tick(FPS)
    window.blit(background, (0,0))
    player.update()
    enemies.update()
    enemies.draw(window)
    missed_counter.update()
    display.update()
    for e in event.get():
        if e.type == QUIT:
            game = False