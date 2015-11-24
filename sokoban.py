#/usr/bin/python
# coding: utf-8

# 引入pygame库
import pygame, sys, os
from pygame.locals import *

#移动箱子在地图上的位置, level为地图列表, i为箱子位置
def move_box(level, i):
    #为空间或人-->箱子,否则-->箱子和目标重合
    if level[i] == '-' or level[i] == '@':
        level[i] ='$'
    else:
        level[i] = '*'

#移动人在地图中的位置,i为人的位置
def move_man(level, i):
    #空间或箱子-->人
    if level[i] == '-' or level[i] == '$':
        level[i] = '@'
    else:
        level[i] = '+'

#移动后位置重置
def move_floor(level, i):
    #如果原来为人或箱子,则标为空间,否则标为目标点
    if level[i] == '@' or level[i] == '$':
        level[i] = '-'
    else:
        level[i] = '.'

#获取位移量:d 移动方向.width为游戏窗口宽度
def get_offset(d, width):
    #d表示上下左右4种动作分别对应字典offset_map中的key
    offset_map = {'l': -1, 'u': -width, 'r': 1, 'd': width}
    return offset_map[d.lower()]

class Sokoban:
    # 初始化游戏
    def __init__(self):
        #设置地图
        file_data = []
        file1 = open("data.txt", "r")
        text_lines = file1.readlines()
        for eachline in text_lines:
            for word in eachline:
                if word in ('-','+','*','@','$','#','.'):
                    file_data += word

        file1.close()
        self.level = file_data
        #设置地图的宽度和高度以及人在地图中的位置
        #共19列
        self.w = 19

        #共11行
        self.h = 11

        # 人的初始化位置在self.level[163]
        self.man = 163

        # 使用solution记录每次移动,可用来实现撤销操作undo
        self.solution = []

        #记录推箱子的次数
        self.push = 0

        #使用todo记录撤销操作,用来实现重做操作tedo
        self.todo = []

    #画图,根据地图level将内容显示到pygame的窗口中
    def draw(self, screen, skin):

        # 获取每个图像元素的宽度
        w = skin.get_width() / 4

        # 遍历地图level中的每个字符元素
        for i in range(0, self.w):
            for j in range(0, self.h):
                #获取地图中的第j行第i列
                item = self.level[j*self.w + i]

                if item == '#':
                    screen.blit(skin, (i * w, j * w), (0, 2*w, w, w,))
                elif item == '-':
                    screen.blit(skin, (i * w, j * w), (0, 0, w, w))
                elif item == '$':
                    screen.blit(skin, (i * w, j * w), (2 * w, 0, w, w))
                elif item == '@':
                    screen.blit(skin, (i * w, j * w), (w, 0, w, w))
                elif item == ".":
                    screen.blit(skin, (i * w, j * w), (0, w, w, w))
                elif item == "*":
                    screen.blit(skin, (i * w, j * w), (2 * w, w, w, w))
                elif item == "+":
                    screen.blit(skin, (i * w, j * w), (w, w, w, w))

    #移动操作,d表示方向
    def move(self, d):
        #调用内部函数_move实现移动操作
        self._move(d)
        #重置todo列表,一旦有移动操作则重>做操作失效，
        # 重做操作只有在撤销操作后才可以被激活
        self.todo = []

        # 内部移动操作函数：用来更新移动操作后各个元素在地图中的位置变化，d表示移动的方向

    def _move(self, d):
        #获得移动在地图中的位移量 [***]
        h = get_offset(d, self.w)

        # 如果移动的目标区域为空间或目标点，则只需要移动人即可
        if self.level[self.man + h] == '-' or self.level[self.man + h] == '.':
            #移动人到目标位置
            move_man(self.level, self.man + h)
            #人移动后设置人原来的位置
            move_floor(self.level, self.man)
            #人所在新位置
            self.man += h
            #将移动操作存入solution
            self.solution += d

        #如果移动的目标区域为箱子，则需要移动箱子和人
        elif self.level[self.man + h] == '*' or self.level[self.man + h] == '$':
            # 箱子下一个位置和人所在位置的位移
            h2 = h * 2
            # 需要判断箱子下一个位置为空间或目标>点才可以移动
            if self.level[self.man + h2] == '-' or self.level[self.man + h2] == '.':

                move_box(self.level, self.man + h2)

                move_man(self.level, self.man + h)

                move_floor(self.level, self.man)

                self.man += h
                #移动操作标为大写,表示推了箱子
                self.solution += d.upper()
                #步骤+1
                self.push += 1

    # 撤销操作：撤销前一次移动的步骤
    def undo(self):
        #判断是否有移动记录
        if self.solution.__len__()>0:

            self.todo.append(self.solution[-1])

            self.solution.pop()

            h=get_offset(self.todo[-1],self.w)* -1

            if self.todo[-1].islower():

                move_man(self.level, self.man + h)

                move_floor(self.level, self.man)

                self.man += h

            else:

                move_floor(self.level,self.man-h)
                move_box(self.level,self.man)
                move_man(self.level,self.man+h)
                self.man+=h
                self.push-=1



    def redo(self):
        if self.todo.__len__()>0:
            self._move(self.todo[-1].lower())

            self.todo.pop()



def main():
    #启动并初始化pygame
    pygame.init()
    # 设置pygame显示puzzle = puzzlefilename.readlines()窗口大小为宽400,高300像素
    screen = pygame.display.set_mode((400, 300))

    #加载图像元素
    skinfilename = os.path.join('borgar.png')
    try:
        skin = pygame.image.load(skinfilename)
    except pygame.error, msg:
        print 'cannot load skin'
        raise SystemExit, msg
    skin = skin.convert()

    screen.fill(skin.get_at((0, 0)))

    pygame.display.set_caption('Sokoban')

    skb = Sokoban()
    skb.draw(screen, skin)

    clock = pygame.time.Clock()
    pygame.key.set_repeat(200, 50)

    while True:
        clock.tick(60)

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:

                if event.key == K_LEFT:
                    skb.move('l')
                    skb.draw(screen, skin)

                elif event.key == K_UP:
                    skb.move('u')
                    skb.draw(screen, skin)

                elif event.key == K_RIGHT:
                    skb.move('r')
                    skb.draw(screen, skin)

                elif event.key == K_DOWN:
                    skb.move('d')
                    skb.draw(screen, skin)

                elif event.key == K_BACKSPACE:
                    skb.undo()
                    skb.draw(screen, skin)

                elif event.key == K_SPACE:
                    skb.redo()
                    skb.draw(screen, skin)

        pygame.display.update()

        pygame.display.set_caption(skb.solution.__len__().__str__() + '/' + skb.push.__str__() + ' - Sokoban')

if __name__ == '__main__':
    main()





















