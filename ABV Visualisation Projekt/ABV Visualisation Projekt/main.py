import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from PIL import Image
import numpy as np


n = int(input("Enter length of graph for Celtic knot : "))
m = int(input("Enter width of graph for Celtic Knot : "))
size_of_draw = 100
if n * m >= 40:
    size_of_draw = 50
elif n * m >= 100:
    size_of_draw = 25
img = [[(1., 1., 1.) for i in range(2 * m * size_of_draw)] for j in range(2 * n * size_of_draw)]


def rotate_square_array(a):
    new = [[(0, 0, 0) for i in range(len(a))] for j in range(len(a))]
    for i in range(len(a)):
        for j in range(len(a)):
            new[i][j] = a[-j][i]
    return new


def rotate_directions(d):
    ans = []
    ans.append((-d[0][1], d[0][0]))
    ans.append((-d[1][1], d[1][0]))
    return ans


def plot(f, domain=[0, 2 * m, 0, 2 * n], res=(2 * size_of_draw * m, 2 * size_of_draw * n)):
    left = domain[0]
    right = domain[1]
    bottom = domain[2]
    top = domain[3]
    img = [[(1., 1., 1.) for i in range(res[0])] for j in range(res[1])]

    column_width = res[0] // right
    line_length = res[1] // top

    for x in range(0, res[1], line_length):
        for y in range(res[0]):
            img[x][y] = (0, 0, 0)

    for y in range(0, res[0], column_width):
        for x in range(res[1]):
            img[x][y] = (0, 0, 0)

    for cy in range(0, res[0], column_width):
        for cx in range(0, res[1], line_length):
            cn = cy // column_width
            cm = cx // line_length
            sector_img = drawings[list_of_states[cm][cn][0] - 1]
            for i in range(list_of_states[cm][cn][1]):
                sector_img = rotate_square_array(sector_img)
            for x in range(1, size_of_draw):
                for y in range(1, size_of_draw):
                    img[cx + x][cy + y] = sector_img[x][y]
                    if img[cx + x][cy + y] == (1., 0, 0) and count_colors != 1:
                        color = (list_of_colors[cm][cn] - 1) / (count_colors - 1)
                        img[cx + x][cy + y] = (color, 0, 1 - color)
            if cn * cm != 0 and (cn + cm) % 2 and cn != 2 * m and cm != 2 * n:
                for x in range(cx - size_of_draw // 6, cx + size_of_draw // 14):
                    for y in range(cy - size_of_draw // 6, cy + size_of_draw // 14):
                        if (x - cx) ** 2 + (y - cy) ** 2 < (size_of_draw // 14) ** 2:
                            img[x][y] = (0, 1., 0)
    plt.imshow(img, extent=domain)


def colorize(ld):
    lc = [[0 for i in range(2 * m)] for j in range(2 * n)]
    color_counter = 0
    for i in range(len(ld)):
        for j in range(len(ld[0])):
            prev_move = (ld[i][j][0][0], ld[i][j][0][1])
            item = (j, i)
            direction = ld[item[1]][item[0]][0]
            if direction == prev_move or item[0] + direction[0] >= len(lc[0]) or item[1] + direction[1] >= len(
                    lc):
                direction = ld[item[1]][item[0]][1]
            item = (item[0] + direction[0], item[1] + direction[1])
            prev_move = (-direction[0], -direction[1])
            if lc[item[1]][item[0]] == 0:
                color_counter += 1
            while lc[item[1]][item[0]] == 0:
                lc[item[1]][item[0]] = color_counter
                direction = ld[item[1]][item[0]][0]
                if direction == prev_move or item[0] + direction[0] >= len(lc[0]) or item[1] + direction[1] >= len(lc):
                    direction = ld[item[1]][item[0]][1]
                item = (item[0] + direction[0], item[1] + direction[1])
                prev_move = (-direction[0], -direction[1])
    return (lc, color_counter)


def update_direction(x, y):
    direction = drawings_directions[list_of_states[x][y][0] - 1]
    for _ in range(list_of_states[x][y][1]):
        direction = rotate_directions(direction)
    list_of_directions[x][y] = direction


def set_barrier(x, y, domain=[0, 2 * m, 0, 2 * n]):
    x = np.round(x).astype(int)
    y = np.round(y).astype(int)
    if x * y != 0 and (x + y) % 2 and y != 2 * n and x != 2 * m:
        y = 2 * n - y
        #vertical barrier
        if list_of_states[y][x] == (2, 3) or list_of_states[y][x] == (7, 1):
            list_of_states[y][x] = (5, 1)
        elif list_of_states[y][x] == (4, 1):
            list_of_states[y][x] = (7, 3)
        elif list_of_states[y][x] == (4, 3):
            list_of_states[y][x] = (2, 1)
        elif list_of_states[y][x] == (3, 0) or list_of_states[y][x] == (6, 2):
            list_of_states[y][x] = (1, 0)
        #horisontal barrier
        elif list_of_states[y][x] == (5, 1):
            list_of_states[y][x] = (1, 2)
        elif list_of_states[y][x] == (2, 1):
            list_of_states[y][x] = (6, 0)
        elif list_of_states[y][x] == (1, 0):
            list_of_states[y][x] = (5, 0)
        elif list_of_states[y][x] == (7, 3):
            list_of_states[y][x] = (3, 2)
        #crossing
        elif list_of_states[y][x] == (6, 0):
            list_of_states[y][x] = (4, 3)
        elif list_of_states[y][x] == (5, 0):
            if x % 2 == 0:
                list_of_states[y][x] = (3, 0)
            else:
                list_of_states[y][x] = (6, 2)
        elif list_of_states[y][x] == (1, 2):
            if x % 2 == 0:
                list_of_states[y][x] = (7, 1)
            else:
                list_of_states[y][x] = (2, 3)
        elif list_of_states[y][x] == (3, 2):
            list_of_states[y][x] = (4, 1)
        update_direction(y, x)

        #vertical barrier
        if list_of_states[y - 1][x] == (3, 3) or list_of_states[y - 1][x] == (6, 1):
            list_of_states[y - 1][x] = (5, 1)
        elif list_of_states[y - 1][x] == (4, 0):
            list_of_states[y - 1][x] = (3, 1)
        elif list_of_states[y - 1][x] == (4, 2):
            list_of_states[y - 1][x] = (6, 3)
        elif list_of_states[y - 1][x] == (2, 2) or list_of_states[y - 1][x] == (7, 0):
            list_of_states[y - 1][x] = (1, 1)
        #horizontal barrier
        elif list_of_states[y - 1][x] == (5, 1):
            list_of_states[y - 1][x] = (1, 3)
        elif list_of_states[y - 1][x] == (3, 1):
            list_of_states[y - 1][x] = (7, 2)
        elif list_of_states[y - 1][x] == (1, 1):
            list_of_states[y - 1][x] = (5, 0)
        elif list_of_states[y - 1][x] == (6, 3):
            list_of_states[y - 1][x] = (2, 0)
        #crossing
        elif list_of_states[y - 1][x] == (7, 2):
            list_of_states[y - 1][x] = (4, 0)
        elif list_of_states[y - 1][x] == (5, 0):
            if x % 2:
                list_of_states[y - 1][x] = (7, 0)
            else:
                list_of_states[y - 1][x] = (2, 2)
        elif list_of_states[y - 1][x] == (1, 3):
            if x % 2:
                list_of_states[y - 1][x] = (3, 3)
            else:
                list_of_states[y - 1][x] = (6, 1)
        elif list_of_states[y - 1][x] == (2, 0):
            list_of_states[y - 1][x] = (4, 2)
        update_direction(y - 1, x)
        #vertical barrier
        if list_of_states[y - 1][x - 1] == (3, 2) or list_of_states[y - 1][x - 1] == (6, 0):
            list_of_states[y - 1][x - 1] = (1, 2)
        elif list_of_states[y - 1][x - 1] == (4, 3):
            list_of_states[y - 1][x - 1] = (7, 1)
        elif list_of_states[y - 1][x - 1] == (4, 1):
            list_of_states[y - 1][x - 1] = (2, 3)
        elif list_of_states[y - 1][x - 1] == (2, 1) or list_of_states[y - 1][x - 1] == (7, 3):
            list_of_states[y - 1][x - 1] = (5, 1)
        #horizontal barrier
        elif list_of_states[y - 1][x - 1] == (5, 1):
            list_of_states[y - 1][x - 1] = (1, 0)
        elif list_of_states[y - 1][x - 1] == (2, 3):
            list_of_states[y - 1][x - 1] = (6, 2)
        elif list_of_states[y - 1][x - 1] == (1, 2):
            list_of_states[y - 1][x - 1] = (5, 0)
        elif list_of_states[y - 1][x - 1] == (7, 1):
            list_of_states[y - 1][x - 1] = (3, 0)
        #crossing
        elif list_of_states[y - 1][x - 1] == (6, 2):
            list_of_states[y - 1][x - 1] = (4, 1)
        elif list_of_states[y - 1][x - 1] == (5, 0):
            if x % 2:
                list_of_states[y - 1][x - 1] = (6, 0)
            else:
                list_of_states[y - 1][x - 1] = (3, 2)
        elif list_of_states[y - 1][x - 1] == (3, 0):
            list_of_states[y - 1][x - 1] = (4, 3)
        elif list_of_states[y - 1][x - 1] == (1, 0):
            if x % 2:
                list_of_states[y - 1][x - 1] = (2, 1)
            else:
                list_of_states[y - 1][x - 1] = (7, 3)
        update_direction(y - 1, x - 1)
        #vertical barrier
        if list_of_states[y][x - 1] == (4, 0):
            list_of_states[y][x - 1] = (6, 1)
        elif list_of_states[y][x - 1] == (4, 2):
            list_of_states[y][x - 1] = (3, 3)
        elif list_of_states[y][x - 1] == (2, 0) or list_of_states[y][x - 1] == (7, 2):
            list_of_states[y][x - 1] = (1, 3)
        elif list_of_states[y][x - 1] == (3, 1) or list_of_states[y][x - 1] == (6, 3):
            list_of_states[y][x - 1] = (5, 1)
        #horizontal barrier
        elif list_of_states[y][x - 1] == (5, 1):
            list_of_states[y][x - 1] = (1, 1)
        elif list_of_states[y][x - 1] == (3, 3):
            list_of_states[y][x - 1] = (7, 0)
        elif list_of_states[y][x - 1] == (1, 3):
            list_of_states[y][x - 1] = (5, 0)
        elif list_of_states[y][x - 1] == (6, 1):
            list_of_states[y][x - 1] = (2, 2)
        #crossing
        elif list_of_states[y][x - 1] == (7, 0):
            list_of_states[y][x - 1] = (4, 2)
        elif list_of_states[y][x - 1] == (5, 0):
            if x % 2:
                list_of_states[y][x - 1] = (7, 2)
            else:
                list_of_states[y][x - 1] = (2, 0)
        elif list_of_states[y][x - 1] == (2, 2):
            list_of_states[y][x - 1] = (4, 0)
        elif list_of_states[y][x - 1] == (1, 1):
            if x % 2:
                list_of_states[y][x - 1] = (3, 1)
            else:
                list_of_states[y][x - 1] = (6, 3)
        update_direction(y, x - 1)
        global list_of_colors, count_colors
        list_of_colors, count_colors = colorize(list_of_directions)
        plt.clf()
        plot(lambda z:z)


def import_png(image_path, mirror=False):
    img_1 = [[(1., 1., 1.) for i in range(size_of_draw)] for j in range(size_of_draw)]
    image = Image.open(image_path)
    image_array = np.array(image)
    for x in range(size_of_draw):
        for y in range(size_of_draw):
            ix = int(np.round(x / (size_of_draw - 1) * 899))
            iy = int(np.round(y / (size_of_draw - 1) * 899))
            color = image_array[ix, iy]
            if mirror:
                img_1[size_of_draw - x - 1][y] = (color[0] / 255, color[1] / 255, color[2] / 255)
            else:
                img_1[x][y] = (color[0] / 255, color[1] / 255, color[2] / 255)
    return img_1


def on_click(event):
    if event.button is MouseButton.LEFT:
        set_barrier(event.xdata, event.ydata)


even_line = [(2, 1)] + [(4, 2), (4, 3)] * (m - 1) + [(3, 3)]
odd_line = [(3, 1)] + [(4, 1), (4, 0)] * (m - 1) + [(2, 3)]
list_of_states = ([[(1, 1)] + [(3, 2), (2, 2)] * (m - 1) + [(1, 2)]] +
                  [odd_line[:] if i % 2 else even_line[:] for i in range(2 * n - 2)] +
                  [[(1, 0)] + [(2, 0), (3, 0)] * (m - 1) + [(1, 3)]])

drawings_directions = list()
drawings_directions.append([(1, 0), (0, -1)])
drawings_directions.append([(-1, 0), (1, -1)])
drawings_directions.append([(-1, -1), (1, 0)])
drawings_directions.append([(-1, 1), (1, -1)])
drawings_directions.append([(-1, 0), (1, 0)])
drawings_directions.append([(-1, 0), (1, 1)])
drawings_directions.append([(-1, 1), (1, 0)])
list_of_directions = []
for i in range(2 * n):
    list_of_directions.append([])
    for j in range(2 * m):
        direction = drawings_directions[list_of_states[i][j][0] - 1]
        for _ in range(list_of_states[i][j][1]):
            direction = rotate_directions(direction)
        list_of_directions[-1].append(direction)


list_of_colors, count_colors = colorize(list_of_directions)


drawings = []
drawings.append(import_png('Img1_2.png'))
drawings.append(import_png('Img2_2.png'))
drawings.append(import_png('Img3_2.png'))
drawings.append(import_png('Img4_2.png'))
drawings.append(import_png('Img5_2.png'))
drawings.append(import_png('Img2_2.png', 1))
drawings.append(import_png('Img3_2.png', 1))


plt.ion()
plt.connect('button_press_event', on_click)
plot(lambda z: z)
while True:
    plt.pause(1)
