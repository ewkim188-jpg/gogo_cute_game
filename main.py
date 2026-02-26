import pygame
import random
import sys
import time
import asyncio

async def main():
    pygame.init()
    pygame.mixer.init()

    # --- Screen Setup ---
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Cute Food Catching Game")

    clock = pygame.time.Clock()
    
    # Use default fonts for better web compatibility
    font = pygame.font.SysFont("Arial", 36)
    big_font = pygame.font.SysFont("Arial", 72)

    # --- Colors ---
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # --- Assets ---
    try:
        background_img = pygame.image.load("background.png").convert()
    except:
        background_img = None

    try:
        mouth_open_img = pygame.image.load("mouth_open.png").convert_alpha()
        mouth_close_img = pygame.image.load("mouth_close.png").convert_alpha()
    except:
        mouth_open_img = mouth_close_img = None

    try:
        food_images = {
            "red": pygame.image.load("food_red.png"),
            "yellow": pygame.image.load("food_yellow.png"),
            "blue": pygame.image.load("food_blue.png"),
            "green": pygame.image.load("food_green.png"),
        }
    except:
        food_images = None

    try:
        catch_sound = pygame.mixer.Sound("catch.wav")
    except:
        catch_sound = None

    # --- Food Types ---
    foods = [
        {"type": "pass", "name": "red"},
        {"type": "pass", "name": "yellow"},
        {"type": "catch", "name": "blue"},
        {"type": "catch", "name": "green"},
    ]

    # --- Helpers ---
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
            colors = {"red": (255, 100, 100), "yellow": (255, 255, 150),
                      "blue": (100, 150, 255), "green": (100, 255, 150)}
            pygame.draw.circle(screen, colors[food["name"]], (x, y), 20)

    def draw_mouth(opened=True):
        if mouth_open_img and mouth_close_img:
            img = mouth_open_img if opened else mouth_close_img
            screen.blit(img, (WIDTH//2 - img.get_width()//2, HEIGHT - 150))
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

    # --- Game State ---
    state = "START"
    stats = {"red": 0, "yellow": 0, "blue": 0, "green": 0}
    score = 0
    start_time = 0
    foods_list = []
    score_popups = []
    mouth_open = True

    while True:
        draw_background()
        
        if state == "START":
            title = big_font.render("Cute Food Catching", True, BLACK)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 120))
            guide1 = font.render("Apple, Egg = Let Pass", True, BLACK)
            guide2 = font.render("Chicken, Ramen = Click!", True, BLACK)
            screen.blit(guide1, (WIDTH//2 - guide1.get_width()//2, 280))
            screen.blit(guide2, (WIDTH//2 - guide2.get_width()//2, 330))
            
            if food_images:
                for i, name in enumerate(["red", "yellow", "blue", "green"]):
                    x = WIDTH//2 - 180 + i * 120
                    img = food_images[name]
                    screen.blit(img, (x - img.get_width()//2, 420))
            
            start_btn = draw_button("START GAME", WIDTH//2 - 100, 520, 200, 60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_btn.collidepoint(event.pos):
                        state = "PLAYING"
                        start_time = time.time()
                        foods_list = []
                        score = 0
                        stats = {"red": 0, "yellow": 0, "blue": 0, "green": 0}

        elif state == "PLAYING":
            elapsed = time.time() - start_time
            if elapsed > 30:
                state = "RESULT"
                continue

            if random.random() < 0.05:
                foods_list.append(create_food())

            for food in foods_list[:]:
                food["y"] += food["vy"]
                if food["y"] >= HEIGHT - 100:
                    mouth_open = not mouth_open
                    if food["type"] == "pass":
                        stats[food["name"]] += 1
                    foods_list.remove(food)
                else:
                    draw_food(food)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos
                    for food in foods_list[:]:
                        if (food["x"] - mx)**2 + (food["y"] - my)**2 < 40**2:
                            if food["type"] == "catch":
                                score += 1
                                stats[food["name"]] += 1
                                if catch_sound: catch_sound.play()
                                score_popups.append({"x": mx, "y": my, "timer": 20})
                                foods_list.remove(food)

            for popup in score_popups[:]:
                lbl = font.render("+1", True, (255, 100, 150))
                screen.blit(lbl, (popup["x"], popup["y"]))
                popup["y"] -= 2
                popup["timer"] -= 1
                if popup["timer"] <= 0: score_popups.remove(popup)

            draw_mouth(mouth_open)
            time_left = max(0, int(30 - elapsed))
            screen.blit(font.render(f"Score: {score}", True, BLACK), (20, 20))
            screen.blit(font.render(f"Time: {time_left}s", True, BLACK), (20, 60))

        elif state == "RESULT":
            title = big_font.render("Game Over!", True, BLACK)
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            res = [f"Chickens: {stats['blue']}", f"Ramen: {stats['green']}",
                   f"Apples: {stats['red']}", f"Eggs: {stats['yellow']}"]
            for i, line in enumerate(res):
                txt = font.render(line, True, BLACK)
                screen.blit(txt, (WIDTH//2 - txt.get_width()//2, 220 + i*40))
            
            restart_btn = draw_button("RESTART", WIDTH//2 - 100, 500, 200, 60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_btn.collidepoint(event.pos):
                        state = "START"

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

asyncio.run(main())
