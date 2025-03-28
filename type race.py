import copy
import pygame
import random
pygame.init()

from nltk.corpus import words
wordlist = words.words()
len_indexes = []
length = 1

wordlist.sort(key=len)
for i in range(len(wordlist)):
    if len(wordlist[i]) > length:
        length += 1
        len_indexes.append(i)
len_indexes.append(len(wordlist))
print(len_indexes)
        

WIDTH = 800
HEIGHT = 600
screen =  pygame.display.set_mode([WIDTH,HEIGHT])
pygame.display.set_caption('Typing Racing!!⌨️')
surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
timer = pygame.time.Clock()
fps = 60

level = 1
active_string = ''
score = 0
#high_score = 1
lives = 5
paused = True
submit = ''
word_objects = []
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 
                     'p', 'q','r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

new_level = True
choices = [False, True, False, False, False, False, False]
header_font = pygame.font.Font('fonts/Square.ttf', 50)
pause_font = pygame.font.Font('fonts/1up.ttf', 38)
banner_font = pygame.font.Font('fonts/1up.ttf', 28)
font = pygame.font.Font('fonts/AldotheApache.ttf', 48)

pygame.mixer.init()
pygame.mixer.music.load("assets music/Sakura-Girl-Daisy-chosic.com_.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)
click = pygame.mixer.Sound("assets music/click.mp3")
woosh = pygame.mixer.Sound("assets music/correct-6033.mp3")
wrong = pygame.mixer.Sound("assets music/Instrument Strum.mp3")
click.set_volume(0.4)
woosh.set_volume(0.4)
wrong.set_volume(0.4)

file = open('high_score.txt', 'r')
read = file.readlines()
high_score = int(read[0])
file.close()

class Word:
     def __init__(self, text, speed, y_pos, x_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.speed = speed
    
     def draw(self):
         color = 'black'
         screen.blit(font.render(self.text, True, color), (self.x_pos, self.y_pos))
         act_len = len(active_string)
         if active_string == self.text[:act_len]:
             screen.blit(font.render(active_string, True, 'green'), (self.x_pos, self.y_pos))
        
     def update(self):
         self.x_pos -= self.speed



class Button:
    def __init__(self, x_pos, y_pos, text, clicked, surf):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text = text
        self.clicked = clicked
        self.surf = surf

    def draw(self):
        cir = pygame.draw.circle(self.surf, (45, 89, 135), (self.x_pos, self.y_pos), 35)
        if cir.collidepoint(pygame.mouse.get_pos()):
            butts = pygame.mouse.get_pressed()
            if butts[0]:
                pygame.draw.circle(self.surf, (190, 35, 35), (self.x_pos, self.y_pos), 35)
                self.clicked = True
            else:
                pygame.draw.circle(self.surf, (190, 89, 135), (self.x_pos, self.y_pos), 35)     
        pygame.draw.circle(self.surf, 'white', (self.x_pos, self.y_pos), 35, 3)
        self.surf.blit(pause_font.render(self.text, True, 'white'), (self.x_pos - 15, self.y_pos - 25))
        
                
def draw_screen():
    pygame.draw.rect(screen, (32, 42, 68), [0, HEIGHT - 100, WIDTH, 100])
    pygame.draw.rect(screen, 'black', [0,0, WIDTH, HEIGHT],5)
    pygame.draw.line(screen, 'white',(250, HEIGHT - 100), (250, HEIGHT), 2)
    pygame.draw.line(screen, 'white',(700, HEIGHT - 100), (700, HEIGHT), 2)
    pygame.draw.line(screen, 'white',(0, HEIGHT - 100), (WIDTH, HEIGHT - 100), 2)
    pygame.draw.rect(screen, 'white', [0,0, WIDTH, HEIGHT],2)
    
    screen.blit(header_font.render(f'Level: {level}', True,'white'), (10, HEIGHT - 75))
    screen.blit(header_font.render(f'"{active_string}"', True,'white'), (270, HEIGHT - 75))
    
    pause_btn = Button(748, HEIGHT - 52, 'II', False, screen)
    pause_btn.draw()
    
    screen.blit(banner_font.render(f'Score: {score}', True,'black'), (250, 10))
    screen.blit(banner_font.render(f'Best: {high_score}', True,'black'), (550, 10))
    screen.blit(banner_font.render(f'Lives: {lives}', True,'black'), (10, 10))
    return pause_btn.clicked

def draw_pause():
    choice_commits = copy.deepcopy(choices)
    surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(surface, (0, 0, 0, 100), [100, 100, 600, 300], 0, 5)
    pygame.draw.rect(surface, (0, 0, 0, 200), [100, 100, 600, 300], 5, 5)
    resume_btn = Button(160, 200, '>', False, surface)
    resume_btn.draw()
    quit_btn = Button(410, 200, 'X', False, surface)
    quit_btn.draw()
    
    surface.blit(header_font.render('MENU', True, 'white'), (110, 110))
    surface.blit(header_font.render('PLAY!', True, 'white'), (210, 175))
    surface.blit(header_font.render('QUIT', True, 'white'), (450, 175))
    surface.blit(header_font.render('Active Letter Lengths:', True, 'white'), (110, 250))
    
    for i in range(len(choices)):
        btn = Button(160 + (i*80), 350, str(i+2), False, surface)
        btn.draw()
        if btn.clicked:
            if choice_commits[i]:
                choice_commits[i] = False
            else:
                choice_commits[i] = True
        if choices[i]:
            pygame.draw.circle(surface, 'green', (160 + (i * 80), 350), 35, 5)
                    
    screen.blit(surface, (0, 0))
    return resume_btn.clicked, choice_commits, quit_btn.clicked

def check_answer(scor):
    for wrd in word_objects:
        if wrd.text == submit:
            points = wrd.speed * len(wrd.text) * 10 * (len(wrd.text) /4)
            scor += int(points)
            word_objects.remove(wrd)
            woosh.play()
    return scor
    
def generate_level():
    word_objs = []
    include = []
    vertical_spacing = (HEIGHT - 150) // level
    if True not in choices:
        choices[0] = True
    for i in range(len(choices)):
        if choices[i]:
            include.append((len_indexes[i], len_indexes[i+1]))
    for i in range(level):
        speed = random.randint(2, 3)
        y_pos = random.randint(10 + (i * vertical_spacing), (i+1) * vertical_spacing)
        x_pos = random.randint(WIDTH, WIDTH + 1000)
        ind_sel = random.choice(include)
        index = random.randint(ind_sel[0], ind_sel[1])
        text = wordlist[index].lower()
        new_word = Word(text, speed, y_pos, x_pos)
        word_objs.append(new_word) 
    return word_objs

def check_high_score():
    global high_score
    if score > high_score:
        high_score = score
        file = open('high_score.txt', 'w')
        file.write(str(int(high_score)))
        file.close()

   
run = True
while run:
    screen.fill('light blue')
    timer.tick(fps)
    pause_butt = draw_screen()
    if paused:
        resume_butt, changes, quit_butt = draw_pause()
        if resume_butt:
            paused = False
        if quit_butt:
            check_high_score()
            run = False
    elif new_level and not paused:
        word_objects = generate_level()
        new_level = False 
    else:
        for w in word_objects:
            w.draw()
            if not paused:
                w.update()
            if w.x_pos < -200:
                word_objects.remove(w)
                lives -= 1   
    if len(word_objects) <= 0 and not paused:
        level += 1
        new_level = True
    
    if submit != '':
        init = score
        score = check_answer(score)
        submit = ''
        if init == score:
            wrong.play()
            pass
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check_high_score()
            run = False
        
        if event.type == pygame.KEYDOWN:
            if not paused:
                if event.unicode.lower() in letters:
                    active_string += event.unicode.lower()
                    click.play()
                if event.key == pygame.K_BACKSPACE and len(active_string) > 0:
                    active_string = active_string[:-1]
                    click.play()
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    submit = active_string
                    active_string = ''
            if event.key == pygame.K_ESCAPE:
                if paused:
                    paused = False
                else:
                    paused = True 
        if event.type == pygame.MOUSEBUTTONUP and paused:
            if event.button == 1:
                choices = changes
                           

    if pause_butt:
        paused = True
    
        
    if lives < 0:
        paused = True
        level = 1
        lives = 5
        word_objects = []
        new_level = True
        check_high_score()
        score = 0
            
                                 
    pygame.display.flip()
pygame.quit()    
