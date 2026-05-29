import pygame
import sys
import random
import math
from collections import deque

# 1. Инициализация pygame и создание окна ДО импорта load
pygame.init()
pygame.mixer.init()

WIDTH = 1500
HEIGHT = 1000
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('underverse')
clock = pygame.time.Clock()
FPS = 60

# 2. Теперь можно импортировать модули, которые используют convert_alpha()
from load import *
from sprites.sprite_classes import *
from camera import Camera

# Константы
BLACK = (0, 0, 0)

HP_BAR_WIDTH = 300
HP_BAR_HEIGHT = 30
HP_BAR_X = 200
HP_BAR_Y = 20
WAVE_DELAY = 3.0

MAP_SIZE = 8000

# Глобальные переменные




# Игровые переменные
camera = None
all_sprites = None
bg_sprites = None
water_group = None
collision_sprites = None
player_group = None
player = None
zombi_group = None
bull_group = None
grav_group = None
trava_group = None
kysty_group = None
kamn_group = None
kustik_group = None
bochka_group = None
aptechka_group = None
hp = 100
attack_z = False
current_wave = 1
enemies_alive = 0
wave_in_progress = False
wave_timer = 0.0
game_map = []
game_map_details = []

_grid_cache = None
_grid_last_update = 0
GRID_UPDATE_INTERVAL = 2.0

mapFile = 'game_locations/test_player1.txt'
mapFile_detail = 'game_locations/Mb_1_loc.txt'



# -------------------- Вспомогательные функции --------------------
def loadMap(mapFile):
    global game_map
    game_map = []
    with open(mapFile, 'r') as file:
        for line in file:
            cleaned = line.strip().replace('\n', '').replace('\r', '')
            if cleaned:
                game_map.append(cleaned.split(','))

def loadMap_detail(mapFile_detail):
    global game_map_details
    game_map_details = []
    with open(mapFile_detail, 'r') as file:
        for line in file:
            cleaned = line.strip().replace('\n', '').replace('\r', '')
            if cleaned:
                game_map_details.append(cleaned.split(','))

def drawMap():
    global water_group, collision_sprites, bg_sprites, grav_group, trava_group, kysty_group
    water_group.empty()
    collision_sprites.empty()
    bg_sprites.empty()
    grav_group.empty()
    trava_group.empty()
    kysty_group.empty()

    for i, row in enumerate(game_map):
        for j, tile in enumerate(row):
            pos = [j * 80, i * 80]
            if tile == '1':  # вода
                water = Water(water_image, pos)
                water_group.add(water)
                bg_sprites.add(water)
                collision_sprites.add(water)
            elif tile == '2':  # трава
                trava = Trava(trava_image, pos)
                trava_group.add(trava)
                bg_sprites.add(trava)
            elif tile == '3':  # гравий
                gravey = Gravey(grav_image, pos)
                grav_group.add(gravey)
                bg_sprites.add(gravey)
                collision_sprites.add(gravey)
            elif tile == '4':  # кусты
                kysty = Kysty(kysty_image, pos)
                kysty_group.add(kysty)
                bg_sprites.add(kysty)

def drawMap_details():
    global kamn_group, bg_sprites, kustik_group
    kamn_group.empty()
    kustik_group.empty()
    for i, row in enumerate(game_map_details):
        for j, tile in enumerate(row):
            pos = [j * 80, i * 80]
            if tile == '1':
                kamn = Kamn(kamn_image, pos)
                kamn_group.add(kamn)
                bg_sprites.add(kamn)

            elif tile == '2':
                kustik = Kysty(kusty_image, pos)
                kustik_group.add(kustik)
                bg_sprites.add(kustik)


def clear_all_groups():
    """Очищает все группы спрайтов"""
    for group in [water_group, bull_group, grav_group, trava_group, kysty_group,
                  kustik_group, kamn_group, all_sprites, bg_sprites, collision_sprites,
                  player_group, zombi_group, bochka_group, aptechka_group]:
        if group:
            group.empty()

