import pygame
import random
import math
pygame.init()

class DrawEverything:
    BLACK = 0,0,0
    WHITE = 255,255,255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    PADDING = 100
    BLUE = 0, 0, 255
    PADDING2 = 150
    GREYS = [
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192),
    ]

    FONT = pygame.font.SysFont('georiga', 30)
    LARGEFONT = pygame.font.SysFont('georiga', 40)
    
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("SORTING ALGORITHM")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_value = max(lst)
        self.min_value = min(lst)

        self.blockWidth = round((self.width - self.PADDING) / len(lst))
        self.blockHeight = (self.height - self.PADDING2) // (self.max_value - self.min_value)
        self.start_point = self.PADDING // 2

def draw(draw_everything, algoName, ascend):
    draw_everything.window.fill(draw_everything.WHITE)

    title = draw_everything.LARGEFONT.render(f"{algoName} - {'Ascending' if ascend else 'Descending'}", 1, draw_everything.BLUE)
    draw_everything.window.blit(title, (draw_everything.width/2 - title.get_width()/2, 5))
    
    directions = draw_everything.FONT.render("R - Change Order | SPACE - Start Sorting | A - Ascend | D - Descend", 1, draw_everything.BLACK)
    draw_everything.window.blit(directions, (draw_everything.width/2 - directions.get_width()/2, 45))

    sort = draw_everything.FONT.render("| I - Insertion Sort | B - Bubble Sort | S - Selection Sort |", 1, draw_everything.BLACK)
    draw_everything.window.blit(sort, (draw_everything.width/1.15 - directions.get_width()/1.15, 75))

    draw_list(draw_everything)
    pygame.display.update

def draw_list(draw_everything, color_position={}, clear_bg=False):
    lst = draw_everything.lst

    if clear_bg:
        clear_rect = (draw_everything.PADDING//2, draw_everything.PADDING2, draw_everything.width - draw_everything.PADDING, draw_everything.height - draw_everything.PADDING2)
        pygame.draw.rect(draw_everything.window, draw_everything.WHITE, clear_rect)
    
    for x, val in enumerate(lst):
        x = draw_everything.start_point + x *  draw_everything.blockWidth
        y = draw_everything.height - (val - draw_everything.min_value) * draw_everything.blockHeight

        color = draw_everything.GREYS[x % 3]

        if x in color_position:
            color = color_position[x]

        pygame.draw.rect(draw_everything.window, color, (x, y, draw_everything.blockWidth, draw_everything.height))
    
    if clear_bg:
        pygame.display.update()

def generateList(x, min_value, max_value):
    lst = []

    for _ in range(x):
        value = random.randint(min_value, max_value)
        lst.append(value)

    return lst

def bubbleSort(draw_everything, ascend=True):
    lst = draw_everything.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascend) or (num1 < num2 and not ascend):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_everything, {j: draw_everything.GREEN, j + 1: draw_everything.RED}, True)
                yield True
    return lst

def insertionSort(draw_everything, ascend=True):
    lst = draw_everything.lst

    for i in range(1, len(lst)):
        key = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > key and ascend
            descending_sort = i > 0 and lst[i-1] < key and not ascend

            if not ascending_sort and not descending_sort:
                break
                
            lst[i] = lst[i-1]
            i = i - 1
            lst[i] = key
            draw_list(draw_everything, {i - 1: draw_everything.BLUE, i: draw_everything.RED}, True)
            yield True

    return lst

def selectionSort(draw_everything, ascend=True):
    lst = draw_everything.lst
    
    for i in range(len(lst)):
          
        min_idx = i
        for j in range(i+1, len(lst)):
            if (lst[min_idx] > lst[j] and ascend) or (lst[min_idx] < lst[j] and not ascend):
                min_idx = j
                
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        draw_list(draw_everything, {i: draw_everything.BLUE, min_idx: draw_everything.RED}, True)
        yield True

    return lst


def main():
    run = True
    sort = False
    ascend = True
    clock = pygame.time.Clock()

    x = 50
    min_value = 0
    max_value = 100

    lst = generateList(x, min_value, max_value)
    draw_everything = DrawEverything(800, 600, lst)

    sorting_algo = bubbleSort
    sortingAlgoName = "Bubble Sort"
    sortingAlgoGen = None

    while run:
        clock.tick(120)
        
        if sort:
            try:
                next(sortingAlgoGen)
            except StopIteration:
                sort = False
        else:
            draw(draw_everything, sortingAlgoName, ascend)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generateList(x, min_value, max_value)
                draw_everything.set_list(lst)
                sort = False
            elif event.key == pygame.K_SPACE and sort == False:
                sort = True
                sortingAlgoGen = sorting_algo(draw_everything, ascend)
            elif event.key == pygame.K_a and sort == False:
                ascend = True
            elif event.key == pygame.K_d and sort == False:
                ascend = False
            elif event.key == pygame.K_i and sort == False:
                sorting_algo = insertionSort
                sortingAlgoName = " Insertion Sort "
            elif event.key == pygame.K_b and sort == False:
                sorting_algo = bubbleSort
                sortingAlgoName = " Bubble Sort "
            elif event.key == pygame.K_s and sort == False:
                sorting_algo = selectionSort
                sortingAlgoName = " Selection Sort "
                
    
    pygame.quit()

if __name__ == "__main__":
    main()