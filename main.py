# -*- coding: utf-8 -*-
# main.py
import neopixel
from machine import Pin, ADC, Timer, WDT
import random
import time
from palettes import ColorDict
import json

# Push button globals
push_button_pin = 22

# ADC globals
brightness_sensor_pin = 26
brightness_control_pin = 27

# Indicator LED globals
indicator_pin = 25

# Neopixel globals
neopixel_pin = 15
led_count = 48

# Misc globals
time_delay = 0.001
global_current_gradient = None
global_mode_changed_flag = None
global_current_palette = "magenta-blue"
global_current_palette_index = 0
global_brightness_factor = 0.1
global_brightness_mode = 'manual'
global_mode_value_index = 0
global_mode_value = None
global_save_flag = 0

devmode = False

class FakeWDT:
    @staticmethod
    def feed():
        pass

# Setup hardware watchdog
watchdog_timer_value = 8000
if devmode:
    global_wdt = FakeWDT()
else:
    global_wdt = WDT(timeout=watchdog_timer_value)

class ProgramControl:

    def __init__(self):
        global global_current_palette
        global global_current_palette_index
        global global_brightness_factor
        global global_brightness_mode
        global global_mode_value
        global global_mode_value_index

        try:
            self.load_config('config.json')
            #with open('config.json', 'r') as file:
            #    self.config_dict = json.load(file)
            #    global_current_palette = self.config_dict['global_brightness_mode']
            #    global_mode_value_index = self.config_dict['global_mode_value_index']

        except OSError:
            
            self.config_dict = {
            'global_current_palette_index':1,
            'global_current_palette':"magenta-blue",
            'global_brightness_factor':0.1,
            'global_brightness_mode':'manual',
            'global_mode_value_index':0
            }
            
            self.save_config('config.json')
            self.load_config('config.json')

        self.palette_control = PaletteControl()
        self.led_control = LEDControl(neopixel_pin, led_count)
        self.brightness_control = BrightnessControl(brightness_sensor_pin, brightness_control_pin, global_brightness_mode)
        self.mode_control = ModeControl(self.led_control, global_mode_value_index)

        self.button_control = ButtonControl(push_button_pin, self.mode_control, self.palette_control, self.brightness_control)
        
        self.check_timer = Timer()
        self.check_timer.init(period=250, callback=self.check_save)

    def check_save(self, t=None):
        if global_save_flag == 1:
            self.save_config('config.json')

    def save_config(self, config_file):
        global global_save_flag
        global watchdog_timer_value
        global global_mode_changed_flag
        
        self.refresh_config_dict()
        
        with open(config_file, 'w') as file:
            json.dump(self.config_dict, file)
            print('config file saved!')
        global_save_flag = 0

        if global_mode_changed_flag == 1:
            WDT(timeout = 10)
            time.sleep(0.5)

    def load_config(self, config_file):
        global global_current_palette
        global global_brightness_factor
        global global_brightness_mode
        global global_mode_value_index
        global global_current_palette_index

        with open(config_file, 'r') as file:
            self.config_dict = json.load(file)
            global_current_palette_index = self.config_dict['global_current_palette_index']
            global_current_palette = self.config_dict['global_current_palette']
            global_brightness_factor = self.config_dict['global_brightness_factor']
            global_brightness_mode = self.config_dict['global_brightness_mode']
            global_mode_value_index = self.config_dict['global_mode_value_index']

    def refresh_config_dict(self):
        self.config_dict = {
        'global_current_palette_index':global_current_palette_index,
        'global_current_palette':global_current_palette,
        'global_brightness_factor':global_brightness_factor,
        'global_brightness_mode':global_brightness_mode,
        'global_mode_value_index':global_mode_value_index
        }

    def run(self):
        global global_save_flag
        global global_mode_value
        global global_mode_changed_flag
        global watchdog_timer_value
        global global_mode_value_index
        
        self.load_config('config.json')
        
        while True:
            try:
                while True:
                    if global_save_flag == 1:
                        self.save_config('config.json')
                        global_save_flag = 0
                    if global_mode_value_index == 0:
                        self.mode_control.cycle()
                    elif global_mode_value_index == 1:
                        self.mode_control.sweeping_colors()
                    elif global_mode_value_index == 2:
                        self.mode_control.rotator()
                    elif global_mode_value_index == 3:
                        self.mode_control.ocean_waves()
                    elif global_mode_value_index == 4:
                        self.mode_control.flame()
                    elif global_mode_value_index == 5:
                        self.mode_control.test_sequence1()
                    elif global_mode_value_index == 6:
                        self.mode_control.test_sequence2()
            except Exception as e:
                raise(e)


