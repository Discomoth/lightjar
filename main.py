# -*- coding: utf-8 -*-
# main.py
import neopixel
from machine import Pin
import random
import time
from palettes import ColorDict

color_dict = ColorDict.get_colordict()
color_names = ColorDict.get_colornames()

p = Pin(5, Pin.OUT)
ind_led = Pin(25, Pin.OUT)
led_count = 48
n = neopixel.NeoPixel(p, led_count, timing=1)

def reset_leds():
    for index in range(len(n)):
        n[index] = (0,0,0)

reset_leds()

time_delay = 0.001

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

# Remap LEDs to handle alternating direction
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

n.n_r = remap_leds(n)

# Mode 1

while False:
    for led in range(led_count):
        for intensity in range(32):
            n[led] = (intensity*8, intensity*8, intensity*8)
            n.write()
            time.sleep(time_delay)
        ind_led.toggle()
    for led in range(led_count):
        for intensity in range(32):
            n[led] = (intensity*8, 0, 0)
            n.write()
            time.sleep(time_delay)
        ind_led.toggle()
    for led in range(led_count):
        for intensity in range(32):
            n[led] = (0, intensity*8, 0)
            n.write()
            time.sleep(time_delay)
        ind_led.toggle()
    for led in range(led_count):
        for intensity in range(32):
            n[led] = (0, 0, intensity*8)
            n.write()
            time.sleep(time_delay)
        ind_led.toggle()
    for led in range(led_count):
        for intensity in range(32):
            n[led] = (0, 0, 0)
            n.write()
            time.sleep(time_delay)
        ind_led.toggle()

# Mode 2

while False:
    for intensity in range(32):
        for led in range(led_count):
            n[led]=(intensity*8,intensity*8,intensity*8)
            n[led-1] = (0,0,0)
            n.write()
            time.sleep(0.01)

def test_seq_1():
    leds = [x for x in n.n_r]
    led_columns = []
    for column in range(6):
        col_list = []
        for row in range(8):
            col_list.append(leds.pop(0))
        led_columns.append(col_list)
    for led in range(8):
        for column in led_columns:
            n[column[led]] = (128,128,128)
        n.write()
        time.sleep(0.1)
    for led in range(8):
        for column in led_columns:
            n[column[led]] = (0,0,0)
        n.write()
        time.sleep(0.1)
        
def sweeping_colors():
    
    colors = [x for x in palettes.gradient_2]
    colors_rev = [x for x in palettes.gradient_2]
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
            time.sleep(0.05)
    for color in colors_rev:
        for led in range(8):
            for column in led_columns:
                n[column[led]] = color
            n.write()
            time.sleep(0.05)
    

# Sequence Functions
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

while True:
    try:
        sweeping_colors()
    except KeyboardInterrupt:
        reset_leds()
        break
