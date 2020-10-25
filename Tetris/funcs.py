def make_color_darker(hexcolor: str, blacklevel: float):
    blacklevel = 1 - blacklevel
    if not (0 <= blacklevel <= 1):
        raise ValueError("Blacklevel has to be a number between 0 and 1")
    red = int(f"{hexcolor[1]}{hexcolor[2]}", 16)
    green = int(f"{hexcolor[3]}{hexcolor[4]}", 16)
    blue = int(f"{hexcolor[5]}{hexcolor[6]}", 16)
    colorlist = "#"
    for color in (red, green, blue):
        hexnum = hex(int(color * blacklevel))
        hexnum = hexnum[2:]
        if len(hexnum) == 1:
            hexnum += "0"
        colorlist += hexnum
    return colorlist


def hexcolor_to_rgb(hexcolor: str):
    rgb = (int(f"{hexcolor[1]}{hexcolor[2]}", 16),
           int(f"{hexcolor[3]}{hexcolor[4]}", 16),
           int(f"{hexcolor[5]}{hexcolor[6]}", 16))
    return rgb


def rgb_to_hexcolor(rgb: tuple):
    colorlist = "#"
    for color in rgb:
        hexnum = hex(int(color))
        hexnum = hexnum[2:]
        if len(hexnum) == 1:
            hexnum += "0"
        colorlist += hexnum
    return colorlist


def time_has_went_by(start_time, ms_interval):
    second_interval = ms_interval / 1000
    import time
    current_time = time.time()
    if current_time - start_time > second_interval:
        return True
    else:
        return False


if __name__ == '__main__':
    print(rgb_to_hexcolor((0, 0, 255)))
