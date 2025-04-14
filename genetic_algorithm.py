import random
from job_shop_problem import JobShopProblem  # Importon klasën JobShopProblem nga file-i tjetër

class GeneticAlgorithm:
    def __init__(self, problem, population_size=20, generations=100, mutation_rate=0.1):
        # Konstruktori i klasës, ku përcaktohen parametrat e algoritmit
        self.problem = problem  # Problemi i caktuar (në këtë rast, problemet e Job-Shop)
        self.population_size = population_size  # Madhësia e popullatës të gjeneruar për çdo brez
        self.generations = generations  # Numri i brezave që do të krijohen
        self.mutation_rate = mutation_rate  # Norma e mutacionit, sa shpesh do të ndodhin mutacione

    def create_chromosome(self):
        # Kjo metodë krijon një kromozom të ri, që është një listë e kombinuar e punëve
        chromosome = []
        for job_id, job in enumerate(self.problem.jobs_data):
            # Përdor id-në e punës dhe e shton atë disa herë në kromozom për çdo operacion në këtë punë
            chromosome += [job_id] * len(job)
        random.shuffle(chromosome)  # Përdor një pasqyrë të rastësishme për të përzier kromozomin
        return chromosome  # Kthehet kromozomi i krijuar

    def initialize_population(self):
        # Kjo metodë krijon një popullatë fillestare të kromozomëve
        return [self.create_chromosome() for _ in range(self.population_size)]  # Krijon një listë me kromozome

    def tournament_selection(self, population):
        # Përdor selektimin me turne për të zgjedhur dy prindër nga popullata
        k = 3  # Numri i kandidaturave që do të përzgjidhen për të bërë turne
        candidates = random.sample(population, k)  # Zgjedh rastësisht 3 kandidatë nga popullata
        candidates.sort(key=lambda x: self.problem.decode(x))  # Rendit kandidatë sipas vlerës së dekoduar (përshtatshmërisë)
        return candidates[0], candidates[1]  # Kthehen dy prindërit më të mirë (me vlerën më të ulët të përshtatshmërisë)

    def crossover(self, parent1, parent2):
        # Kjo metodë kryen operacionin e crossover-it për të krijuar një fëmijë nga dy prindër
        size = len(parent1)  # Gjatësia e kromozomeve (numri i punëve)
        a, b = sorted(random.sample(range(size), 2))  # Zgjedh dy pozita të rastësishme për të krijuar një segment
        child = [None] * size  # Krijo një kromozom bosh për fëmijën
        segment = parent1[a:b]  # Merr segmentin nga prindi 1

        child[a:b] = segment.copy()  # Përdor segmentin nga prindi 1 për të mbushur kromozomin e fëmijës

        # Përdor një fjalor për të numëruar sa herë paraqitet secili gjene në segmentin e fëmijës
        counts = {i: segment.count(i) for i in set(segment)}
        fill = []  # Lista për të mbushur pozitat e mbetura të kromozomit të fëmijës

        # Përdor prindin 2 për të mbushur pozitat bosh në fëmijë
        for gene in parent2:
            if counts.get(gene, 0) < parent1.count(gene):  # Nëse gjeni nuk është shtuar ende
                fill.append(gene)  # Shto gjene në listën e mbushjes
                counts[gene] = counts.get(gene, 0) + 1  # Përditëso fjalorin për numrin e gjeneve të përdorur

        j = 0  # Llogaritës për të mbushur pozitat bosh të kromozomit
        for i in range(size):
            if child[i] is None:  # Nëse pozita është bosh
                child[i] = fill[j]  # Mbush me një gjene nga lista 'fill'
                j += 1

        return child  # Kthehet kromozomi i fëmijës

    def mutate(self, chromosome):
        # Përdor mutacionin për të ndryshuar një kromozom në mënyrë të rastësishme
        if random.random() < self.mutation_rate:  # Nëse rastësisht ndodh mutacioni
            a, b = random.sample(range(len(chromosome)), 2)  # Zgjedh dy pozita të rastësishme
            chromosome[a], chromosome[b] = chromosome[b], chromosome[a]  # Ndrysho vlerat në ato pozita
        return chromosome  # Kthehet kromozomi i modifikuar

    def run(self):
        # Kjo metodë ekzekuton algoritmin gjenetik
        population = self.initialize_population()  # Krijon popullatën fillestare
        best = min(population, key=lambda x: self.problem.decode(x))  # Zgjedh kromozomin më të mirë
        best_score = self.problem.decode(best)  # Vlera e përshtatshmërisë për kromozomin më të mirë

        for _ in range(self.generations):  # Për çdo brez (gjenetik)
            new_population = []  # Krijo një popullatë të re
            for _ in range(self.population_size):
                p1, p2 = self.tournament_selection(population)  # Zgjedh dy prindër
                child = self.crossover(p1, p2)  # Bëj crossover për të krijuar një fëmijë
                child = self.mutate(child)  # Bëj mutacion për fëmijën
                new_population.append(child)  # Shto fëmijën në popullatën e re

            population = new_population  # Përditëso popullatën me të re
            current_best = min(population, key=lambda x: self.problem.decode(x))  # Zgjedh kromozomin më të mirë në popullatën e re
            current_score = self.problem.decode(current_best)  # Vlera e përshtatshmërisë për kromozomin më të mirë të ri
            if current_score < best_score:  # Nëse kromozomi i ri është më i mirë
                best = current_best  # Përditëso kromozomin më të mirë
                best_score = current_score  # Përditëso vlerën e përshtatshmërisë

        return best, best_score  # Kthehet kromozomi më i mirë dhe vlera e tij e përshtatshmërisë
