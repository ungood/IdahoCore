from colorsys import *
import random, math

def rgb(r, g, b):
    return (r, g, b)

def hsl(h, s, l):
    return hls_to_rgb(h, l, s)

def hsv(h, s, v):
    return hsv_to_rgb(h, s, v)

def scale(c, factor):
    r, g, b = c
    return rgb(r * factor, g * factor, b * factor)

def lerp(a, b, f):
    """http://processing.org/reference/lerp_.html"""
    delta = b - a
    return a + (delta * f)

def get(func_or_value, time, delta):
    """Returns the result of calling func_or_value if func_or_value is callable,
else returns it as a value.

    The benefit of this is that we can pass either functions or constant values
    to various effects and it will work the same."""
    
    try:
        return func_or_value(time, delta)
    except TypeError:
        return func_or_value

# ===== BLEND MODES ====

def blend(color1, color2, f):
    """Blend two colors together, by some fraction between 0 (color1) and 1 (color2)"""
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    red = lerp(r1, r2, f)
    green = lerp(g1, g2, f)
    blue = lerp(b1, b2, f)
    return rgb(red, green, blue)

def multiply(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return rgb(r1 * r2, g1 * g2, b1 *b2)

def add(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return rgb(min(r1 + r2, 1.0), min(g1 + g2, 1.0), min(b1 + b2, 1.0))

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


class StripePalette(Palette):
    """Creates a palette with one stripe of the foreground color, and the rest the background color."""
    def __init__(self, n, foreground, background):
        self.palette = [foreground] + [background for x in range(n-1)]


class CandyPalette(Palette):
    """Creates a palette that repeats the given colors, like a candycane."""
    def __init__(self, n, colors):
        numColors = len(colors)
        self.palette = [colors[x % numColors] for x in range(n)]


class FadePalette(Palette):
    """Creates a palette that fades between two colors."""
    def __init__(self, n, color1, color2):
        halfway = float(n)/2
        self.palette = [blend(color1, color2, abs(halfway - float(x)) / halfway) for x in range(n)]

# ===== WAVEFORMS ====

class Sine:
    """Creates a class that will produce a sine wave with the following parameters:

    min    -- the minimum value
    max    -- the maximum value
    period -- the number of units between one peak and the next.
    """
    def __init__(self, min, max, period):
        self.min = min
        self.max = max
        self.period = period

    def __call__(self, time, delta):
        min = get(self.min, time, delta)
        max = get(self.max, time, delta)
        period = get(self.period, time, delta)

        coeff = (float(max) - min) / 2
        mid = min + coeff
        mult = math.pi * 2 / period
        
        return coeff * math.sin(time * mult) + mid


class Uniform:
    """Creates a waveform that returns a (uniform) random number each time it is
    called."""

    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __call__(self, time, delta):
        min = get(self.min, time, delta)
        max = get(self.max, time, delta)

        return random.uniform(min, max)


class Sawtooth:
    """Creates a sawtooth waveform."""
    def __init__(self, min, max, period):
        self.min = min
        self.max = max
        self.period = period

    def __call__(self, time, delta):
        min = get(self.min, time, delta)
        max = get(self.max, time, delta)
        period = get(self.period, time, delta)

        delta = max - min
        return delta * ((time / period) - math.floor(time / period)) + min


class Beat:
    """Creates a waveform that stays at min for some time, then ramps up to max
    and back down to min.  A little like a heart beat."""
    def __init__(self, min, max, minTime, maxTime):
        self.min = min
        self.max = max
        self.minTime = minTime
        self.maxTime = maxTime
        self.elapsed = 0.0

    def __call__(self, time, delta):
        min = get(self.min, time, delta)
        max = get(self.max, time, delta)
        minTime = get(self.minTime, time, delta)
        maxTime = get(self.maxTime, time, delta)

        self.elapsed += delta

        if(self.elapsed >= minTime + maxTime):
            self.elapsed = 0

        if(self.elapsed < minTime):
            return min

        return ((self.elapsed - minTime) / minTime) * (max - min)

# ===== EFFECTS =====


class Blender:
    """Given a list of palettes, will blend from one palette to a randomly picked palette, over and over.

    stableTime -- the amount of time (in ms) to leave an effect running.
    blendTime  -- the amount of time (in ms) to blend between effects.

    """
    
    def __init__(self, palettes, stableTime, blendTime):
        random.seed()
        self.palettes = palettes
        self.stableTime = stableTime
        self.blendTime = blendTime
        self.next = palettes[0]
        self.updateNextPalette(0, 0)

    def updateNextPalette(self, time, delta):
        self.elapsed = 0
        self.curStableTime = get(self.stableTime, time, delta)
        self.curBlendTime = get(self.blendTime, time, delta)
        self.current = self.next
        self.next = self.palettes[random.randint(0, len(self.palettes) - 1)]

    def __call__(self, time, delta):
        """Gets the next frame, given that total time (in ms) has passed, and delta (ms) have passed since last update."""

        self.elapsed += delta

        if(self.elapsed >= self.curStableTime + self.curBlendTime):
            self.updateNextPalette(time, delta)

        if(self.elapsed < self.curStableTime):
            return self.current(time, delta)

        position = float(self.elapsed - self.curStableTime) / self.curBlendTime
        return blend_palettes(self.current(time, delta), self.next(time, delta), position)


class Rotator:
    """Given a palette, will return a palette that has been rotated over time.
   
    calcPeriod -- a callable that returns the period (number of ms to move one position) 
    """
    def __init__(self, source, period):
        self.position = 0.0
        self.period = period
        self.source = source

    def __call__(self, time, delta):
        palette = self.source(time, delta)

        period = get(seslf.period, time, delta)
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


class BlendEffect:
    def __init__(self, source1, source2, f):
        self.source1 = source1
        self.source2 = source2
        self.f = f

    def __call__(self, time, delta):
        f = get(self.f, time, delta)
        palette1 = self.source1(time, delta)
        palette2 = self.source2(time, delta)
        return blend_palettes(palette1, palette2, self.f)


class AdditionEffect:
    def __init__(self, source1, source2):
        self.source1 = source1
        self.source2 = source2

    def __call__(self, time, delta):
        palette1 = self.source1(time, delta)
        palette2 = self.source2(time, delta)

        return [add(palette1[x], palette2[x]) for x in range(len(palette1))]


class MultiplyEffect:
    def __init__(self, source1, source2):
        self.source1 = source1
        self.source2 = source2

    def __call__(self, time, delta):
        palette1 = self.source1(time, delta)
        palette2 = self.source2(time, delta)

        return [multiply(palette1[x], palette2[x]) for x in
                range(len(palette1))]


class LimitingEffect:
    def __init__(self, source, maxFactor):
        self.maxFactor = maxFactor
        self.source = source

    def __call__(self, time, delta):
        total = 0.0

        palette = self.source(time, delta)
        for col in palette:
            r, g, b = col
            total += r + g + b

        maxAmount = len(palette) * 3 * self.maxFactor;
        if(total > maxAmount):
            factor = maxAmount / total;
            palette = [scale(c, factor) for c in palette]

        return palette
           

if __name__ == "__main__":
    palette = MonoPalette(3, White)
    limiter = LimitingEffect(palette, 0.5)
    result = limiter(0, 0)
    print(result)
