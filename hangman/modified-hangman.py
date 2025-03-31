import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 800, 500
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game!")

# button variables
RADIUS = 20
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)
BUTTON_FONT = pygame.font.SysFont('comicsans', 50)

# load images.
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# game variables
words = ["IDE", "REPLIT", "PYTHON", "PYGAME"]
max_mistakes = 3  # Default difficulty
hint_used = False  # Track if the hint has been used

def draw():
    win.fill(WHITE)
    # draw title
    text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # draw word
    display_word = "".join([letter + " " if letter in guessed else "_ " for letter in word])
    text = WORD_FONT.render(display_word, 1, BLACK)
    win.blit(text, (400, 200))

    # draw buttons
    for x, y, ltr, visible in letters:
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, BLACK)
            win.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
    
    win.blit(images[hangman_status], (150, 100))

    # draw the hint button (now at middle-left side, only if not used)
    if not hint_used:
        hint_button = pygame.Rect(50, HEIGHT / 2 - 25, 120, 50)  # Positioned at middle-left
        pygame.draw.rect(win, (0, 0, 255), hint_button)  # Blue color for Hint
        hint_text = BUTTON_FONT.render("Hint", 1, BLACK)
        win.blit(hint_text, (hint_button.x + (hint_button.width - hint_text.get_width()) // 2,
                             hint_button.y + (hint_button.height - hint_text.get_height()) // 2))

    pygame.display.update()

def display_message(message):
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - 100))

    restart_button = pygame.Rect(250, 300, 150, 50)
    quit_button = pygame.Rect(450, 300, 150, 50)
    hint_button = pygame.Rect(50, HEIGHT / 2 - 25, 120, 50)  # Positioned at middle-left

    pygame.draw.rect(win, GREEN, restart_button)
    pygame.draw.rect(win, RED, quit_button)

    restart_text = BUTTON_FONT.render("Restart", 1, BLACK)
    quit_text = BUTTON_FONT.render("Quit", 1, BLACK)

    win.blit(restart_text, (restart_button.x + (restart_button.width - restart_text.get_width()) // 2,
                            restart_button.y + (restart_button.height - restart_text.get_height()) // 2))
    win.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2,
                         quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

    # Draw the hint button (now at middle-left side, only if not used)
    if not hint_used:
        pygame.draw.rect(win, (0, 0, 255), hint_button)  # Blue color for Hint
        hint_text = BUTTON_FONT.render("Hint", 1, BLACK)
        win.blit(hint_text, (hint_button.x + (hint_button.width - hint_text.get_width()) // 2,
                             hint_button.y + (hint_button.height - hint_text.get_height()) // 2))

    pygame.display.update()
    return restart_button, quit_button, hint_button

def main():
    global hangman_status, guessed, word, letters, hint_used
    hangman_status = 0
    guessed = []
    word = random.choice(words)
    for letter in letters:
        letter[3] = True  # Reset letter visibility
    hint_used = False  # Reset hint usage when starting a new game
    
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible and math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2) < RADIUS:
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            global max_mistakes
                            hangman_status += 1
                
                # Check if hint button is clicked
                hint_button = pygame.Rect(50, HEIGHT / 2 - 25, 120, 50)  # Positioned at middle-left
                if hint_button.collidepoint(m_x, m_y) and not hint_used:
                    hint_used = True
                    display_hint()

        draw()

        if all(letter in guessed for letter in word):
            restart_button, quit_button, _ = display_message("You WON!")
            return handle_end_screen(restart_button, quit_button)

        if hangman_status >= max_mistakes:
            restart_button, quit_button, _ = display_message("You LOST!")
            return handle_end_screen(restart_button, quit_button)

def handle_end_screen(restart_button, quit_button):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(pygame.mouse.get_pos()):
                    return True
                if quit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    return False

def display_hint():
    # Provide a hint by showing one letter
    for letter in word:
        if letter not in guessed:
            guessed.append(letter)
            break

def difficulty_screen():
    global max_mistakes
    win.fill(WHITE)
    text = TITLE_FONT.render("Choose Difficulty", 1, BLACK)
    win.blit(text, (WIDTH / 2 - text.get_width() / 2, 100))

    easy_button = pygame.Rect(250, 250, 150, 50)
    hard_button = pygame.Rect(450, 250, 150, 50)

    pygame.draw.rect(win, GREEN, easy_button)
    pygame.draw.rect(win, RED, hard_button)

    easy_text = BUTTON_FONT.render("Easy", 1, BLACK)
    hard_text = BUTTON_FONT.render("Hard", 1, BLACK)

    win.blit(easy_text, (easy_button.x + (easy_button.width - easy_text.get_width()) // 2,
                         easy_button.y + (easy_button.height - easy_text.get_height()) // 2))
    win.blit(hard_text, (hard_button.x + (hard_button.width - hard_text.get_width()) // 2,
                         hard_button.y + (hard_button.height - hard_text.get_height()) // 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.collidepoint(pygame.mouse.get_pos()):
                    max_mistakes = 5
                    return True
                if hard_button.collidepoint(pygame.mouse.get_pos()):
                    max_mistakes = 3
                    return True

while True:
    if not difficulty_screen():
        break
    if not main():
        break
