import pygame
import time
import random
from palettes import ColorDict

color_dict = ColorDict.get_colordict()
color_names = ColorDict.get_colornames()

pygame.init()
screen = pygame.display.set_mode((900, 500))
clock = pygame.time.Clock()
running = True

def interpolate_colors(start, end, steps):
    start_color = (start[0]/256, start[1]/256, start[2]/256)
    end_color = (end[0]/256, end[1]/256, end[2]/256)

    red_diff = end_color[0] - start_color[0]
    green_diff = end_color[1] - start_color[1]
    blue_diff = end_color[2] - start_color[2]

    red_delta = red_diff/steps
    green_delta = green_diff/steps
    blue_delta = blue_diff/steps

    return_gradient = []
    for step in range(0, steps):
        interp_color = (
            int((start_color[0] + (red_delta*step))*256),
            int((start_color[1] + (green_delta*step))*256),
            int((start_color[2] + (blue_delta*step))*256),
            )
        return_gradient.append(interp_color)
    return return_gradient

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

def sweeping_colors():
    
    random_color = color_names[random.randrange(0, len(color_names))]
    print(random_color)
    colors = interpolate_colors(color_dict[random_color][0],color_dict[random_color][1],256)
    colors_rev = [x for x in colors]
    colors_rev.reverse()
    
    leds = [x for x in n.n_r]
    led_columns = []
    for column in range(6):
        col_list = []
        for row in range(8):
            col_list.append(leds.pop(0))
        led_columns.append(col_list)
        
    for color in colors:
        for led in range(8):
            for column in led_columns:
                n[column[led]] = color
            n.write()
            time.sleep(0.0001)
    for color in colors_rev:
        for led in range(8):
            for column in led_columns:
                n[column[led]] = color
            n.write()
            time.sleep(0.0001)
    

while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	sweeping_colors()

	clock.tick(60)

pygame.quit()
