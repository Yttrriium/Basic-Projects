import pygame
from pygame import mixer
import os
import time
import vlc

pygame.init()
mixer.init()

#Display settings
W, H = 1000, 500
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("Drink Water")
pygame.display.set_icon(pygame.image.load(os.path.join('gow.ico')))
FPS = 60

#Colors
LBLUE = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (211, 211, 211)
RED = (255, 0, 0)
color = GREY

#Text and fonts
font = pygame.font.SysFont('SCHLBKI.ttf', 64)
font2 = pygame.font.SysFont('SCHLBKI.ttf', 50)
font3 = pygame.font.SysFont('SCHLBKI.ttf', 45)

#Title 
text = font.render('Drink your water!', True, WHITE, LBLUE)
textRect = text.get_rect()
textRect.center = (W/2, 100)

#Input Field
ques = font2.render('How many glasses of water did you drink until now?', True, WHITE)
quesRect = ques.get_rect()
quesRect.center = (500, 200)

#Alarm
media = vlc.MediaPlayer('song.mp4')
al = font.render('Time to drink you water!', True, WHITE)
stop = font2.render('STOP', True, LBLUE)
snooze = font2.render('SNOOZE', True, LBLUE)
alRect = pygame.Rect(240, 372, 300, 50)
inp_rect = pygame.Rect(W/2 - 100, 250, 200, 50)
stop_rect = pygame.Rect(50, 350, 165, 70)
snooze_rect = pygame.Rect(W - 215, 350, 165, 70)

def main():
    que = True
    current_time = int(time.strftime("%H")) + 1
    minute = 0
    button = False
    r = 0
    gls = 8
    user_text = ''
    clock = pygame.time.Clock()
    active = False
    L = True
    while r == 0:
        clock.tick(FPS)  
        if active == False and user_text != '' and L == True:
            gls -= int(user_text)
            L = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                r = 4
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inp_rect.collidepoint(event.pos) and que:
                    active = True 
                else:
                    active = False
                if button and stop_rect.collidepoint(event.pos):
                    media.stop()
                    button = False
                    gls -= 1
                    current_time += 1
                    minute = 0
                elif button and snooze_rect.collidepoint(event.pos):
                    media.stop()
                    minute = int(time.strftime("%M")) + 10
                    if minute >= 60:
                        minute -= 60
                    button = False
            if event.type == pygame.KEYDOWN:
                if active == True:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode
        
        text_surface = font.render(user_text, True, WHITE)
        if active:
            color = WHITE
        else:
            color = GREY
        
        #Check for input
        if user_text >= '0' and user_text <= '7':
            que = False

        #check time
        if (current_time== int(time.strftime("%H")) and minute == 0) or minute == int(time.strftime("%M")):
            button = True
            media.play()
        
        #draw on screen
        win.fill(LBLUE)
        win.blit(text, textRect)
        #Input field
        if que:
            pygame.draw.rect(win, color, inp_rect, 2)
            win.blit(text_surface, (inp_rect.x + 90, inp_rect.y + 9))
            win.blit(ques, quesRect)
        #Alarm 
        if button == True:
            pygame.draw.rect(win,WHITE,stop_rect)
            win.blit(stop, (stop_rect.x + 40, stop_rect.y + 22))
            pygame.draw.rect(win,WHITE,snooze_rect) 
            win.blit(snooze, (snooze_rect.x + 10, stop_rect.y + 22))
            win.blit(al, alRect)
        pygame.display.update()

        #Errors 
        if user_text <= '0'and user_text.isdigit() and user_text != '':
            r = 2
        elif user_text == '8' or (user_text >= '8' and user_text.isdigit()) and user_text != '':
            r = 1
        elif user_text.isdigit() == False and user_text != '':
            r = 3
        if gls == 0:
            r = 1
    
    #Error Handling
    if r < 4:
        ercol = WHITE
        message = ''
        if r == 1:
            message = 'Congrats! You drank enough water for today, bye for now!'
        elif r == 2 or r == 3:
            message = 'The number you have introduced is too low or has letters, try again!' 
            ercol = RED
        er = font3.render(message, True, ercol)
        erR = er.get_rect()
        erR.center = (500, 450)
        win.blit(er, erR)
        pygame.display.update()
        pygame.time.delay(3000)
    pygame.quit()

if __name__ == "__main__":
    main()