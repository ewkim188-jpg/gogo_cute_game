import pygame
import random
import sys
import time

pygame.init()
pygame.mixer.init()

# ---------------- 화면 설정 ----------------
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🍭 귀여운 음식 잡기 게임 🍭")

clock = pygame.time.Clock()
font = pygame.font.SysFont("malgungothic", 36)
big_font = pygame.font.SysFont("malgungothic", 72)

# ---------------- 색상 ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ---------------- 이미지 & 사운드 ----------------
# ⚠️ 아래 경로에 이미지와 사운드를 넣어주세요!
# 각 파일명은 자유롭게 바꾸셔도 됩니다.

# 배경 이미지 (없으면 기본 흰색)
try:
    background_img = pygame.image.load("background.png").convert()
except:
    background_img = None

# 입 이미지 (열림, 닫힘)
try:
    mouth_open_img = pygame.image.load("mouth_open.png").convert_alpha()
    mouth_close_img = pygame.image.load("mouth_close.png").convert_alpha()
except:
    mouth_open_img = mouth_close_img = None

# 음식 이미지들
try:
    food_images = {
        "red": pygame.image.load("food_red.png"),
        "yellow": pygame.image.load("food_yellow.png"),
        "blue": pygame.image.load("food_blue.png"),
        "green": pygame.image.load("food_green.png"),
    }
except:
    food_images = None

# 효과음
try:
    catch_sound = pygame.mixer.Sound("catch.wav")
except:
    catch_sound = None

# ---------------- 음식 종류 ----------------
foods = [
    {"type": "pass", "name": "red"},
    {"type": "pass", "name": "yellow"},
    {"type": "catch", "name": "blue"},
    {"type": "catch", "name": "green"},
]

# ---------------- 함수들 ----------------

def draw_background():
    if background_img:
        screen.blit(pygame.transform.scale(background_img, (WIDTH, HEIGHT)), (0, 0))
    else:
        screen.fill(WHITE)

def draw_food(food):
    x, y = food["x"], food["y"]
    if food_images:
        img = food_images[food["name"]]
        screen.blit(img, (x - img.get_width()//2, y - img.get_height()//2))
    else:
        # 이미지 없을 시 기본 원 표시
        colors = {"red": (255, 100, 100), "yellow": (255, 255, 150),
                  "blue": (100, 150, 255), "green": (100, 255, 150)}
        pygame.draw.circle(screen, colors[food["name"]], (x, y), 20)

def draw_mouth(opened=True):
    if mouth_open_img and mouth_close_img:
        img = mouth_open_img if opened else mouth_close_img
        screen.blit(img, (WIDTH//2 - img.get_width()//2, HEIGHT - 120))
    else:
        if opened:
            pygame.draw.arc(screen, BLACK, (WIDTH//2-100, HEIGHT-100, 200, 100), 0, 3.14, 8)
        else:
            pygame.draw.line(screen, BLACK, (WIDTH//2-100, HEIGHT-50), (WIDTH//2+100, HEIGHT-50), 8)

def draw_button(text, x, y, w, h):
    pygame.draw.rect(screen, BLACK, (x, y, w, h), 3)
    label = font.render(text, True, BLACK)
    screen.blit(label, (x + (w - label.get_width())//2, y + (h - label.get_height())//2))
    return pygame.Rect(x, y, w, h)

def create_food():
    f = random.choice(foods)
    return {"x": random.randint(50, WIDTH-50), "y": 0, "type": f["type"], "name": f["name"], "vy": random.randint(4, 7)}

# ---------------- 시작 화면 ----------------
def start_screen():
    while True:
        draw_background()
        title = big_font.render("🍓 귀여운 음식 잡기 🍓", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))

        guide1 = font.render("사과, 계란 = 통과!", True, BLACK)
        guide2 = font.render("치킨, 라면 = 클릭으로 잡기!", True, BLACK)
        screen.blit(guide1, (WIDTH//2 - guide1.get_width()//2, 280))
        screen.blit(guide2, (WIDTH//2 - guide2.get_width()//2, 330))

        # 음식 미리보기
        for i, name in enumerate(["red", "yellow", "blue", "green"]):
            x = WIDTH//2 - 180 + i * 120
            if food_images:
                img = food_images[name]
                screen.blit(img, (x - img.get_width()//2, 420))
            else:
                draw_food({"x": x, "y": 440, "name": name, "type": "pass" if i < 2 else "catch"})

        start_btn = draw_button("게임 시작", WIDTH//2 - 100, 520, 200, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(30)

# ---------------- 결과 화면 ----------------
def result_screen(stats):
    while True:
        draw_background()
        title = big_font.render("🎉 게임 종료! 🎉", True, BLACK)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))

        results = [
            f"잡은 치킨: {stats['blue']}개",
            f"잡은 라면: {stats['green']}개",
            f"통과한 사과: {stats['red']}개",
            f"통과한 계란: {stats['yellow']}개"
        ]

        for i, line in enumerate(results):
            txt = font.render(line, True, BLACK)
            screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 250 + i*50))

        restart_btn = draw_button("다시 시작", WIDTH//2 - 100, 520, 200, 60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(30)

# ---------------- 게임 본체 ----------------
def game():
    start_time = time.time()
    foods_list = []
    stats = {"red": 0, "yellow": 0, "blue": 0, "green": 0}
    score = 0
    fall_speed = 5
    mouth_open = True
    score_popups = []  # "+1" 표시용 리스트

    while True:
        elapsed = time.time() - start_time
        if elapsed > 30:
            break

        draw_background()

        # 음식 생성
        if random.random() < 0.03:
            foods_list.append(create_food())

        # 음식 이동 및 그리기
        for food in foods_list[:]:
            food["y"] += food["vy"]

            # 입에 닿으면 제거
            if food["y"] >= HEIGHT - 100:
                mouth_open = not mouth_open
                if food["type"] == "pass":
                    stats[food["name"]] += 1
                foods_list.remove(food)
            else:
                draw_food(food)

        # 클릭 이벤트
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for food in foods_list[:]:
                    if (food["x"] - mx)**2 + (food["y"] - my)**2 < 30**2:
                        if food["type"] == "catch":
                            score += 1
                            stats[food["name"]] += 1
                            if catch_sound: catch_sound.play()
                            score_popups.append({"x": mx, "y": my, "timer": 30})
                            foods_list.remove(food)

        # "+1" 표시
        for popup in score_popups[:]:
            label = font.render("+1", True, (255, 100, 150))
            screen.blit(label, (popup["x"], popup["y"]))
            popup["y"] -= 1
            popup["timer"] -= 1
            if popup["timer"] <= 0:
                score_popups.remove(popup)

        # 입 그리기
        draw_mouth(mouth_open)

        # 점수 & 시간 표시
        time_left = max(0, int(30 - elapsed))
        score_text = font.render(f"점수: {score}", True, BLACK)
        time_text = font.render(f"남은 시간: {time_left}s", True, BLACK)
        screen.blit(score_text, (20, 20))
        screen.blit(time_text, (20, 60))

        pygame.display.flip()
        clock.tick(30)

    result_screen(stats)


# ---------------- 메인 루프 ----------------
while True:
    start_screen()
    game()
