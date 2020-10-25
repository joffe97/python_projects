from collections import OrderedDict


def write(name, score):
    stopwhile = 0
    file_write = open('highscores.txt', 'a')

    while True:
        file_read = open('highscores.txt', 'r')
        if stopwhile == 1:
            file_read.close()
            break
        stopwhile = 1
        for file_line in file_read:
            if file_line[0:(len(file_line) - 1)] == name:
                name = input('Navn: ')
                stopwhile = 0

    file_write.write(name + '\n' + score + '\n')
    file_write.close()
    file_read.close()


def read(returnedhighscore='all'):
    highscores = {}
    file_counter = 0

    file_read = open('highscores.txt', 'r')

    for file_line in file_read:
        if file_counter % 2 == 0:
            file_singleword = file_line[0:(len(file_line) - 1)]
        elif file_counter % 2 == 1:
            file_singlescore = int(file_line[0:(len(file_line) - 1)])
            highscores[file_singleword] = file_singlescore
        file_counter += 1

    file_read.close()

    highscores = OrderedDict(sorted(highscores.items(), reverse=True, key=lambda x: x[1]))

    if returnedhighscore == 'all':
        return highscores

    # Top 5
    highscore_top5_counter = 0
    highscores_top5_name = []
    highscores_top5_score = []

    for k in highscores:
        if highscore_top5_counter == 5:
            break
        highscores_top5_name.append(k)
        highscores_top5_score.append(highscores[k])
        highscore_top5_counter += 1

    if returnedhighscore == 'name':
        return highscores_top5_name
    elif returnedhighscore == 'score':
        return highscores_top5_score