class LEDControl:

    def __init__(self, neopixel_pin, led_count, indicator_state=True):
        self.neopixel_pin = Pin(neopixel_pin, Pin.OUT, pull=Pin.PULL_DOWN)
        self.indicator_pin = Pin(25, Pin.OUT)
        self.n = neopixel.NeoPixel(self.neopixel_pin, led_count, timing=1)
        self.indicator = Pin(self.indicator_pin)
        self.indicator_state = indicator_state
        self.n_scaled = [(0,0,0) for x in range(len(self.n))]
        
        self.indicator_led_timer = Timer()
        self.indicator_led_timer.init(mode=Timer.PERIODIC, period=500, callback=self.indicator_toggle)

        # Remap leds for correct sequencing
        self.n_r = self.remap_leds()

    def indicator_toggle(self, t=None):
        self.indicator.toggle()

    def write(self):
        global global_wdt
        global global_brightness_factor
        global global_mode_changed_flag
        global watchdog_timer_value
        
        global_wdt.feed()
        
        initial_sequence = [x for x in self.n]
        for index, color_value in enumerate(self.n):
            self.n[index] = (
                int(self.n[index][0]*global_brightness_factor),
                int(self.n[index][1]*global_brightness_factor),
                int(self.n[index][2]*global_brightness_factor)
                )
        self.n.write()
        for pos, x in enumerate(initial_sequence):
            self.n[pos] = x

    def remap_leds(self):
        final_list = []
        temp_list = []
        reverse = True
        for led in range(len(self.n)):
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

class BrightnessControl:

    def __init__(self, brightness_sensor_pin, brightness_input_pin, brightness_factor=50, brightness_mode='manual'):
        global global_brightness_factor
        global global_brightness_mode

        self.input = ADC(brightness_input_pin)
        self.sensor = ADC(brightness_sensor_pin)

        self.last_sensor_value = self._measure_sensor()
        self.last_input_value = self._measure_input()

        self.mode = global_brightness_mode

        # Hardware timer interrupt to check brightness
        self.check_timer = Timer()
        self.check_timer.init(period=100, callback=self.read_brightness)

    def _pass(self):
        pass

    def _measure_sensor(self):
        value = self.sensor.read_u16() / 65535
        if value > 1:
            return 1
        elif value < 0:
            return 0
        else:
            return value

    def _measure_sensor_inv(self):
        value =  0.5 - (self.sensor.read_u16()/65535)
        if value > 1:
            return 1
        elif value < 0:
            return 0
        else:
            return value

    def _measure_input(self):
        value = self.input.read_u16() / 65535
        if value > 1:
            return 1
        elif value < 0:
            return 0
        else:
            return value

    def read_brightness(self, t=None):
        global global_brightness_factor
        if self.mode == 'manual':
            raw_value = self._measure_input()
            global_brightness_factor = raw_value
        elif self.mode == 'automatic':
            raw_value = self._measure_sensor()
            global_brightness_factor = raw_value
        elif self.mode == 'automatic_inv':
            raw_value = self._measure_sensor_inv()
            global_brightness_factor = raw_value

    def toggle_automatic_brightness(self):
        global global_brightness_mode

        if self.mode == 'manual':
            self.mode = 'automatic'
        elif self.mode == 'automatic':
            self.mode = 'automatic_inv'
        elif self.mode == 'automatic_inv':
            self.mode = 'manual'

        global_brightness_mode = self.mode

