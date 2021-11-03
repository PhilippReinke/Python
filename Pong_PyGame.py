import pygame as pg
from sys import exit
import numpy as np

# basics
pg.init()
sWidth, sHeight = (600,350)
sWidthHalf = int(sWidth/2); sHeightHalf = int(sHeight/2)
screen = pg.display.set_mode((sWidth, sHeight))
pg.display.set_caption("Pong")
clock = pg.time.Clock()

# player params
Pspeed	= 3
dir		= { pg.K_LEFT: (0,-Pspeed), pg.K_RIGHT: (0,Pspeed) }
Pheight = 60
PheightHalf = int(Pheight/2)
# left player
Lplayer = pg.Rect(10, sHeightHalf-PheightHalf, 15, Pheight)
Lchange	= (0,0)
# right player
Rplayer = pg.Rect(sWidth-25, sHeightHalf-PheightHalf, 15, Pheight)
Rchange	= (0,0)
# ball
ballSpeed  = 7
ballChange = [-ballSpeed,0]
ballPos    = [sWidthHalf, sHeightHalf]
ballRect   = pg.draw.circle(screen, "white", ballPos, 10)
# points
points	   = [0,0]
pg.font.init()
myfont = pg.font.SysFont(None, 70)

while True:
	# check for events
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
			exit()
		if event.type == pg.KEYDOWN:
			if event.key in dir:
				Lchange = dir[event.key]
		if event.type == pg.KEYUP:
			if event.key == pg.K_LEFT and Lchange != (0,Pspeed):
				Lchange = (0,0)
			if event.key == pg.K_RIGHT and Lchange != (0,-Pspeed):
				Lchange = (0,0)

	# make screen black 
	screen.fill("Black")

	# right players logic
	if ballRect.center[1] > Rplayer.bottom:
		Rchange = (0,Pspeed)
	elif ballRect.center[1] < Rplayer.top:
		Rchange = (0,-Pspeed)
	else:
		Rchange = (0,0)

	# move players and draw them
	if Lplayer.bottom >= sHeight and Lchange == (0,Pspeed) or Lplayer.top <= 0 and Lchange == (0,-Pspeed):
		Lchange = (0,0)
	Lplayer.move_ip(Lchange)
	if Rplayer.bottom >= sHeight and Rchange == (0,Pspeed) or Rplayer.top <= 0 and Rchange == (0,-Pspeed):
		Rchange = (0,0)
	Rplayer.move_ip(Rchange)
	pg.draw.rect(screen, "white", Lplayer)
	pg.draw.rect(screen, "white", Rplayer)	

	# line in middle
	pg.draw.line(screen, "white", (sWidthHalf,0), (sWidthHalf,sHeight), 3)

	# check if ball hit upper or lower boundary and draw ball
	if ballRect.top <= 0 or ballRect.bottom >= sHeight:
		ballChange = [ballChange[0], -ballChange[1]]
	ballPos[0] += ballChange[0]
	ballPos[1] += ballChange[1]
	ballRect = pg.draw.circle(screen, "white", ballPos, 10)

	# left player hits ball
	if Lplayer.colliderect(ballRect):
		# ration is between -1 and 1 and 0 is center
		ratioCollisionPoint = np.pi * (ballRect.center[1] - Lplayer.center[1]) / (3*PheightHalf)
		# rotate (3, 0) by maximally pi/3 (and a bit actually)
		ballChange = [ballSpeed*np.cos(ratioCollisionPoint),ballSpeed*np.sin(ratioCollisionPoint)]
	if Rplayer.colliderect(ballRect):
		ratioCollisionPoint = np.pi * (ballRect.center[1] - Rplayer.center[1]) / (3*PheightHalf)
		ballChange = [-ballSpeed*np.cos(ratioCollisionPoint),ballSpeed*np.sin(ratioCollisionPoint)]

	# left player missed ball
	if ballRect.left <= 8:
		ballPos = [sWidthHalf, sHeightHalf]
		ballChange = [-ballSpeed,0]
		points[1] += 1
	# right player missed ball
	elif ballRect.right >= sWidth-2:
		ballPos = [sWidthHalf, sHeightHalf]
		ballChange = [ballSpeed,0]
		points[0] += 1

	# score
	scoreLeft = myfont.render(f"{points[0]}", False, (210,210,210))
	scoreLeftRect = scoreLeft.get_rect(midtop=(sWidthHalf-50,20))
	screen.blit(scoreLeft, scoreLeftRect)
	scoreLeft = myfont.render(f"{points[1]}", False, (210,210,210))
	scoreLeftRect = scoreLeft.get_rect(midtop=(sWidthHalf+50,20))
	screen.blit(scoreLeft, scoreLeftRect)
	lastPoints = points

	# update and wait
	pg.display.update()
	clock.tick(60)