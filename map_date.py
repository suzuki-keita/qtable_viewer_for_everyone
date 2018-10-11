#!/usr/local/bin python
# -*- coding:utf-8 -+-
import main
import const
import random
import numpy as np

class map_date:
    def __init__(self):
        """
        mapping_table[x][y][action][direction]

        [direction] (x,y)が4の位置にあるときの周りのマップデータを示す。
        ０│１│２　
        ー＋ー＋ー
        ３│４│５
        ー＋ー＋ー
        ６│７│８
        """
        self.mapping_table = 0
        self.qtable = 0
        self.start_grid = [-1,-1]
        self.goal_grid = [-1,-1]
        self.qtable_format = 0 #15 = random_Q_learning用format
        self.route_x = []
        self.route_y = []
        self.max_row = 0
        self.max_col = 0
        self.max_action = 0

    def table_init(self,row,col,action):
        self.max_row = row
        self.max_col = col
        self.max_action = action
        self.mapping_table = np.zeros((self.max_row+1, self.max_col+1, self.max_action+1, const.MAP))
        self.qtable = np.zeros((self.max_row+1, self.max_col+1, self.max_action+1))
    
    def follow_route(self):
        #Q値情報を元にゴールまでのルートを作成する
        self.route_x = []
        self.route_y = []
        self.q = 0
        self.grid_x = self.start_grid[0]
        self.grid_y = self.start_grid[1]
        self.max = 0
        self.next_grid_x = 0
        self.next_grid_y = 0
        self.tmp = [0,0,0]
        self.goals_x = [self.goal_grid[0],self.goal_grid[0]-1,self.goal_grid[0]+1,self.goal_grid[0]]
        self.goals_y = [self.goal_grid[1]-1,self.goal_grid[1],self.goal_grid[1],self.goal_grid[1]+1]
        self.step = 0
        self.follow_fin = False
        while(self.step < 100):
            if self.goal_grid[0] == self.grid_x and self.goal_grid[1] == self.grid_y:
                self.follow_fin = True
                break
            self.route_x.append(self.grid_x)
            self.route_y.append(self.grid_y)
            self.action = self.get_max_q_action(self.qtable,self.grid_x,self.grid_y)
            self.grid_x,self.grid_y = self.get_direction_return_xy(self.grid_x,self.grid_y,self.action)
            self.step = self.step + 1
        if self.follow_fin == True:
            return 1
        else:
            return 0

    def get_direction_return_xy(self,_x,_y,_a):
        _x = int(_x)
        _y = int(_y)
        #エージェントの上下左右のみ検出
        if _a == const.UP:
            _x = _x
            _y = _y - 1
        elif _a == const.LEFT:
            _x = _x - 1
            _y = _y
        elif _a == const.RIGHT:
            _x = _x + 1
            _y = _y
        elif _a == const.DOWN:
            _x = _x
            _y = _y + 1
        if _x > self.max_row or _x < 0 or _y > self.max_col or _y < 0:
            return -1,-1
        else:
            return _x,_y
    """
    def get_direction_return_q(self,number,_qtable,_x,_y):
        #number_to_direction
        _x = int(_x)
        _y = int(_y)
        #エージェントの上下左右のみ検出
        if number == 1:
            _x = _x
            _y = _y - 1
        elif number == 3:
            _x = _x - 1
            _y = _y
        elif number == 5:
            _x = _x + 1
            _y = _y
        elif number == 7:
            _x = _x
            _y = _y + 1

        #データ整形
        if _x > const.S_NUM_ROW or _x < 0 or _y > const.S_NUM_COL or _y < 0:
            return 0.0,_x,_y
        else:
            return self.get_max_q_action_return_q(_qtable,_x,_y),_x,_y
    """
    def get_infomation(self):
        #各種情報を取得
        #経路長
        self.route_length = len(self.route_x)
        self.route_rotation = 0
        self.route_possibility = 0
        self.possibility_table = np.zeros((self.max_row+1, self.max_col+1))
        self.maps = []
        for i in range(0,self.route_length):
            #回転数
            #篠田のアドバイスで解決ゾロリ
            if i != self.route_length -1:
                if self.get_max_q_action(self.qtable,self.route_x[i],self.route_y[i]) != self.get_max_q_action(self.qtable,self.route_x[i+1],self.route_y[i+1]):
                    self.route_rotation = self.route_rotation + 1
            #エージェントが取り得る他の路
            #右
            x = self.route_x[i]+1
            y = self.route_y[i]
            if self.mapping_table[x][y][0][4] == const.ROAD:
                if str(x)+str(y) not in self.maps:
                    self.maps.append(str(x)+str(y))
                    self.route_possibility = self.route_possibility + 1

            #左
            x = self.route_x[i]-1
            y = self.route_y[i]
            if self.mapping_table[x][y][0][4] == const.ROAD:
                if str(x)+str(y) not in self.maps:
                    self.maps.append(str(x)+str(y))
                    self.route_possibility = self.route_possibility + 1
            #下
            x = self.route_x[i]
            y = self.route_y[i]+1
            if self.mapping_table[x][y][0][4] == const.ROAD:
                if str(x)+str(y) not in self.maps:
                    self.maps.append(str(x)+str(y))
                    self.route_possibility = self.route_possibility + 1

            #上
            x = self.route_x[i]
            y = self.route_y[i]-1
            if self.mapping_table[x][y][0][4] == const.ROAD:
                if str(x)+str(y) not in self.maps:
                    self.maps.append(str(x)+str(y))
                    self.route_possibility = self.route_possibility + 1

        for i in range(0, self.route_length):
            if str(self.route_x[i])+str(self.route_y[i]) in self.maps:
                self.route_possibility = self.route_possibility - 1
        return self.route_length,self.route_rotation,self.route_possibility

    def get_max_q_action(self,_qtable,_x,_y):
        m = 0.0
        action = 0
        for i in range(const.Action_no):
            if float(_qtable[_x][_y][i]) >= float(m):
                m = _qtable[_x][_y][i]
                action = i
        if _qtable[_x][_y][0] == 0.00 and _qtable[_x][_y][1] == 0.00 and _qtable[_x][_y][2] == 0.00 and _qtable[_x][_y][3] == 0.00 and _qtable[_x][_y][4] == 0.00:   #�e�s����Q�l��0�̏ꍇ
            i = random.randint(0,4)
        return action

    def get_max_q_action_return_q(self,_qtable,_x,_y):
        m = 0.0
        for i in range(const.Action_no):
            if float(_qtable[_x][_y][i]) >= float(m):
                m = _qtable[_x][_y][i]
        if _qtable[_x][_y][0] == 0.00 and _qtable[_x][_y][1] == 0.00 and _qtable[_x][_y][2] == 0.00 and _qtable[_x][_y][3] == 0.00 and _qtable[_x][_y][4] == 0.00:
            return 0
        return m

    def get_max_q_prob(self,_qtable,_x,_y):
        choosen = 0                  #ボルツマンによって選択された行動
        denom = 0                    #ボルツマンの分母
        prob = [0 for i in range(const.Action_no)] #それぞれの行動に対する確率
        posible_action = []
        max_prob = 0

        for act in range(const.Action_no):
            posible_action.append([act,_qtable[_x][_y][act]])

        for act in range(len(posible_action)):
            no = posible_action[act]
            tmp = no[1] / const.T
            denom = np.exp(tmp) + denom

        for act in range(len(posible_action)):
            no = posible_action[act]
            tmp = no[1] / const.T
            prob[act] =  np.exp(tmp) / denom
            if max_prob < prob[act]:
                max_prob = prob[act]

        return max_prob
