import pygame
import time
import random
from palettes import ColorDict

color_dict_obj = ColorDict()

color_dict = color_dict_obj.get_colordict()
color_names = color_dict_obj.get_colornames()

pygame.init()
screen = pygame.display.set_mode((900, 500))
clock = pygame.time.Clock()
running = True

current_palette = None
current_gradient = None

def _interpolate_colors(start, end, steps):
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

def interpolate_colors(color_name, steps):
    step_num = int(steps/len(color_dict[color_name]))
    return_gradient = []
    
    color_values = color_dict[color_name]
    for color_index in range(len(color_values)):
        if color_index + 1 == len(color_values):
            return_gradient.extend([color for color in return_gradient[::-1]])
            return return_gradient
        else:
            start_color = (
                color_values[color_index][0]/step_num,
                color_values[color_index][1]/step_num,
                color_values[color_index][2]/step_num
                )
            end_color = (
                color_values[color_index + 1][0]/step_num,
                color_values[color_index + 1][1]/step_num,
                color_values[color_index + 1][2]/step_num
                )

            red_diff = end_color[0] - start_color[0]
            green_diff = end_color[1] - start_color[1]
            blue_diff = end_color[2] - start_color[2]

            red_delta = red_diff/step_num
            green_delta = green_diff/step_num
            blue_delta = blue_diff/step_num

            for step in range(0, step_num):
                interp_color = (
                    int((start_color[0] + (red_delta*step))*step_num),
                    int((start_color[1] + (green_delta*step))*step_num),
                    int((start_color[2] + (blue_delta*step))*step_num),
                    )
                return_gradient.append(interp_color)

def regen_palette(palette, steps=256):
    global current_gradient
    global current_palette

    if palette == current_palette:
        return current_gradient
    else:
        current_palette = palette
        current_gradient = interpolate_colors(current_palette, steps)

def list_shift(list_obj, num):
    num = num % len(list_obj)
    return list_obj[num:] + list_obj[:num]

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

num_pixels = 48
n = NeoPixel(num_pixels, screen)

# Establish columns
leds = [x for x in n.n_r]
led_columns = []
for column in range(6):
    col_list = []
    for row in range(8):
        col_list.append(leds.pop(0))
    led_columns.append(col_list)
del leds

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
    
def ocean_waves():
    color = []
    color.extend(current_gradient)
    colorpos = 0
    reset = False
    for _ in range(8):
        for iterator in range(8):
            if not reset:
                colorpos += 1
            else:
                colorpos -= 1


            if colorpos == 0:
                reset = False
            elif colorpos == 64:
                reset = False

            for column in led_columns:
                for pos, led in enumerate(column[::iterator+2]):
                    n[led] = (
                        color[colorpos][0],
                        color[colorpos][1],
                        color[colorpos][2])
                    n.write()
            for column in led_columns:
                for pos, led in enumerate(column[1::iterator+2]):
                    n[led] = (
                        color[colorpos][0],
                        color[colorpos][1],
                        color[colorpos][2])
                    n.write()


def color_chase():
    global current_palette
    global current_gradient

    fade_pattern = []
    fade_pattern.extend([x for x in range(1, 25)])
    fade_pattern.extend([256 for x in range(num_pixels+25)])

    shifted_palette = list_shift(current_gradient, random.randint(0, len(current_gradient)))
    for fade in range(35, len(fade_pattern)+35):
        shifted_fade = list_shift(fade_pattern, fade)
        for led in n.n_r:
            n[led] = (
                shifted_palette[led][0]/shifted_fade[led],
                shifted_palette[led][1]/shifted_fade[led],
                shifted_palette[led][2]/shifted_fade[led]
                )
        time.sleep(0.1)
        n.write()

def cycle():
    global current_palette
    global current_gradient
    
    pixel_list = list(range(num_pixels))

    for j in range(len(current_gradient)):
        shifted_palette = list_shift(current_gradient, j)
        for i in pixel_list:
            n[i] = shifted_palette[i]
        n.write()
        time.sleep(0.01)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    regen_palette(color_names[random.randrange(0, len(color_names))], 512)
    print(current_palette)

    while True:
        try:
            flame()
        except KeyboardInterrupt:
            quit()

    clock.tick(60)

pygame.quit()
