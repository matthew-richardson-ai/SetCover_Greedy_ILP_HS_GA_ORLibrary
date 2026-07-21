"""
===============================================================================
CSC 2400 — Term Project: Unweighted Set Cover Problem (SCP)
Module: Harmony Search (HS) & Binary Repair Function
Author: Abdullah Javed
===============================================================================
Description:
    Nature-inspired metaheuristic utilizing Harmony Memory (HM), Harmony Memory
    Considering Rate (HMCR), and Pitch Adjusting Rate (PAR). Includes a custom 
    three-stage binary repair function to guarantee 100% universe coverage.

Complexity:
    Theta(T * HMS * m) where T is max_iter, HMS is Harmony Memory Size, 
    and m is total available subsets.
===============================================================================
"""
import numpy as np

# --- 1. REPAIR LOGIC ---
def repair_harmony(harmony, subsets, universe_size):
    """
    Specialized binary repair function to handle uncovered universe elements.
    Ensures the candidate solution is mathematically valid.
    """
    covered = set()
    
    # Step 1: Track elements covered by currently selected subsets
    for idx, selected in enumerate(harmony):
        if selected == 1:
            covered.update(subsets[idx])
            
    # Step 2: If all elements are covered, the solution is valid
    if len(covered) == universe_size:
        return harmony
        
    # Step 3: If not fully covered, greedily add subsets to fill the gaps
    for idx, selected in enumerate(harmony):
        if selected == 0:
            current_subset = set(subsets[idx])
            # Only switch a bit to '1' if the subset contributes unrepresented elements
            if not current_subset.issubset(covered):
                harmony[idx] = 1
                covered.update(current_subset)
                
        # Break early if the universe is fully covered to save compute cycles
        if len(covered) == universe_size:
            break
            
    # Fallback Heuristic: If still uncovered due to rigid iteration, clear the remaining gaps
    if len(covered) < universe_size:
        uncovered_elements = set(range(universe_size)) - covered
        while uncovered_elements:
            # Find the remaining subset that covers the maximum number of uncovered elements
            best_subset_idx = -1
            best_cover_count = -1
            
            for idx, subset in enumerate(subsets):
                intersection_len = len(set(subset).intersection(uncovered_elements))
                if intersection_len > best_cover_count:
                    best_cover_count = intersection_len
                    best_subset_idx = idx
            
            if best_subset_idx != -1:
                harmony[best_subset_idx] = 1
                uncovered_elements -= set(subsets[best_subset_idx])
            else:
                break # Avoid infinite loop if an instance is structurally unsolvable
            
    return harmony

# --- 2. FITNESS EVALUATION ---
def calculate_fitness(harmony, subsets, universe_size):
    """
    Evaluates the quality of an improvised harmony (candidate solution).
    Lower fitness scores are better (fewer subsets used).
    """
    repaired_harmony = repair_harmony(harmony, subsets, universe_size)
    harmony[:] = repaired_harmony[:]
    return int(np.sum(harmony))

# --- 3. HARMONY SEARCH ALGORITHM ---
def run_harmony_search(subsets, universe_size, hms=30, hmcr=0.85, par=0.1, max_iter=500):
    """
    Nature-inspired Harmony Search metaheuristic optimization loop.
    
    Parameters:
    - hms: Harmony Memory Size (equivalent to population size)
    - hmcr: Harmony Memory Considering Rate (probability of choosing a gene from memory)
    - par: Pitch Adjusting Rate (probability of mutating a memory-selected gene)
    - max_iter: Total number of improvisation cycles
    """
    num_subsets = len(subsets)
    
    # 1. Initialize the Harmony Memory (HM) with random valid solutions
    harmony_memory = np.random.randint(2, size=(hms, num_subsets))
    fitness_scores = np.zeros(hms)
    
    for i in range(hms):
        fitness_scores[i] = calculate_fitness(harmony_memory[i], subsets, universe_size)
        
    best_harmony = None
    best_fitness = float("inf")
    
    # Establish our starting best-case scenario
    current_best_idx = np.argmin(fitness_scores)
    if fitness_scores[current_best_idx] < best_fitness:
        best_fitness = fitness_scores[current_best_idx]
        best_harmony = harmony_memory[current_best_idx].copy()
        
    # 2. Begin the main improvisation loop
    for iteration in range(max_iter):
        new_harmony = np.zeros(num_subsets, dtype=int)
        
        # Improvise a new candidate solution bit by bit
        for j in range(num_subsets):
            
            # Memory Consideration Phase
            if np.random.rand() < hmcr:
                random_hm_idx = np.random.randint(0, hms)
                new_harmony[j] = harmony_memory[random_hm_idx, j]
                
                # Pitch Adjustment Phase (Bit-flip mutation)
                if np.random.rand() < par:
                    new_harmony[j] = 1 - new_harmony[j]
            else:
                # Random Selection Phase
                new_harmony[j] = np.random.randint(2)
                
        # 3. Apply the repair function and evaluate the new harmony
        new_fitness = calculate_fitness(new_harmony, subsets, universe_size)
        
        # 4. Update the Harmony Memory if the new solution outperforms the worst one
        worst_idx = np.argmax(fitness_scores)
        if new_fitness < fitness_scores[worst_idx]:
            harmony_memory[worst_idx] = new_harmony
            fitness_scores[worst_idx] = new_fitness
            
        # Update the absolute historical best 
        if new_fitness < best_fitness:
            best_fitness = new_fitness
            best_harmony = new_harmony.copy()
            
        # Print progress tracking logic exactly like the Genetic Algorithm module
        if (iteration + 1) % 50 == 0 or iteration == 0:
            print(f"HS Iteration {iteration + 1}/{max_iter} | Best Cover Size Found: {best_fitness}")
            
    return best_harmony, best_fitness
