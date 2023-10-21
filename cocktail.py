import re
# from reagent import Reagent
# from metrics import DistanceMetric


class Cocktail():
    """docstring for Cocktail"""

    default_gene_length = 3

    def __init__(self, score=[0, 0]):
        self.candidate = [0 for i in range(Cocktail.default_gene_length)]
        self.fitness = 0.0
        self.novelty = 0.0
        self.parent = {}
        self.score = score
        self.fingerprint_cached = None

    def get_buffer(self):
        return (self.candidate[1].name + " " + self.candidate[2].name).upper()

    def to_list(self):
        a = [str(c.name).strip().upper() for c in self.candidate]
        a.append(self.get_parents())
        return a

    def get_gene(self, index):
        return self.candidate[index]

    def set_gene(self, index, reagent):
        self.candidate[index] = reagent
        # self.candidate.append(reagent)

    def size(self):
        return len(self.candidate)

    # def get_novel(self, neighbours):
    #     dist_metric = DistanceMetric()
    #     total_score = 0
    #     for i in range(len(neighbours)):
    #         # print(self.to_params_list())
    #         # print(neighbours[i].to_params_list())
    #         total_score += dist_metric.get_distance(self.to_params_list(), neighbours[i].to_params_list())
    #     return total_score

    def get_novel_euc(self, neighbours):
        total_score = 0
        for i in range(len(neighbours)):
            # print(neighbours[i])
            total_score_local = 0
            for j in range(Cocktail.default_gene_length):
                total_score_local += abs(neighbours[i].candidate[j].score - self.candidate[i].score)
            total_score_local /= Cocktail.default_gene_length
            total_score += total_score_local
        return total_score

    def get_novelty(self):
        return float(self.novelty)

    def get_fitness(self):
        totalScore = 0
        for i in range(Cocktail.default_gene_length):
            totalScore += self.candidate[i].score
        return (totalScore / Cocktail.default_gene_length)

    def to_params_list(self):
        return [[[re.sub(' +', ' ', r.name).strip().lower()] for r in self.candidate[1:] if str(r.name).replace("  ", " ").strip().lower() is not ""], self.candidate[0].name]

    def get_parents(self):
        # return str(self.parent)
        return "; ".join(self.parent.keys())

    def to_str(self):
        return str(self.candidate[1].name) + " + " + str(self.candidate[2].name)

    def to_list_all(self):
        return [str(c.name).strip().upper() for c in self.candidate]

    def __str__(self):
        # print
        # return str(self.candidate[1].name) + " + " + str(self.candidate[2].name)
        return [self.candidate[0].name, [str(r.name) for r in self.candidate[1:]]]

