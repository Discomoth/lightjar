# -*- coding: utf-8 -*-
# main.py
import neopixel
from machine import Pin
import time

p = Pin(5, Pin.OUT)
ind_led = Pin(25, Pin.OUT)
led_count = 48
n = neopixel.NeoPixel(p, led_count, timing=1)

time_delay = 0.001

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

while True:
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
