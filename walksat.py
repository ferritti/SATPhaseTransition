from common import *

class WalkSAT:
    def __init__(self, formula, max_flips, p):
        if not 0 <= p <= 1:
            raise ValueError("p deve essere tra 0 e 1")
        if max_flips <= 0:
            raise ValueError("max_flips deve essere positivo")

        self.formula = formula
        self.max_flips = max_flips
        self.p = p
        self.symbols = self.extract_symbols()

    #Estrae i simboli dalla formula
    def extract_symbols(self):
        variables = set()
        for clause in self.formula:
            for literal in clause:
                var = literal[len(NEG):] if literal.startswith(NEG) else literal
                variables.add(var)
        return variables

    #Assegna valori casuali ai simboli
    def initialize_assignment(self):
        return {var: random.choice([True, False]) for var in self.symbols}

    #Controlla se l'assegnamento soddisfa un letterale
    def is_literal_satisfied(self, literal, assignment):
        if literal.startswith(NEG):
            return not assignment[literal[len(NEG):]]
        return assignment[literal]

    #Controlla se l'assegnamento soddisfa una clausola
    def is_clause_satisfied(self, clause, assignment):
        return any(self.is_literal_satisfied(lit, assignment) for lit in clause)

    #Conta le clausole soddisfatte dall'assegnamento
    def count_satisfied_clauses(self, assignment):
        return sum(1 for clause in self.formula if self.is_clause_satisfied(clause, assignment))

    #Conta le clausole insoddisfatte dall'assegnamento
    def count_unsatisfied_clauses(self, assignment):
        return sum(1 for clause in self.formula if not self.is_clause_satisfied(clause, assignment))

    #Trova una clausola insoddisfatta
    def find_unsatisfied_clause(self, assignment):
        for clause in self.formula:
            if not self.is_clause_satisfied(clause, assignment):
                return clause
        return None

    #Conta quante clausole sarebbero soddisfatte dopo il flip di un simbolo
    def count_satisfied_clauses_after_flip(self, sym, assignment):
        new_assignment = assignment.copy()
        new_assignment[sym] = not new_assignment[sym]
        return self.count_satisfied_clauses(new_assignment)


    def solve(self):
        model = self.initialize_assignment()
        num_flips = 0

        while num_flips < self.max_flips:
            if self.count_unsatisfied_clauses(model) == 0:
                return model, num_flips

            #Trova una clausola insoddisfatta
            clause = self.find_unsatisfied_clause(model)

            #Estrae i simboli proposizionali dalla clausola
            symbols = [lit[len(NEG):] if lit.startswith(NEG) else lit for lit in clause]

            if random.random() <= self.p:
                sym = random.choice(symbols) #Scelta casuale del simbolo
            else:
                best_sym = None
                best_score = -1

                #Scelta del simbolo che massimizza il numero di clausole soddisfatte dopo il flip
                for s in symbols:
                    score = self.count_satisfied_clauses_after_flip(s, model)
                    if score > best_score:
                        best_score = score
                        best_sym = s

                sym = best_sym

            model[sym] = not model[sym] #Flip del valore di verità del simbolo

            num_flips += 1

        return None, num_flips