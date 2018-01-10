#!/usr/bin/python3
# -*-coding: utf-8 -*

import random
from pyeasyga import pyeasyga
from operator import attrgetter
from models.matrix.Matrix import Matrix
from GA.GaSimulator import GaSimulator
from tools import Tools
from tools.Configs import Models
from tools.Configs import ConfigExp2
from tools.Configs.Matrices.GoalMatrices import GoalMatrices

current_model = ''


# generated at random
# each weight or threshold is a single gene within the genome and is a real number in range [0,1]
def create_individual(data: [str]) -> [float]:
    return [random.uniform(0, 1) for _ in range(len(data))]


def one_point_crossover(parent_1: [float], parent_2: [float]) -> ([float], [float]):
    crossover_index = random.randrange(1, len(parent_1))
    child_1 = parent_1[:crossover_index] + parent_2[crossover_index:]
    child_2 = parent_2[:crossover_index] + parent_1[crossover_index:]
    return child_1, child_2


def simple_mutation(individual: [float]) -> [float]:
    mutate_index = random.randrange(len(individual))
    individual[mutate_index] = random.uniform(0, 1)


# the selection probability is proportional to the fitness of the individual
def roulette_wheel_selector(population: [pyeasyga.Chromosome]) -> pyeasyga.Chromosome:
    sum_of_fitness = 0
    fitnesses = []
    # sort from worst to fittest individual
    population.sort(key=attrgetter('fitness'))

    for individual in population:
        fitnesses.append(individual.fitness)
        sum_of_fitness += individual.fitness

    rand = random.random() * sum_of_fitness

    for i in range(len(population)):
        if fitnesses[i] < rand:
            return population[i]

    # when rounding errors occur, we return the fittest individual
    return population[-1]


def fitness(individual: [float], data: [str]) -> float:
    conf = {}
    model_conf = {}
    if current_model is 'dipm':
        conf = ConfigExp2.config_dipm_exp2()
        model_conf = Models.get_dipm_base_generator()
    elif current_model is 'scpm':
        conf = ConfigExp2.config_scpm_exp2()
        model_conf = Models.get_scpm_base_generator()
    # we update the model's weights' configuration
    model_conf = Tools.update_conf(model_conf, data, individual)
    # we update the sim's configuration
    conf.update({'model_conf': {0: model_conf, 1: model_conf}})

    filenames = GaSimulator.run_sims(current_model, conf)
    # print('filenames: ' + str(filenames))
    results = GaSimulator.analyze_results(filenames, conf)
    print('results: ' + str(results))

    matrix = Tools.generate_simple_ability_matrix(results[0], results[1], 0.05)
    goal = Matrix()
    if current_model is 'dipm':
        goal = GoalMatrices.dipm()
    elif current_model is 'scpm':
        goal = GoalMatrices.scpm()

    fitness_value = Tools.value_for_fitness(matrix, goal)

    return fitness_value


def run_ga(data: [str], population_size: int, generations: int, crossover_proba: float,
           mutation_proba: float, elitism: bool) -> [str]:
    ga = pyeasyga.GeneticAlgorithm(data, population_size, generations, crossover_proba, mutation_proba, elitism)

    ga.create_individual = create_individual
    ga.crossover_function = one_point_crossover
    ga.mutate_function = simple_mutation
    ga.selection_function = roulette_wheel_selector
    ga.fitness_function = fitness

    random.seed()
    ga.run()
    return ga.best_individual()