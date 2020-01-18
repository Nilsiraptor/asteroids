import pygame
import math
import random

#%%

pygame.init()

Width = 800
Height = 600

gameDisplay = pygame.display.set_mode((Width, Height))

pygame.display.set_caption("Game")

clock = pygame.time.Clock()

font = pygame.font.Font("brandish.ttf", 32)
score = font.render("000", True, (127, 127, 0))
points = 0
print(score.get_height())

orRocket = pygame.image.load("rocket.png")
rocket = orRocket
orRocket_fire = pygame.image.load("rocket_fire.png")
rocket_fire = orRocket_fire

img = rocket

size = 120
angle = 0
vel_x, vel_y = 0, 0

bullets = []
comets = [[[0, 0], 1, random.randrange(0, 360), 200]]

pygame.display.set_icon(img)

#%%

def car(x, y):
    gameDisplay.blit(img, (x-img.get_width()/2, y-img.get_height()/2))
    
def bullet(pos):
    pygame.draw.circle(gameDisplay, (255, 0, 0), (int(pos[0]), int(pos[1])), 2)
    
def comet(pos, rad):
    if int(rad) >= 3:
        pygame.draw.circle(gameDisplay, (200, 200, 255), (int(pos[0]), int(pos[1])), int(rad), 3)
    else:
        pygame.draw.circle(gameDisplay, (200, 200, 255), (int(pos[0]), int(pos[1])), 2)
        
    
def splitComet(com):
    comets.append([[com[0][0]-0.3*com[3]*math.sin((com[2]+60)*math.pi/180), com[0][1]+0.3*com[3]*math.cos((com[2]+60)*math.pi/180)], com[1]+1, com[2]+60, com[3]*0.7])
    comets.append([[com[0][0]-0.3*com[3]*math.sin((com[2]-60)*math.pi/180), com[0][1]+0.3*com[3]*math.cos((com[2]-60)*math.pi/180)], com[1]+1, com[2]-60, com[3]*0.7])
    comets.remove(com)
    
def dist(pos1, pos2):
    return math.sqrt(math.pow(pos1[0]-pos2[0], 2)+math.pow(pos1[1]-pos2[1], 2))

def newScore():
    return font.render(str(points).zfill(3), True, (127, 127, 0))
      
    

#%%

running = True
x, y = Width/2, Height/2

while running:
    #print(clock.get_time())
    #print(len(comets))
    #print(len(bullets))
    gameDisplay.fill((0,0,0))
    for event in pygame.event.get():
        #print(event)
        
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([[x, y], angle])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bullets.append([[x, y], angle])
        
    keys = pygame.key.get_pressed()
            
    if keys[pygame.K_a]:
        angle += 0.2*clock.get_time()
        angle = angle%360
        
    if keys[pygame.K_d]:
        angle -= 0.2*clock.get_time()
        angle = angle%360
        
    if keys[pygame.K_w]:
        vel_x -= 0.005*math.sin(angle*math.pi/180)*clock.get_time()
        vel_y += 0.005*math.cos(angle*math.pi/180)*clock.get_time()
        
        img = pygame.transform.rotate(orRocket_fire, angle)
    else:
        img = pygame.transform.rotate(orRocket, angle)
 
    x += vel_x*0.05*clock.get_time()
    y -= vel_y*0.05*clock.get_time()
    
    x = x%Width
    y = y%Height
    
    for bul in bullets:
        for com in comets:
            if dist(com[0], bul[0]) < com[3]:
                try:
                    bullets.remove(bul)
                except ValueError:
                    print("Bullet not found!")
                splitComet(com)
                points += 1
                score = newScore()
                break
        
        bul[0][0] -= 0.2*math.sin(bul[1]*math.pi/180)*clock.get_time()
        bul[0][1] -= 0.2*math.cos(bul[1]*math.pi/180)*clock.get_time()
        bul[0][0] = bul[0][0]%Width
        bul[0][1] = bul[0][1]%Height
        bullet(bul[0])
            
    for com in comets:
        com[0][0] -= 0.01*com[1]*math.sin(com[2]*math.pi/180)*clock.get_time()
        com[0][1] -= 0.01*com[1]*math.cos(com[2]*math.pi/180)*clock.get_time()
        com[0][0] = com[0][0]%Width
        com[0][1] = com[0][1]%Height
        comet(com[0], com[3])
        if dist(com[0], (x, y)) < com[3]+30:
            running = False
            break
    
    if x > Width - size:
        car(x-Width, y)
    elif x < size:
        car(x+Width, y)
    if y > Height - size:
        car(x, y-Height)
        if x > Width - size:
            car(x-Width, y-Height)
        elif x < size:
            car(x+Width, y-Height)
    elif y < size:
        car(x, y+Height)
        if x > Width - size:
            car(x-Width, y+Height)
        elif x < size:
            car(x+Width, y+Height)
    
    
    car(x, y)
    
    gameDisplay.blit(score, (Width-score.get_width(), Height-44))
        
    pygame.display.update()
    
    clock.tick(60)
    
#%%
    
file = open("highscore.txt", "r+")
high = file.readline()
high = int(high)
#print(high)
file.close()

if high > points:
    highscore = font.render("Der Highscore ist: " + str(high), True, (255, 255, 255))
else:
    highscore = font.render("Der bisherige Highscore war: " + str(high), True, (255, 255, 255))
    file = open("highscore.txt", "w")
    file.write(str(points))
    file.close()

    
game = font.render("Du hast verloren!", True, (255, 255, 255))
gameover = font.render("Deine Punktzahl ist:", True, (255, 255, 255))
gameoverpoints = font.render(str(points), True, (255, 255, 255))

    
over = True
while over:
    gameDisplay.fill((0,0,0))
    gameDisplay.blit(game, ((Width-game.get_width())/2, Height/5))
    gameDisplay.blit(gameover, ((Width-gameover.get_width())/2, 2*Height/5))
    gameDisplay.blit(gameoverpoints, ((Width-gameoverpoints.get_width())/2, 3*Height/5))
    gameDisplay.blit(highscore, ((Width-highscore.get_width())/2, 4*Height/5))
    
    
    for event in pygame.event.get():
        #print(event)
        
        if event.type == pygame.QUIT:
            over = False
            break
        
    pygame.display.update()
    
    clock.tick(10)
    
pygame.quit()
quit()