class ButtonControl:
    """
    Quick press (sub 1 second) = change colors
    Short press (about 1 second) = change mode
    Long press (more than 1 second) = change brightness mode
    """

    def __init__(self, button_pin, mode_control_obj, palette_control_obj, brightness_control_obj):
        self.button = Pin(button_pin, Pin.IN, pull=None)
        self.button.irq(trigger=Pin.IRQ_RISING, handler=self.button_irq_handler)

        self.mode_control = mode_control_obj
        self.palette_control = palette_control_obj
        self.brightness_control = brightness_control_obj

    def _increment_mode(self):
        self.mode_control

    def button_irq_handler(self, t=None):
        global global_current_palette
        global global_save_flag
        global program_control

        start_time = time.ticks_ms()
        while self.button.value() == 0:
            pass
        time_delta = time.ticks_diff(time.ticks_ms(), start_time)

        #For now I have removed the mode change functionality.
        # Perhaps in a future version of firmware they will be enabled
        # but as they stand now, the switching mechanism is a little jank
        # and the modes themselves are not all that imperssive...

        if 50 < time_delta < 1000:
            print('color change')
            self.palette_control.next_palette()
            print(f'new_palette: {global_current_palette}')
            program_control.save_config('config.json')
        #elif 750 < time_delta < 2000:
        #    print('mode change')
        #    self.mode_control.next_mode()
        #    program_control.save_config('config.json')
        elif 1000 < time_delta:
            print('brightness mode change')
            self.brightness_control.toggle_automatic_brightness()
            program_control.save_config('config.json')
        else:
            pass

