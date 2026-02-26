import pygame
import random
import math
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
print("Working Directory:", os.getcwd())

# ---------------- 기본 설정 ----------------
WIDTH, HEIGHT = 1200, 900
FPS = 60
GAME_TIME = 30_000  # 30초 (ms)
TARGET_CAL = 4000   # 박살낸 칼로리 기준 성공 목표
ASSET_DIR = "images"
SOUND_DIR = "sounds"

LED_RED = (255, 80, 60)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("건강한 음식 게임 확장판")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("malgungothic", 18)
font_medium = pygame.font.SysFont("malgungothic", 20, bold=True)
font_semilarge = pygame.font.SysFont("malgungothic", 30, bold=True)
font_large = pygame.font.SysFont("malgungothic", 40, bold=True)
font_timer = pygame.font.SysFont("consolas", 32, bold=True)

# ---------------- 공용 텍스트 함수 ----------------
def draw_text(surface, text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(img, rect)

# ---------------- 음식 데이터 ----------------
FOOD_SPECS = [
    ("라면", 70, True,  (255, 120, 120), "라면.png"),
    ("피자", 90, True,  (255, 120, 120), "피자.png"),
    ("햄버거", 80, True, (255, 120, 120), "햄버거.png"),
    ("닭다리", 60, True, (255, 120, 120), "닭다리.png"),
    ("도넛", 65, True, (255, 120, 120), "도넛.png"),
    ("아이스크림", 65, True, (255, 120, 120), "아이스크림.png"),

    ("계란후라이", 12, False, (120, 255, 120), "계란.png"),
    ("사과", 8, False, (120, 255, 120), "사과.png"),
    ("두부", 9, False, (120, 255, 120), "두부.png"),
    ("생선", 14, False, (120, 255, 120), "생선.png"),
    ("스테이크", 25, False, (120, 255, 120), "스테이크.png"),
    ("당근", 25, False, (120, 255, 120), "당근.png"),
]

FOOD_SIZE = 100

#--------음식 영혼 데이터-------
SOUL_IMAGES = {
    "계란후라이": pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, "계란영혼.png")).convert_alpha(),
        (120, 120)
    ),
    "사과": pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, "사과영혼.png")).convert_alpha(),
        (120, 120)
    ),
    "두부": pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, "두부영혼.png")).convert_alpha(),
        (120, 120)
    ),
    "생선": pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, "생선영혼.png")).convert_alpha(),
        (120, 120)
    ),
    "스테이크": pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, "고기영혼.png")).convert_alpha(),
        (120, 120)
    ),
    "당근": pygame.transform.smoothscale(
        pygame.image.load(os.path.join(ASSET_DIR, "당근영혼.png")).convert_alpha(),
        (120, 120)
    ),
}

# ---------------- 아이템 이미지 ----------------
ITEM_IMAGES = {
    "umbrella": pygame.image.load(os.path.join(ASSET_DIR, "Um.png")).convert_alpha(),
    "ultimate": pygame.image.load(os.path.join(ASSET_DIR, "Hammer.png")).convert_alpha(),
    "cheatingday": pygame.image.load(os.path.join(ASSET_DIR, "Cheat.png")).convert_alpha(),
}

#-------HUD용 아이콘-----
ICON_SIZE = 50
HUD_ICONS = {k: pygame.transform.smoothscale(v, (ICON_SIZE, ICON_SIZE))
             for k, v in ITEM_IMAGES.items()}


UMBRELLA_IMG = pygame.image.load(os.path.join(ASSET_DIR, "Umbrella.png")).convert_alpha()
UMBRELLA_SCALE = 1.0
w = int(WIDTH * UMBRELLA_SCALE)
h = int(HEIGHT * UMBRELLA_SCALE)
UMBRELLA_SCALED = pygame.transform.smoothscale(UMBRELLA_IMG, (w, h))

# 반투명도 설정 (0~255)
UMBRELLA_T = 200
UMBRELLA_SCALED.set_alpha(UMBRELLA_T)


#------해머 충격파 이미지-----
SHOCK_IMG = pygame.image.load(os.path.join(ASSET_DIR, "SHOCK.png")).convert_alpha()
SHOCK_IMG = pygame.transform.smoothscale(SHOCK_IMG, (220, 220))   # 원하는 크기

# ---------------- 사운드 로드 ----------------



SOUND_SWING_NORMAL = pygame.mixer.Sound(os.path.join(SOUND_DIR, "SWING_NORMAL.mp3"))
SOUND_HIT_BAD = pygame.mixer.Sound(os.path.join(SOUND_DIR, "HIT_BAD.mp3"))


SOUND_ITEM = pygame.mixer.Sound(os.path.join(SOUND_DIR, "ITEM_GET.wav"))

SOUND_LEVELUP = pygame.mixer.Sound(os.path.join(SOUND_DIR, "LVUP.mp3"))

