from matplotlib import colormaps
from matplotlib.colors import to_hex
import numpy as np

def setup_palette():
	with open('output.py', 'w') as file:
		pass

setup_palette()

def save_palette(name:str, color_list:list):
	with open('output.py', 'a') as file:
		file.write(f"\"{name}\":[hex_to_rgb(color) for color in {color_list}],\n")

name_filter = [
	'inferno',
	'plasma',
	'turbo',
	'Blues',
	'Purples',
	'Reds',
	'Spectral',
	'autumn',
	'cool',
	'coolwarm',
	'ocean',
	'prism',
	'rainbow',
	'spring', 
	'summer',
	'terrain',
	'winter',
]

with open('output.py', 'a') as file:
	file.write(f"palette_names = {[x for x in colormaps if x in name_filter]}\n\n" + 'color_dict = {')

for name in [color for color in colormaps if color in name_filter]:
	cmap = [color for color in colormaps[name](np.linspace(0, 1, 2))]
	html_values = [to_hex(color) for color in cmap]

	save_palette(name, html_values)

with open('output.py', 'a') as file:
	file.write('}')