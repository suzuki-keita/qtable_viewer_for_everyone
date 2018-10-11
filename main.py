#!/usr/local/bin python
# -*- coding:utf-8 -+-

import logging

import csv
import const
import pygame
import random
import math
import os
import glob
import sys
from pygame.locals import *
import map_date

args = sys.argv
if len(args) != 2:
    print("Error:引数にQtableのCSVファイルを指定してください!")
    sys.exit(1)
FILE_NAME = args[1]

SCR_RECT = Rect(0, 0, const.SCR_X, const.SCR_Y+const.Text_Y)   #Rect(left,top,width,height)
CS = const.CS
NUM_ROW = int(const.SCR_X / CS)   # フィールドの行数11
NUM_COL = int(const.SCR_Y / CS)  # フィールドの列数11

class main:

    def __init__(self):
        logging.basicConfig(format='%(levelname)s:%(thread)d:%(module)s:%(message)s', level=logging.DEBUG)
        pygame.init()
        self.screen = pygame.display.set_mode(SCR_RECT.size)   #以下、self.名称はアトリビュートを追加
        self.screen.fill((255,255,255))
        self.font = pygame.font.SysFont("timesnewroman",42)

        self.map = map_date.map_date()
        self.max_row = 0
        self.max_col = 0
        self.max_action = 0
        self.qtable_reader(FILE_NAME)
        self.draw(self.screen,os.path.basename(FILE_NAME))
        self.page = 0
        self.infomation = [0,0,0]
        while (1):
            pygame.time.Clock().tick(10000)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:  # 閉じるボタンが押されたら終了
                    pygame.quit()       # Pygameの終了(画面閉じられる)
                    sys.exit()
                elif event.type==KEYDOWN:   #キーを押したとき
                    if event.key==K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def qtable_reader(self,_name):
        #リマインド：ここらへんのコードめっちゃ汚くてキモいから誰か書き直して
        self.qtable = []
        self.table_length = 0
        self.map_f = []
        self.map_g = []
        self.map_h = []
        self.map_i = []
        self.map_e = []
        self.map_j = []
        self.map_k = []
        self.map_l = []
        self.map_m = []

        with open(_name,'r') as o:
            dataReader = csv.reader(o)
            for row in dataReader:
                if self.max_row < int(row[0]):
                    self.max_row = int(row[0])
                if self.max_col < int(row[1]):
                    self.max_col = int(row[1])
                if self.max_action < int(row[2]):
                    self.max_action = int(row[2])
        self.map.table_init(self.max_row, self.max_col, self.max_action)
        with open(_name, 'r') as o:
            dataReader = csv.reader(o)
            for row in dataReader:
                self.map.qtable_format = len(row)
                # q値を配列qtableに書き込み
                self.qtable.append(float(row[3]))
                if self.map.qtable_format == 15:
                    # QテーブルのF列を書き込み
                    self.map_f.append(float(row[5]))
                    # QテーブルのG列を書き込み
                    self.map_g.append(float(row[6]))
                    # QテーブルのH列を書き込み
                    self.map_h.append(float(row[7]))
                    # QテーブルのI列を書き込み
                    self.map_i.append(float(row[8]))
                    # QテーブルのE列を書き込み
                    self.map_e.append(float(row[4]))
                    # QテーブルのJ列を書き込み
                    self.map_j.append(float(row[9]))
                    # QテーブルのK列を書き込み
                    self.map_k.append(float(row[10]))
                    # QテーブルのL列を書き込み
                    self.map_l.append(float(row[11]))
                    # QテーブルのM列を書き込み
                    self.map_m.append(float(row[12]))
                    # start座標を書き込み
                    self.map.start_grid[0] = int(row[13])
                    self.map.start_grid[1] = int(row[14])
                # q_tableの長さ
                self.table_length = self.table_length + 1
        self.count_qtable = 0
        for x in range(1, self.max_row+1):
            for y in range(1, self.max_col+1):
                for action in range(self.max_action+1):
                    # self.qtable_c[x][y][action] = const.TRANCE_RATE*self.qtable[self.count_qtable]
                    # q値と状態、行動の対応を作成
                    self.map.qtable[x][y][action] = self.qtable[self.count_qtable]
                    if self.map.qtable_format == 15:
                        # 周囲9マスのマップデータと状態、行動の対応を作成
                        self.map.mapping_table[x][y][action][0] = self.map_f[self.count_qtable]
                        self.map.mapping_table[x][y][action][1] = self.map_g[self.count_qtable]
                        self.map.mapping_table[x][y][action][2] = self.map_h[self.count_qtable]
                        self.map.mapping_table[x][y][action][3] = self.map_i[self.count_qtable]
                        self.map.mapping_table[x][y][action][4] = self.map_e[self.count_qtable]
                        self.map.mapping_table[x][y][action][5] = self.map_j[self.count_qtable]
                        self.map.mapping_table[x][y][action][6] = self.map_k[self.count_qtable]
                        self.map.mapping_table[x][y][action][7] = self.map_l[self.count_qtable]
                        self.map.mapping_table[x][y][action][8] = self.map_m[self.count_qtable]
                    self.count_qtable = self.count_qtable + 1
        if self.map.qtable_format == 15:
            #goal座標を書き込み
            for x in range(1, self.max_row+1):
                for y in range(1, self.max_col+1):
                    if self.map.mapping_table[x][y][0][4] == const.GOAL:
                        self.map.goal_grid[0] = x
                        self.map.goal_grid[1] = y
                        break
            
            self.fin = self.map.follow_route()
            if self.fin == 0:
                return 0
            else:
                self.infomation = self.map.get_infomation()
                return 1

    def draw(self, screen,_name):
         self.screen.fill((255,255,255))
         sysfont = pygame.font.SysFont(None, 30)
         for x in range(1, self.max_row+1):
            for y in range(1, self.max_col+1):
                if self.map.qtable_format == 15:
                    #壁・路の色塗り
                    if self.map.mapping_table[x][y][0][4] == const.ROAD:
                        const.CS_COLOR = (255, 255, 255)
                    else:
                        const.CS_COLOR = (0, 0, 0)
                    pygame.draw.rect(screen,const.CS_COLOR,Rect((x-1)*CS+10,y*CS,CS,CS))
                else:
                    pygame.draw.rect(screen, (255, 255, 255),Rect((x-1)*CS+10, y*CS, CS, CS))

                if self.map.get_max_q_action_return_q(self.map.qtable,x,y) != 0:   #色を濃くしていく部分（元のサンプルコード）
                    val = self.map.get_max_q_action_return_q(self.map.qtable,x,y)
                    if val > 1:
                         val = 1
                    val *= 255.0   #複合演算子
                    color = (255,255-val,255-val)
                    pygame.draw.rect(screen,color,Rect((x-1)*CS+10,y*CS,CS,CS))
                    num = self.map.get_max_q_action(self.map.qtable,x,y)
                    direction = u""
                    if num==const.UP:
                        direction = u"↑"
                    elif num==const.DOWN:
                        direction = u"↓"
                    elif num==const.LEFT:
                        direction = u"←"
                    else:
                        direction = u"→"
                if self.map.qtable_format == 15:
                    #start地点の色塗り
                    if int(x) == int(self.map.start_grid[0]) and int(y) == int(self.map.start_grid[1]):
                        const.CS_COLOR = (255, 204, 0)
                        pygame.draw.rect(screen,const.CS_COLOR,Rect((x-1)*CS+10,y*CS,CS,CS))
                    #goal地点の色塗り
                    if int(x) == int(self.map.goal_grid[0]) and int(y) == int(self.map.goal_grid[1]):
                        const.CS_COLOR = (36, 193, 227)
                        pygame.draw.rect(screen,const.CS_COLOR,Rect((x-1)*CS+10,y*CS,CS,CS))

                if self.map.get_max_q_action_return_q(self.map.qtable,x,y) > 0 and self.map.get_max_q_prob(self.map.qtable,x,y) >= 0.9:
                    screen.blit(self.font.render(direction, True, (0,0,0)), ((x-1)*CS+10,y*CS))

                pygame.draw.rect(screen,(50,50,50),Rect((x-1)*CS+10,y*CS,CS,CS),1)
                if self.map.qtable_format == 15:
                    lengths = sysfont.render('lengths='+'%d' %self.infomation[0], False, (0,0,0))
                    rotation=sysfont.render('rotation='+'%d' %self.infomation[1], False, (0,0,0))
                    possibility=sysfont.render('possibility='+'%d' %self.infomation[2], False, (0,0,0))
                    self.screen.blit(lengths, (20, const.SCR_Y+35))
                    self.screen.blit(rotation, (20, const.SCR_Y+70))
                    self.screen.blit(possibility, (20, const.SCR_Y+105))
                filename = sysfont.render('file_name='+'%s' %_name, False, (0,0,0))
                self.screen.blit(filename, (20,const.SCR_Y+140))

    def write_qtable_information(self,_filename,_date):
        with open(_filename,mode="w") as w:
            writer = csv.writer(w, lineterminator='\n')
            writer.writerows(_date)
        return 1

if __name__ == '__main__':
    main()
