if items.itemattributes_current['tales'] > talenumber:
    tale.append(players.Character('tale1', csize - 5 + items.itemattributes_current['size'], ccolor))
    talenumber += 1

for tales in range(items.itemattributes_current['tales']):
    tale[tales].size = character.size - 5

    if tales == 0:
        tale_distance[tales].append((character.size + tale.size) / 2)
        followmidtpos = midtpos
        followdirection = direction
    else:
        followmidtpos = tale[tales - 1].midtpos
        followdirection = tale[tales - 1].direction

    while True:
        if tale[tales].direction == 0:
            if followdirection == 0:  # Haleposisjon når retningen er opp
                if midtpos_gml[0] == followmidtpos[0]:
                    talepos = [norm.pos()[0], norm.pos()[1] - (character.size + tale.size) / 2]  # / 2
                    break
            else:
                if talepos[1] > midtpos[1]:  # Endrer retning på hale
                    tale.direction = followdirection
                    continue
                else:
                    talepos = [talepos[0], talepos[1] + hastighet]  # Holder haleretning frem til sving
                    break

        if tale[tales].direction == 90:
            if followdirection == 90:  # Haleposisjon når retningen er mot høyre
                if midtpos_gml[1] == midtpos[1]:
                    talepos = [norm.pos()[0] - (character.size + tale.size) / 2, norm.pos()[1]]
                    break
            else:
                if talepos[0] > midtpos[0]:  # Endrer retning på hale
                    tale.direction = followdirection
                    continue
                else:
                    talepos = [talepos[0] + hastighet, talepos[1]]  # Holder haleretning frem til sving
                    break

        if tale[tales].direction == 180:
            if followdirection == 180:  # Haleposisjon når retningen er ned
                if midtpos_gml[0] == midtpos[0]:
                    talepos = [norm.pos()[0], norm.pos()[1] + (character.size + tale.size) / 2]
                    break
            else:
                if talepos[1] < midtpos[1]:  # Endrer retning på hale
                    tale.direction = followdirection
                    continue
                else:
                    talepos = [talepos[0], talepos[1] - hastighet]  # Holder haleretning frem til sving
                    break

        if tale[tales].direction == 270:
            if followdirection == 270:  # Haleposisjon når retningen er mot høyre
                if midtpos_gml[1] == midtpos[1]:
                    talepos = [norm.pos()[0] + (character.size + tale.size) / 2, norm.pos()[1]]
                    break
            else:
                if talepos[0] < midtpos[0]:  # Endrer retning på hale
                    tale.direction = followdirection
                    continue
                else:
                    talepos = [talepos[0] - hastighet, talepos[1]]  # Holder haleretning frem til sving
                    break

        else:
            talepos = [0, 0]
            break

    tale[tales].drawtale(talepos)
    tale[tales].midtpos = talepos
