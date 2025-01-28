from common import *
from kcnf_generator import KCNFGenerator
from walksat import WalkSAT

def analyze_phase_transition(num_symbols, len_clauses, num_samples, num_ratios):
    ratios = np.linspace(0.5, 8, num_ratios)
    sat_probabilities = []    #Lista probabilità di soddisfacibilità
    avg_iterations_list = []  #Lista numero medio di iterazioni

    if num_symbols <= 0 or len_clauses <= 0 or num_samples <= 0 or num_ratios < 2:
        raise ValueError("num_symbols, len_clauses, num_samples devono essere > 0 e num_ratios >= 2")

    print("Analisi transizione di fase in corso...")
    for ratio in tqdm(ratios):
        num_clauses = int(ratio * num_symbols)
        sat_count = 0
        iterations_list = []

        for _ in range(num_samples):
            generator = KCNFGenerator(num_symbols, num_clauses, len_clauses)
            formula = generator.formula
            solver = WalkSAT(formula, 2000, 0.5)

            solution, iterations = solver.solve()
            iterations_list.append(iterations)

            if solution is not None:
                sat_count += 1

        sat_prob = sat_count / num_samples
        avg_iterations = np.mean(iterations_list)

        sat_probabilities.append(sat_prob)
        avg_iterations_list.append(avg_iterations)

    plt.figure(figsize=(12, 5))

    #Grafico probabilità di soddisfacibilità
    plt.subplot(1, 2, 1)
    plt.plot(ratios, sat_probabilities, 'b-', marker='+')
    plt.grid(True)
    plt.xlabel('rapporto clausole/simboli m/n')
    plt.ylabel('P (soddisfacibile)')

    #Grafico numero medio di iterazioni
    plt.subplot(1, 2, 2)
    plt.plot(ratios, avg_iterations_list, '--x', markersize=8, label='WalkSAT')
    plt.grid(True)
    plt.xlabel('rapporto clausole/simboli m/n')
    plt.ylabel('numero medio di iterazioni')
    plt.ylim(0, 2000)
    plt.legend()

    plt.tight_layout()
    plt.show()

def run_analysis():
    n = 50             #Numero di simboli proposizionali
    k = 3              #Numero letterali per clausola
    num_samples = 100  #Numero di formule generate per ciascun rapporto m/n
    num_ratios = 50    #Numero di rapporti m/n

    analyze_phase_transition(n, k, num_samples, num_ratios)

if __name__ == "__main__":
    run_analysis()