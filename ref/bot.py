import config
import telebot
import random
import time
import copy
from Initial_condition import white, black
from PIL import Image, ImageDraw


white_mod = white
black_mod = black
n2_spisok = ()
ur = 3
k_rez = 0
o_rez = 0
poz1_x = -1
f_hi = True

bot = telebot.TeleBot(config.TOKEN)
game_start = 0
smth = ''


def novaya_igra():
    global pole
    pole = [[0, 3, 0, 3, 0, 3, 0, 3],
            [3, 0, 3, 0, 3, 0, 3, 0],
            [0, 3, 0, 3, 0, 3, 0, 3],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]]


def vivod(a, b, x, y):
    for i in range(0, 8):
        for j in range(0, 8):
            if pole[i][j] == 3 or pole[i][j] == 4:
                break
            else:
                bot.send_message(smh, 'Игра окончена!\nЧтобы начать новую игру напиши /restart')
                novaya_igra()
                return
    field = Image.open('field.png')
    draw = ImageDraw.Draw(field)
    for i in range(0, 8):
        for j in range(0, 8):
            if pole[i][j] == 1:
                draw.ellipse((45 + (100 * j), 45 + (100 * i), 130 + (100 * j), 130 + (100 * i)), fill='white')
            elif pole[i][j] == 2:
                draw.ellipse((45 + (100 * j), 45 + (100 * i), 130 + (100 * j), 130 + (100 * i)), fill='white')
                draw.ellipse((66 + (100 * j), 66 + (100 * i), 109 + (100 * j), 109 + (100 * i)), fill='black')
            elif pole[i][j] == 3:
                draw.ellipse((45 + (100 * j), 45 + (100 * i), 130 + (100 * j), 130 + (100 * i)), fill='black')
            elif pole[i][j] == 4:
                draw.ellipse((45 + (100 * j), 45 + (100 * i), 130 + (100 * j), 130 + (100 * i)), fill='black')
                draw.ellipse((66 + (100 * j), 66 + (100 * i), 109 + (100 * j), 109 + (100 * i)), fill='white')
    field.save('field1.png', quality=100)
    field.close()


def spisok_hk():
    spisok = prosmotr_hodov_k1([])
    if not (spisok):
        spisok = prosmotr_hodov_k2([])
    return spisok


