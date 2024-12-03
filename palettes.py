# -*- coding: utf-8 -*-
# colors.py

palette_names = ['inferno', 'plasma', 'turbo', 'Blues', 'Purples', 'Reds', 'Spectral', 'autumn', 'cool', 'coolwarm', 'ocean', 'prism', 'rainbow', 'spring', 'summer', 'terrain', 'winter']


def hex_to_rgb(hex_str):
    hex_str = hex_str.replace('#', '')
    return (int(hex_str[0:2],16), int(hex_str[2:4],16), int(hex_str[4:6],16))

#Matplotlib color gradients
class ColorDict:

    @staticmethod
    def get_colornames():
        return palette_names

    @staticmethod
    def get_colordict():
        color_dict = {"inferno":[hex_to_rgb(color) for color in ['#000004', '#fcffa4']],
            "plasma":[hex_to_rgb(color) for color in ['#0d0887', '#f0f921']],
            "turbo":[hex_to_rgb(color) for color in ['#30123b', '#7a0403']],
            "Blues":[hex_to_rgb(color) for color in ['#f7fbff', '#08306b']],
            "Purples":[hex_to_rgb(color) for color in ['#fcfbfd', '#3f007d']],
            "Reds":[hex_to_rgb(color) for color in ['#fff5f0', '#67000d']],
            "Spectral":[hex_to_rgb(color) for color in ['#9e0142', '#5e4fa2']],
            "autumn":[hex_to_rgb(color) for color in ['#ff0000', '#ffff00']],
            "cool":[hex_to_rgb(color) for color in ['#00ffff', '#ff00ff']],
            "coolwarm":[hex_to_rgb(color) for color in ['#3b4cc0', '#b40426']],
            "ocean":[hex_to_rgb(color) for color in ['#008000', '#ffffff']],
            "prism":[hex_to_rgb(color) for color in ['#ff0000', '#54ff00']],
            "rainbow":[hex_to_rgb(color) for color in ['#8000ff', '#ff0000']],
            "spring":[hex_to_rgb(color) for color in ['#ff00ff', '#ffff00']],
            "summer":[hex_to_rgb(color) for color in ['#008066', '#ffff66']],
            "terrain":[hex_to_rgb(color) for color in ['#333399', '#ffffff']],
            "winter":[hex_to_rgb(color) for color in ['#0000ff', '#00ff80']],
        }
        return color_dict