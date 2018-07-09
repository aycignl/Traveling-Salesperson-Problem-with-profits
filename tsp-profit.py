
# coding: utf-8

# ## Import required libraries

import random
import math
from operator import attrgetter
import time
import xlrd


# ## Setup for reading data


# eil51, eil76, eil101
# dataset-LowProfit.xls, dataset-HighProfit.xls
dataset_name = 'eil51'
file_name = 'dataset-LowProfit.xls'


# ## Functions


def euclidean_distance(ca, cb):
    dist = math.sqrt((ca.x - cb.x) ** 2 + (ca.y - cb.y) ** 2)
    return round(dist, 2)


def generate_customer_matrix(a):
    customer_matrix = [[0 for x in range(len(a))] for y in range(len(a))]
    for r in range(len(a)):
        for c in range(len(a)):
            if r == c:
                customer_matrix[r][c] = - math.inf
            else:
                customer_matrix[r][c] = a[c].profit - round(euclidean_distance(a[r], a[c]), 2)
    return customer_matrix;


class CustomerLocation:
    # number of the city on the file
    indis = 0
    # coordinates of the cities
    x = 0
    y = 0
    # profit gained by visiting a city
    profit = 0

    def __init__(self, indis=None, x=None, y=None, profit=None):
        self.indis = indis
        self.x = x
        self.y = y
        self.profit = profit

    def __str__(self):
        return str(self.indis)

    def __repr__(self):
        return self.__str__()


def init(file_name, result_file):
    # Read Excel file with file name and sheet name
    xl = xlrd.open_workbook(file_name)
    points = xl.sheet_by_name(result_file)
    print(points)
    for point in points.get_rows():
        a.append(CustomerLocation(int(point[0].value), int(point[1].value), int(point[2].value), int(point[3].value)))
    print(a)


# In[16]:

def construct_route():
    # keep a list of unvisited cities
    unvisited_cities = a.copy()
    print('unvisited: ', unvisited_cities)
    # choose the city with best profit
    starting_city = max(a, key=attrgetter('profit'))
    route = [starting_city]
    last_added = starting_city
    print('start with city : ', starting_city)
    unvisited_cities.remove(starting_city)

    while unvisited_cities:
        candidate_city = None
        candidate_profit = -math.inf
        for next_city in unvisited_cities:
            next_profit = customer_matrix[last_added.indis - 1][next_city.indis - 1]
            if next_profit > candidate_profit:
                candidate_city = next_city
                candidate_profit = next_profit
        if candidate_city is not None:
            route.append(candidate_city)
            last_added = candidate_city
            unvisited_cities.remove(candidate_city)
    return route


def improve_solution(unvisited_cities, route):
    # at first there is no unvisited cities, removed cities from the route will be added here
    improvement = True
    while improvement:
        improvement = False

        # if route consists of only 2 cities and profit is less than 0, it is better not to visit any cities
        if len(route) == 2:
            current_profit = customer_matrix[route[0].indis - 1][route[1].indis - 1]
            if current_profit < 0:
                route.remove(route[1])
        # if there are more than 2 cities in the route, check if removing a city improves the profit
        if len(route) > 2:
            for c in range(len(route)):
                next_indis = c + 1
                if next_indis >= len(route):
                    next_indis = 0
                current_profit = customer_matrix[route[c - 1].indis - 1][route[c].indis - 1] +                                  customer_matrix[route[c].indis - 1][route[next_indis].indis - 1]
                possible_profit = customer_matrix[route[c - 1].indis - 1][route[next_indis].indis - 1]
                if possible_profit > current_profit:
                    improvement = True
                    unvisited_cities.append(route[c])
                    route.remove(route[c])
                    break;
        else:
            improvement = False
        # If there are unvisited cities, insert those between consecutive cities when there is improvement
        if len(unvisited_cities) != 0:
            inserted_cities = unvisited_cities.copy()
            for u in range(len(unvisited_cities)):
                best_improvement = 0
                indis_r = -1
                for r in range(len(route)):
                    possible_profit = customer_matrix[route[r - 1].indis - 1][unvisited_cities[u].indis - 1] +                                       customer_matrix[unvisited_cities[u].indis - 1][route[r].indis - 1]
                    current_profit = customer_matrix[route[r - 1].indis - 1][route[r].indis - 1]
                    if (possible_profit - current_profit) > best_improvement:
                        indis_r = r
                        best_improvement = (possible_profit - current_profit)
                if indis_r > -1:
                    improvement = True
                    route.insert(indis_r, unvisited_cities[u])
                    inserted_cities.remove(unvisited_cities[u])
            unvisited_cities = inserted_cities
    return route, unvisited_cities


