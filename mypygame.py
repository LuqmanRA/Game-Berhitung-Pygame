import pygame
import random

pygame.init()

pygame.mixer.init()

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (235, 54, 13)

# Lebar dan Tinggi Layar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Berhitung")

# Icon
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

# Background
background = pygame.image.load('assets/background.png')

# Font
font = pygame.font.Font(None, 36)

# Muat backsound
backsound = pygame.mixer.Sound('assets/backsound.mp3')

# Putar backsound secara terus-menerus (-1 untuk putar secara terus-menerus)
backsound.play(-1)

# Atur volume backsound (misalnya setengah dari volume maksimum)
backsound.set_volume(0.1)

# Muat efek suara 
sound_effect_correct = pygame.mixer.Sound('assets/sound-correct.mp3')
sound_effect_wrong = pygame.mixer.Sound('assets/sound-wrong.mp3')
sound_effect_lose = pygame.mixer.Sound('assets/sound-lose.mp3')
sound_effect_win = pygame.mixer.Sound('assets/sound-win.mp3')

# Fungsi untuk memainkan efek suara
def play_correct_sound():
    sound_effect_correct.play()

def play_win_sound():
    sound_effect_win.play()

def play_wrong_sound(volume):
    sound_effect_wrong.set_volume(volume)
    sound_effect_wrong.play()

def play_lose_sound(volume):
    sound_effect_lose.set_volume(volume)
    sound_effect_lose.play()

# Fungsi untuk membuat soal matematika acak
def level_1():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 5)
    operator = random.choice(['+', '-'])
    question = f"{num1} {operator} {num2}"
    answer = str(eval(question))
    return question, answer

def level_2():
    num1 = random.randint(10, 20)
    num2 = random.randint(1, 10)
    operator = random.choice(['+', '-'])
    question = f"{num1} {operator} {num2}"
    answer = str(eval(question))
    return question, answer

def level_3():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 5)
    operator = random.choice(['*'])
    question = f"{num1} {operator} {num2}"
    answer = str(eval(question))
    return question, answer

def level_4():
    num1 = random.randint(5, 10)
    num2 = random.randint(5, 10)
    operator = random.choice(['*'])
    question = f"{num1} {operator} {num2}"
    answer = str(eval(question))
    return question, answer

# Fungsi untuk menampilkan teks di layar
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Fungsi utama game
def main():
    running = True
    clock = pygame.time.Clock()
    
    score = 0
    max_attempts = 3
    question, correct_answer = level_1()
    user_answer = ''
    input_active = True
    timer = 30  # Waktu dalam detik
    countdown_timer = pygame.USEREVENT + 1  # Event kustom untuk pengurangan waktu
    pygame.time.set_timer(countdown_timer, 1000)  # Atur timer pengurangan waktu setiap 1 detik

    while running:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == countdown_timer:
                timer -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Cek jawaban ketika pemain menekan Enter
                    if user_answer == correct_answer:
                        score += 1
                        if (score < 50):
                            play_correct_sound()
                        if (score >= 0 and score <= 10):
                            question, correct_answer = level_1()
                        if (score > 10 and score <= 20):
                            question, correct_answer = level_2()
                        if (score > 20 and score <= 30):
                            question, correct_answer = level_3()
                        if (score > 30):
                            question, correct_answer = level_4()
                        user_answer = ''
                        if (timer > 25):
                            timer = 30
                        if (timer <= 25):
                            timer += 5
                    else:
                        if (max_attempts > 1):
                            play_wrong_sound(0.3)
                        if (score >= 0 and score <= 10):
                            question, correct_answer = level_1()
                        if (score > 10 and score <= 20):
                            question, correct_answer = level_2()
                        if (score > 20 and score <= 30):
                            question, correct_answer = level_3()
                        if (score > 30):
                            question, correct_answer = level_4()
                        max_attempts -= 1
                        timer -= 5
                        if max_attempts == 0:
                            running = False
                        else:
                            user_answer = ''
                elif event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]
                else:
                    if input_active:
                        user_answer += event.unicode

        if max_attempts == 0 or timer <= 0:
            backsound.stop()
            play_lose_sound(1.0)
            screen.blit(background, (0, 0))
            draw_text("Game Berakhir! Skor Anda: " + str(score), font, WHITE, screen, 225, 280)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        if score == 50:
            backsound.stop()
            play_win_sound()
            screen.blit(background, (0, 0))
            draw_text("Selamat Anda Menang!", font, WHITE, screen, 250, 280)
            pygame.display.flip()
            pygame.time.wait(2000)
            if (pygame.time.wait(2000)):
                screen.blit(background, (0, 0))
                draw_text("Game Berakhir! Skor Anda: " + str(score), font, WHITE, screen, 225, 280)
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False

        draw_text("Skor: " + str(score), font, WHITE, screen, 150, 200)
        draw_text("Sisa Kesalahan: " + str(max_attempts), font, RED, screen, 150, 225)
        draw_text(user_answer, font, RED, screen, 415, 300)
        draw_text(question, font, WHITE, screen, 300, 300)
        draw_text(" = ", font, WHITE, screen, 375, 300)
        if(timer > 10):
            draw_text(f"Waktu: {timer}", font, BLACK, screen, 600, 20)
        if(timer <= 10):
            draw_text(f"Waktu: ", font, BLACK, screen, 600, 20)
            draw_text(f"             " + str(timer), font, RED, screen, 600, 20)
        # Gambar garis (x1, y1) hingga (x2, y2)
        pygame.draw.line(screen, WHITE, (413, 320), (453, 320), 2)  # (x1, y1) dan (x2, y2) dengan ketebalan garis 3 pixel

        pygame.display.flip()
        clock.tick(60)

    backsound.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
