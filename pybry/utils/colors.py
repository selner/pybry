from PIL import Image, ImageDraw

from pybry.utils.logutil import logger

#
# Adapted from https://gist.github.com/zollinger/1722663
#


def get_colors(image_file, maxcolors=10, resize=640):
	# Resize image to speed up processing
	img = Image.open(image_file)
	img = img.copy()
	img.thumbnail((resize, resize))
	
	# Reduce to palette
	paletted = img.convert('P', palette=Image.ADAPTIVE, colors=maxcolors * 2)
	
	# Find dominant colors
	palette = paletted.getpalette()
	color_counts = sorted(paletted.getcolors(), reverse=True)
	total = 0
	for i in range(maxcolors):
		color, cnt = color_counts[i]
		total += cnt
	#
	# for i in range(maxcolors):
	#     cnt = color_counts[i][1]
	#     color_counts[2] = cnt/total
	
	colors = []
	for i in range(maxcolors):
		palette_index = color_counts[i][1]
		dominant_color = palette[palette_index * 3:palette_index * 3 + 3]
		colors.append(tuple(dominant_color))
	
	return colors


#
# Adapted from https://gist.github.com/zollinger/1722663
#
def save_color_palette(colors, swatchsize=150, outfile="palette.png"):
	num_colors = len(colors)
	palette = Image.new('RGB', (swatchsize * num_colors, swatchsize))
	draw = ImageDraw.Draw(palette)
	
	posx = 0
	for color in colors:
		draw.rectangle([posx, 0, posx + swatchsize, swatchsize], fill=color)
		posx += swatchsize
	
	del draw
	palette.save(outfile, "PNG")


# if __name__ == '__main__':
#     input_file = sys.argv[1]
#     output_file = sys.argv[2]
#     colors = get_colors(input_file)
#     save_palette(colors, outfile = output_file)


#
# def enhance_image_color(image_file):
#     img = Image.open(image_file)
#     img = img.copy()
#     color = ImageEnhance.Color(img)
#     file, ext = image_file.split(".")
#     newfile = f'{file}-enhanced.{ext}'
#     color.enhance(1.25).save(newfile)
#     return newfile
#

def get_colorapi_qsparam(rgb=None, hex=None):
	queryparam = ""
	if rgb and isinstance(rgb, tuple):
		queryparam = f'rgb={rgb[0]},{rgb[1]},{rgb[2]}'
	elif hex:
		queryparam = 'hex=' + hex.removeprefix("#")
	
	return queryparam


def call_colorapi(uri, rgb=None, hex=None):
	api = uri
	queryparam = get_colorapi_qsparam(rgb, hex)
	if queryparam:
		api += f'&{queryparam}'
	
	from requests import get
	
	logger.debug(f'... calling thecolorapi with "{queryparam}:  {api}"')
	resp = get(api)
	print(resp.text)
	
	if not resp.ok:
		logger.error(f'... ERROR:  thecolorapi call failed"')
		resp.raise_for_status()
	
	respdata = resp.json()
	
	logger.debug(f'... colorapi returned: {respdata}')
	
	return respdata


def identify_color(rgb=None, hex=None):
	api = "http://thecolorapi.com/id?format=json"
	return call_colorapi(api, rgb, hex)


# Define mode by which to generate the scheme from the seed color
# string (optional) Default: monochrome Example: analogic
# Choices: monochrome monochrome-dark monochrome-light analogic complement analogic-complement triad quad
def get_scheme_from_color(rgb=None, hex=None, mode="complement"):
	api = f'http://thecolorapi.com/scheme?format=json&count=6&mode={mode}'
	return call_colorapi(api, rgb, hex)