def swap(current, indis1, indis2):
    difference = 0
    new_route = current.copy()
    next1 = indis1 + 1
    if next1 == len(current):
        next1 = 0
    next2 = indis2 + 1
    if next2 == len(current):
        next2 = 0

    difference -= customer_matrix[new_route[indis1 - 1].indis - 1][new_route[indis1].indis - 1]
    difference -= customer_matrix[new_route[indis1].indis - 1][new_route[next1].indis - 1]
    difference -= customer_matrix[new_route[indis2 - 1].indis - 1][new_route[indis2].indis - 1]
    difference -= customer_matrix[new_route[indis2].indis - 1][new_route[next2].indis - 1]

    difference += customer_matrix[new_route[indis1 - 1].indis - 1][new_route[indis2].indis - 1]
    difference += customer_matrix[new_route[indis2].indis - 1][new_route[next1].indis - 1]
    difference += customer_matrix[new_route[indis2 - 1].indis - 1][new_route[indis1].indis - 1]
    difference += customer_matrix[new_route[indis1].indis - 1][new_route[next2].indis - 1]

    first_city = new_route[indis1]
    second_city = new_route[indis2]

    new_route[indis1] = second_city
    new_route[indis2] = first_city
    return difference, new_route


def flip(current, indis1, indis2):
    difference = 0
    new_route = current.copy()
    next1 = indis1 + 1
    if next1 == len(current):
        next1 = 0
    next2 = indis2 + 1
    if next2 == len(current):
        next2 = 0

    difference -= customer_matrix[new_route[indis1 - 1].indis - 1][new_route[indis1].indis - 1]
    difference -= customer_matrix[new_route[indis1].indis - 1][new_route[next1].indis - 1]
    difference -= customer_matrix[new_route[indis2].indis - 1][new_route[next2].indis - 1]

    difference += customer_matrix[new_route[indis1 - 1].indis - 1][new_route[next1].indis - 1]
    difference += customer_matrix[new_route[indis2].indis - 1][new_route[indis1].indis - 1]
    difference += customer_matrix[new_route[indis1].indis - 1][new_route[next2].indis - 1]

    first_city = new_route[indis1]
    new_route.pop(indis1)

    new_route.insert(indis2+1, first_city)
    return difference, new_route


def shuffle_swap(current):
    while True:
        indis1 = random.randint(0, len(current) - 1)
        indis2 = random.randint(0, len(current) - 1)
        if indis1 != indis2:
            difference, new_route = swap(current, indis1, indis2)
            return (indis1, indis2), difference, new_route

def shuffle_flip(current):
    while True:
        indis1 = random.randint(0, len(current) - 1)
        indis2 = random.randint(0, len(current) - 1)
        if indis1 != indis2:
            difference, new_route = flip(current, indis1, indis2)
            return (indis1, indis2), difference, new_route


def calculate_profit(solution):
    total_profit = 0
    if len(solution) == 1:
        return solution[0].profit
    for i in range(-1, len(solution) - 1):
        total_profit += customer_matrix[solution[i].indis - 1][solution[i + 1].indis - 1]
    return total_profit


def tabu_search(best):
    route_len = len(best)
    tabu_list = []
    tabu_list_size = route_len
    candidate_size = route_len*3
    current = best.copy()
    tabu_best = best.copy()
    is_improved = True
    while is_improved:
        is_improved = False
        tabu_list = []
        for i in range(route_len*10):
            candidate_list = []
            for j in range(candidate_size):
                candidate_chosen = False
                t = 0
                while t < route_len and not candidate_chosen:
                    t += 1
                    swap_operator, difference, candidate = shuffle_swap(current)
                    if (swap_operator[0], swap_operator[1]) not in tabu_list and (swap_operator[1], swap_operator[0]) not in tabu_list:
                        candidate_list.append((swap_operator, difference, candidate))
                        candidate_chosen = True

            candidate_list.sort(key=lambda x: x[1], reverse=True)
            if not candidate_list:
                continue
            best_candidate = candidate_list[0]
            #if best_candidate[1] > 0:
            current = best_candidate[2]
            tabu_list.append(best_candidate[0])
            if len(tabu_list) > tabu_list_size:
                tabu_list.pop(0)
            #print('inner tabu current:', calculate_profit(current))
            if calculate_profit(current) > calculate_profit(tabu_best):
                is_improved = True
                tabu_best = current.copy()

        current = tabu_best.copy()
    return tabu_best

