from colorsys import *
import random, math

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

def blend_palettes(pal1, pal2, f):
    """Blends two palettes together"""
    return [blend(pal1[i], pal2[i], f) for i in range(len(pal1))]
        

Red    = rgb(1, 0, 0)
Green  = rgb(0, 1, 0)
Blue   = rgb(0, 0, 1)
Yellow = rgb(1, 1, 0)
Cyan   = rgb(0, 1, 1)
Purple = rgb(1, 0, 1)
Black  = rgb(0, 0, 0)
White  = rgb(1, 1, 1) 

# ===== PALETTES =====
class Palette:
    def __call__(self, time, delta):
        return self.palette

class RainbowPalette(Palette):
    """Creates a palette of N colors, evenly spaced around the HSV color wheel"""
    def __init__(self, n, saturation, luminosity):
        self.palette = [hsv(float(x) / n, saturation, luminosity) for x in range(n)]
        
class MonoPalette(Palette):
    """Creates a palette of N instances of the same color"""
    def __init__(self, n, color):
        self.palette = [color for x in range(n)]

class CandyPalette(Palette)
    """Creates a palette that repeats the given colors, like a candycane."""
    def __init__(self, n, colors)
        numColors = len(colors)
        self.palette = [colors[x % numColors] for x in range(n)]

class FadePalette(Palette)
    """Creates a palette that fades the between two colors."""
    def __init__(self, n, color1, color2):
        halfway = float(n)/2
        self.palette = [blend(color1, color2, abs(halfway - float(x)) / halfway) for x in range(n)]

# ===== TIME FLUCTUATORS ====

class SineWave:
    """Creates a class that will produce a sine wave with the following parameters:

    min    -- the minimum value
    max    -- the maximum value
    period -- the number of units between one peak and the next.
    """
    def __init__(self, min, max, period):
        self.coeff = (float(max) - min) / 2
        self.mid = min + self.coeff
        self.mult = math.pi * 2 / period

    def __call__(self, x):
        return math.sin(x * self.mult) * self.coeff + self.mid


class Constant:
    """Creates a callable that returns a constant value."""
    def __init__(self, value):
        self.value = float(value)

    def __call__(self, x):
        return self.value

# ===== EFFECTS =====

class PaletteBlender:
    """Given a list of palettes, will blend from one palette to a randomly picked palette, over and over.
    
    calcPeriod -- should be a callable that returns a period at time t.
        The period is the number of ms to blend palettes together.
    """
    
    def __init__(self, palettes, calcPeriod):
        random.seed()
        self.palettes = palettes
        self.current = self.getNextPalette()
        self.next = self.getNextPalette()
        self.position = 0.0
        self.calcPeriod = calcPeriod

    def getNextPalette(self):
        return self.palettes[random.randint(0,len(self.palettes)-1)]

    def update(self, time, delta):
        """Gets the next frame, given that total time (in ms) has passed, and delta (ms) have passed since last update."""

        period = self.calcPeriod(time)
        velocity = delta / period
        self.position += velocity
        while self.position > 1:
            self.current = self.next
            self.next = self.getNextPalette()
            self.position -= 1

        return blend_palettes(self.current, self.next, self.position)


class Rotator:
    """Given a palette, will return a palette that has been rotated over time.
   
    calcPeriod -- a callable that returns the period (number of ms to move one position) 
    """
    def __init__(self, calcPeriod):
        self.position = 0.0
        self.calcPeriod = calcPeriod

    def update(self, palette, time, delta):
        period = self.calcPeriod(time)
        velocity = delta / period
        self.position += velocity

        strands = len(palette)
        result = []
        for i in range(strands):
            fpart, pos = math.modf(self.position)
            cur = int(pos + i) % strands
            next = int(cur + 1) % strands
            result.append(blend(palette[cur], palette[next], abs(fpart)))

        return result


if __name__ == "__main__":
    pal1 = [Red, Green, Blue]
    pal2 = [Black, Black, Black]
    sine = SineWave(50, 200, 10)
    #blender = PaletteBlender([pal1, pal2], sine) # a palette blender that varies the speed of its blending over time (sinusoidally)
    #for x in range(10):
    #    print blender.update(x*20, 20)
    rotator = Rotator(Constant(100)) # a rotator that rotates one strand in a constant 100 ms, negative values would rotate the opposite direction
    for x in range(10):
        print rotator.update(pal1, x*20, 20)

