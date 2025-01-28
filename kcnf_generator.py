from common import *

class KCNFGenerator:
    def __init__(self, num_symbols, num_clauses, len_clause):
        if num_symbols <= 0 or num_clauses <= 0 or len_clause <= 0:
            raise ValueError("numero simboli, numero clausole e lunghezza clausola devono essere > 0")

        self.n = num_symbols
        self.m = num_clauses
        self.k = len_clause
        self.literals = self.generate_literals()
        self.formula = self.generate_formula()


    def generate_literals(self):
        letters = string.ascii_uppercase
        literals = []

        length = 1
        while len(literals) < self.n:
            combinations = [''.join(c) for c in product(letters, repeat=length)] #Combinazioni di lettere di lunghezza length
            literals.extend(combinations[:self.n - len(literals)]) #Aggiunge le combinazioni mancanti
            length += 1

        negated_literals = [f"{NEG}{lit}" for lit in literals] #Letterali negativi
        return literals + negated_literals


    #Controlla se è presente almeno un letterale sia nella forma positiva che negativa
    def is_tautology(self, clause):
        for lit in clause:
            if lit.startswith(NEG):
                positive = lit[len(NEG):] #Estrae la sotto-stringa senza il simbolo NEG
                if positive in clause:
                    return True
            else:
                negative = f"{NEG}{lit}"
                if negative in clause:
                    return True
        return False


    #Genera una clausola che non è tautologica e con k letterali distinti
    def generate_clause(self):
        while True:
            clause = frozenset(random.sample(self.literals, self.k)) #Crea una clausola con k letterali distinti (immutabile)

            if not self.is_tautology(clause):
                return clause


    #Genera una formula k-CNF completa con m clausole distinte
    def generate_formula(self):
        formula = []
        seen_clauses = set()


        while len(formula) < self.m:
            new_clause = self.generate_clause()

            #Aggiunge la clausola solo se non è già presente
            if new_clause not in seen_clauses:
                formula.append(new_clause)
                seen_clauses.add(new_clause)

        return formula


    def formula_to_string(self, formula):
        clauses = []
        for clause in formula:
            clause_str = f" ∨ ".join(clause)
            clauses.append(f"({clause_str})")

        return f" ∧ ".join(clauses)