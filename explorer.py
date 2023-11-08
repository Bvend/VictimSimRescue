## EXPLORER AGENT
### @Author: Tacla, UTFPR
### It walks randomly in the environment looking for victims.

import sys
import os
import random
from abstract_agent import AbstractAgent
from physical_agent import PhysAgent
from abc import ABC, abstractmethod

pos_vict = []


class Explorer(AbstractAgent):
    def __init__(self, env, config_file, resc):
        """ Construtor do agente random on-line
        @param env referencia o ambiente
        @config_file: the absolute path to the explorer's config file
        @param resc referencia o rescuer para poder acorda-lo
        """

        super().__init__(env, config_file)

        # Specific initialization for the rescuer
        self.resc = resc  # reference to the rescuer agent
        self.rtime = self.TLIM  # remaining time to explore

        self.victim = []

        self.dir = random.choice([0, 1, 2, 3]);  # ru, rd, ld, lu
        self.x = 0
        self.y = 0
        self.path = {}
        self.path[(0, 0)] = [0, (0, 0)]

    def deliberate(self) -> bool:
        """ The agent chooses the next action. The simulator calls this
        method at each cycle. Must be implemented in every agent"""

        # No more actions, time almost ended
        if self.rtime < 10.0:
            # time to wake up the rescuer
            # pass the walls and the victims (here, they're empty)
            print(f"{self.NAME} I believe I've remaining time of {self.rtime:.1f}")
            # self.resc.go_save_victims([],[])
            self.resc.body.set_state(PhysAgent.ENDED)  ##
            for vict in self.victim:
                if not ((self.x, self.y) in self.victim):
                    pos_vict.append(vict)
            return False

        # Check the neighborhood obstacles
        obstacles = self.body.check_obstacles()

        # Determines next position
        dx = 0
        dy = 0
        rand = random.choice(range(0, 8))
        if self.dir == 0:
            if rand < 3 or rand >= 6:
                dx = 1
            if rand >= 3:
                dy = -1
            if obstacles[0] != PhysAgent.CLEAR and obstacles[2] != PhysAgent.CLEAR:
                self.dir = 2
            elif obstacles[0] != PhysAgent.CLEAR:
                self.dir = 1
            elif obstacles[2] != PhysAgent.CLEAR:
                self.dir = 3
        elif self.dir == 1:
            if rand < 3 or rand >= 6:
                dx = 1
            if rand >= 3:
                dy = 1
            if obstacles[4] != PhysAgent.CLEAR and obstacles[2] != PhysAgent.CLEAR:
                self.dir = 3
            elif obstacles[4] != PhysAgent.CLEAR:
                self.dir = 0
            elif obstacles[2] != PhysAgent.CLEAR:
                self.dir = 2
        elif self.dir == 2:
            if rand < 3 or rand >= 6:
                dx = -1
            if rand >= 3:
                dy = 1
            if obstacles[4] != PhysAgent.CLEAR and obstacles[6] != PhysAgent.CLEAR:
                self.dir = 0
            elif obstacles[4] != PhysAgent.CLEAR:
                self.dir = 3
            elif obstacles[6] != PhysAgent.CLEAR:
                self.dir = 1
        else:
            if rand < 3 or rand >= 6:
                dx = -1
            if rand >= 3:
                dy = -1
            if obstacles[0] != PhysAgent.CLEAR and obstacles[6] != PhysAgent.CLEAR:
                self.dir = 1
            elif obstacles[0] != PhysAgent.CLEAR:
                self.dir = 2
            elif obstacles[6] != PhysAgent.CLEAR:
                self.dir = 0
        if dx == 0 and dy == -1 and obstacles[0] != PhysAgent.CLEAR \
                or dx == 1 and dy == -1 and obstacles[1] != PhysAgent.CLEAR \
                or dx == 1 and dy == 0 and obstacles[2] != PhysAgent.CLEAR \
                or dx == 1 and dy == 1 and obstacles[3] != PhysAgent.CLEAR \
                or dx == 0 and dy == 1 and obstacles[4] != PhysAgent.CLEAR \
                or dx == -1 and dy == 1 and obstacles[5] != PhysAgent.CLEAR \
                or dx == -1 and dy == 0 and obstacles[6] != PhysAgent.CLEAR \
                or dx == -1 and dy == -1 and obstacles[7] != PhysAgent.CLEAR:
            options = []
            for i in range(0, 8):
                if obstacles[i] == PhysAgent.CLEAR:
                    options.append(i)
            rand = random.choice(options)
            if rand == 0:
                dx = 0
                dy = -1
            elif rand == 1:
                dx = 1
                dy = -1
            elif rand == 2:
                dx = 1
                dy = 0
            elif rand == 3:
                dx = 1
                dy = 1
            elif rand == 4:
                dx = 0
                dy = 1
            elif rand == 5:
                dx = -1
                dy = 1
            elif rand == 6:
                dx = -1
                dy = 0
            else:
                dx = -1
                dy = -1
        if (self.x + dx, self.y + dy) in self.path:
            tx = [0, 1, 1, 1, 0, -1, -1, -1]
            ty = [-1, -1, 0, 1, 1, 1, 0, -1]
            options_ = []
            for i in range(0, 8):
                if obstacles[i] == PhysAgent.CLEAR and not ((self.x + tx[i], self.y + ty[i]) in self.path):
                    options_.append(i)
            if len(options_) != 0:
                rand = random.choice(options_)
                dx = tx[rand]
                dy = ty[rand]

        # Updates return path and costs
        tx = [0, 1, 1, 1, 0, -1, -1, -1]
        ty = [-1, -1, 0, 1, 1, 1, 0, -1]
        parent = self.path[(self.x, self.y)][1]
        for i in range(0, 8):
            if (self.x + tx[i], self.y + ty[i]) in self.path:
                if self.path[(self.x + tx[i], self.y + ty[i])][0] < self.path[parent][0]:
                    parent = (self.x + tx[i], self.y + ty[i])
        if parent != self.path[(self.x, self.y)][1]:
            if self.x != parent[0] and self.y != parent[1]:
                self.path[(self.x, self.y)][0] = self.path[parent][0] + self.COST_DIAG
            else:
                self.path[(self.x, self.y)][0] = self.path[parent][0] + self.COST_LINE
            self.path[(self.x, self.y)][1] = parent

        # Sets expected cost for the next position
        if not ((self.x + dx, self.y + dy) in self.path):
            if dx != 0 and dy != 0:
                cost = self.path[(self.x, self.y)][0] + self.COST_DIAG
            else:
                cost = self.path[(self.x, self.y)][0] + self.COST_LINE
            self.path[(self.x + dx, self.y + dy)] = [cost, (self.x, self.y)]

        # Considers returning to base
        if self.path[(self.x + dx, self.y + dy)][0] > self.rtime - self.COST_READ - 10.0:
            dx = self.path[(self.x, self.y)][1][0] - self.x
            dy = self.path[(self.x, self.y)][1][1] - self.y

        # Moves the body to another position
        self.x += dx
        self.y += dy
        result = self.body.walk(dx, dy)

        # Update remaining time
        if dx != 0 and dy != 0:
            self.rtime -= self.COST_DIAG
        else:
            self.rtime -= self.COST_LINE

        # Test the result of the walk action
        if result == PhysAgent.BUMPED:
            walls = 1  # build the map- to do
            # print(self.name() + ": wall or grid limit reached")

        if result == PhysAgent.EXECUTED:
            # check for victim returns -1 if there is no victim or the sequential
            # the sequential number of a found victim
            seq = self.body.check_for_victim()
            if seq >= 0:
                if not ((self.x, self.y) in self.victim):
                    vs = self.body.read_vital_signals(seq)
                    self.rtime -= self.COST_READ
                    # print("exp: read vital signals of " + str(seq))
                    # print(vs)
                    # self.victim[(self.x, self.y)] = seq                        ##
                    self.victim.append((self.x, self.y))

        return True

    @staticmethod
    def clustering():
        INF = 1123456789
        minx = INF
        miny = INF
        maxx = -INF
        maxy = -INF
        for vict in pos_vict:  # victms[i][0] eh o x e victims[i][1] eh o y
            if vict[0] < minx:
                minx = vict[0]
            if vict[1] < miny:
                miny = vict[1]
            if vict[0] > maxx:
                maxx = vict[0]
            if vict[1] > maxy:
                maxy = vict[1]
        max_iterations = 1123456
        current_it = 0
        updated_clusters = 1
        vict_cent = [-1 for i in range(len(pos_vict))]
        cent_coord = []
        for i in range(4):
            cent_coord.append((random.choice(range(minx, maxx + 1)), \
                               random.choice(range(miny, maxy + 1))))
        while updated_clusters and current_it < max_iterations:
            updated_clusters = 0
            current_it += 1
            new_vict_cent = []
            for i in range(len(pos_vict)):
                best_centroid = -1
                best_dist = INF
                for j in range(4):
                    dist = ((pos_vict[i][0] - cent_coord[j][0]) ** 2 + (pos_vict[i][1] - cent_coord[j][1]) ** 2) ** 0.5
                    if dist < best_dist:
                        best_centroid = j
                        best_dist = dist
                new_vict_cent.append(best_centroid)
            num_vict_in_cent = [0 for i in range(4)]
            for i in range(4):
                cent_coord[i] = (0, 0)
            for i in range(len(pos_vict)):
                if vict_cent[i] != new_vict_cent[i]:
                    updated_clusters = 1
                    vict_cent[i] = new_vict_cent[i]
                num_vict_in_cent[new_vict_cent[i]] += 1
                cent_coord[new_vict_cent[i]] = (cent_coord[new_vict_cent[i]][0] + pos_vict[i][0], \
                                                cent_coord[new_vict_cent[i]][1] + pos_vict[i][1])

            for i in range(4):
                if num_vict_in_cent[i] != 0:
                    cent_coord[i] = (cent_coord[i][0] / num_vict_in_cent[i], \
                                     cent_coord[i][1] / num_vict_in_cent[i])
        for i in range(miny, maxy + 1):
            for j in range(minx, maxx + 1):
                if (j, i) in pos_vict:
                    id = pos_vict.index((j, i))
                    print(f"{vict_cent[id]}", end="")
                else:
                    print(" ", end="")
            print("")