def prosmotr_hodov_k2(spisok):
    for y in range(8):
        for x in range(8):
            if pole[y][x] == 3:
                for ix, iy in (-1, 1), (1, 1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if pole[y + iy][x + ix] == 0:
                            spisok.append(((x, y), (x + ix, y + iy)))
                        if pole[y + iy][x + ix] == 1 or pole[y + iy][x + ix] == 2:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if pole[y + iy * 2][x + ix * 2] == 0:
                                    spisok.append(((x, y), (
                                    x + ix * 2, y + iy * 2)))
            if pole[y][x] == 4:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if pole[y + iy * i][x + ix * i] == 0:
                                spisok.append(((x, y), (x + ix * i, y + iy * i)))
                            if pole[y + iy * i][x + ix * i] == 1 or pole[y + iy * i][x + ix * i] == 2:
                                osh += 1
                            if pole[y + iy * i][x + ix * i] == 3 or pole[y + iy * i][x + ix * i] == 4 or osh == 2:
                                break
    return spisok


def proverka_hi(tur, spisok):
    global pole, k_rez, o_rez
    global ur
    if not (spisok):
        spisok = spisok_hi()

    if spisok:
        k_pole = copy.deepcopy(pole)
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in spisok:
            t_spisok = hod(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_spisok:
                proverka_hi(tur, t_spisok)
            else:
                if tur < ur:
                    proverka_hk(tur + 1, (), [])
                else:
                    s_k, s_i = skan()
                    o_rez += (s_k - s_i)
                    k_rez += 1

            pole = copy.deepcopy(k_pole)
    else:
        s_k, s_i = skan()
        o_rez += (s_k - s_i)
        k_rez += 1


def prosmotr_hodov_k1(spisok):
    for y in range(8):
        for x in range(8):
            spisok = prosmotr_hodov_k1p(spisok, x, y)
    return spisok


def proverka_hk(tur, n_spisok, spisok):
    global pole
    global n2_spisok
    global l_rez, k_rez, o_rez
    if not (spisok):
        spisok = spisok_hk()

    if spisok:
        k_pole = copy.deepcopy(pole)
        for ((poz1_x, poz1_y), (poz2_x, poz2_y)) in spisok:  # проходим все ходы по списку
            t_spisok = hod(0, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_spisok:
                proverka_hk(tur, (n_spisok + ((poz1_x, poz1_y),)), t_spisok)
            else:
                proverka_hi(tur, [])
                if tur == 1:
                    t_rez = o_rez / k_rez
                    if not (n2_spisok):
                        n2_spisok = (n_spisok + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        l_rez = t_rez
                    else:
                        if t_rez == l_rez:
                            n2_spisok = n2_spisok + (n_spisok + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                        if t_rez > l_rez:
                            n2_spisok = ()
                            n2_spisok = (n_spisok + ((poz1_x, poz1_y), (poz2_x, poz2_y)),)
                            l_rez = t_rez
                    o_rez = 0
                    k_rez = 0

            pole = copy.deepcopy(k_pole)
    else:
        s_k, s_i = skan()
        o_rez += (s_k - s_i)
        k_rez += 1


def skan():
    global pole
    s_i = 0
    s_k = 0
    for i in range(8):
        for ii in pole[i]:
            if ii == 1: s_i += 1
            if ii == 2: s_i += 3
            if ii == 3: s_k += 1
            if ii == 4: s_k += 3
    return s_k, s_i


def hod_kompjutera():  # !!!
    global f_hi
    global n2_spisok
    proverka_hk(1, (), [])
    if n2_spisok:
        kh = len(n2_spisok)
        th = random.randint(0, kh - 1)
        dh = len(n2_spisok[th])
        for h in n2_spisok:
            h = h
        for i in range(dh - 1):
            spisok = hod(1, n2_spisok[th][i][0], n2_spisok[th][i][1], n2_spisok[th][1 + i][0], n2_spisok[th][1 + i][1])
        n2_spisok = []
        f_hi = True

    s_k, s_i = skan()
    if not (s_i):
        soobsenie(2)
    elif not (s_k):
        soobsenie(1)
    elif f_hi and not (spisok_hi()):
        soobsenie(3)
    elif not (f_hi) and not (spisok_hk()):
        soobsenie(3)


def soobsenie(s):
    global f_hi
    z = 'Игра завершена'
    bot.send_message(smh, )
    vivod(-1, -1, -1, -1)
    f_hi = True


def hod_igroka():
    global poz1_x, poz1_y, poz2_x, poz2_y
    global f_hi
    f_hi = False
    spisok = spisok_hi()
    if spisok:
        if ((poz1_x, poz1_y), (poz2_x, poz2_y)) in spisok:
            t_spisok = hod(1, poz1_x, poz1_y, poz2_x, poz2_y)
            if t_spisok:
                f_hi = True
        else:
            f_hi = True


def prosmotr_hodov_i2(spisok):
    for y in range(8):
        for x in range(8):
            if pole[y][x] == 1:
                for ix, iy in (-1, -1), (1, -1):
                    if 0 <= y + iy <= 7 and 0 <= x + ix <= 7:
                        if pole[y + iy][x + ix] == 0:
                            spisok.append(((x, y), (x + ix, y + iy)))
                        if pole[y + iy][x + ix] == 3 or pole[y + iy][x + ix] == 4:
                            if 0 <= y + iy * 2 <= 7 and 0 <= x + ix * 2 <= 7:
                                if pole[y + iy * 2][x + ix * 2] == 0:
                                    spisok.append(((x, y), (
                                    x + ix * 2, y + iy * 2)))
            if pole[y][x] == 2:
                for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
                    osh = 0
                    for i in range(1, 8):
                        if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                            if pole[y + iy * i][x + ix * i] == 0:
                                spisok.append(((x, y), (x + ix * i, y + iy * i)))
                            if pole[y + iy * i][x + ix * i] == 3 or pole[y + iy * i][x + ix * i] == 4:
                                osh += 1
                            if pole[y + iy * i][x + ix * i] == 1 or pole[y + iy * i][x + ix * i] == 2 or osh == 2:
                                break
    return spisok


def hod(f, poz1_x, poz1_y, poz2_x, poz2_y):
    global pole
    if f: vivod(poz1_x, poz1_y, poz2_x, poz2_y)
    if poz2_y == 0 and pole[poz1_y][poz1_x] == 1:
        pole[poz1_y][poz1_x] = 2
    if poz2_y == 7 and pole[poz1_y][poz1_x] == 3:
        pole[poz1_y][poz1_x] = 4
    pole[poz2_y][poz2_x] = pole[poz1_y][poz1_x]
    pole[poz1_y][poz1_x] = 0
    kx = ky = 1
    if poz1_x < poz2_x: kx = -1
    if poz1_y < poz2_y: ky = -1
    x_poz, y_poz = poz2_x, poz2_y
    while (poz1_x != x_poz) or (poz1_y != y_poz):
        x_poz += kx
        y_poz += ky
        if pole[y_poz][x_poz] != 0:
            pole[y_poz][x_poz] = 0
            if f: vivod(-1, -1, -1, -1)
            if pole[poz2_y][poz2_x] == 3 or pole[poz2_y][poz2_x] == 4:
                return prosmotr_hodov_k1p([], poz2_x, poz2_y)
            elif pole[poz2_y][poz2_x] == 1 or pole[poz2_y][poz2_x] == 2:
                return prosmotr_hodov_i1p([], poz2_x, poz2_y)
    if f: vivod(poz1_x, poz1_y, poz2_x, poz2_y)


def prosmotr_hodov_k1p(spisok, x, y):
    if pole[y][x] == 3:
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if pole[y + iy][x + ix] == 1 or pole[y + iy][x + ix] == 2:
                    if pole[y + iy + iy][x + ix + ix] == 0:
                        spisok.append(((x, y), (x + ix + ix, y + iy + iy)))
    if pole[y][x] == 4:
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0
            for i in range(1, 8):
                if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                    if osh == 1:
                        spisok.append(((x, y), (x + ix * i, y + iy * i)))
                    if pole[y + iy * i][x + ix * i] == 1 or pole[y + iy * i][x + ix * i] == 2:
                        osh += 1
                    if pole[y + iy * i][x + ix * i] == 3 or pole[y + iy * i][x + ix * i] == 4 or osh == 2:
                        if osh > 0: spisok.pop()
                        break
    return spisok


def spisok_hi():
    spisok = prosmotr_hodov_i1([])
    if not (spisok):
        spisok = prosmotr_hodov_i2([])
    return spisok


def prosmotr_hodov_i1(spisok):
    spisok = []
    for y in range(8):
        for x in range(8):
            spisok = prosmotr_hodov_i1p(spisok, x, y)
    return spisok


def prosmotr_hodov_i1p(spisok, x, y):
    if pole[y][x] == 1:
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            if 0 <= y + iy + iy <= 7 and 0 <= x + ix + ix <= 7:
                if pole[y + iy][x + ix] == 3 or pole[y + iy][x + ix] == 4:
                    if pole[y + iy + iy][x + ix + ix] == 0:
                        spisok.append(((x, y), (x + ix + ix, y + iy + iy)))
    if pole[y][x] == 2:
        for ix, iy in (-1, -1), (-1, 1), (1, -1), (1, 1):
            osh = 0
            for i in range(1, 8):
                if 0 <= y + iy * i <= 7 and 0 <= x + ix * i <= 7:
                    if osh == 1:
                        spisok.append(((x, y), (x + ix * i, y + iy * i)))
                    if pole[y + iy * i][x + ix * i] == 3 or pole[y + iy * i][x + ix * i] == 4:
                        osh += 1
                    if pole[y + iy * i][x + ix * i] == 1 or pole[y + iy * i][x + ix * i] == 2 or osh == 2:
                        if osh > 0: spisok.pop()
                        break
    return spisok


#bot.message_handler(commands=['level'])
#def level(message):
#    global ur
#    bot.send_message(smh, 'Ты можешь выбрать один из 3 уровней сложности!')


@bot.message_handler(commands=['restart'])
def restart(message):
    novaya_igra()
    bot.send_message(smh, 'Вы начали заново!')
    p = open('field2.png', 'rb')
    bot.send_photo(int(smh), p)


@bot.message_handler(commands=['start'])
def start(message):
    global smh
    smh = message.chat.id
    bot.send_message(message.chat.id, 'Привет!\nЯ - бот для игры в шашки против компьютера. Чтобы '
                                      'сыграть в шашки напиши /game.\nИспользуя /re')


@bot.message_handler(commands=['game'])
def game(message):
    global smh
    smh = message.chat.id
    p = open('field2.png', 'rb')
    bot.send_photo(int(smh), p)
    bot.send_message(message.chat.id, 'Игра началась! Чтобы ходить используй такой шаблон, иначе я тебя не пойму. '
                                      'Первое сообщение вида: \na3 \nЭто выбранная шашка которой хочешь пойти. Затем '
                                      'вторым сообщением такого же вида: \nb4 \nТы указываешь клетку на которую хочешь '
                                      'переместить шашку. Чтобы начать игру заново напиши: /restart')


@bot.message_handler(content_types=['photo'])
def photo(message):
    bot.send_message(smh, 'Ничего не понял')


@bot.message_handler(content_types=['text'])
def pozici_2(message):
    global poz1_x, poz1_y, poz2_x, poz2_y, x, y
    global f_hi
    global smh
    global idk
    idk = message.text
    smh = message.chat.id
    smth = message.text
    if len(smth) != 2:
        bot.send_message(message.chat.id, 'Я тебя не понимаю. Для хода напиши начальные'
                                          ' координаты пешки, а затем и координаты на которые хочешь пойти, '
                                          'в таком формате a3, следующим сообщением b4, '
                                          'где a3 - начальные координаты пешки, b4 - конечные')
        return
    else:
        if (smth[0] == 'a' or smth[0] == 'b' or smth[0] == 'c' or smth[0] == 'd' or smth[0] == 'e' or smth[0] == 'f' or smth[0] == 'g' or smth[0] == 'h'):
            if (smth[1] == '1' or smth[1] == '2' or smth[1] == '3' or smth[1] == '4' or smth[1] == '5' or smth[1] == '6' or smth[1] == '7' or smth[1] == '8'):
                if smth[0] == 'a':
                    x = 0
                elif smth[0] == 'b':
                    x = 1
                elif smth[0] == 'c':
                    x = 2
                elif smth[0] == 'd':
                    x = 3
                elif smth[0] == 'e':
                    x = 4
                elif smth[0] == 'f':
                    x = 5
                elif smth[0] == 'g':
                    x = 6
                elif smth[0] == 'h':
                    x = 7
                else:
                    bot.send_message(message.chat.id, 'Я тебя не понимаю. Для хода напиши начальные'
                                                      ' координаты пешки, а затем и координаты на которые хочешь пойти, '
                                                      'в таком формате a3, следующим сообщением b4, '
                                                      'где a3 - начальные координаты пешки, b4 - конечные')
                if smth[1] == '1':
                    y = 7
                elif smth[1] == '2':
                    y = 6
                elif smth[1] == '3':
                    y = 5
                elif smth[1] == '4':
                    y = 4
                elif smth[1] == '5':
                    y = 3
                elif smth[1] == '6':
                    y = 2
                elif smth[1] == '7':
                    y = 1
                elif smth[1] == '8':
                    y = 0
                else:
                    bot.send_message(message.chat.id, 'Я тебя не понимаю. Для хода напиши начальные'
                                                      ' координаты пешки, а затем и координаты на которые хочешь '
                                                      'пойти, в таком формате a3, следующим сообщением b4, '
                                                      'где a3 - начальные координаты пешки, b4 - конечные')

    if pole[y][x] == 1 or pole[y][x] == 2:
        print(x, y)
        poz1_x, poz1_y = x, y
    else:
        if poz1_x != -1:
            poz2_x, poz2_y = x, y
            if f_hi:
                hod_igroka()
                sender()
                bot.send_message(message.chat.id, 'Компьютер думает...')
                if not (f_hi):
                    time.sleep(0.5)
                    hod_kompjutera()
                    sender()
                    bot.send_message(message.chat.id, 'Твой ход!')
            poz1_x = -1


def sender():
    p = open('field1.png', 'rb')
    bot.send_photo(int(smh), p)


novaya_igra()
bot.polling(none_stop=True)