def restart():
    global camera, all_sprites, bg_sprites, water_group, collision_sprites, player_group, player
    global zombi_group, bull_group, hp, grav_group, trava_group, kysty_group, current_wave
    global enemies_alive, wave_in_progress, wave_timer, kamn_group, kustik_group, bochka_group, aptechka_group

    # Очистка старых спрайтов
    clear_all_groups()

    # Создание новых групп
    bochka_group = pygame.sprite.Group()
    aptechka_group = pygame.sprite.Group()
    water_group = pygame.sprite.Group()
    bull_group = pygame.sprite.Group()
    grav_group = pygame.sprite.Group()
    trava_group = pygame.sprite.Group()
    kysty_group = pygame.sprite.Group()
    kustik_group = pygame.sprite.Group()
    kamn_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    bg_sprites = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    zombi_group = pygame.sprite.Group()

    camera = Camera(MAP_SIZE, MAP_SIZE, WIDTH, HEIGHT)
    player = Player(solid_image_walk_right['walk_horisont'][0], (1000, 1000),
                    collision_sprites, bull_group, camera, all_sprites, gun_sound)
    hp = 100
    player_group.add(player)
    all_sprites.add(player)

    # Загрузка карты
    loadMap(mapFile)
    drawMap()
    loadMap_detail(mapFile_detail)
    drawMap_details()

    # Сброс волн
    current_wave = 1
    enemies_alive = 0
    wave_in_progress = False
    wave_timer = 2.0

def spawn_zombies_for_wave():
    global wave_in_progress, enemies_alive, current_wave
    spawn_bochka_in_front_of_player()
    num_zombies = current_wave + 3
    for _ in range(num_zombies):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.randint(300, 800)
        world_x = player.rect.centerx + distance * math.cos(angle)
        world_y = player.rect.centery + distance * math.sin(angle)
        world_x = max(50, min(MAP_SIZE-50, world_x))
        world_y = max(50, min(MAP_SIZE-50, world_y))
        new_zombie = Zombi(zombi_image_idle[0], (world_x, world_y))
        new_zombie.all_sprites = all_sprites
        new_zombie.player = player
        zombi_group.add(new_zombie)
        all_sprites.add(new_zombie)
        enemies_alive += 1
    wave_in_progress = True

def spawn_bochka_in_front_of_player():
    global bochka_group, all_sprites, player
    direction = player.im_dir
    distance = 200
    px, py = player.rect.center
    if direction == 'up':
        sx, sy = px, py - distance
    elif direction == 'down':
        sx, sy = px, py + distance
    elif direction == 'left':
        sx, sy = px - distance, py
    else:
        sx, sy = px + distance, py
    sx = max(50, min(MAP_SIZE-50, sx))
    sy = max(50, min(MAP_SIZE-50, sy))
    bochka = Bochka(bochka_image, (sx, sy))
    bochka_group.add(bochka)
    all_sprites.add(bochka)

def spawn_aptechka_relative_to_bochka(bochka_pos, direction):
    global aptechka_group, all_sprites
    bx, by = bochka_pos
    distance = 80
    if direction == 'up':
        pos = (bx, by - distance)
    elif direction == 'down':
        pos = (bx, by + distance)
    elif direction == 'left':
        pos = (bx - distance, by)
    else:
        pos = (bx + distance, by)
    pos = (max(50, min(MAP_SIZE-50, pos[0])), max(50, min(MAP_SIZE-50, pos[1])))
    aptechka = Aptechka(aptechka_image, pos)
    aptechka_group.add(aptechka)
    all_sprites.add(aptechka)

# -------------------- BFS и навигация --------------------
def get_grid(force=False):
    global _grid_cache, _grid_last_update
    now = pygame.time.get_ticks() / 1000.0
    if _grid_cache and not force and (now - _grid_last_update) < GRID_UPDATE_INTERVAL:
        return _grid_cache
    grid_w = MAP_SIZE // 40
    grid_h = MAP_SIZE // 40
    grid = [[0]*grid_w for _ in range(grid_h)]
    for water in water_group:
        x, y = water.rect.x//40, water.rect.y//40
        if 0 <= x < grid_w and 0 <= y < grid_h:
            grid[y][x] = 1
    for grav in grav_group:
        x, y = grav.rect.x//40, grav.rect.y//40
        if 0 <= x < grid_w and 0 <= y < grid_h:
            grid[y][x] = 1
    _grid_cache = grid
    _grid_last_update = now
    return grid

