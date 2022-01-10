import os
import random
import ctypes

import pygame
import win32api
import win32con
import win32gui

pygame.init()
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
user32 = ctypes.windll.user32
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

FONT_SIZE = 12
COLOR = "green"
COLOR_DOWN = "lightgreen"


class Symbol:
	def __init__(self, x, y, speed):
		self.x, self.y = x, y
		self.speed = speed
		self.value = random.choice(normal_symbols)
		self.interval = random.randrange(5, 15)

	def draw(self, color):
		frames = pygame.time.get_ticks()
		if not frames % self.interval:
			self.value = random.choice(normal_symbols if color == COLOR else last_symbols)

		self.y = self.y + self.speed if self.y < screen_height else -FONT_SIZE
		screen.blit(self.value, (self.x, self.y))

	def stop(self, color):
		frames = pygame.time.get_ticks()
		if not frames % self.interval:
			self.value = random.choice(normal_symbols if color == COLOR else last_symbols)

		if self.y < screen_height:
			self.y += self.speed
			self.speed /= 1.005
			screen.blit(self.value, (self.x, self.y))

class SymbolCol:
	def __init__(self, x, y):
		self.col_height = random.randrange(8, 18)
		self.speed = random.randrange(7, 15)
		self.symbols = [
			Symbol(x, i, self.speed)
			for i in range(y, y - FONT_SIZE * self.col_height, -FONT_SIZE)
		]
	def stop_matrix(self):
		[
			symbol.stop(COLOR)
			if i else symbol.stop(COLOR_DOWN)
			for i, symbol in enumerate(self.symbols)
		]

	def draw(self):
		[
			symbol.draw(COLOR)
			if i else symbol.draw(COLOR_DOWN)
			for i, symbol in enumerate(self.symbols)
		]


screen = pygame.display.set_mode([screen_width, screen_height], pygame.NOFRAME)
color_to_zero_alpha = (0, 0, 0)
ticks = 0

hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(
	hwnd,
	win32con.GWL_EXSTYLE,
	win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED
)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOSIZE)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*color_to_zero_alpha), 0, win32con.LWA_COLORKEY)

clock = pygame.time.Clock()

# path_to_data = os.path.expanduser('~\\AppData\\Local\\Screensavers\\')
path_to_data = ""
fonts_names = [el[2] for el in os.walk(path_to_data + "fonts")][0]
FONTS = [
	pygame.font.Font(path_to_data + "fonts\\" + name, FONT_SIZE, bold=True)
	for name in fonts_names
]
FONTS.append(pygame.font.SysFont("comic sans ms", FONT_SIZE, bold=True))
FONTS.append(pygame.font.SysFont("verdana", FONT_SIZE, bold=True))

def generate_columns():
	global normal_symbols, last_symbols
	# katakana = [chr(int('0x30a0', 16) + i) for i in range(96)]
	english_letters = [chr(i) for i in range(65, 90)]
	font = random.choice(FONTS)
	normal_symbols = [font.render(char, True, (0, random.randrange(40, 256), 0)) for char in english_letters]
	last_symbols = [font.render(char, True, pygame.Color(COLOR_DOWN)) for char in english_letters]
	symbol_columns = [SymbolCol(x, 0) for x in range(0, screen_width, FONT_SIZE)]

	return symbol_columns


TPS = 30
HALF_MINUTE = TPS * 15
symbol_columns = []

try:
	while 1:
		if ticks % HALF_MINUTE == 0:
			if symbol_columns:
				for i in range(200):
					screen.fill(color_to_zero_alpha)
					[symbol_column.stop_matrix() for symbol_column in symbol_columns]
					pygame.display.update()
					clock.tick(TPS)
			symbol_columns = generate_columns()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				break
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					break
		screen.fill(color_to_zero_alpha)

		[symbol_column.draw() for symbol_column in symbol_columns]

		pygame.display.update()
		clock.tick(TPS)
		ticks += 1
except Exception:
	pass
finally:
	pygame.quit()