SOUND_HAMMER_SWING = pygame.mixer.Sound(os.path.join(SOUND_DIR, "HAMMER_SWING.mp3"))
SOUND_HAMMER_HIT   = pygame.mixer.Sound(os.path.join(SOUND_DIR, "HAMMER_HIT.mp3"))

# 볼륨 조절 (필요하면 0.0 ~ 1.0 사이로 조정)
SOUND_SWING_NORMAL.set_volume(0.2)
SOUND_HIT_BAD.set_volume(0.2)
SOUND_ITEM.set_volume(0.2)


SOUND_HAMMER_SWING.set_volume(0.3)
SOUND_HAMMER_HIT.set_volume(0.3)


#------BGM-----
BGM_TITLE = os.path.join(SOUND_DIR, "OPENING.mp3")
BGM_INTRO = os.path.join(SOUND_DIR, "INTRO.mp3")
BGM_GAME = os.path.join(SOUND_DIR, "GAME.mp3")
BGM_CHEATING = os.path.join(SOUND_DIR, "CHEAT.mp3")
BGM_RESULT_GOOD = os.path.join(SOUND_DIR, "END_GOOD.wav")
BGM_RESULT_BAD = os.path.join(SOUND_DIR, "BAD_END.mp3")
#BGM_RESULT_HOW = os.path.join(SOUND_DIR, "BAD_END.mp3")


#--------UI-------
UI_LEVEL = pygame.image.load(os.path.join(ASSET_DIR, "LV_UI.png")).convert_alpha()
UI_LEVEL = pygame.transform.scale(UI_LEVEL, (300, 108))

UI_NOTE = pygame.image.load(os.path.join(ASSET_DIR, "NOTE.png")).convert_alpha()
UI_NOTE = pygame.transform.scale(UI_NOTE, (218, 260))

TIMER_NORMAL = pygame.image.load(os.path.join(ASSET_DIR, "HTIMER.png")).convert_alpha()
TIMER_PANIC = pygame.image.load(os.path.join(ASSET_DIR, "HTIMER_PANIC.png")).convert_alpha()

TIMER_NORMAL = pygame.transform.smoothscale(TIMER_NORMAL, (150,178))
TIMER_PANIC = pygame.transform.smoothscale(TIMER_PANIC, (150, 178))

#-----캐릭터----
IDLE_IMG = pygame.image.load(os.path.join(ASSET_DIR, "MC_IDLE.png")).convert_alpha()
SWING_IMG = pygame.image.load(os.path.join(ASSET_DIR, "MC_HIT.png")).convert_alpha()

IDLE_IMG = pygame.transform.smoothscale(IDLE_IMG, (107, 138))
SWING_IMG = pygame.transform.smoothscale(SWING_IMG, (243, 138))

#----캐릭터-아이템먹은 경우----
MC_ULT_IDLE = pygame.image.load(os.path.join(ASSET_DIR, "MC_ULT_IDLE.png")).convert_alpha()
MC_ULT_SWING = pygame.image.load(os.path.join(ASSET_DIR, "MC_ULT_SWING.png")).convert_alpha()

MC_ULT_IDLE = pygame.transform.smoothscale(MC_ULT_IDLE, (116, 154))
MC_ULT_SWING = pygame.transform.smoothscale(MC_ULT_SWING, (258, 141))

#---폭발 이미지---

EXPLO_IMG_1 = pygame.image.load(os.path.join(ASSET_DIR, "HIt_1.png")).convert_alpha()
EXPLO_IMG_2 = pygame.image.load(os.path.join(ASSET_DIR, "HIT_2.png")).convert_alpha()


for key in ITEM_IMAGES:
    ITEM_IMAGES[key] = pygame.transform.smoothscale(ITEM_IMAGES[key], (FOOD_SIZE, FOOD_SIZE))

def load_food_images():
    images = {}
    for name, cal, is_bad, c, file in FOOD_SPECS:
        path = os.path.join(ASSET_DIR, file)
        if not os.path.isfile(path):
            images[name] = None
            continue
        try:
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.smoothscale(img, (FOOD_SIZE, FOOD_SIZE))
            images[name] = img
        except:
            images[name] = None
    return images

FOOD_IMAGES = load_food_images()

# ---------------- 아이템 타입 ----------------
ITEM_TYPES = ["umbrella", "ultimate", "cheatingday"]




#----------UI------------
#---LV----
def draw_level_ui(surface, level):
    # 패널이 중앙 상단에 위치하도록
    rect = UI_LEVEL.get_rect(topleft=(20, 20))
    surface.blit(UI_LEVEL, rect)

    # 글자 표시 (패널 중앙)
    draw_text(surface, f"LEVEL {level}",
              font_large, (90, 40, 0),
              rect.centerx, rect.centery,
              center=True)
    return rect.bottom 
#-----포스트잇 HUD-----