def bfs(start, goal, grid):
    if start == goal:
        return [start]
    queue = deque()
    queue.append((start, [start]))
    visited = {start}
    while queue:
        cur, path = queue.popleft()
        for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]:
            nx, ny = cur[0]+dx, cur[1]+dy
            if 0 <= nx < len(grid[0]) and 0 <= ny < len(grid) and (nx,ny) not in visited:
                if grid[ny][nx] == 0:
                    if (nx,ny) == goal:
                        return path + [(nx,ny)]
                    visited.add((nx,ny))
                    queue.append(((nx,ny), path+[(nx,ny)]))
    return None

# -------------------- Игровой цикл --------------------
def lvlGame():
    global hp, attack_z, current_wave, enemies_alive, wave_in_progress, wave_timer
    dt = clock.tick(FPS) / 1000.0

    player.update(dt, FPS, solid_image_walk_down['walk_vertical'],
                  solid_image_walk_right['walk_horisont'],
                  solid_image_attack_down['attack'], Bull_image, all_sprites, gun_sound)

    for z in zombi_group:
        z.update(FPS, zombi_image_walk, zombi_image_attack,
                 zombi_image_Hurt, water_group, zombi_image_Dead)

    bull_group.update(dt)

    for z in zombi_group:
        hit = pygame.sprite.spritecollide(z, bull_group, True)
        if hit:
            z.hp_mons -= 1
            if z.hp_mons <= 0 and not z.is_dying:
                z.die()
                enemies_alive -= 1

    # Бочки и аптечки
    hit_bochka = pygame.sprite.spritecollide(player, bochka_group, False)
    for bochka in hit_bochka:
        pos = bochka.rect.center
        direction = player.im_dir
        bochka.kill()
        spawn_aptechka_relative_to_bochka(pos, direction)

    hit_aptechka = pygame.sprite.spritecollide(player, aptechka_group, True)
    if hit_aptechka:
        heal_sound.play()
        hp = min(hp + 30, 100)

    camera.update(player)
    camera.draw(window, bg_sprites, all_sprites)

    if attack_z:
        loos_hp_sound.play()
        hp -= 10
        attack_z = False
    if hp <= 0:
        loosing_life_sound.play()
        return False  # смерть

    # Полоска здоровья
    color = (0,200,0) if hp >= 60 else (255,69,0) if hp > 30 else (139,0,0)
    pygame.draw.rect(window, (150,150,150), (HP_BAR_X, HP_BAR_Y, HP_BAR_WIDTH, HP_BAR_HEIGHT))
    pygame.draw.rect(window, color, (HP_BAR_X, HP_BAR_Y, (hp/100)*HP_BAR_WIDTH, HP_BAR_HEIGHT))
    pygame.draw.rect(window, (0,0,0), (HP_BAR_X, HP_BAR_Y, HP_BAR_WIDTH, HP_BAR_HEIGHT), 2)

    # Волны
    if not wave_in_progress:
        if current_wave <= 1:
            wave_timer += dt
            if wave_timer >= WAVE_DELAY:
                if wave_sound: wave_sound.play()
                wave_timer = 0
                spawn_zombies_for_wave()
        else:
            # ПОБЕДА! Все волны пройдены
            if win_music:
                win_music.play()
            pygame.mixer.music.stop()
            return False
    elif wave_in_progress and len(zombi_group) == 0 and enemies_alive == 0:
        wave_in_progress = False
        current_wave += 1
        print(f"Волна {current_wave - 1} пройдена")
        if current_wave > 10:
            # ПОБЕДА! После завершения 10 волны
            if win_music:
                win_music.play()
            pygame.mixer.music.stop()
            return False


    pygame.display.update()
    return True

