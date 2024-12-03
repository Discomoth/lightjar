import pygame
import time
import random

pygame.init()
screen = pygame.display.set_mode((900, 500))
clock = pygame.time.Clock()
running = True

def hex_to_rgb(hex_str):
	hex_str = hex_str.replace('#', '')
	return (int(hex_str[0:2],16), int(hex_str[2:4],16), int(hex_str[4:6],16))

cool_colors1 = [hex_to_rgb(x) for x in [
	'#0d4682',
	'#275892',
	'#3f68a1',
	'#5878b0',
	'#7089be',
	'#8899cd',
	'#a1aadc',
	'#b9baeb'
]]

def remap_leds(neo_led_obj):
    final_list = []
    temp_list = []
    reverse = True
    for led in range(len(neo_led_obj)):
        temp_list.append(led)

        if (led+1) % 8 == 0 and reverse:
            temp_list.reverse()
            final_list.extend(temp_list)
            temp_list = []
            reverse = False

        elif (led+1) % 8 == 0 and not reverse:
            final_list.extend(temp_list)
            temp_list = []
            reverse = True

    return final_list

class NeoPixel:
	def __init__(self, n_leds, screen):

		self.screen = screen
		self.led_string = [(0,0,0) for x in range(n_leds)]
		self.led_pos = []

		# Simulate positional reversing
		for x in range(n_leds):
			reverse = True
			for column in range(6):
				column_offset = 150*column + 50
				if reverse:
					positions = list(range(8))
					positions.reverse()
					for row in positions:
						row_offset = 50*row + 50
						self.led_pos.append((column_offset, row_offset))
					reverse = False
				else:
					for row in range(8):
						row_offset = 50*row + 50
						self.led_pos.append((column_offset, row_offset))
					reverse = True

		# Correct positional reversing
		self.n_r = remap_leds(self)

	def __len__(self):
		return len(self.led_string)

	def __setitem__(self, index, value):
		self.led_string[index] = value

	def __getitem__(self, index):
		return self.led_string[index]

	def write(self):
		for led in range(len(self)):
			pygame.draw.circle(self.screen, self.led_string[led], self.led_pos[led], 20)
			pygame.display.flip()

n = NeoPixel(48, screen)

def test_sequence():
	for led in n.n_r:
		n[led-1] = (0,0,0)
		n[led] = (255,0,0)
		time.sleep(0.01)
		n.write()

def test_sequence2():
	for intensity in range(32):
		for led in n.n_r:
			n[led] = (intensity*8,0,0)
			time.sleep(0.005)
			n.write()

def test_sequence3():
    color_list = cool_colors1
    for _ in range(len(color_list)):
        for pos, led in enumerate(n.n_r):
            if pos == 0 or pos == 8:
                n[led] = color_list[0]
            elif pos == 1 or pos == 9:
                n[led] = color_list[1]
            elif pos == 2 or pos == 10:
                n[led] = color_list[2]
            elif pos == 3 or pos == 11:
                n[led] = color_list[3]
            elif pos == 4 or pos == 12:
                n[led] = color_list[4]
            elif pos == 5 or pos == 13:
                n[led] = color_list[5]
            elif pos == 6 or pos == 14:
                n[led] = color_list[6]
            elif pos == 7 or pos == 15:
                n[led] = color_list[7]
        
        n.write()
        color_list = [color_list[pos-1] for pos in range(len(color_list))]

        time.sleep(0.25)

def color_rain():
	rain_gradient_map = [
		[1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.9, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.5, 0.9, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
		[0.2, 0.5, 0.9, 1.0, 0.0, 0.0, 0.0, 0.0],
		[0.1, 0.2, 0.5, 0.9, 1.0, 0.0, 0.0, 0.0],
		[0.05, 0.1, 0.2, 0.5, 0.9, 1.0, 0.0, 0.0],
		[0.01, 0.05, 0.1, 0.2, 0.5, 0.9, 1.0, 0.0],
		[0.0, 0.01, 0.05, 0.1, 0.2, 0.5, 0.9, 1.0],
		[0.0, 0.0, 0.01, 0.05, 0.1, 0.2, 0.5, 0.9],
		[0.0, 0.0, 0.0, 0.01, 0.05, 0.1, 0.2, 0.5],
		[0.0, 0.0, 0.0, 0.0, 0.01, 0.05, 0.1, 0.2],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.05, 0.1],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01, 0.05],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.01],
		[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
	]

	rand_col = random.randint(0, 5)
	leds = n.n_r[int(rand_col * 8):int((rand_col * 8)+8)]
	print(f"Col: {rand_col} - LEDs: {leds}")
	rand_color = cool_colors1[random.randint(0, len(cool_colors1)-1)]

	# Compute gradient mapping
	gradient_values = []

	for gradient in rain_gradient_map:
		gradient_step = []
		for led_mult in gradient:
			led_values =(
				int(rand_color[0]*led_mult),
				int(rand_color[1]*led_mult),
				int(rand_color[2]*led_mult))
			gradient_step.append(led_values)

		gradient_values.append(gradient_step)

	for step in gradient_values:
		for pos, led in enumerate(leds):
			n[led] = step[pos]
		n.write()
		time.sleep(0.01)
	time.sleep(random.randrange(0, 100)/100)

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	color_rain()

	clock.tick(60)

pygame.quit()
