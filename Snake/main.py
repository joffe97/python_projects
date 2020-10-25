from myfuncs import *
import figs
import highscorefun
import players
import time
import keyboard
import turtle
import items

# Definere variabler
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '<', '.', '-', ',']
border = [1200 / 2, 700 / 2]
stopwhile = 0
tid = 0
tid2 = 0
tid3 = 0
frame_beginning = 1
frame_end = 0
item_create = 1
midtpos = []
midtpos_gml = []
talepos = []
stopplay = 0
growthpos = []
fpscounter = 0

# Start variabler
cname = 'Square'
ccolor = '#fdf2c3'
fpscap = 400

# - Menyer
startbeforeplay = 0
beforeplay = 0
startplay = 0
checkbeforeplay = 0
play = 0
startendplay = 0
endplay = 0
startmenu = 1
menu = 0
starthighscore = 0
highscore = 0
startsettings = 0
settings = 0
stopgame = 0

# - Variable variabler
menuchoice = [237, 177, 117, 57]

# Standard instillinger
turtle.setup(height=1.0, width=1.0)
turtle.mode('logo')
norm.penup()
norm.hideturtle()
turtle.tracer(0)

Screen().bgpic('pokebackground.png')

while not (keyboard.is_pressed('esc') or stopgame):
    hide_pen(pen)
    hide_pen(pen2)
    hide_pen(pen3)
    hide_pen(pen4)
    hide_pen(pen5)

    # Variabler som resettes
    direction = 0
    name_input = []
    score = 0
    item_create = 1
    items.itemattributes_current = items.itemattributes_layout.copy()
    hastighet = 400 / fpscap  # Multipliser med 0 for testing
    scorefromtick = 0
    fps = 100
    csize = 35

    if startbeforeplay:
        while keyboard.is_pressed('enter'):
            None

        clear_all()

        pen2.fillcolor('lightgrey')
        pen2.begin_fill()
        draw([-border[0] * 0.5, border[1] * 0.07], figs.rectangle, border[0] * 1.0, border[1] * 0.14, pen2, turt=pen2)
        pen2.end_fill()
        stop_draw(pen2)

        start_draw([-280, border[1] * 0.07 - 45], pen2)
        pen2.write('NAME:', font=('Copperplate Gothic Bold', 26))

        startbeforeplay = 0
        beforeplay = 1

    while beforeplay:
        turtle.update()
        pen.clear()

        # Skrive inn navn
        while not stopwhile:
            if 2 < (time.time() - tid) < 10:
                pen4.clear()
            for k in letters:
                if keyboard.is_pressed('backspace') and len(name_input) > 0:
                    del name_input[len(name_input) - 1]
                    name = ''.join(name_input)
                    stopwhile = 1
                    tid2 = time.time()
                    break

                elif keyboard.is_pressed('enter') and not len(name_input) == 0:
                    beforeplay = 0
                    checkbeforeplay = 1
                    stopwhile = 1
                    break

                elif keyboard.is_pressed(k) and len(name_input) <= 16:
                    name_input.append(k)
                    name = ''.join(name_input)
                    stopwhile = 1
                    break
        stopwhile = 0

        start_draw([-140, border[1] * 0.07 - 43], pen)
        pen.write(name, font=('Copperplate Gothic Light', 26))

        while keyboard.is_pressed('enter') or keyboard.is_pressed(k):
            None

        while keyboard.is_pressed('backspace'):
            if 0.4 < (time.time() - tid2) < 10 or 0.07 < (time.time() - tid3) < 0.4:
                tid3 = time.time()
                break

    while checkbeforeplay:
        # file_write = open('highscores.txt', 'a')

        while True:
            file_read = open('highscores.txt', 'r')
            if stopwhile:
                file_read.close()
                break
            stopwhile = 1
            for file_line in file_read:
                if file_line[0:(len(file_line) - 1)] == name:
                    startbeforeplay = 1

        if startbeforeplay:
            start_draw([-280, border[1] * 0.07 + 20], pen4)
            pen4.write('Name already taken...', font=('Copperplate Gothic Bold', 26))
            tid = time.time()
            name_input = []

        else:
            startplay = 1
        file_read.close()
        checkbeforeplay = 0

    if startplay:
        # Renser fra tidligere menyer
        clear_all()

        # Tegner grense
        pen2.fillcolor('#c4fdea')
        pen2.begin_fill()
        pen2.pensize(3)
        draw([-border[0], border[1]], figs.rectangle, border[0] * 2, border[1] * 2, pen2, turt=pen2)
        pen3.pensize(1)
        pen2.end_fill()
        stop_draw(pen2)

        # Setter variabler til valgt character
        character = players.Character(cname, csize, ccolor)
        norm.goto(-csize, csize)

        # Playvariabler - kjøres en gang
        directionchange_pos = [10000, 10000]
        direction_justchanged = 0
        starttime = time.time()
        onesec = time.time()
        onesec_counter = 0
        fifteensec = 0
        tales_wanted = 1
        talenumber = 0
        tales_extra = 0
        tale = []
        tale_distance = []

        # Setter over til while løkke
        play = 1
        startplay = 0

    while play:
        # ##########Setup########## #
        # Starter nytt frame
        frame_beginning = time.time()
        time.sleep(0.0001)

        turtle.update()
        norm.clear()
        pen.clear()

        # ####Variabler#### #
        # Lager variabel som er True hvert 100 ms
        if time.time() - starttime > 0.1:
            fiftyms = time.time()
            isfiftyms = 1
        else:
            isfiftyms = 0

        # Lager variabel som er True hvert 1 sekund
        if time.time() - onesec > 1:
            onesec = time.time()
            onesec_counter += 1
            if isonesec == 0:
                isonesec = 1
                fifteensec += 1
                if fifteensec % 15 == 0:
                    isfifteensec = 1
                else:
                    isfifteensec = 0
            else:
                isonesec = 0
                isfifteensec = 0
        else:
            isonesec = 0
            isfifteensec = 0

        # Setter playvariabler
        character.size = csize + items.itemattributes_current['size']
        hastighet = ((100 + items.itemattributes_current['speed'] + 3 * (
                onesec_counter // 1)) / fps)  # Multipliser med 0 for testing
        scorefromtick += items.itemattributes_current['score_tick'] * isfiftyms
        score = int(items.itemattributes_current['score_instant'] + scorefromtick)

        if isfifteensec:
            tales_extra += 1

        # ##########Player########## #
        # Gammel posisjon
        midtpos_gml = [int(norm.pos()[0]), int(norm.pos()[1])]
        direction_gml = direction

        talesize = character.size - 5

        # Bevegelse
        if abs(directionchange_pos[0] - norm.xcor()) > talesize or abs(directionchange_pos[1] - norm.ycor()) > talesize:
            direction_justchanged = 1
        else:
            direction_justchanged = 0

        if direction_justchanged:
            if keyboard.is_pressed('w') and not (
                    keyboard.is_pressed('a') or keyboard.is_pressed('s') or keyboard.is_pressed('d') or direction == 180):
                direction = 0
            elif keyboard.is_pressed('a') and not (
                    keyboard.is_pressed('w') or keyboard.is_pressed('s') or keyboard.is_pressed('d') or direction == 90):
                direction = 270
            elif keyboard.is_pressed('s') and not (
                    keyboard.is_pressed('a') or keyboard.is_pressed('w') or keyboard.is_pressed('d') or direction == 0):
                direction = 180
            elif keyboard.is_pressed('d') and not (
                    keyboard.is_pressed('a') or keyboard.is_pressed('s') or keyboard.is_pressed('w') or direction == 270):
                direction = 90

        norm.setheading(direction)
        norm.forward(hastighet)

        if direction_gml != direction:
            directionchange_pos = norm.pos()

        # Lager karakter

        # Henter yttergrensene og midtpunktet til characteren
        midtpos = [int(norm.pos()[0]), int(norm.pos()[1])]
        toppos = norm.pos()[1] + character.size / 2
        botpos = norm.pos()[1] - character.size / 2
        leftpos = norm.pos()[0] - character.size / 2
        rightpos = norm.pos()[0] + character.size / 2
        carea = [[leftpos, rightpos],
                 [botpos, toppos]]

        # ##########Hale########## #
        talenumber_old = talenumber
        while True:
            if items.itemattributes_current['tales'] > talenumber:
                tale.append(players.Character('tale1', csize - 5 + items.itemattributes_current['size'], ccolor))
                talenumber += 1
            else:
                break

        for tales in range(items.itemattributes_current['tales']):
            tale[tales].size = character.size - 5

            if tales == 0:
                tale_distance = (character.size + tale[tales].size) / 2
                followmidtpos = midtpos
                followdirection = direction
                followmidtpos_gml = midtpos_gml
            else:
                tale_distance = talesize
                followmidtpos = tale[tales - 1].midtpos
                followdirection = tale[tales - 1].direction

            while True:
                if talenumber_old != talenumber and tales == items.itemattributes_current['tales'] - 1:
                    talepos = followmidtpos
                    break
                if tale[tales].direction == 0:
                    if followdirection == 0:  # Haleposisjon når retningen er opp
                        if followmidtpos_gml[0] == followmidtpos[0]:
                            talepos = [followmidtpos[0], followmidtpos[1] - tale_distance]
                            break
                    else:
                        if tale[tales].midtpos[1] + hastighet > followmidtpos[1]:  # Endrer retning på hale ved sving
                            tale[tales].direction = followdirection
                            continue
                        else:
                            talepos = [tale[tales].midtpos[0], tale[tales].midtpos[1] + hastighet]  # Holder haleretning frem til sving
                            break

                if tale[tales].direction == 90:
                    if followdirection == 90:  # Haleposisjon når retningen er mot høyre
                        if followmidtpos_gml[1] == followmidtpos[1]:
                            talepos = [followmidtpos[0] - tale_distance, followmidtpos[1]]
                            break
                    else:
                        if tale[tales].midtpos[0] + hastighet > followmidtpos[0]:  # Endrer retning på hale
                            tale[tales].direction = followdirection
                            continue
                        else:
                            talepos = [tale[tales].midtpos[0] + hastighet, tale[tales].midtpos[1]]  # Holder haleretning frem til sving
                            break

                if tale[tales].direction == 180:
                    if followdirection == 180:  # Haleposisjon når retningen er ned
                        # if followmidtpos_gml[0] == followmidtpos[0]:
                        talepos = [followmidtpos[0], followmidtpos[1] + tale_distance]
                        break
                    else:
                        if tale[tales].midtpos[1] - hastighet < followmidtpos[1]:  # Endrer retning på hale
                            tale[tales].direction = followdirection
                            continue
                        else:
                            talepos = [tale[tales].midtpos[0], tale[tales].midtpos[1] - hastighet]  # Holder haleretning frem til sving
                            break

                if tale[tales].direction == 270:
                    if followdirection == 270:  # Haleposisjon når retningen er mot venstre
                        if followmidtpos_gml[1] == followmidtpos[1]:
                            talepos = [followmidtpos[0] + tale_distance, followmidtpos[1]]
                            break
                    else:
                        if tale[tales].midtpos[0] - hastighet < followmidtpos[0]:  # Endrer retning på hale
                            tale[tales].direction = followdirection
                            continue
                        else:
                            talepos = [tale[tales].midtpos[0] - hastighet, tale[tales].midtpos[1]]  # Holder haleretning frem til sving
                            break

                else:
                    talepos = [0, 0]
                    break

            # tale[tales].drawtale(talepos)
            tale[tales].midtpos = talepos
            tale[tales].rightpos = talepos[0] + tale[tales].size / 2
            tale[tales].leftpos = talepos[0] - tale[tales].size / 2
            tale[tales].botpos = talepos[1] - tale[tales].size / 2
            tale[tales].toppos = talepos[1] + tale[tales].size / 2
            followmidtpos_gml = talepos

            if (leftpos < tale[tales].rightpos - 2 and rightpos > tale[tales].leftpos + 2 and botpos < tale[tales].toppos - 2 \
                    and toppos > tale[tales].botpos + 2) and tales > 2 and not (tales == items.itemattributes_current['tales'] - 1):
                stopplay = 1
        for tales in range(items.itemattributes_current['tales']):
            tale[items.itemattributes_current['tales'] - 1 - tales].drawtale(tale[items.itemattributes_current['tales'] - 1 - tales].midtpos)
        character.drawplayer(norm.pos())

        # ##########Items########## #
        # Lager item
        if item_create:
            itemattributes_previous = items.itemattributes_current.copy()
            while True:
                item_create = 0
                pen5.clear()
                items.att1 = itemattributes_previous.copy()
                items.att2 = itemattributes_previous.copy()
                item = items.Items(border, 1)
                item2 = items.Items(border, 2)
                if (item.itemname == item2.itemname) \
                        or (leftpos - 10 <= item.area[0][1] and rightpos + 10 >= item.area[0][0] and botpos - 10 <=
                            item.area[1][1] and toppos - 10 >= item.area[1][0]) \
                        or (leftpos - 10 <= item2.area[0][1] and rightpos + 10 >= item2.area[0][0] and botpos - 10 <=
                            item2.area[1][1] and toppos + 10 >= item2.area[1][0]):
                    continue
                else:
                    break

        # Hendelse ved kollisjon mellom character og item
        if leftpos <= item.area[0][1] and rightpos >= item.area[0][0] and botpos <= item.area[1][1] and toppos >= \
                item.area[1][0] and not item_create:
            items.itemattributes_current = items.att1.copy()
            item_create = 1
        elif leftpos <= item2.area[0][1] and rightpos >= item2.area[0][0] and botpos <= item2.area[1][1] and toppos >= \
                item2.area[1][0] and not item_create:
            items.itemattributes_current = items.att2.copy()
            item_create = 1

        # ##########Lastfinish########## #
        # End game
        if toppos > border[1] or botpos < -border[1] or leftpos < -border[0] or rightpos > border[0] or stopplay:
            stopplay = 0
            startendplay = 1
            play = 0

        # Fps
        frame_end = time.time()
        while 1 / (frame_end - frame_beginning) > fpscap:
            frame_end = time.time()

        fps = 1 / (frame_end - frame_beginning)

        # if fps + 40 < fpscap and fps > 20:  # Setter stabil fps
        #     fpscounter += 1
        #     if fpscounter == 10:
        #         fpscap = fps + 20
        #         fpscounter = 0

        nowscore = items.itemattributes_current['score_tick']
        # Skrift over spill
        draw([-border[0] + 20, border[1] + 5], pen.write,
             str(f'Fps: {int(fps)}' + '\t' * 11 + f'Score: {score}\n{onesec_counter}\t{nowscore}\t{midtpos_gml}'),
             False,
             'left', ('Arial', 16))

    if startendplay:
        while keyboard.is_pressed('enter'):
            None

        # Skriver inn highscore
        with open('highscores.txt', 'a') as file_write:
            try:
                file_write.write(str(name) + '\n' + str(score) + '\n')
            except NameError:
                name = 'N/A'

        endgameborder = [border[0] * 0.4, border[1] * 0.4]

        # Tegner grense
        pen4.fillcolor('lightgrey')
        pen4.begin_fill()
        for k in range(4):
            draw([-endgameborder[0] + k, endgameborder[1] - k], figs.rectangle, (endgameborder[0] - k) * 2,
                 (endgameborder[1] - k) * 2, pen4, turt=pen4)
        pen4.end_fill()

        draw([0, 50], pen4.write, str('GAME OVER'), False, 'center', ('Algerian', 55), turt=pen4)
        draw([0, -5], pen4.write, str('Score: ' + str(score)), False, 'center', ('Copperplate Gothic Bold', 22),
             turt=pen4)
        draw([-176, -110], pen4.write, str('Play again'), False, 'left', ('Copperplate Gothic Bold', 18), turt=pen4)
        draw([55, -110], pen4.write, str('Go back'), False, 'left', ('Copperplate Gothic Bold', 18), turt=pen4)

        menuchoice = [-180, 35]
        menuchoice_index = 0

        startendplay = 0
        endplay = 1

    while endplay:
        turtle.update()
        pen3.clear()
        if keyboard.is_pressed('a') and menuchoice_index == 1:
            menuchoice_index = 0
        elif keyboard.is_pressed('d') and menuchoice_index == 0:
            menuchoice_index = 1

        if keyboard.is_pressed('enter'):
            if menuchoice_index == 0:
                endplay = 0
                startplay = 1
            elif menuchoice_index == 1:
                endplay = 0
                startmenu = 1

        start_draw([menuchoice[menuchoice_index], -77], pen3, 5)
        figs.rectangle(150, 40, pen3)
        stop_draw(pen3)

    if startmenu:
        while keyboard.is_pressed('enter'):
            None
        clear_all()

        start_draw([-91, 202], pen)
        pen.write('Start game', font=('Copperplate Gothic Bold', 22))
        start_draw([-91, 142], pen)
        pen.write('Highscore', font=('Copperplate Gothic Bold', 22))
        start_draw([-91, 82], pen)
        pen.write('Settings', font=('Copperplate Gothic Bold', 22))
        start_draw([-91, 22], pen)
        pen.write('End game', font=('Copperplate Gothic Bold', 22))

        norm.hideturtle()
        pen2.penup()
        menuchoice = [237, 177, 117, 57]
        menuchoice_index = 0
        menuchoice_index_old = 0
        menu = 1
        startmenu = 0

    while menu:
        turtle.update()
        pen2.clear()

        if menuchoice_index != menuchoice_index_old and (keyboard.is_pressed('s') or keyboard.is_pressed('w')):
            time.sleep(0.18)

        menuchoice_index_old = menuchoice_index

        if keyboard.is_pressed('s') and menuchoice_index < (len(menuchoice) - 1):
            menuchoice_index += 1
        elif keyboard.is_pressed('w') and menuchoice_index > 0:
            menuchoice_index -= 1
        elif keyboard.is_pressed('enter'):
            if menuchoice_index == 0:
                startbeforeplay = 1
            elif menuchoice_index == 1:
                starthighscore = 1
            elif menuchoice_index == 2:
                startsettings = 1
            elif menuchoice_index == 3:
                stopgame = 1
            menu = 0

        start_draw([-100, menuchoice[menuchoice_index]], pen2, 5)
        figs.rectangle(200, 40, pen2)
        stop_draw(pen2)

    if starthighscore:
        while keyboard.is_pressed('enter'):
            None

        clear_all()

        # highscorelist skal defineres etter spillet er ferdig!
        highscorelist_top5_name = highscorefun.read(returnedhighscore='name')
        highscorelist_top5_score = highscorefun.read(returnedhighscore='score')

        start_draw([-91, 202], pen)
        pen.write('Highscore', font=('Copperplate Gothic Bold', 22))
        start_draw([-160, 137], pen)
        pen.write('NAME:', font=('Copperplate Gothic Light', 19))
        start_draw([60, 137], pen)
        pen.write('SCORE:', font=('Copperplate Gothic Light', 19))

        highscore_ydraw = 92
        for k in range(len(highscorelist_top5_name)):
            start_draw([-195, highscore_ydraw], pen)
            pen.write(str(k + 1) + '.  ' + str(highscorelist_top5_name[k]), font=('Copperplate Gothic Light', 18))
            start_draw([60, highscore_ydraw], pen)
            pen.write(str(highscorelist_top5_score[k]), font=('Copperplate Gothic Light', 18))
            highscore_ydraw -= 43

        start_draw([-46, -180], pen)
        pen.write('Back', font=('Copperplate Gothic Bold', 22))

        highscore = 1
        starthighscore = 0

    while highscore:
        turtle.update()
        pen2.clear()

        start_draw([-60, -145], pen2, 5)
        figs.rectangle(110, 40, pen2)
        stop_draw(pen2)

        if keyboard.is_pressed('enter'):
            startmenu = 1
            highscore = 0

    if startsettings:
        while keyboard.is_pressed('enter'):
            None

        clear_all()

        start_draw([-91, 202], pen)
        pen.write('Resolution', font=('Copperplate Gothic Bold', 22))
        start_draw([-91, 142], pen)
        pen.write('Upcoming', font=('Copperplate Gothic Bold', 22))
        start_draw([-91, 82], pen)
        pen.write('Upcoming', font=('Copperplate Gothic Bold', 22))
        start_draw([-91, 22], pen)
        pen.write('Back', font=('Copperplate Gothic Bold', 22))

        norm.hideturtle()
        pen2.penup()
        menuchoice = [237, 177, 117, 57]
        menuchoice_index = 0
        menuchoice_index_old = 0
        settings = 1
        startsettings = 0

    while settings:
        turtle.update()
        pen2.clear()

        if menuchoice_index != menuchoice_index_old and (keyboard.is_pressed('s') or keyboard.is_pressed('w')):
            time.sleep(0.18)

        menuchoice_index_old = menuchoice_index

        if keyboard.is_pressed('s') and menuchoice_index < (len(menuchoice) - 1):
            menuchoice_index += 1
        elif keyboard.is_pressed('w') and menuchoice_index > 0:
            menuchoice_index -= 1
        elif keyboard.is_pressed('enter'):
            if menuchoice_index == 0:
                menuchoice_index == 1
            elif menuchoice_index == 1:
                menuchoice_index = 0
            elif menuchoice_index == 2:
                menuchoice_index = 0
            elif menuchoice_index == 3:
                startmenu = 1
            settings = 0

        start_draw([-100, menuchoice[menuchoice_index]], pen2, 5)
        figs.rectangle(200, 40, pen2)
        stop_draw(pen2)
