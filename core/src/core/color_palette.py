
__dict__ = dict(black 	="#000000",
                gray 	="#808080",
                maroon 	="#800000",
                red 	="#FF0000",
                green 	="#008000",
                lime 	="#00FF00",
                olive 	="#808000",
                yellow 	="#FFFF00",
                navy 	="#000080",
                blue 	="#0000FF",
                purple 	="#800080",
                fuchsia ="#FF00FF",
                teal 	="#008080",
                aqua 	="#00FFFF",
                silver 	="#C0C0C0",
                white 	="#FFFFFF"
            )

            
            
def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple.
    Taken from here:
    http://code.activestate.com/recipes/266466-html-colors-tofrom-rgb-tuples/
    Many thanks go to the authors!"""
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)

    
for k, v in __dict__.iteritems():
    if isinstance(v, str):
        globals()[k] = HTMLColorToRGB(v)