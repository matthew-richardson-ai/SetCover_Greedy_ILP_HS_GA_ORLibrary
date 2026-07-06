import numpy as np


# --- 1. INITIALIZATION ---
def initialize_population(pop_size, num_subsets):
    """Generates a starting population of random candidate solutions."""
    return np.random.randint(2, size=(pop_size, num_subsets))


# --- 2. REPAIR LOGIC ---
def repair_chromosome(chromosome, subsets, universe_size):
    """Checks if a chromosome is valid and fixes missing elements."""
    covered = set()
    for idx, selected in enumerate(chromosome):
        if selected == 1:
            covered.update(subsets[idx])

    if len(covered) == universe_size:
        return chromosome

    for idx, selected in enumerate(chromosome):
        if selected == 0:
            current_subset = set(subsets[idx])
            if not current_subset.issubset(covered):
                chromosome[idx] = 1
                covered.update(current_subset)

        if len(covered) == universe_size:
            break

    return chromosome


# --- 3. FITNESS EVALUATION ---
def calculate_fitness(chromosome, subsets, universe_size):
    """Evaluates the quality of a candidate solution after running repair."""
    repaired_chrom = repair_chromosome(chromosome, subsets, universe_size)
    chromosome[:] = repaired_chrom[:]
    return int(np.sum(chromosome))


# --- 4. SELECTION ---
def selection(population, fitness_scores, tournament_size=3):
    """Selects a parent chromosome from the population using Tournament Selection."""
    pop_size = len(population)
    random_indices = np.random.choice(pop_size, size=tournament_size, replace=False)
    best_index = random_indices[np.argmin(fitness_scores[random_indices])]
    return population[best_index].copy()


def crossover(parent1, parent2):
    """
    Combines two parent chromosomes using single-point crossover
    to produce a single offspring chromosome.
    """
    num_subsets = len(parent1)

    # 1. Choose a random index along the chromosome length to split on
    crossover_point = np.random.randint(1, num_subsets)

    # 2. Combine the slices: Parent 1 (left side) + Parent 2 (right side)
    offspring = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))

    return offspring


def mutate(chromosome, mutation_rate=0.01):
    """
    Iterates through the chromosome and flips bits based on a mutation rate
    probability to maintain genetic diversity.
    """
    # 1. Generate a random float between 0.0 and 1.0 for each bit position
    mutation_mask = np.random.rand(len(chromosome)) < mutation_rate

    # 2. Use a bitwise XOR to invert the bits where the mask evaluates to True
    # (1 becomes 0, 0 becomes 1)
    chromosome[mutation_mask] = 1 - chromosome[mutation_mask]

    return chromosome


def run_genetic_algorithm(
    subsets, universe_size, pop_size=100, generations=500, mutation_rate=0.01
):
    """
    Main evolutionary optimization loop.
    Executes selection, crossover, mutation, and tracking over defined generations.
    """
    num_subsets = len(subsets)

    # 1. Initialize the starting population
    population = initialize_population(pop_size, num_subsets)

    # Track the absolute best solution found across all generations
    best_chromosome = None
    best_fitness = float("inf")  # We want to minimize, so start infinitely high

    # 2. Begin the generational loop
    for generation in range(generations):
        # Calculate fitness for the current population
        fitness_scores = np.array(
            [calculate_fitness(chrom, subsets, universe_size) for chrom in population]
        )

        # Track the best individual in this generation
        current_best_idx = np.argmin(fitness_scores)
        if fitness_scores[current_best_idx] < best_fitness:
            best_fitness = fitness_scores[current_best_idx]
            best_chromosome = population[current_best_idx].copy()

        # Optional: Print generation progress updates
        if (generation + 1) % 50 == 0 or generation == 0:
            print(
                f"Generation {generation + 1}/{generations} | Best Cover Size Found: {best_fitness}"
            )

        # 3. Breed the next generation
        next_population = []

        # Keep the absolute best individual from this generation (Elitism)
        # This guarantees we never lose our top solution due to random mutation
        next_population.append(population[current_best_idx].copy())

        # Fill the rest of the new population slot capacity
        while len(next_population) < pop_size:
            # Selection: Pick two distinct parents using our tournament setup
            parent1 = selection(population, fitness_scores)
            parent2 = selection(population, fitness_scores)

            # Crossover: Combine genes to create a new offspring
            offspring = crossover(parent1, parent2)

            # Mutation: Inject random variations
            offspring = mutate(offspring, mutation_rate)

            next_population.append(offspring)

        # Overwrite old population with the freshly evolved generation
        population = np.array(next_population)

    return best_chromosome, best_fitness
