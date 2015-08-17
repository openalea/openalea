koch_curve = Model("koch_curve")

FLAKE = get_control(u'FLAKE')

if FLAKE.value:
    lstring_flake = koch_curve(";(4)_(0.01)F(1)-(90)F(1)-(90)F(1)-(90)F(1)")
    world["koch_flake"] = lstring_flake
else:
    lstring_curve = koch_curve()
    world["koch_curve"] = lstring_curve
