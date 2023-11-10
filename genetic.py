from datetime import datetime
from math import floor

import numpy as np
from pprint import pprint


class Genetic:
    def __init__(self, n_population, victims_list, wall_list, tlim):
        self.TLIM = tlim
        self.mutation_rate = 0.3

        self.n_population = n_population
        self.walled_positions = wall_list
        self.n_victims = len(victims_list)

        self.victim_dict_coordinate = self._generate_victims_dict(victims_list)
        # exit()
        self.victim_dict_distances = {}

        self.population = self.genesis()
        # print("1")
        self._generate_victims_dict_distances()

        # self.fitness_list = self.get_all_fitnes()

        # progenitors = self.progenitor_selection()

        # print(self.mate_population(progenitors))
        # self._run()

        # exit()

    def genesis(self):
        victim_list = np.array(list(self.victim_dict_coordinate.keys())[1:])
        population_set = []
        for i in range(self.n_population):
            # Randomly generating a new solution
            sol_i = np.append(np.append([0], victim_list[
                np.random.choice(list(range(self.n_victims)), self.n_victims, replace=False)]), [0])
            population_set.append(sol_i)
        return np.array(population_set)

    def _generate_victims_dict_distances(self):
        # not_computed_victims = list(self.victim_dict_coordinate.keys())
        for victim in self.victim_dict_coordinate.keys():
            self.victim_dict_distances[victim] = {}
            self._compute_distances_from_victim(victim)

    def _compute_distances_from_victim(self, victim):
        cont = 0
        possible_moves = [(0, -1), (1, 0), (0, 1), (-1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)]
        node = (self.victim_dict_coordinate[victim]["coord"], [])
        # if node[0] == (0, 0):
        #     return
        frontier = [node]
        explored = []
        while True:
            if len(frontier) == 0:
                return
            node = frontier.pop(0)
            explored.append(node[0])
            for action in possible_moves:
                child = ((node[0][0] + action[0], node[0][1] + action[1]), node[1] + [action])
                if child[0] not in self.walled_positions + explored + [n[0] for n in frontier]:
                    for vic, vic_info in self.victim_dict_coordinate.items():
                        if child[0] == vic_info["coord"]:
                            # if vic not in self.victim_dict_distances:
                            self.victim_dict_distances[victim][vic] = {"trajectory": child[1],
                                                                       "cost": self._calculate_trajectory_cost(child[1])}
                            cont += 1
                            # print(cont)
                        if cont == self.n_victims:
                            return
                    frontier.append(child)

    def _calculate_trajectory_cost(self, trajectory):
        cost = 0
        for move in trajectory:
            if move[0] != 0 and move[1] != 0:
                cost += 1.5
            else:
                cost += 1
        return cost

    def _generate_victims_dict(self, victims_list):
        victim_dict = {}
        i = 1
        victim_dict[0] = {"coord": (0, 0), "severity": 0}
        for victim in victims_list:
            victim_dict[i] = {"coord": victim[0], "severity": victim[1]}
            i = i + 1
        return victim_dict

    def _fitness_eval(self, victim_list):
        total = 0
        points = 0
        for i in range(self.n_victims - 1):
            a = victim_list[i]
            b = victim_list[i + 1]
            total += self.victim_dict_distances[a][b]["cost"]
        if total >= self.TLIM:
            del victim_list[-2]
            return self._fitness_eval(victim_list)
        # print(self.victim_dict_coordinate)
        for victim in victim_list:
            if self.victim_dict_coordinate[victim]["severity"] == 1:
                points += 6
            if self.victim_dict_coordinate[victim]["severity"] == 2:
                points += 3
            if self.victim_dict_coordinate[victim]["severity"] == 3:
                points += 2
            if self.victim_dict_coordinate[victim]["severity"] == 4:
                points += 1
        # print(fit)
        return points / total

    def _get_all_fitnes(self):
        fitnes_list = np.zeros(self.n_population)

        # Looping over all solutions computing the fitness for each solution
        # print(self.population)
        for i in range(self.n_population):
            fitnes_list[i] = self._fitness_eval(self.population[i])

        # print(fitnes_list)

        return fitnes_list

    def _progenitor_selection(self):
        total_fit = self.fitness_list.sum()
        #print(total_fit)
        #print("asdddddddddddddddddddddddddddddddddddddddddddddddddddddddd")
        if total_fit == 0:
            prob_list = np.zeros(self.n_population)
            for i in range(len(prob_list)):
                prob_list[i] = 1 / len(prob_list)
        else:
            prob_list = self.fitness_list / total_fit
        # print(prob_list)
        # exit()

        # Notice there is the chance that a progenitor. mates with oneself
        progenitor_list_a = np.random.choice(list(range(len(self.population))), len(self.population), p=prob_list,
                                             replace=True)
        progenitor_list_b = np.random.choice(list(range(len(self.population))), len(self.population), p=prob_list,
                                             replace=True)

        progenitor_list_a = self.population[progenitor_list_a]
        progenitor_list_b = self.population[progenitor_list_b]

        return np.array([progenitor_list_a, progenitor_list_b])

    def _mate_progenitors(self, prog_a, prog_b):
        offspring = prog_a[0:floor(self.n_victims / 2)]

        for victim in prog_b:

            if not victim in offspring:
                offspring = np.concatenate((offspring, [victim]))

        return np.append(offspring, [0])

    def _mate_population(self, progenitor_list):
        new_population_set = []
        for i in range(progenitor_list.shape[1]):
            prog_a, prog_b = progenitor_list[0][i], progenitor_list[1][i]
            offspring = self._mate_progenitors(prog_a, prog_b)
            new_population_set.append(offspring)

        return new_population_set

    def _mutate_offspring(self, offspring):
        for q in range(int(self.n_victims * self.mutation_rate)):
            a = np.random.randint(1, self.n_victims - 1)
            b = np.random.randint(1, self.n_victims - 1)

            offspring[a], offspring[b] = offspring[b], offspring[a]

        return offspring

    def _mutate_population(self, new_population_set):
        mutated_pop = []
        for offspring in new_population_set:
            mutated_pop.append(self._mutate_offspring(offspring))
        return np.array(mutated_pop)

    def run(self):
        self.fitness_list = self._get_all_fitnes()
        # mutated_pop = self.mutate_population(self.population)
        best_solution = [-1, 0, np.array([])]

        for i in range(1000):
            if i % 100 == 0: print(i, self.fitness_list.max(), self.fitness_list.mean(),
                                   datetime.now().strftime("%d/%m/%y %H:%M"))
            self.fitness_list = self._get_all_fitnes()

            # Saving the best solution
            if self.fitness_list.max() > best_solution[1]:
                best_solution[0] = i
                best_solution[1] = self.fitness_list.max()
                best_solution[2] = np.array(self.population)[self.fitness_list.max() == self.fitness_list]

            progenitor_list = self._progenitor_selection()
            new_population_set = self._mate_population(progenitor_list)
            self.population = self._mutate_population(new_population_set)

        return best_solution, self.victim_dict_distances
