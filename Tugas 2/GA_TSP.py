import random
# Membuat matriks jarak antar kota secara acak
def create_distance_matrix(num_cities):
    matrix = []
    for i in range(num_cities):
        row = []
        for j in range(num_cities):
            if i == j:
                row.append(0)
            elif j > i:
                row.append(random.randint(1, 100))
            else:
                row.append(matrix[j][i])
        matrix.append(row)
    return matrix

# Membuat populasi awal secara acak
def create_initial_population(num_cities, pop_size):
    population = []
    for i in range(pop_size):
        individual = list(range(num_cities))
        random.shuffle(individual)
        population.append(individual)
    return population

# Menghitung jarak total dari sebuah rute
def calculate_distance(route, distance_matrix):
    dist = 0
    for i in range(len(route)-1):
        dist += distance_matrix[route[i]][route[i+1]]
    dist += distance_matrix[route[-1]][route[0]]
    return dist

# Memilih individu dengan metode tournament selection
def tournament_selection(population, k, distance_matrix):
    selected = []
    for i in range(len(population)):
        tournament = random.sample(population, k)
        winner = min(tournament, key=lambda x: calculate_distance(x, distance_matrix))
        selected.append(winner)
    return selected

# Menggabungkan parent menjadi child
def mate(parent1, parent2):
    child = [-1] * len(parent1)
    start, end = sorted([random.randint(0, len(parent1)-1) for _ in range(2)])
    for i in range(start, end+1):
        child[i] = parent1[i]
    remaining_cities = [c for c in parent2 if c not in child]
    for i in range(len(child)):
        if child[i] == -1:
            child[i] = remaining_cities.pop(0)
    return child

# Melakukan mutasi pada sebuah individu
def mutate(individual):
    start, end = sorted([random.randint(0, len(individual)-1) for _ in range(2)])
    individual[start:end+1] = reversed(individual[start:end+1])
    return individual

# Menggunakan genetic algorithm untuk menyelesaikan TSP
def genetic_algorithm(distance_matrix, pop_size, num_generations, mutation_rate, k):
    # Membuat populasi awal secara acak
    population = create_initial_population(len(distance_matrix), pop_size)

    for generation in range(num_generations):
        # Memilih parents dengan metode tournament selection
        parents = tournament_selection(population, k, distance_matrix)

        # Menghasilkan child memlaui mate
        offspring = []
        for i in range(0, pop_size-2, 2):
            parent1, parent2 = parents[i], parents[i+1]
            child1 = mate(parent1, parent2)
            child2 = mate(parent2, parent1)
            offspring.extend([child1, child2])

        # Memilih parent terbaik untuk dijadikan elitism
        elite = min(population, key=lambda x: calculate_distance(x, distance_matrix))

        # Melakukan mutasi pada setiap keturunan
        for i in range(len(offspring)):
            if random.random() < mutation_rate:
                offspring[i] = mutate(offspring[i])

        # Menambahkan elitism ke populasi dan menghapus individu paling buruk
        population = sorted(offspring + [elite], key=lambda x: calculate_distance(x, distance_matrix))[:pop_size]

        # Menampilkan jarak terpendek pada setiap 10 generasi
        if generation % 10 == 0:
            print("Generation ", generation, ": ", calculate_distance(population[0], distance_matrix))

    # Mengembalikan rute terbaik yang ditemukan
    return population[0]

if __name__ == "__main__":
    # Membuat matriks jarak antar kota secara acak
    distance_matrix = create_distance_matrix(10)

    # Menjalankan algoritma genetika untuk TSP
    best_route = genetic_algorithm(distance_matrix, pop_size=100, num_generations=500, mutation_rate=0.1, k=10)

    # Mencetak hasil
    print("Best route found:", best_route)
    print("Distance:", calculate_distance(best_route, distance_matrix))
