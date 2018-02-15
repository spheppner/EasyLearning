#!/usr/bin/python3
def start():
	import pygame_textinput
	import pygame
	import random
	pygame.init()
	
	# Create TextInput-object
	textinput = pygame_textinput.TextInput() # Text: print(textinput.get_text())

	pygame.display.set_caption("Geographie | Drücke ESCAPE zum Verlassen!")
	screen = pygame.display.set_mode((1000, 200))
	clock = pygame.time.Clock()
	nationen = ["Österreich", "Slovenien", "Spanien", "Russland", "Niederlande", "Italien", "Deutschland", "England", "Dänemark", "Tschechien", "Kroatien"]
	points = 0

	def write(background, text, x = 10, y = 50, color = (0,0,0), font = "mono", fontsize = None, center = False):
		if fontsize is None:
			fontsize = 24
		font = pygame.font.SysFont(font, fontsize, bold = True)
		fw, fh = font.size(text)
		surface = font.render(text, True, color)
		if center:
			background.blit(surface, (x-fw//2, y-fh//2))
		else:
			background.blit(surface, (x, y))


	def changeText():
		text = random.choice(nationen)
		return text
	
	def writeNations():
		text = changeText()
		write(screen, text, 700, 50)
		text = changeText()
		write(screen, text, 700, 100)
		text = changeText()
		write(screen, text, 700, 150)
	
	text = changeText()
	
	while True:
		screen.fill((225, 225, 225))
		writeNations()
		write(screen, str(points), 950, 50, (255, 0, 255))
			
		events = pygame.event.get()
		for event in events:
			if event.type == pygame.QUIT:
				exit()
		
		if textinput.get_text() == text:
			screen.fill((225, 225, 225))
			text = changeText()
			textinput.input_string = ""
			textinput.cursor_position = 0
			points += 1
		
		# Feed it with events every frame
		textinput.update(events)
		# Blit its surface onto the screen
		screen.blit(textinput.get_surface(), (10, 150))

		pygame.display.update()
		clock.tick(30)