def tabu_search_3opt(best):
    route_len = len(best)
    tabu_list = []
    tabu_list_size = route_len
    candidate_size = route_len*3
    current = best.copy()
    tabu_best = best.copy()
    is_improved = True
    while is_improved:
        is_improved = False
        tabu_list = []
        for i in range(route_len*10):
            candidate_list = []
            for j in range(candidate_size):
                candidate_chosen = False
                t = 0
                while t < route_len and not candidate_chosen:
                    t += 1
                    swap_operator, difference, candidate = shuffle_flip(current)
                    if (swap_operator[0],swap_operator[1]) not in tabu_list and (swap_operator[1],swap_operator[0]) not in tabu_list:
                        candidate_list.append((swap_operator, difference, candidate))
                        candidate_chosen = True

            candidate_list.sort(key=lambda x: x[1], reverse=True)
            if not candidate_list:
                continue
            best_candidate = candidate_list[0]
            #if best_candidate[1] > 0:
            current = best_candidate[2]
            tabu_list.append(best_candidate[0])
            if len(tabu_list) > tabu_list_size:
                tabu_list.pop(0)
            #print('inner tabu current:', calculate_profit(current))
            if calculate_profit(current) > calculate_profit(tabu_best):
                is_improved = True
                tabu_best = current.copy()

        current = tabu_best.copy()
    return tabu_best


def solve_tsp():
    route = construct_route()
    print(route)
    print(calculate_profit(route))
    print("initial solution")
    print(route)
    print(calculate_profit(route))
    best = route
    unvisited_cities = []
    best, unvisited_cities = improve_solution([], route)
    print("improved initial solution")
    print(best)
    print(calculate_profit(best))

    for t in range(1):
        print("t=", t)
        if t == 0:
            tabu_best = best.copy()
        else:
            tabu_best = random.sample(a, len(a))
            unvisited_cities = []
        is_improved = True
        i = 0

        while is_improved and i < 100:
            is_improved = False
            i += 1
            for j in range(2):
                tabu_best = tabu_search(tabu_best)
                print("swap tabu search reasult : ", len(tabu_best), " ", calculate_profit(tabu_best))
                tabu_best, unvisited_cities = improve_solution(unvisited_cities, tabu_best)
                print("improved tabu reasult : ", len(tabu_best), " ", calculate_profit(tabu_best))
                if calculate_profit(tabu_best) > calculate_profit(best):
                    print("swap tabu search improved reasult : ", len(tabu_best), " ", calculate_profit(tabu_best))
                    best = tabu_best.copy()
                    is_improved = True
            if not is_improved:
                for j in range(2):
                    tabu_best = tabu_search_3opt(tabu_best)
                    print("tabu search reasult : ", len(tabu_best), " ", calculate_profit(tabu_best))
                    tabu_best, unvisited_cities = improve_solution(unvisited_cities, tabu_best)
                    print("improved tabu reasult : ", len(tabu_best), " ", calculate_profit(tabu_best))
                    if calculate_profit(tabu_best) > calculate_profit(best):
                        print("flip tabu search improved reasult : ", len(tabu_best), " ", calculate_profit(tabu_best))
                        best = tabu_best.copy()
                        is_improved = True
            tabu_best = best.copy()
            print("=====best===== ", len(best), calculate_profit(best))
            print(best)


# ## Main Solver

# list of customer locations (with coordinates and profit value)
a = []
init(file_name, dataset_name)
# matrix of the utilities gained by going from a city to a city
# profit of going from a to b = profit - distance of cities
customer_matrix = generate_customer_matrix(a)
start_time = time.time()
solve_tsp()
end_time = time.time()
print("CPU time : ", (end_time - start_time))