def draw_note_ui(
    surface, panel_y,
    penalty, total_bad_cal, remain,
    umbrella_timer, ultimate_timer, cheating_timer
):
    # 포스트잇 위치 (LEVEL 아래)
    note_rect = UI_NOTE.get_rect(topleft=(20, 100))
    surface.blit(UI_NOTE, note_rect)

    # 패널티
    draw_text(surface, f"Penalty: {penalty}",
              font_medium, (80,40,40),
              note_rect.left + 30, note_rect.top + 90)

    # 칼로리 (박살낸 칼로리)
    draw_text(surface, f"Calorie: {total_bad_cal}kcal",
              font_medium, (80,40,40),
              note_rect.left + 30, note_rect.top + 130)
 
 
#----햄타이머----       
def draw_timer_ui(surface, remain):
    
    # 남은 시간 (분/초 단위)
    sec = remain // 1000
    minutes = sec // 60
    seconds = sec % 60
    time_str = f"{minutes:02d}:{seconds:02d}"
    
    if sec <= 10:
        timer_img = TIMER_PANIC    
    else:
        timer_img = TIMER_NORMAL
        
    # --- 시계 그림 표시 ---
    timer_rect = timer_img.get_rect(topright=(WIDTH - 20, 20))
    surface.blit(timer_img, timer_rect)
    
    show_number = True
    if sec <= 10:
        blink = (pygame.time.get_ticks() // 300) % 2  # 숫자 깜빡임 주기
        if blink == 0:
            return        

    # LED 숫자 
    text_x = timer_rect.centerx
    text_y = timer_rect.top + 116   # 화면 아래쪽 부분 (숫자 창)
    
    draw_text(surface, time_str,
              font_timer, LED_RED,
              text_x, text_y,
              center=True)       
        
        
        
# ---------------- 음식 / 아이템 생성 ----------------
def create_item():
    item_type = random.choice(ITEM_TYPES)
    rect = pygame.Rect(
        random.randint(20, WIDTH - 20 - FOOD_SIZE),
        random.randint(-350, -50),
        FOOD_SIZE, FOOD_SIZE
    )
    return {
        "type": "item",
        "item_type": item_type,
        "rect": rect,
        "speed": random.uniform(3.0, 5.8),
        "angle": random.uniform(0, 360),
        "rotation_speed": random.uniform(-3, 3),
        "bounced": False    
    }

def create_food():
    # 2% 확률로 아이템 생성
    if random.random() < 0.05:
        return create_item()

    base = random.choice(FOOD_SPECS)
    name, cal, is_bad, color, file = base
    rect = pygame.Rect(
        random.randint(20, WIDTH - 20 - FOOD_SIZE),
        random.randint(-350, -50),
        FOOD_SIZE, FOOD_SIZE,
    )
    return {
        "type": "food",
        "name": name,
        "cal": cal,
        "is_bad": is_bad,
        "rect": rect,
        "speed": random.uniform(3.0, 6.0),
        "image": FOOD_IMAGES.get(name),
        "angle": random.uniform(0, 360),
        "rotation_speed": random.uniform(-3, 3),
        "bounced": False    # ★ 여기 매우 중요
    }
    
#--- 플레이 배경---
GAME_BG = pygame.image.load(os.path.join(ASSET_DIR, "BG.png")).convert()
GAME_BG = pygame.transform.scale(GAME_BG, (WIDTH, HEIGHT))


# ----- popup -----
class PopupText:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color

        self.life = 40
        self.max_life = 40

        self.scale = 1.4
        self.scale_shrink_speed = 0.02

        self.dy = -0.5
        self.alpha = 255

    def update(self):
        self.y += self.dy

        if self.scale > 1.0:
            self.scale -= self.scale_shrink_speed

        self.life -= 1

        self.alpha = int(255 * (self.life / self.max_life))
        if self.alpha < 0:
            self.alpha = 0

    def draw(self, surf):
        font = pygame.font.SysFont("malgungothic", 40, bold=True)
        text_surface = font.render(self.text, True, self.color)
        text_surface.set_alpha(self.alpha)

        scaled_w = int(text_surface.get_width() * self.scale)
        scaled_h = int(text_surface.get_height() * self.scale)
        text_surface = pygame.transform.scale(text_surface, (scaled_w, scaled_h))

        rect = text_surface.get_rect(center=(self.x, self.y))
        surf.blit(text_surface, rect)

    def is_dead(self):
        return self.life <= 0


class AngelEffect:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.dy = -2         # 위로 올라가는 속도
        self.alpha = 255     # 시작 투명도
        self.scale = 0.6     # 시작 크기
        self.scale_speed = 0.01  # 천천히 커짐
        self.dead = False

    def update(self):
        self.y += self.dy               # 위로 이동
        self.alpha -= 6                 # 점점 투명해짐
        self.scale += self.scale_speed  # 약간 크게

        if self.alpha <= 0:
            self.dead = True

    def draw(self, surf):
        img = self.image.copy()
        img.set_alpha(self.alpha)

        w = int(img.get_width() * self.scale)
        h = int(img.get_height() * self.scale)

        img = pygame.transform.smoothscale(img, (w, h))
        rect = img.get_rect(center=(self.x, self.y))
        surf.blit(img, rect)

    def is_dead(self):
        return self.dead

# ---------------- 폭발 (종류별 이펙트) ----------------
class Explosion:
    def __init__(self, x, y, kind=None):
        self.x = x
        self.y = y
        self.kind = kind
        
        # 1단계(작은 폭발) 이미지 스케일 범위
        self.scale1_start = 0.01
        self.scale1_end   = 0.08

        # 2단계(가시 폭발) 이미지 스케일 범위
        self.scale2_start = self.scale1_end
        self.scale2_end   = 0.15

        self.stage = 0            # 0=이미지1, 1=이미지2
        self.timer = 0
        self.max_timer = 12       # 각 단계 프레임 수

        self.dead = False

    def update(self):
        self.timer += 1

        if self.stage == 0:
            # 1단계 스케일을 선형 보간
            t = self.timer / self.max_timer
            self.scale = self.scale1_start + (self.scale1_end - self.scale1_start) * t

            if self.timer >= self.max_timer:
                # 다음 이미지로 넘어가기
                self.stage = 1
                self.timer = 0

        else:
            # 2단계 스케일을 선형 보간
            t = self.timer / self.max_timer
            self.scale = self.scale2_start + (self.scale2_end - self.scale2_start) * t

            if self.timer >= self.max_timer:
                self.dead = True

    def draw(self, surf):
        if self.kind == "bad":
            if self.stage == 0:
                img = EXPLO_IMG_1
            else:
                img = EXPLO_IMG_2
    # 빨간 폭발
        elif self.kind == "penalty":
            if self.stage == 0:
                img = EXPLO_IMG_1
            else:
                img = EXPLO_IMG_2    # 파란 폭발 (원하면 따로 이미지 넣을 수도)
        else:
            if self.stage == 0:
                img = EXPLO_IMG_1
            else:
                img = EXPLO_IMG_2 
        
        w = int(img.get_width() * self.scale)
        h = int(img.get_height() * self.scale)

        scaled = pygame.transform.smoothscale(img, (w, h))
        rect = scaled.get_rect(center=(self.x, self.y))
        surf.blit(scaled, rect)

    def is_dead(self):
        return self.dead
    
    
# ---------------- 우산 그림 ----------------
def draw_umbrella(surface, cx, top_y):
    img = UMBRELLA_SCALED
    rect = img.get_rect(center=(WIDTH//2, HEIGHT-220))
    surface.blit(img, rect)
    return rect

# ---------------- 입 ----------------


# ---------------- 타이틀 화면 ----------------
def title_screen():
    pygame.mixer.music.load(BGM_TITLE)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    
    bg_img = pygame.image.load(os.path.join(ASSET_DIR, "BG.png")).convert()
    bg_img = pygame.transform.scale(bg_img, (1200, 900))

    title_img = pygame.image.load(os.path.join(ASSET_DIR, "TITLE.png")).convert_alpha()
    title_img = pygame.transform.scale(title_img, (800, 800))
    start_btn_img = pygame.image.load(os.path.join(ASSET_DIR, "START.png")).convert_alpha()
    start_btn_img = pygame.transform.smoothscale(start_btn_img, (250, 100))

    title_rect = title_img.get_rect(center=(WIDTH // 2, 350))
    start_btn_rect = start_btn_img.get_rect(center=(WIDTH // 2, 600))

    running = True
    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if e.type == pygame.KEYDOWN:
                running = False

            if e.type == pygame.MOUSEBUTTONDOWN:
                if start_btn_rect.collidepoint(e.pos):
                    running = False

        screen.blit(bg_img, (0, 0))
        screen.blit(title_img, title_rect)
        screen.blit(start_btn_img, start_btn_rect)

        pygame.display.flip()

# ---------------- 인트로 화면 ----------------

INTRO_SCENES = [
    ("intro_1.png", (700, 700), (600, 450)),   # (파일명, (가로,세로), (center_x, center_y))
    ("intro_2.png", (700, 700), (600, 450)),
    ("intro_3.png", (700, 700), (600, 450)),
    ("intro_4.png", (700, 700), (600, 450)),
    ("intro_5.png", (700, 700), (600, 450)),
    ("intro_6.png", (700, 700), (600, 450)),
    ("intro_7.png", (700, 700), (600, 450)),
    ("intro_8.png", (700, 700), (600, 450))
]

def intro_screen():
    pygame.mixer.music.fadeout(500)  # 0.5초간 부드럽게 페이드아웃
    pygame.mixer.music.load(BGM_INTRO)
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
    # 이미지 로드 (크기, 위치 정보는 INTRO_SCENES에서 가져옴)
    
    intro_imgs = []

    for filename, size, center in INTRO_SCENES:
        path = os.path.join(ASSET_DIR, filename)
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, size)  # 원하는 크기 설정
        rect = img.get_rect(center=center)             # 원하는 위치 설정
        intro_imgs.append((img, rect))

    idx = 0
    fade_alpha = 0
    fade_speed = 1.5

    running = True
    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # 클릭/키 입력 → 다음 이미지
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                idx += 1
                fade_alpha = 0
                if idx >= len(intro_imgs):
                    return  # 인트로 종료

        # 페이드 인 증가
        if fade_alpha < 255:
            fade_alpha = min(fade_alpha + fade_speed, 255)

        # 배경
        screen.fill((0, 0, 0))

        # 현재 이미지 그리기
        img, rect = intro_imgs[idx]
        temp = img.copy()
        temp.set_alpha(fade_alpha)
        screen.blit(temp, rect)

        pygame.display.flip()
        
# ---------------- 게임 방법 ----------------
COMIC = [
       ("게임 목표", ["나쁜 음식은 박살!",
                "좋은 음식은 보호!",
                "아이템을 활용해 살아남아보세요!"]),
]

def comic_screen():
    pygame.mixer.music.fadeout(500)
    idx = 0
    while idx < len(COMIC):
        title, lines = COMIC[idx]
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                idx += 1

        screen.fill((210,225,255))
        panel = pygame.Rect(80,120, WIDTH-160, HEIGHT-240)
        pygame.draw.rect(screen, (255,255,255), panel)
        pygame.draw.rect(screen, (80,80,120), panel, 3)

        draw_text(screen, title, font_large, (255,180,0), WIDTH//2, 60, center=True)

        y = panel.top + 40
        for line in lines:
            draw_text(screen, line, font_medium, (40,40,40), panel.left+30, y)
            y += 40

        draw_text(screen, "클릭 또는 키 입력 → 계속", font_small, (80,80,120), WIDTH//2, HEIGHT-40, center=True)
        pygame.display.flip()

# ---------------- 결과 화면 ----------------
def result_screen(total_cal, eaten_cal, penalty):
    success = total_cal >= TARGET_CAL

    # --------------------
    # (1) 현재 게임 화면 캡처
    # --------------------
    frozen_bg = screen.copy()  # 지금 게임 화면 그대로 캡처

    # 흐림 효과 대신 반투명 흰색 레이어 사용
    blur_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    blur_overlay.fill((255, 255, 255, 180))   # 180 정도면 적당히 뿌옇게 됨

    # --------------------
    # (2) 양피지 이미지 로드
    # --------------------
    paper_img = pygame.image.load(os.path.join(ASSET_DIR, "양피지.png")).convert_alpha()
    paper_img = pygame.transform.smoothscale(paper_img, (900, 900))
    paper_rect = paper_img.get_rect(center=(WIDTH//2, HEIGHT//2))

    # --------------------
    # (3) 몸 상태 문구
    # --------------------
    if eaten_cal < 1000:
        body_msg = ["너무 적게 먹었어요...", "에너지가 부족할 수 있어요!"]
    elif eaten_cal < 1500:
        body_msg = ["딱 적당한 한 끼였어요!", "건강한 식사예요!"]
    elif eaten_cal < 2000:
        body_msg = ["조금 많이 먹었어요.", "다음엔 양을 조금 줄여봐요!"]
    else:
        body_msg = ["꽤 과식했어요!", "자주 이러면 살이 찔 수 있어요!"]

    # --------------------
    # (4) BGM
    # --------------------
    
    #pygame.mixer.music.load(BGM_RESULT_HOW)
    #pygame.mixer.music.set_volume(0.5)
    #pygame.mixer.music.play(-1)

    running = True
    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                return success

        # (A) 멈춰있는 게임 화면 먼저 뿌리기
        screen.blit(frozen_bg, (0, 0))

        # (B) 화면을 살짝 흐리게(반투명 흰색 덮기)
        screen.blit(blur_overlay, (0, 0))

        # (C) 양피지 패널 그리기
        screen.blit(paper_img, paper_rect)

        # (D) 양피지 위에 결과 텍스트 적기
        title = "성공! 건강을 지켰어요!" if success else "실패... 나쁜 음식이 많았어요!"
        title_color = (80,180,120) if success else (200,60,60)

        draw_text(screen, title, font_large, title_color,
                  WIDTH//2, paper_rect.top + 200, center=True)

        draw_text(screen, f"박살낸 칼로리: {total_cal} kcal",
                  font_medium, (40,40,40),
                  WIDTH//2, paper_rect.top + 300, center=True)

        draw_text(screen, f"먹은 칼로리: {eaten_cal} kcal",
                  font_medium, (40,40,40),
                  WIDTH//2, paper_rect.top + 350, center=True)

        draw_text(screen, f"페널티: {penalty} 번",
                  font_medium, (40,40,40),
                  WIDTH//2, paper_rect.top + 400, center=True)

        y = paper_rect.top + 530
        for line in body_msg:
            draw_text(screen, line, font_semilarge, (60,60,100), WIDTH//2, y, center=True)
            y += 40

        draw_text(screen, "클릭 또는 키 입력 → 엔딩",
                  font_medium, (100,100,150),
                  WIDTH//2, paper_rect.bottom - 150, center=True)

        pygame.display.flip()

# ---------------- 엔딩 컷신 화면 ----------------
def ending_cutscene_screen(success):
    pygame.mixer.music.stop() 
    # 엔딩 이미지 선택
    if success:
        ending_img = pygame.image.load(os.path.join(ASSET_DIR, "Ending_Good_1.png")).convert_alpha()
        pygame.mixer.music.load(BGM_RESULT_GOOD)   # 있으면 적용
    else:
        ending_img = pygame.image.load(os.path.join(ASSET_DIR, "Ending_Bad_1.png")).convert_alpha()
        pygame.mixer.music.load(BGM_RESULT_BAD)    # 있으면 적용


    # BGM 시작
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

    fade = 0
    fade_speed = 3

    running = True
    while running:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                pygame.mixer.music.fadeout(500)
                return  # 엔딩 종료 → 메인으로

        # 배경
        screen.fill((240,240,255))

        # 페이드 인
        if fade < 255:
            fade = min(255, fade + fade_speed)

        temp = ending_img.copy()
        temp.set_alpha(fade)

        rect = temp.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(temp, rect)

        # 안내 문구
        draw_text(
            screen,
            "클릭 또는 키 입력 → 타이틀로",
            font_semilarge,
            (90,90,140),
            WIDTH//2,
            HEIGHT - 50,
            center=True
        )

        pygame.display.flip()

# ---------------- 게임 메인 루프 ----------------
def game_loop():
    pygame.mixer.music.stop() 
    foods = [create_food() for _ in range(10)]
    explosions = []
    popup_texts = []
    angel_effects = []
    
    pygame.mixer.music.load(BGM_GAME)
    pygame.mixer.music.set_volume(0.9)
    pygame.mixer.music.play(-1)

    total_bad_cal = 0  # 박살낸 칼로리
    eaten_cal = 0      # 먹은 칼로리
    penalty = 0        # 좋은 음식 때린 횟수

    mouth_open = 0.15
    chomp_timer = 0
    mood = "normal"

    level = 1
    next_level_score = [0, 200, 400, 600, 900, 1200, 1600,1800,2100,2500]
    level_up_timer = 0

    umbrella_timer = 0
    ultimate_timer = 0
    cheating_timer = 0
    
    swing_frame_timer = 0
    
    
    start_time = pygame.time.get_ticks()
    pygame.mouse.set_visible(False)
    running = True
    
    

    while running:
        dt = clock.tick(FPS)
        now = pygame.time.get_ticks()
        remain = max(0, GAME_TIME - (now - start_time))

        if remain <= 0:
            break

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = pygame.mouse.get_pos()
                swing_frame_timer = 150 
                # ────────────────────── 소리 재생 로직 시작 ──────────────────────
                if ultimate_timer > 0:
                    # 망치 모드 → 무거운 망치 소리
                    SOUND_HAMMER_SWING.play()
                else:
                    # 일반 상태 → 가벼운 휘익 소리
                    SOUND_SWING_NORMAL.play()

                # 망치 모드: 광역 타격 + 아이템도 획득
                if ultimate_timer > 0:
                    SOUND_HAMMER_HIT.play()
                    for food in foods:
                        dx = food["rect"].centerx - mx
                        dy = food["rect"].centery - my
                        if dx*dx + dy*dy <= (150*150):
                            if food["type"] == "item":
                                if food["item_type"] == "umbrella":
                                    umbrella_timer = 4000
                                    SOUND_ITEM.play()
                                elif food["item_type"] == "ultimate":
                                    ultimate_timer = 4000
                                    SOUND_ITEM.play()
                                elif food["item_type"] == "cheatingday":
                                    cheating_timer = 5000
                                    SOUND_ITEM.play()
                                    pygame.mixer.music.load(BGM_CHEATING)
                                    pygame.mixer.music.play(-1)
                                explosions.append(Explosion(food["rect"].centerx, food["rect"].centery, "bonus"))
                                popup_texts.append(PopupText(food["rect"].centerx, food["rect"].centery, "ITEM!", (255, 200, 0)))
                                food.update(create_food())
                                continue
                            
                            if food["type"] == "food":
                                if food["is_bad"]:
                                    total_bad_cal += food["cal"]
                                    explosions.append(Explosion(food["rect"].centerx, food["rect"].centery, "bad"))
                                    popup_texts.append(PopupText(food["rect"].centerx, food["rect"].centery, "GOOD!", (60, 150, 255)))
                                else:
                # ⭐ 치팅데이 판정 추가
                                    if cheating_timer > 0:
                                        total_bad_cal += 50
                                        popup_texts.append(PopupText(food["rect"].centerx, food["rect"].centery, "GOOD!", (255, 240, 120)))
                                        explosions.append(Explosion(food["rect"].centerx, food["rect"].centery, "bonus"))
                                    else:
                                        penalty += 1
                                        soul_img = SOUL_IMAGES.get(food["name"]) 

                                # 해당 음식의 영혼 이미지가 존재할 때만 이펙트 생성
                                        if soul_img:
                                            angel_effects.append(
                                                AngelEffect(
                                                    food["rect"].centerx,
                                                    food["rect"].centery,
                                                    soul_img
                                                )
                                            )
                                        SOUND_HIT_BAD.play()
                            food.update(create_food()) 
                            
                            
                    continue

                # 일반 모드
                for food in reversed(foods):
                    hitbox = food["rect"].inflate(40, 40)
                    if hitbox.collidepoint(mx, my):
                        if food["type"] == "item":
                            if food["item_type"] == "umbrella":
                                umbrella_timer = 4000
                                SOUND_ITEM.play()
                            elif food["item_type"] == "ultimate":
                                ultimate_timer = 4000
                                SOUND_ITEM.play()
                            elif food["item_type"] == "cheatingday":
                                cheating_timer = 5000
                                SOUND_ITEM.play()
                                pygame.mixer.music.load(BGM_CHEATING)
                                pygame.mixer.music.play(-1)
                            explosions.append(Explosion(food["rect"].centerx, food["rect"].centery, "bonus"))
                            popup_texts.append(PopupText(food["rect"].centerx, food["rect"].centery, "ITEM!", (255, 200, 0)))
                            food.update(create_food())
                            
                            

                        if food["is_bad"]:
                            total_bad_cal += food["cal"]
                            explosions.append(Explosion(food["rect"].centerx, food["rect"].centery, "bad"))
                            popup_texts.append(PopupText(food["rect"].centerx, food["rect"].centery, "GOOD!", (60, 150, 255)))
                            SOUND_HIT_BAD.play()
                            
                        else:
                            if cheating_timer > 0:
                                total_bad_cal += 50
                                explosions.append(Explosion(food["rect"].centerx, food["rect"].centery, "bonus"))
                                popup_texts.append(PopupText(food["rect"].centerx, food["rect"].centery, "GOOD!", (255, 240, 120)))
                  
                            else:
                                penalty += 1
                                soul_img = SOUL_IMAGES.get(food["name"])

                                # 해당 음식의 영혼 이미지가 존재할 때만 이펙트 생성
                                if soul_img:
                                    angel_effects.append(
                                        AngelEffect(
                                            food["rect"].centerx,
                                            food["rect"].centery,
                                            soul_img
                                        )
                                    )
                                    
                                popup_texts.append(PopupText(food["rect"].centerx, food["rect"].centery, "BAD!", (255, 60, 60)))
                                SOUND_HIT_BAD.play()
                        food.update(create_food())
                        break

        # 난이도 레벨업
        if level < 9 and total_bad_cal >= next_level_score[level]:
            level += 1
            level_up_timer = 1200
            SOUND_LEVELUP.play()
            for f in foods:
                f["speed"] *= 1.18

        
     # 우산 판정   
        umbrella_rect = None
        if umbrella_timer > 0:
            umbrella_rect = draw_umbrella(screen, 0, 0)
                
        # 음식 이동
        for food in foods:
            
            # 튕김 음식 처리
            if food["bounced"] >= 1:
                food["bounced"] += 1
                
                food["rect"].x += food["vx"]
                food["rect"].y += food["vy"]
                food["vy"] += 0.5
                food["angle"] += food["rotation_speed"]
                
                if food["bounced"] >= 20:     # 튕긴 후 몇 프레임 유지?
                    food.update(create_food())
                continue
            
            food["rect"].y += food["speed"]
            if food["type"] in ("food", "item"):
                food["angle"] += food["rotation_speed"]
                
            if umbrella_rect and food["type"] == "food" and food["is_bad"]:
            # 우산 이미지보다 약간 위쪽에서 튕기게 조정
                umbrella_hitbox = umbrella_rect.copy()
                umbrella_hitbox.bottom = min(umbrella_rect.bottom, HEIGHT)

            # 우산 충돌 지점을 아래쪽으로 20~40px 만큼 올려주기
                umbrella_hitbox.y = umbrella_hitbox.bottom - 400   # ← 이 값만 조절하면 끝
                umbrella_hitbox.height = 400

                if umbrella_hitbox.colliderect(food["rect"]):
                
            # 첫 충돌
                    food["bounced"] = 1 # 튕김 상태 진입
                    angle = math.radians(random.uniform(-160, -20))    # 위쪽 180도 범위 랜덤 각도
                    power = random.uniform(14.0, 22.0) # 기본 튕김 파워 (조절 가능)

                    # 방향 벡터로 나눔
                    food["vx"] = math.cos(angle) * power       # 좌우 튕김
                    food["vy"] = -abs(math.sin(angle) * power) # 위로 튕김
                    food["rotation_speed"] = random.uniform(8, 15) # 회전 강화
                    food["rect"].y -= 10 # 시작 시 약간 위로 밀어주기
                          
                    continue
                
        
            if food["rect"].bottom >= HEIGHT - 10:
                if umbrella_timer > 0:
                    explosions.append(Explosion(food["rect"].centerx, HEIGHT-90, "bad"))
                else:
                    chomp_timer = 200
                    mouth_open = 1.0
                    # 여기서 실제 먹은 칼로리 합산
                    if food["type"] == "food":
                        eaten_cal += food["cal"]


                food.update(create_food())
                continue
            
            
        if chomp_timer > 0:
            chomp_timer -= dt
    
            

        if umbrella_timer > 0: umbrella_timer -= dt
        if ultimate_timer > 0: ultimate_timer -= dt
        
        if cheating_timer > 0: 
            cheating_timer -= dt
            if cheating_timer <= 0:
                pygame.mixer.music.load(BGM_GAME)
                pygame.mixer.music.play(-1)
                
        if level_up_timer > 0: level_up_timer -= dt
        if swing_frame_timer > 0: swing_frame_timer -= dt

        for ex in explosions:
            ex.update()
        explosions[:] = [e for e in explosions if not e.is_dead()]
        
        for ae in angel_effects:
            ae.update()
        angel_effects[:] = [ae for ae in angel_effects if not ae.is_dead()]

        for p in popup_texts:
            p.update()
        popup_texts[:] = [p for p in popup_texts if not p.is_dead()]

        # -------- 그리기 --------
        screen.blit(GAME_BG, (0, 0))

        umbrella_rect = None
        if umbrella_timer > 0:
            umbrella_rect = draw_umbrella(screen, 0, 0)
    
        if cheating_timer > 0:
            tint = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            tint.fill((255,255,120,60))
            screen.blit(tint, (0,0))


        for food in foods:
            if food["type"] == "food":
                if food["image"] is not None:
                    rotated = pygame.transform.rotate(food["image"], food["angle"])
                    rot_rect = rotated.get_rect(center=food["rect"].center)
                    screen.blit(rotated, rot_rect)
                else:
                    pygame.draw.ellipse(screen, (200,200,200), food["rect"])
            else:
                img = ITEM_IMAGES[food["item_type"]]
                rotated = pygame.transform.rotate(img, food["angle"])
                rot_rect = rotated.get_rect(center=food["rect"].center)
                screen.blit(rotated, rot_rect)

        for ex in explosions:
            ex.draw(screen)
        
        for ae in angel_effects:
            ae.draw(screen)
            
        #--------UI 그리기------
        panel_bottom = draw_level_ui(screen, level)

        draw_note_ui(
            screen, panel_bottom,
            penalty, total_bad_cal, remain,
            umbrella_timer, ultimate_timer, cheating_timer)
        
        
        draw_timer_ui(screen, remain)

        if level_up_timer > 0:
            draw_text(screen, "★ LEVEL UP! ★", font_large, (255,180,0), WIDTH//2, 150, center=True)

        y_item = 200
        x_item = WIDTH - 200
        if umbrella_timer > 0:
            # 아이콘
            screen.blit(HUD_ICONS["umbrella"], (x_item, y_item))
            # 텍스트
            draw_text(screen, "우산 모드!", font_medium, (90,130,220),
                x_item + ICON_SIZE + 8, y_item + 4)
            y_item += ICON_SIZE + 6

        if ultimate_timer > 0:
            screen.blit(HUD_ICONS["ultimate"], (x_item, y_item))
            draw_text(screen, "필살기 모드!", font_medium, (220,100,100),
                x_item + ICON_SIZE + 8, y_item + 4)
            y_item += ICON_SIZE + 6

        if cheating_timer > 0:
            screen.blit(HUD_ICONS["cheatingday"], (x_item, y_item))
            draw_text(screen, "치팅데이!", font_medium, (220,190,0),
                x_item + ICON_SIZE + 8, y_item + 4)

        mx, my = pygame.mouse.get_pos()
        if ultimate_timer > 0:
            if swing_frame_timer > 0:
                impact_x = mx -110
                impact_y = my 
                img = MC_ULT_SWING   # ★ 도깨비방망이 스윙 이미지
                shock_rect = SHOCK_IMG.get_rect(center=(impact_x, impact_y))
                screen.blit(SHOCK_IMG, shock_rect)
            else:
                img = MC_ULT_IDLE   # ★ 도깨비방망이 대기 이미지
        else:
            if swing_frame_timer > 0:
                img = SWING_IMG       # ★ 기본 스윙 이미지
            else:
                img = IDLE_IMG        # ★ 기본 대기 이미지 

        rect = img.get_rect(center=(mx, my))    
        screen.blit(img, rect)

        for p in popup_texts:
            p.draw(screen)

        pygame.display.flip()

    pygame.mouse.set_visible(True)
    pygame.mixer.music.fadeout(300)
    return total_bad_cal, eaten_cal, penalty

# ---------------- 메인 ----------------
def main():
    while True:
        title_screen()
        intro_screen()
        comic_screen()
        total_cal, eaten_cal, penalty = game_loop()
        success = result_screen(total_cal, eaten_cal, penalty)
        ending_cutscene_screen(success)

if __name__ == "__main__":
    main()