class ModeControl:

    def __init__(self, neopixel_obj, initial_mode_index=0):
        global global_mode_value
        global global_mode_value_index

        self.modes = [
            self.sweeping_colors,
            self.ocean_waves,
            self.color_chase,
            self.cycle,
            self.rotator,
            self.flame,
            self.test_sequence1,
            self.test_sequence2
        ]

        # Set global mode on instantiation
        global_mode_value_index = initial_mode_index
        global_mode_value = self.modes[global_mode_value_index]
        self.current_mode_value = global_mode_value
        self.neopixel = neopixel_obj

    def next_mode(self):
        global global_mode_value_index
        global global_mode_changed_flag
        global_mode_value_index += 1
        if global_mode_value_index >= len(self.modes)-1:
            global_mode_value_index = 0
        global_mode_changed_flag = 1

    @staticmethod
    def list_shift(list_obj, num):
        num = num % len(list_obj)
        return list_obj[num:] + list_obj[:num]

    def reset_leds(self):
        for index in range(len(self.neopixel.n)):
            self.neopixel.n[index] = (0,0,0)
        self.neopixel.write()

    def test_sequence1(self):
        for led in self.neopixel.n_r:
            self.neopixel.n[led-1] = (0,0,0)
            self.neopixel.n[led] = (255,0,0)
            time.sleep(0.01)
            self.neopixel.write()

    def test_sequence2(self):
        for intensity in range(32):
            for led in self.neopixel.n_r:
                self.neopixel.n[led] = (intensity*8,0,0)
                time.sleep(0.005)
                self.neopixel.write()

    def sweeping_colors(self):
        global global_current_gradient
        global time_delay
        
        colors = global_current_gradient
        colors_rev = [x for x in colors]
        colors_rev.reverse()
        
        leds = [x for x in self.neopixel.n_r]
        led_columns = []
        for column in range(6):
            col_list = []
            for row in range(8):
                col_list.append(leds.pop(0))
            led_columns.append(col_list)
            
        for color in colors:
            for led in range(8):
                for column in led_columns:
                    self.neopixel.n[column[led]] = color
                self.neopixel.write()
                time.sleep(time_delay*50)
        for color in colors_rev:
            for led in range(8):
                for column in led_columns:
                    self.neopixel.n[column[led]] = color
                self.neopixel.write()
                time.sleep(time_delay*50)
        
    def ocean_waves(self):
        color = []
        color.extend(global_current_gradient)
        colorpos = 0
        reset = False

        leds = [x for x in self.neopixel.n_r]
        led_columns = []
        for column in range(6):
            col_list = []
            for row in range(8):
                col_list.append(leds.pop(0))
            led_columns.append(col_list)
        
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
                        self.neopixel.n[led] = (
                            color[colorpos][0],
                            color[colorpos][1],
                            color[colorpos][2])
                        self.neopixel.write()
                for column in led_columns:
                    for pos, led in enumerate(column[1::iterator+2]):
                        self.neopixel.n[led] = (
                            color[colorpos][0],
                            color[colorpos][1],
                            color[colorpos][2])
                        self.neopixel.write()

    def color_chase(self):
        global global_current_gradient
        global time_delay

        fade_pattern = []
        fade_pattern.extend([x for x in range(1, 25)])
        fade_pattern.extend([256 for x in range(len(self.neopixel.n)+25)])

        shifted_palette = self.list_shift(global_current_gradient, random.randint(0, len(global_current_gradient)))
        for fade in range(35, len(fade_pattern)+35):
            shifted_fade = self.list_shift(fade_pattern, fade)
            for led in self.neopixel.n_r:
                self.neopixel.n[led] = (
                    int(shifted_palette[led][0]/shifted_fade[led]),
                    int(shifted_palette[led][1]/shifted_fade[led]),
                    int(shifted_palette[led][2]/shifted_fade[led])
                    )
            time.sleep(time_delay*5)
            self.neopixel.write()

    def cycle(self):
        global global_current_gradient
        
        pixel_list = list(range(len(self.neopixel.n_r)))

        for j in range(len(global_current_gradient)):
            shifted_palette = self.list_shift(global_current_gradient, j)
            for i in pixel_list:
                self.neopixel.n[i] = shifted_palette[i]
            self.neopixel.write()
            time.sleep(0.01)

    def rotator(self):
        global global_current_gradient

        rings = []
        for y in range(8):
            temp_ring = []
            for x in range(6):
                temp_ring.append(y + 8*x)
            rings.append(temp_ring)
        for color_offset in range(0, 64, 16):
            for pos, ring in enumerate(rings):
                shifted_gradient = self.list_shift(global_current_gradient, color_offset)
                for led in ring:
                    interpolated_colors = PaletteControl.interpolation_2_point(self.neopixel.n[led], shifted_gradient[led], 12)
                    for inter_color in interpolated_colors:
                        self.neopixel.n[self.neopixel.n_r[led]] = inter_color
                        self.neopixel.write()
                #time.sleep(0.01)

    def flame(self):
        columns = []
        for x in range(6):
            temp_column = []
            for y in range(8):
                temp_column.append(y + 8*x)
            columns.append(temp_column)

        flame_gradient = PaletteControl.interpolation_2_point((255, 247, 93), (161, 1, 0), 8)

        for column in columns:
            fill = random.randint(2, 8)
            partial = column
            partial.reverse()
            partial = partial[:fill]
            for led in column:
                self.neopixel.n[self.neopixel.n_r[led]] = (0,0,0)
            for pos, led in enumerate(partial):
                self.neopixel.n[self.neopixel.n_r[led]] = flame_gradient[pos]
            self.neopixel.write()
            time.sleep(0.025)
        

class PaletteControl:

    def __init__(self):
        global global_current_palette_index
        
        self.color_dict = ColorDict()
        self.palette_names = self.color_dict.get_colornames()
        self.palette_dict = self.color_dict.get_colordict()
        self.regen_palette(self.palette_names[global_current_palette_index])

    def regen_palette(self, palette, steps=256):
        global global_current_palette
        global global_current_gradient

        global_current_palette = palette
        global_current_gradient = self.interpolation_multipoint(global_current_palette, steps)

    def next_palette(self):
        global global_current_palette_index
        global global_current_palette
        
        global_current_palette_index += 1
        if global_current_palette_index > len(self.palette_names)-1:
            global_current_palette_index = 0
        self.regen_palette(self.palette_names[global_current_palette_index], 64)

    @staticmethod
    def interpolation_2_point(start, end, steps):
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

    def interpolation_multipoint(self, color_name, steps):
        step_num = int(steps/len(self.palette_dict[color_name]))
        return_gradient = []
        
        color_values = self.palette_dict[color_name]
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
                    
if __name__ == '__main__':
    program_control = ProgramControl()
    program_control.run()
