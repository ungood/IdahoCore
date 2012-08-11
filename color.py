from colorsys import *

def rgb(r, g, b):
    return (r, g, b)

def hsl(h, s, l):
    return hls_to_rgb(h, l, s)

def hsv(h, s, v):
    return hsv_to_rgb(h, s, v)

def lerp(a, b, f):
    """http://processing.org/reference/lerp_.html"""
    delta = b - a
    return a + (delta * f)

def blend(color1, color2, f):
    """Blend two colors together, by some fraction between 0 (color1) and 1 (color2)"""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    red = lerp(r1, r2, f)
    green = lerp(g1, g2, f)
    blue = lerp(b1, b2, f)
    return rgb(red, green, blue)

Red    = rgb(1, 0, 0)
Green  = rgb(0, 1, 0)
Blue   = rgb(0, 0, 1)
Yellow = rgb(1, 1, 0)
Cyan   = rgb(0, 1, 1)
Purple = rgb(1, 0, 1)
Black  = rgb(0, 0, 0)
White  = rgb(1, 1, 1)

def rainbow_palette(n, saturation, luminosity):
    """Creates a palette of N colors, evenly spaced around the HSV color wheel"""
    palette = [hsv(float(x) / n, saturation, luminosity/(float(x)+1)) for x in range(n)]
    return palette
    