class Zombi(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        global attack_z
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 4
        self.dir = "top"
        self.timer_move = 0
        self.trigger = False
        self.timer_anime = 0
        self.frame = 0
        self.path = None
        self.state = 'walk'
        self.attack_timer = 0
        self.attack_duration = 60
        self.hp_mons = 2
        self.t = True
        self.anime = False
        self.is_dying = False
        self.dead_animation_finished = False
        self.water_group = None
        self.player = None
        self.all_sprites = None

    def die(self):
        if self.state != 'dead' and not self.is_dying:
            self.state = 'dead'
            self.is_dying = True
            self.anime = True
            self.frame = 0
            self.timer_anime = 0

    def try_move(self, dx, dy):
        next_rect = self.rect.move(dx, dy)
        if not (0 <= next_rect.x <= MAP_SIZE-40 and 0 <= next_rect.y <= MAP_SIZE-40):
            return False
        temp = pygame.sprite.Sprite()
        temp.rect = next_rect
        if pygame.sprite.spritecollide(temp, self.water_group, False):
            return False
        if pygame.sprite.spritecollide(temp, grav_group, False):
            return False
        if self.player and pygame.sprite.collide_rect(temp, self.player):
            return False
        return True

    def update(self, FPS, walk_img, attack_img, hurt_img, water_group, dead_img):
        global attack_z
        self.water_group = water_group
        self.player = player
        if not self.player or self.dead_animation_finished:
            return
        if self.state == 'dead':
            self.animation(FPS, walk_img, attack_img, hurt_img, dead_img)
            return

        self.timer_move += 1
        dist = ((self.rect.centerx - self.player.rect.centerx)**2 + (self.rect.centery - self.player.rect.centery)**2)**0.5

        if self.hp_mons == 1 and self.t:
            self.state = 'hurt'
            self.frame = 0
            self.t = False
            self.anime = True

        if dist < 80:
            if self.state not in ('attack','hurt'):
                self.state = 'attack'
                self.attack_timer = self.attack_duration
                self.frame = 0
                self.anime = True
                attack_z = True
            elif self.state == 'attack':
                self.attack_timer -= 1
                if self.attack_timer <= 0:
                    self.state = 'walk'
        else:
            if self.state == 'attack':
                self.state = 'walk'
                self.frame = 0

        self.trigger = dist < 1500
        if self.state != 'hurt':
            if self.trigger:
                if self.timer_move % 90 == 0:
                    grid = get_grid()
                    start = (self.rect.x//40, self.rect.y//40)
                    goal = (self.player.rect.x//40, self.player.rect.y//40)
                    self.path = bfs(start, goal, grid)
                if hasattr(self,'path') and self.path and len(self.path)>1:
                    self.move_along_path()
                else:
                    self.random_movement()
            else:
                self.random_movement()

        self.animation(FPS, walk_img, attack_img, hurt_img, dead_img)

    def move_along_path(self):
        if not self.path or len(self.path)<=1:
            return
        nx, ny = self.path[1]
        tx = nx*40 + 20
        ty = ny*40 + 20
        dx = 0
        if abs(self.rect.centerx - tx) > self.speed:
            dx = self.speed if self.rect.centerx < tx else -self.speed
            self.dir = 'right' if dx>0 else 'left'
            if self.try_move(dx, 0):
                self.rect.x += dx
        elif len(self.path)>1:
            self.path.pop(0)
        dy = 0
        if abs(self.rect.centery - ty) > self.speed:
            dy = self.speed if self.rect.centery < ty else -self.speed
            self.dir = 'bottom' if dy>0 else 'top'
            if self.try_move(0, dy):
                self.rect.y += dy
        elif len(self.path)>1:
            self.path.pop(0)
        self.anime = True

    def random_movement(self):
        if self.timer_move % 60 == 0:
            self.dir = random.choice(['top','bottom','left','right'])
        dx = dy = 0
        if self.dir == 'top': dy = -self.speed
        elif self.dir == 'bottom': dy = self.speed
        elif self.dir == 'left': dx = -self.speed
        else: dx = self.speed
        if self.try_move(dx, dy):
            self.rect.x += dx
            self.rect.y += dy
            self.anime = True
        else:
            self.dir = random.choice(['top','bottom','left','right'])
            self.anime = False

    def animation(self, FPS, walk, attack, hurt, dead):
        if self.state == 'walk':
            frames = walk['walk']
            delay = FPS * 0.1
        elif self.state == 'attack':
            frames = attack
            delay = FPS * 0.1
        elif self.state == 'hurt':
            frames = hurt
            delay = FPS * 0.1
        elif self.state == 'dead':
            frames = dead
            delay = FPS * 0.2
        else:
            return
        if not frames:
            return
        if self.anime:
            self.timer_anime += 1
            if self.frame >= len(frames):
                self.frame = 0
            img = frames[self.frame]
            if self.dir == 'left':
                img = pygame.transform.flip(img, True, False)
            self.image = img
            if self.timer_anime >= delay:
                self.frame += 1
                self.timer_anime = 0
                if self.state == 'hurt' and self.frame >= len(frames):
                    self.state = 'walk'
                    self.frame = 0
                    self.anime = False
                if self.state == 'dead' and self.frame >= len(frames):
                    self.dead_animation_finished = True
                    self.kill()
        else:
            if self.state == 'walk' and frames:
                self.image = frames[0]

# -------------------- Кнопки и меню --------------------
from pygame.locals import *
WHITE = (255,255,255)

class SimpleButton:
    STATE_IDLE = 'idle'
    STATE_ARMED = 'armed'
    STATE_DISAMED = 'disarmed'
    def __init__(self, window, loc, up, down, callback=None):
        self.window = window
        self.loc = loc
        self.surfaceUp = up if not isinstance(up, str) else pygame.image.load(up)
        self.surfaceDown = down if not isinstance(down, str) else pygame.image.load(down)
        self.surfaceUp.set_colorkey(WHITE)
        self.surfaceDown.set_colorkey(WHITE)
        self.rect = self.surfaceUp.get_rect(topleft=loc)
        self.state = SimpleButton.STATE_IDLE
        self.callback = callback

    def handleEvent(self, event):
        if event.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
            return False
        point_in = self.rect.collidepoint(event.pos)
        if self.state == SimpleButton.STATE_IDLE:
            if event.type == MOUSEBUTTONDOWN and point_in:
                self.state = SimpleButton.STATE_ARMED
        elif self.state == SimpleButton.STATE_ARMED:
            if event.type == MOUSEBUTTONUP and point_in:
                self.state = SimpleButton.STATE_IDLE
                if self.callback:
                    self.callback()
                return True
            if event.type == MOUSEMOTION and not point_in:
                self.state = SimpleButton.STATE_DISAMED
        elif self.state == SimpleButton.STATE_DISAMED:
            if point_in:
                self.state = SimpleButton.STATE_ARMED
            elif event.type == MOUSEBUTTONUP:
                self.state = SimpleButton.STATE_IDLE
        return False

    def draw(self):
        img = self.surfaceDown if self.state == SimpleButton.STATE_ARMED else self.surfaceUp
        self.window.blit(img, self.loc)


def draw_button_with_text(button, font, text, color=(0, 0, 0)):
    # Сначала рисуем саму кнопку
    button.draw()

    # Отображаем текст с чёрной обводкой для читаемости (опционально)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect(center=button.rect.center)

    # Если текст выходит за пределы кнопки, уменьшаем шрифт
    if text_rect.width > button.rect.width - 20 or text_rect.height > button.rect.height - 10:
        smaller_font = pygame.font.Font(None, int(font.get_height() * 0.7))
        text_surf = smaller_font.render(text, True, color)
        text_rect = text_surf.get_rect(center=button.rect.center)

    button.window.blit(text_surf, text_rect)

def show_main_menu():
    font = pygame.font.Font(None, 48)
    bg_color = (80,80,80)
    bw, bh = 200, 80
    y_start = HEIGHT//2 - 100
    spacing = 40
    btn_play = SimpleButton(window, (WIDTH//2 - bw//2, y_start), button_up_img, button_down_img)
    btn_settings = SimpleButton(window, (WIDTH//2 - bw//2, y_start+bh+spacing), button_up_img, button_down_img)
    btn_quit = SimpleButton(window, (WIDTH//2 - bw//2, y_start+2*(bh+spacing)), button_up_img, button_down_img)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            if btn_play.handleEvent(event):
                return 'play'
            if btn_settings.handleEvent(event):
                return 'settings'
            if btn_quit.handleEvent(event):
                return 'quit'
        window.fill(bg_color)
        draw_button_with_text(btn_play, font, "ИГРАТЬ")
        draw_button_with_text(btn_settings, font, "НАСТРОЙКИ")
        draw_button_with_text(btn_quit, font, "ВЫХОД")
        pygame.display.update()
        clock.tick(60)

# -------------------- Запуск игры --------------------
def run_game():
    pygame.mixer_music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    restart()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True
        if not lvlGame():
            pygame.mixer.music.stop()
            return True



# Предзагрузка изображений кнопок (из вашего load.py)
button_frames = load_image('assets/images/buttons_animation')


# Главный цикл
main_active = True
while main_active:
    choice = show_main_menu()
    if choice == 'play':
        run_game()
    elif choice == 'settings':
        print("Настройки")
        pygame.time.wait(500)
    else:
        main_active = False

pygame.quit()
sys.exit()