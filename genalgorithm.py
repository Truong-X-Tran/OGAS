import copy
import random
import pickle
from operator import itemgetter
# from enum import Enum
from reagent import Reagent
from cocktail import Cocktail
from population import Population
from metrics import DistanceMetric
from helper import *


class ReagentType:
    PH, CHEMICAL, ANION, CATION = range(4)


class GenAlgorithm():
    """docstring for GenAlgorithm"""

    rnd = random.random()

    def __init__(self, inputfile, outputfile='GA-Output.xlsx', pop=100,
            iterations=400, mutation=0.5, tournament=2,
            rank_range='0-10', novelty=True,
            parent1_rank_range='0-4', parent2_rank_range='4-10', rankfile=None):
        self.helper = Helper(inputfile)
        if rankfile:
            self.helper_rank = Helper(rankfile)
        else:
            self.helper_rank = None

        self.outputfile = outputfile
        self.number_of_distinct_buffer = 1
        self.new_pop_size = int(pop)
        self.old_population = Population(self.new_pop_size)
        self.mutation_rate = float(mutation)
        self.tournament_size = int(tournament)
        self.elitism = False
        self.novelty = novelty
        self.rank_range = rank_range
        self.parent_rank_ranges = [parent1_rank_range, parent2_rank_range]
        self.num_iter = int(iterations)
        self.reagent_type = ReagentType.PH

        self.scores_of_preps = {}
        self.scores_of_salts = {}
        self.scores_of_phs = {}

        self.dist_metric = None
        try:
            print "Loading Pickle"
            with open('hwi-compunds.pickle', 'rb') as handle:
                self.dist_metric = pickle.load(handle)
            print "Loaded Pickle"
        except:
            pass

        print self.rank_range, self.parent_rank_ranges

    def get_rank_of_reagent(self, reagent, rt, helper=None):
        if helper is None:
            helper = self.helper
        sa = helper.columns.get('S_a')
        sb = helper.columns.get('S_b')
        sc = helper.columns.get('S_c')
        # print "=="
        # print reagent, type(reagent)
        # print "=="
        if (rt == ReagentType.PH):
            phs = [(sa[i] + sb[i] + sc[i]) / 3.0
                   for (i, val) in enumerate(
                   helper.columns['Ph'])
                   if val == reagent]
            not_phs = [(sa[i] + sb[i] + sc[i]) / 3.0
                   for (i, val) in enumerate(
                   helper.columns['Ph'])
                   if val != reagent]
            avg_rank_of_ph = 0.0
            avg_rank_of_not_ph = 0.0
            try:
                avg_rank_of_ph = float(sum(phs)) / len(phs)
            except:
                pass
            avg_rank_of_not_ph = float(sum(not_phs)) / len(not_phs)
            # print (avg_rank_of_ph, avg_rank_of_not_ph)
            return float(avg_rank_of_ph) / avg_rank_of_not_ph
        else:
            c1a = helper.columns.get('C1_Anion')
            c2a = helper.columns.get('C2_Anion')
            c3a = helper.columns.get('C3_Anion')
            c4a = helper.columns.get('C4_Anion')
            c5a = helper.columns.get('C5_Anion')
            c1c = helper.columns.get('C1_Cation')
            c2c = helper.columns.get('C2_Cation')
            c3c = helper.columns.get('C3_Cation')
            c4c = helper.columns.get('C4_Cation')
            c5c = helper.columns.get('C5_Cation')

            chems = [(sa[i] + sb[i] + sc[i]) / 3.0
                   for (i, val) in enumerate(
                   helper.columns['Ph'])
                   if (
                    ((c1a[i].lower() + " " + c1c[i].lower()).strip() == reagent.lower().strip()) or
                    ((c2a[i].lower() + " " + c2c[i].lower()).strip() == reagent.lower().strip()) or
                    ((c3a[i].lower() + " " + c3c[i].lower()).strip() == reagent.lower().strip()) or
                    ((c4a[i].lower() + " " + c4c[i].lower()).strip() == reagent.lower().strip()) or
                    ((c5a[i].lower() + " " + c5c[i].lower()).strip() == reagent.lower().strip())
                    )
                   ]
            # print(chems)
            avg_rank_of_chem = float(sum(chems)) / len(chems)

            if reagent != "":

                not_chems = [(sa[i] + sb[i] + sc[i]) / 3.0
                       for (i, val) in enumerate(
                       helper.columns['Ph'])
                       if (
                        ((c1a[i].lower() + " " + c1c[i].lower()).strip() != reagent.lower().strip()) or
                        ((c2a[i].lower() + " " + c2c[i].lower()).strip() != reagent.lower().strip()) or
                        ((c3a[i].lower() + " " + c3c[i].lower()).strip() != reagent.lower().strip()) or
                        ((c4a[i].lower() + " " + c4c[i].lower()).strip() != reagent.lower().strip()) or
                        ((c5a[i].lower() + " " + c5c[i].lower()).strip() != reagent.lower().strip())
                        )
                       ]

                avg_rank_of_not_chem = float(sum(not_chems)) / len(not_chems)

                # print (avg_rank_of_chem, avg_rank_of_not_chem)
                return float(avg_rank_of_chem) / avg_rank_of_not_chem
            else:
                return float(avg_rank_of_chem) / self.get_average_score(helper)

    def get_average_score(self, helper=None):
        if helper is None:
            helper = self.helper
        sa = sum(helper.columns.get('S_a')) / float(helper.size())
        sb = sum(helper.columns.get('S_b')) / float(helper.size())
        sc = sum(helper.columns.get('S_c')) / float(helper.size())
        return (sa + sb + sc) / 3.0

    def get_population_from_file(self):
        low, high = [int(i) for i in self.rank_range.split('-')]
        print len(self.helper.columns['Ph'])
        print len(self.helper.columns['C1_Anion'])
        distinct_tuples = [[self.helper.columns['Ph'][i], (self.helper.columns['C1_Anion'][i] + " " + self.helper.columns['C1_Cation'][i]).lower().strip(), (self.helper.columns['C2_Anion'][i] + " " + self.helper.columns['C2_Cation'][i]).lower().strip()] for i in range(len(self.helper.columns['Ph']))]
        print "bef ", len(distinct_tuples)
        print "aft ", len([list(x) for x in set(tuple(x) for x in distinct_tuples)])
        dddd = [list(x) for x in set(tuple(x[1:]) for x in distinct_tuples)]
        print dddd[0]
        print len(dddd)

        distinct_tuples.sort(key=lambda x: x[1])
        # from operator import itemgetter
        # sorted(distinct_tuples, key=itemgetter(0))
        # for _ in distinct_tuples:
        #     print _

        # print [c for c in self.helper.columns['C1_M']]
        # print [c for c in self.helper.columns['C2_M']]
        for i in range(self.helper.size()):
            sa = self.helper.columns.get('S_a')[i]
            sb = self.helper.columns.get('S_b')[i]
            sc = self.helper.columns.get('S_c')[i]
            # score = (sa + sb + sc) / 3.0
            score = max([sa , sb , sc])
            # print score
            # print "=========="
            # print self.helper.columns['C1_M'][i]
            # print str(self.helper.columns['C1_M'][i])
            # print float(self.helper.columns['C1_M'][i])

            # print [c for c in self.helper.columns['C1_M']]
            # print self.helper.columns['C2_M'][9]
            # print str(self.helper.columns['C2_M'][i])
            # print float(self.helper.columns['C2_M'][i])
            # exit()
            # c1M = 0.0
            # c2M = 0.0
            try:
                c1M = float(self.helper.columns['C1_M'][i])
            except:
                print self.helper.columns['C1_M'][i]

            try:
                c2M = float(self.helper.columns['C2_M'][i])
            except:
                print self.helper.columns['C2_M'][i]

            ph = self.helper.columns['Ph'][i]

            precipitant = (self.helper.columns['C1_Anion'][i] + " " + self.helper.columns['C1_Cation'][i]).strip().upper()

            if precipitant not in self.scores_of_preps:
                self.scores_of_preps[precipitant] = [{'conc':c1M, 'score': score}]
            else:
                self.scores_of_preps[precipitant].append({'conc':c1M, 'score': score})

            salt = (self.helper.columns['C2_Anion'][i] + " " + self.helper.columns['C2_Cation'][i]).strip().upper()

            if salt not in self.scores_of_salts:
                self.scores_of_salts[salt] = [{'conc':c2M, 'score': score}]
            else:
                self.scores_of_salts[salt].append({'conc':c2M, 'score': score})

            rank_of_ph = self.get_rank_of_reagent(ph, ReagentType.PH)
            pH = Reagent(ph, "PH", rank_of_ph)

            rank_of_precipitant = self.get_rank_of_reagent(precipitant, ReagentType.CHEMICAL)
            # precipitant = str(precipitant).replace("\t", " ").replace("  ", " ").strip().strip().lower()
            # precipitant = re.sub(' +', ' ', precipitant).strip().lower()
            precipitant = Reagent(precipitant, "PRECIPITANT", rank_of_precipitant)

            rank_of_salt = self.get_rank_of_reagent(salt, ReagentType.CHEMICAL)
            # salt = re.sub(' +', ' ', salt).strip().lower()
            salt = Reagent(salt, "SALT", rank_of_salt)
            # print pH, precipitant, salt
            # exit()

            cocktail = Cocktail()
            cocktail.set_gene(0, pH)
            cocktail.set_gene(1, precipitant)
            cocktail.set_gene(2, salt)
            cocktail.score = [c1M, c2M]

            r = rank_of_ph + rank_of_precipitant + rank_of_salt
            cocktail.fitness = r
            if r > low and r < high:
                # print(r)
                self.old_population.save_cocktail(i, cocktail)

        if self.new_pop_size > len(self.old_population.cocktails):
            self.new_pop_size = len(self.old_population.cocktails)
        return self.old_population

    def crossover(self, parent1, parent2):
        child = Cocktail()
        crossover_point = random.randint(0, parent1.size() - 1)
        for i in range(parent1.size()):
            if i <= crossover_point:
                child.set_gene(i, parent1.get_gene(i))
            else:
                child.set_gene(i, parent2.get_gene(i))
        if parent1.parent == {} or parent2.parent == {}:
        #     child.parent[0] = child.to_str() + " => " + parent1.to_str() + " | " + parent2.to_str()
            parent1.parent = { self.get_buffer_name(parent1.candidate[0].name) + " + " + parent1.to_str() : 0 }
            parent2.parent = { self.get_buffer_name(parent2.candidate[0].name) + " + " + parent2.to_str() : 0 }

        # child.parent.extend(parent1.parent)
        # child.parent.extend(parent2.parent)
        child.parent = dict(parent1.parent.items() + parent2.parent.items() + [(k, parent1.parent[k] + parent2.parent[k]) for k in parent2.parent.viewkeys() & parent1.parent.viewkeys()])
        # print child.parent
        # child.parent[1] = child.to_str() + " => " + parent1.to_str_parent() + " | " + parent2.to_str_parent()
        # child.parent[1] = child.to_str() + " => " + parent1.to_str() + " | " + parent2.to_str()
        # child.parent[0] = self.get_buffer_name(parent1.candidate[0].name) + " + " + parent1.to_str()
        # child.parent[1] = self.get_buffer_name(parent2.candidate[0].name) + " + " + parent2.to_str()
        return child

    def tournament_selection(self, pop):
        tournament = Population(self.tournament_size)
        for i in range(self.tournament_size):
            random_id = random.randint(0, self.new_pop_size - 1)
            tournament.save_cocktail(i, pop.get_cocktail(random_id))

        return tournament.get_fittest()

    def tournament_selection_novelty(self, pop, novelty=False):
        tournament = Population(self.tournament_size)
        for i in range(self.tournament_size):
            random_id = random.randint(0, self.new_pop_size - 1)
            tournament.save_cocktail(i, pop.get_cocktail(random_id))
        if novelty:
            return tournament.get_fittest_cached()
        return tournament.get_fittest()

    def tournament_selection_novelty_parent(self, pop, novelty=False, parent=0):
        tournament = Population(self.tournament_size)
        low, high = [int(i) for i in self.parent_rank_ranges[parent - 1].split('-')]
        cocktails_in_range = [c for c in pop.cocktails if c.fitness > low and c.fitness < high]
        for i in range(self.tournament_size):
            random_id = random.randint(0, len(cocktails_in_range) - 1)
            tournament.save_cocktail(i, cocktails_in_range[random_id])
        if novelty:
            return tournament.get_fittest_cached()
        return tournament.get_fittest()

    def tournament_selection_fit(self, pop):
        cocktails = pop.cocktails[:]
        newlist = sorted(cocktails, key=lambda x: x.get_fitness(), reverse=True)
        total = len(newlist) // 2
        newlist = newlist[: total]
        random_id = random.randint(0, total - 1)
        fittest = newlist[random_id]
        return fittest

    def tournament_selection_unfit(self, pop):
        cocktails = pop.cocktails[:]
        newlist = sorted(cocktails, key=lambda x: x.get_fitness())
        total = len(newlist) // 2
        newlist = newlist[: total]
        random_id = random.randint(0, total - 1)
        fittest = newlist[random_id]
        return fittest

    def evolve_population(self, pop, iterations, novelty=False):
        new_population = Population(self.new_pop_size)
        if iterations == 0:
            # print([c.fitness for c in pop.cocktails])
            for i in range(self.new_pop_size):
                parent1 = self.tournament_selection_novelty_parent(pop, novelty, 1)
                parent2 = self.tournament_selection_novelty_parent(pop, novelty, 2)
                child = self.crossover(parent1, parent2)
                new_population.save_cocktail(i, child)
        else:
            for i in range(self.new_pop_size):
                parent1 = self.tournament_selection_novelty(pop, novelty)
                parent2 = self.tournament_selection_novelty(pop, novelty)
                child = self.crossover(parent1, parent2)
                new_population.save_cocktail(i, child)

        if (iterations < self.num_iter - 1):
            for i in range(0, new_population.population_size()):
                new_population.cocktails[i] = self.mutate(new_population.get_cocktail(i), pop)

        return new_population

    def mutate(self, cocktail, pop):
        for i in range(cocktail.size()):
            randomId = random.random()

            if (randomId < self.mutation_rate):
                randomOldCocktailID = random.randint(0, self.old_population.population_size() - 1)
                rndCocktail = self.old_population.get_cocktail(randomOldCocktailID)

                rndGenetId = random.randint(0, 2)
                mutantGene = rndCocktail.get_gene(rndGenetId)

                cocktail.set_gene(rndGenetId, mutantGene)
        return cocktail

    def merge_files(self, sorted_indices, ext_inputs, all_labels, all_files, all_inputs, uniq_inputs, commands=["--AED" , "AbIPP-Combined-1.xlsx", "KpIPP-Combined-1.xlsx"]):
        wb1 = Workbook()
        ws1 = wb1.active
        headers = ["Well_Id", "B_Anion", "B_Cation", "Ph", "B_Conc",\
         "C1_Anion", "C1_Cation", "C1_Conc", "C1_M", "C1_Ph",\
          "C2_Anion", "C2_Cation", "C2_Conc", "C2_M", "C2_Ph",\
           "C3_Anion", "C3_Cation", "C3_Conc", "C3_M", "C3_Ph",\
            "C4_Anion", "C4_Cation", "C4_Conc", "C4_M", "C4_Ph",\
             "C5_Anion", "C5_Cation", "C5_Conc", "C5_M", "C5_Ph",\
              "S_a", "S_b", "S_c", "Rank"]

        headers.extend(all_labels)

        ws1.append(headers)
	full_rows = []
        row_index = 0

        print all_files
        print all_labels
        print ext_inputs[:10]
        for i, f in enumerate(all_files):
            if all_labels[i] == "AED":
                aed = True
            else:
		aed = False

            wb2 = load_workbook(f)
            ws2 = wb2.active
            # ws2 = wb2['Sheet1']
            if not aed:
                for row in tuple(ws2.rows)[1:]:
                    full_row = [cell.value for cell in row]
                    full_row.extend(ext_inputs[row_index])
                    full_rows.append(full_row)
                    row_index += 1
            else:
                for row in tuple(ws2.rows)[1:]:
                    full_row = [cell.value for cell in row[8:]]
                    full_row.extend(ext_inputs[row_index])
                    full_rows.append(full_row)
                    row_index += 1

        print "row index", row_index

        for fr in sorted_indices:
            # if fr not in common_indices:
                ws1.append(full_rows[fr])

        ws_stats = wb1.create_sheet(title="Statistics")
        headers_stats = [""]
        headers_stats.extend(all_labels)
        headers_stats.append("ALL")

        ws_stats.append(headers_stats)

        total_conditions = [sum([row[i] for row in ext_inputs]) for i in range(len(all_labels))]
        total_conditions.insert(0, "Total Solutions")
        # print total_conditions

        for i, lbl in enumerate(all_labels):
            commons = [sum([1 for row in ext_inputs if (row[i] and row[j] and i!=j)]) for j in range(len(all_labels))]
            all_1s = [1 for _ in range(len(all_labels))]
            only_1s = [0 for _ in range(len(all_labels))]
            only_1s[i] = 1
            commons[i] = sum([1 for row in ext_inputs if row==only_1s])
            commons.append(sum([1 for row in ext_inputs if row==all_1s]))
            commons.insert(0, lbl)
            ws_stats.append(commons)

        print "[][][][][][][]"
        top_scores = [max([float(x[-(len(all_labels)+1)]) for x in rows]) for rows in all_inputs]
        top_scores.insert(0, "Top Score")
        ws_stats.append(top_scores)

        indices = [0,1,2,3,5]
        distinct_fams = [len(set(tuple([x[j] for j in indices]) for x in all_inputs[i])) for i in range(len(all_labels))]
        distinct_fams.insert(0, "Distinct Families")
        ws_stats.append(distinct_fams)

        # print distinct_fams
        # distinct_fams = [len(set_gene)]

        ws_stats.append(total_conditions)
        ws_stats.append([])
        ws_stats.append([])

        total_conditions = [row_index]
        total_conditions.insert(0, "Total Solutions")
        ws_stats.append(total_conditions)
        # print total_conditions

        distinct_fams = [len(set(tuple([x[j] for j in indices]) for x in uniq_inputs ))]
        distinct_fams.insert(0, "Distinct Families")
        ws_stats.append(distinct_fams)
        print distinct_fams



        wb1.save(commands[0])

    def save_output(self, candidates, outputfilename=""):
        wb = Workbook()

        # grab the active worksheet
        ws = wb.active

        # Rows can also be appended
        ws.append(["Well_Id", "B_Anion", "B_Cation", "Ph", "B_Conc",\
         "C1_Anion", "C1_Cation", "C1_Conc", "C1_M", "C1_Ph",\
          "C2_Anion", "C2_Cation", "C2_Conc", "C2_M", "C2_Ph",\
           "C3_Anion", "C3_Cation", "C3_Conc", "C3_M", "C3_Ph",\
            "C4_Anion", "C4_Cation", "C4_Conc", "C4_M", "C4_Ph",\
             "C5_Anion", "C5_Cation", "C5_Conc", "C5_M", "C5_Ph",\
              "S_a", "S_b", "S_c", "Rank"])
        for c in candidates:
            a = ['']
            a.append(c[0])
            a.append('')
            a.append(c[1])
            a.append(c[2])
            a.append(c[3])
            a.append('')
            a.append(c[4])
            a.append('')
            a.append('')
            a.append(c[5])
            a.append('')
            a.append(c[6])
            a.extend(['' for i in range(20)])
            a.append(c[8])
            ws.append(a)
        # Save the file
        wb.save(outputfilename + self.outputfile)

        wb_parents = Workbook()

        # grab the active worksheet
        ws_parents = wb_parents.active

        # Rows can also be appended
        ws_parents.append(["B_Anion", "C1", "C2"])
        all_parents = candidates[0][7].upper().split(";")
        for parent in all_parents:
            p = parent.split("+")
            a = []
            a.append(p[0])
            a.append(p[1])
            a.append(p[2])
            ws_parents.append(a)
        # Save the file
        # wb_parents.save(outputfilename + self.outputfile.split(".")[0] + "_parents." + self.outputfile.split(".")[1])

    def get_datatable_from_population(self, pop):
        # [ph, precipitant, salt]
        return [c.to_list() for c in pop.cocktails]

    def get_buffer_name(self, ph_val):
        ph = self.helper.columns.get('Ph')
        ba = self.helper.columns.get('B_Anion')
        bc = self.helper.columns.get('B_Cation')

        # print(ph_val)
        buffers = [(ba[j].upper() + " " + bc[j].upper()).strip() for (j, val) in enumerate(ph) if str(val) == str(ph_val) and ph_val is not None]
        buffers = list(set(buffers))
        # print(buffers)
        if buffers == []:
            return ""
        return buffers[0]

    def generate_concentrations(self, candidate_triples):
        c1a = self.helper.columns.get('C1_Anion')
        c2a = self.helper.columns.get('C2_Anion')
        c1c = self.helper.columns.get('C1_Cation')
        c1C = self.helper.columns.get('C1_Conc')
        c1M = self.helper.columns.get('C1_M')
        c2C = self.helper.columns.get('C2_Conc')
        c2M = self.helper.columns.get('C2_M')
        c2c = self.helper.columns.get('C2_Cation')
        ph = self.helper.columns.get('Ph')
        ba = self.helper.columns.get('B_Anion')
        bc = self.helper.columns.get('B_Cation')

        # print(candidate_triples[0])
        # print(c1C)
        # print(c1c)
        candidates = []
        for i in range(len(candidate_triples)):
            # give  all buffer for ph = row's ph value
            # print(candidate_triples[i][0])
            buffers = [(ba[j].upper() + " " + bc[j].upper()).strip() for (j, val) in enumerate(ph) if str(val) == candidate_triples[i][0]]
            buffers = list(set(buffers))
            # print(buffers)
            prep = [(str(c1M[j])).strip() for (j, val) in enumerate(ph) if (c1a[j].upper() + " " + c1c[j].upper()).strip() == candidate_triples[i][1]]
            salt = [(str(c2M[j])).strip() for (j, val) in enumerate(ph) if (c2a[j].upper() + " " + c2c[j].upper()).strip() == candidate_triples[i][2]]
            prep = list(set(prep))
            salt = list(set(salt))

            # print(salt)
            for m in range(len(prep)):
                for n in range(len(salt)):
                    a = [""]
                    try:
                        a = [buffers[0]]
                    except:
                        a = [""]
                    a.append(candidate_triples[i][0])
                    a.append("0.1")
                    a.append(candidate_triples[i][1])
                    a.append(prep[m])
                    a.append(candidate_triples[i][2])
                    a.append(salt[n])
                    a.append(candidate_triples[i][3])
                    candidates.append(a)

        return candidates

    def apply_ranking(self, candidates, helper):
        for i in range(len(candidates)):
            rank_of_ph = self.get_rank_of_reagent(candidates[i][1], ReagentType.PH, helper)
            rank_of_prep = self.get_rank_of_reagent(candidates[i][3], ReagentType.CHEMICAL, helper)
            rank_of_salt = self.get_rank_of_reagent(candidates[i][5], ReagentType.CHEMICAL, helper)

            avg_rank = (rank_of_ph + rank_of_prep + rank_of_salt) / 3.0
            candidates[i].append(avg_rank)

        return candidates

    def get_inputs(self, rank=False):
        for k in self.helper.columns.keys():
            for i in range(len(self.helper.columns.get(k))):
                if self.helper.columns.get(k)[i] is None:
                    self.helper.columns.get(k)[i] = ""
                # self.helper.columns.get(k)[i] = self.helper.columns.get(k)[i].upper()
        c1a = self.helper.columns.get('C1_Anion')
        c2a = self.helper.columns.get('C2_Anion')
        c1c = self.helper.columns.get('C1_Cation')
        c1C = self.helper.columns.get('C1_Conc')
        c1M = self.helper.columns.get('C1_M')
        c2C = self.helper.columns.get('C2_Conc')
        c2M = self.helper.columns.get('C2_M')
        c2c = self.helper.columns.get('C2_Cation')
        ph = self.helper.columns.get('Ph')
        ba = self.helper.columns.get('B_Anion')
        bc = self.helper.columns.get('B_Cation')
        bconc = self.helper.columns.get('B_Conc')
        rank = self.helper.columns.get('Rank')
        # print len(c1a)
        # print list(self.helper.columns)
        inputs = []
        upper_limit = len(c1a)
        # if upper_limit > 1000:
        #     upper_limit = 1000
        if rank:
            for i in range(upper_limit):
                inputs.append([ba[i] + " " + bc[i], ph[i], bconc[i], c1a[i] + " " + c1c[i], c1M[i], c2a[i] + " " + c2c[i], c2M[i], rank[i] ])
        else:
            for i in range(upper_limit):
                inputs.append([ba[i] + " " + bc[i], ph[i], bconc[i], c1a[i] + " " + c1c[i], c1M[i], c2a[i] + " " + c2c[i], c2M[i] ])


        # print type(inputs[0][0])
        inputs = [[str(inp.upper().strip()) if isinstance(inp, basestring) else str(inp) for inp in inpt] for inpt in inputs]
        # print(inputs)
        return inputs


    def apply_gen_algorithm(self):
        pop = self.get_population_from_file()
        print "asd     ", len(pop.cocktails)
        print "asd     ", pop.cocktails[0].__str__()
        # return

        self.scores_of_preps = {k: sorted(self.scores_of_preps[k], key=itemgetter('conc')) for k in self.scores_of_preps.keys()}
        self.scores_of_salts = {k: sorted(self.scores_of_salts[k], key=itemgetter('conc')) for k in self.scores_of_salts.keys()}
        # print self.scores_of_preps
        # for k,v in self.scores_of_preps.iteritems():
        #     print k
        #     for c in v:
        #         print c['conc'], ': ', c['score']
        # for k,v in self.scores_of_salts.iteritems():
        #     print k
        #     for c in v:
        #         print c['conc'], ': ', c['score']
        print("File Loaded")
        print(pop.cocktails[0].__str__())
        pop_len = len(pop.cocktails)
        print(pop_len)

        insights_ip = {}
        insights_op = {}
        insights_ip['salts'] = len(set([c.__str__()[1][0] for c in pop.cocktails]))
        insights_ip['precipitants'] = len(set([c.__str__()[1][1] for c in pop.cocktails]))
        insights_ip['distinct_families'] = len(set([c.__str__()[1][0] + c.__str__()[1][1] for c in pop.cocktails]))

        all_cocktails = []
        if not self.novelty:

            # original_small = [p.to_list_all() for p in pop.cocktails]
            print("Genetic")
            old_ones = len(set(all_cocktails))
            for i in range(self.num_iter):
                all_cocktails.extend(copy.deepcopy([''.join(x.to_list_all()) for x in pop.cocktails]))
                # print ''.join(all_cocktails[0].to_list_all())
                # print all_cocktails[0]
                this_cocktails = []
                this_cocktails.extend(copy.deepcopy([''.join(x.to_list_all()) for x in pop.cocktails]))
                # print (i)
                pop = self.evolve_population(pop, i)
                # print pop.cocktails[0].to_str()

                if 1:#i%10 == 0:
                    # all_uniq = set(tuple(x.to_list_all()) for x in all_cocktails)
                    all_uniq = set(all_cocktails)
                    uniq_total = len(all_uniq)
                    # print uniq_total / float(len(all_cocktails))


                    # this_uniq = set(tuple(x.to_list_all()) for x in this_cocktails)
                    this_uniq = set(this_cocktails)
                    # print(list(this_uniq)[0])
                    # all_uniq2 = list(all_uniq)
                    # all_uniq2.extend(list(this_uniq))
                    # print all_uniq2[0]
                    # all_uniq2 = set(all_uniq2)
                    # print len(all_uniq2), len(all_uniq)
                    # intersection = this_uniq.intersection(all_uniq)
                    # print len(intersection), len(this_uniq)

                    uniq_this = len([x for x in this_cocktails if x in all_cocktails])
                    # uniq_this = len(this_uniq.intersection(all_uniq))
                    # print this_uniq
                    # print uniq_this, len(this_uniq), len(all_uniq), len(this_cocktails), len(all_cocktails)
                    # print (len(all_uniq) - old_ones),
                    old_ones = len(all_uniq)
                    # print pop_len - uniq_this
                    pop_len = self.new_pop_size
                    # pop_len = len(pop.cocktails)



            # print "; ".join(pop.cocktails[0].get_parents())

            # print(pop.cocktails[0].get_parents())
            candidates = self.get_datatable_from_population(pop)

            print len(all_cocktails)
            # print all_cocktails[0].to_list_all()
            # print tuple(all_cocktails[0].to_list_all())
            # print set(tuple(all_cocktails[0].to_list_all()))
            # print len(set(tuple(x.to_list_all()) for x in all_cocktails))

            candidate_cocktails = self.generate_concentrations(candidates)
            candidate_cocktails = [['' if c.lower()=='none' else c for c in cocktail] for cocktail in candidate_cocktails]
            # print("conc: ", candidate_cocktails[0][:-1])
            # print(len(candidate_cocktails))
            unique_candidates = [list(x) for x in set(tuple(x) for x in candidate_cocktails)]
            # print(len(unique_candidates[0]))
            # print(unique_candidates[0][:-1])
            # print()
            # print(unique_candidates[0])
            final_candidates = self.apply_ranking(unique_candidates, self.helper_rank)
            # print(final_candidates[0][:-2])
            final_candidates.sort(key=lambda x: -x[-1])
            # print("len: ", len(final_candidates))

            original_small = self.get_inputs()
            final_small = [[f[i] for i in range(7)] for f in final_candidates]
            print "=============="
            print original_small[0]
            # print final_small[0]
            common = set(map(tuple, original_small)) & set(map(tuple, final_small))
            common = [list(c) for c in list(common)]
            # print common
            common_indices = [i for c in common for (i,f) in enumerate(final_small) if c==f]
            common_indices.sort()
            print common_indices

            unacceptable_indices = []
            threshold = int(self.parent_rank_ranges[0].split('-')[0])
            print threshold
            for i, f in enumerate(final_candidates):
                to_del_conc = self.scores_of_preps[f[3]]
                acceptable_concs =  list(set([c['conc'] for c in to_del_conc if c['score'] >= threshold]))
                is_in_range = float(f[4]) in acceptable_concs
                if not is_in_range:
                    unacceptable_indices.append(i)
                # else:
                #     print f[:-2]
                #     print to_del_conc
                #     print acceptable_concs
            # print unacceptable_indices
            print("len: ", len(final_candidates))
            print("len: ", len(unacceptable_indices))
            unacceptable_indices.extend(common_indices)
            unacceptable_indices = list(set(unacceptable_indices))
            j = 0
            for i in unacceptable_indices:
                del final_candidates[i-j]
                j += 1
            # print [final_candidates[i][:-2] for i in common_indices]
            # final_candidates = [[v for i, v in enumerate(s) if i not in common_indices] for s in final_candidates]
            print("len: ", len(final_candidates))

            # insights_op['buffer'] = len(set([f[0] for f in final_candidates]))
            self.save_output(final_candidates)

        else:
            from timeit import default_timer as timer
            start = timer()

            print("Novelty")
            rankings = []
            pop = self.evolve_population(pop, 0)
            pop_archive = copy.deepcopy(pop)

            end = timer()
            print end - start

            if self.dist_metric is None:
                try:
                    self.dist_metric = DistanceMetric()

                    with open('hwi-compunds.pickle', 'wb') as handle:
                        pickle.dump(self.dist_metric, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    print "Pickle Saved"
                except:
                    pass

            pop.dist_metric = self.dist_metric
            pop_archive.dist_metric = self.dist_metric
            old_ones = len(set(all_cocktails))

            for i in range(1, 5):
                print "============== ITERATION", i + 1, "/ 5 ==============="
                pop_archive.cocktails.extend(pop.cocktails)
                pop_archive.set_novelty()
                pop.cocktails = list(pop_archive.cocktails[:-self.new_pop_size])

                # all_cocktails.extend(copy.deepcopy(pop.cocktails))
                all_cocktails.extend(copy.deepcopy([''.join(x.to_list_all()) for x in pop.cocktails]))
                this_cocktails = []
                this_cocktails.extend(copy.deepcopy(pop.cocktails))

                pop = self.evolve_population(pop, i, True)

                if 1:#i%10 == 0:
                    # all_uniq = set(tuple(x.to_list_all()) for x in all_cocktails)
                    # uniq_total = len(all_uniq)
                    # print uniq_total / float(len(all_cocktails))

                    # this_uniq = set(tuple(x.to_list_all()) for x in this_cocktails)
                    # uniq_this = len([x for x in this_uniq if x in all_uniq])
                    # print self.new_pop_size - uniq_this
                    # pop_len = self.new_pop_size

                    all_uniq = set(all_cocktails)
                    # print (len(all_uniq) - old_ones)
                    old_ones = len(all_uniq)
                # uniq_total = len(set(tuple(x.to_list_all()) for x in all_cocktails))
                # print uniq_total / float(len(all_cocktails))
                # pop.cocktail = pop_archive.set_novelty_optimized(pop.cocktails)
                # pop = self.evolve_population(pop, i, True)

                end = timer()
                print end - start


            print "-=-=-=-=-=-=-"
            print len(all_cocktails)
            # print all_cocktails[0].to_list_all()
            # print tuple(all_cocktails[0].to_list_all())
            # print set(tuple(all_cocktails[0].to_list_all()))
            # print len(set(tuple(x.to_list_all()) for x in all_cocktails))
            print "-=-=-=-=-=-=-"

            candidates = self.get_datatable_from_population(pop)
            candidate_cocktails = self.generate_concentrations(candidates)
            print(len(candidate_cocktails))
            unique_candidates = [list(x) for x in set(tuple(x) for x in candidate_cocktails)]
            final_candidates = self.apply_ranking(unique_candidates, self.helper_rank)
            final_candidates.sort(key=lambda x: -x[-1])
            print("len: ", len(final_candidates))

            original_small = self.get_inputs()
            final_small = [[f[i] for i in range(7)] for f in final_candidates]
            # print original_small[0]
            # print final_small[0]
            common = set(map(tuple, original_small)) & set(map(tuple, final_small))
            common = [list(c) for c in list(common)]
            # print common
            common_indices = [i for c in common for (i,f) in enumerate(final_small) if c==f]
            common_indices.sort()
            print common_indices

            unacceptable_indices = []
            threshold = int(self.parent_rank_ranges[0].split('-')[0])
            print threshold
            for i, f in enumerate(final_candidates):
                to_del_conc = self.scores_of_preps[f[3]]
                acceptable_concs =  list(set([c['conc'] for c in to_del_conc if c['score'] >= threshold]))
                is_in_range = float(f[4]) in acceptable_concs
                if not is_in_range:
                    unacceptable_indices.append(i)
                # else:
                #     print f[:-2]
                #     print to_del_conc
                #     print acceptable_concs
            # print unacceptable_indices
            print("len: ", len(final_candidates))
            print("len: ", len(unacceptable_indices))
            unacceptable_indices.extend(common_indices)
            unacceptable_indices = list(set(unacceptable_indices))
            j = 0
            for i in unacceptable_indices:
                del final_candidates[i-j]
                j += 1
            # print [final_candidates[i][:-2] for i in common_indices]
            # final_candidates = [[v for i, v in enumerate(s) if i not in common_indices] for s in final_candidates]
            print("len: ", len(final_candidates))
            print len(pop_archive.dist_metric.cocktails)

            # rankings.append(sum([x[-1] for x in final_candidates[:10]])/10.0)
            self.save_output(final_candidates)
            # print pop_archive.dist_metric.cocktails

            # print(sorted(range(len(rankings)), key=lambda k: rankings[k]))

        all_salts = [f[3] for f in final_candidates]
        all_salts = list(set(all_salts))
        all_salts_scores = [[] for i in range(len(all_salts))]
        for i,s in enumerate(all_salts):
            for f in final_candidates:
                if f[3] == s:
                    all_salts_scores[i].append(f[-1])

        all_salts_scores_avg = [sum(s)/float(len(s)) for s in all_salts_scores]
        # print all_salts_scores_avg
        sorted_avg_salts = [i[0] for i in sorted(enumerate(all_salts_scores_avg), key=lambda x:x[1])]
        sorted_avg_salts = sorted_avg_salts[::-1]
        # print sorted_avg_salts

        all_precipitants = [f[5] for f in final_candidates]
        all_precipitants = list(set(all_precipitants))
        all_precipitants_scores = [[] for i in range(len(all_precipitants))]
        for i,s in enumerate(all_precipitants):
            for f in final_candidates:
                if f[5] == s:
                    all_precipitants_scores[i].append(f[-1])

        all_precipitants_scores_avg = [sum(s)/float(len(s)) for s in all_precipitants_scores]
        # print all_precipitants_scores_avg
        sorted_avg_precipitants = [i[0] for i in sorted(enumerate(all_precipitants_scores_avg), key=lambda x:x[1])]
        sorted_avg_precipitants = sorted_avg_precipitants[::-1]
        # print sorted_avg_precipitants

        insights_op['salts_scores_avg'] = {all_salts[i]:all_salts_scores_avg[i] for i in sorted_avg_salts[:3]}
        insights_op['precipitants_scores_avg'] = {all_precipitants[i]:all_precipitants_scores_avg[i] for i in sorted_avg_precipitants[:3]}

        insights_op['salts'] = len(set([f[3] for f in final_candidates]))
        insights_op['precipitants'] = len(set([f[5] for f in final_candidates]))
        insights_op['distinct_families'] = len(set([f[0] + f[3] + f[5] for f in final_candidates]))
        insights_op['top_score'] = final_candidates[0][-1]
        insights_op['mean_score_top10'] = sum([f[-1] for f in final_candidates[:10]]) / 10.0


        print
        print
        print insights_ip
        print insights_op
        return insights_op

