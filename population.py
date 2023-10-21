import copy
import time
import random
# from cocktail import Cocktail
from openpyxl import *


class Population():
    """docstring for Population"""

    def __init__(self, size, dist_metric=None):
        self.cocktails = []  # [Cocktail() for i in range(size)]
        self.dist_metric = dist_metric

    def get_cocktail(self, index):
        return self.cocktails[index]

    def save_cocktail(self, index, cocktail):
        # self.cocktails[index] = cocktail
        self.cocktails.append(cocktail)

    def population_size(self):
        return len(self.cocktails)

    def save_novelty(self, novelty):
        wb = Workbook()
        ws = wb.active
        for n in novelty:
            ws.append(n)

        wb.save('dist.xlsx')

    def set_novelty_optimized(self, new_cocktails):
        # print [n.novelty for n in self.cocktails]
        pop_size = len(new_cocktails)
        archive_size = len(self.cocktails)
        all_novelty = [[1.0 for i in range(archive_size)] for j in range(pop_size)]
        for i in range(pop_size):
            ck1 = new_cocktails[i].to_params_list()
            # print(i, ck1)
            for j in range(archive_size):
                try:
                    ck2 = self.cocktails[j].to_params_list()
                    dist = self.dist_metric.get_distance(ck1, ck2)
                    # print dist
                    all_novelty[i][j] = dist
                except:
                    pass
                    # print ("error", ck1, ck2)

        # print(all_novelty)
        for i in range(pop_size):
            k_nearest = sorted(list(set(filter(lambda a: a != 0.0, all_novelty[i]))))[:5]
            print sum(k_nearest)
            new_cocktails[i].novelty = sum(k_nearest) / 5.0
            if pop_size == archive_size:
                self.cocktails[i].novelty = sum(k_nearest) / 5.0
        # self.save_novelty(all_novelty)
        # print(all_novelty)

        self.cocktails.sort(key=lambda x: x.novelty, reverse=True)
        self.cocktails = self.cocktails[:pop_size-80]

        most_novel = []

        if pop_size != archive_size:
            for i in range(pop_size):
                nov = new_cocktails[i].novelty
                for j in range(archive_size):
                    if nov > self.cocktails[j].novelty:
                        most_novel.append(copy.deepcopy(new_cocktails[i]))
                        break

        # print [n.novelty for n in most_novel]
        most_novel.sort(key=lambda x: x.novelty, reverse=True)
        most_novel = most_novel[:archive_size]
        self.cocktails[archive_size-len(most_novel):] = list(most_novel)
        self.cocktails.sort(key=lambda x: x.novelty, reverse=True)
        print [n.novelty for n in self.cocktails]


        return new_cocktails

    def set_novelty(self):
        # self.dist_metric = DistanceMetric()
        len_tail = len(self.cocktails)
        all_novelty = [[1.0 for i in range(len_tail)] for j in range(len_tail)]
        for i in range(len_tail):
            ck1 = self.cocktails[i].to_params_list()
            # print(i, ck1)
            for j in range(i, len_tail):
                if i == j:
                    continue
                # start = time.time()

                try:
                    ck2 = self.cocktails[j].to_params_list()
                    dist = self.dist_metric.get_distance(ck1, ck2)
                    # print dist
                    # end = time.time()
                    # duration = end - start
                    # if duration > 0.5:
                        # print(ck1, ck2)
                        # print(j, dist)
                    all_novelty[i][j] = dist
                    all_novelty[j][i] = dist
                except:
                    pass
                    # print ("error", ck1, ck2)

        for i in range(len_tail):
            k_nearest = sorted(list(set(filter(lambda a: a != 0.0, all_novelty[i]))))[:20]
            # print sum(k_nearest) / 20.0
            self.cocktails[i].novelty = sum(k_nearest) / 20.0
        # self.save_novelty(all_novelty)
        # print(all_novelty)


    def get_fittest_cached(self):
        fittest = self.cocktails[0]
        for i in range(self.population_size()):
            # print(self.cocktails[i].get_novelty())
            if (fittest.get_novelty() < self.cocktails[i].get_novelty()):
                fittest = self.cocktails[i]
        return fittest

    def get_fittest_novel(self):
        fittest = self.cocktails[0]
        novel = fittest.get_novel(self.cocktails)
        for i in range(self.population_size()):
            curr_novel = self.cocktails[i].get_novel(self.cocktails)
            if (curr_novel > novel):
                fittest = self.cocktails[i]
                novel = curr_novel
        # print(novel)
        return fittest

    def get_fittest(self):
        fittest = self.cocktails[0]
        for i in range(self.population_size()):
            if (fittest.get_fitness() < self.cocktails[i].get_fitness()):
                fittest = self.cocktails[i]
        return fittest
