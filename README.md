# Analisi della Transizione di Fase nel k-SAT con WalkSAT

Questo progetto studia la transizione di fase nel problema di soddisfacibilità booleana (k-SAT) generando formule k-CNF casuali e risolvendole con l'algoritmo WalkSAT. Produce grafici che mostrano:
- la probabilità che una formula sia soddisfacibile al variare del rapporto m/n (clausole/simboli),
- il numero medio di iterazioni impiegate da WalkSAT.

## Contenuto del progetto
- `common.py`: import comuni (numpy, matplotlib, tqdm, ecc.) e costanti condivise. Definisce `NEG = '¬'` come simbolo di negazione.
- `kcnf_generator.py`: classe `KCNFGenerator` per generare formule k-CNF con:
  - n simboli proposizionali (lettere A, B, ..., anche combinazioni AA, AB, ... se servono),
  - m clausole distinte,
  - clausole di lunghezza k con letterali distinti e non tautologiche (non contengono sia X che ¬X).
- `walksat.py`: classe `WalkSAT`, un risolutore SAT locale randomizzato con parametri:
  - `formula`: lista di clausole (ogni clausola è un `frozenset` di stringhe letterali, es. "A", "¬B"),
  - `max_flips`: massimo numero di flip consentiti (> 0),
  - `p`: probabilità di scelta casuale del simbolo nella clausola insoddisfatta (0 ≤ p ≤ 1).
- `phase_transition.py`: esegue l'analisi della transizione di fase:
  - genera formule per vari rapporti m/n,
  - risolve con WalkSAT,
  - stima la probabilità di soddisfacibilità e l'iterato medio,
  - disegna due grafici con matplotlib.

## Requisiti
- Python 3.8+ (consigliato 3.10+)
- Dipendenze Python:
  - numpy
  - matplotlib
  - tqdm

Installa le dipendenze con:
```bash
pip install numpy matplotlib tqdm
```

Nota: il progetto usa il simbolo Unicode `¬` (negazione). Assicurati che il terminale/font supporti Unicode.

## Utilizzo rapido
Dal terminale, posizionati nella cartella del progetto ed esegui:
```bash
python3 phase_transition.py
```
Questo avvierà l'analisi con i parametri di default:
- n = 50 (numero di simboli proposizionali)
- k = 3 (letterali per clausola, quindi 3-CNF)
- num_samples = 100 (formule generate per ciascun rapporto m/n)
- num_ratios = 50 (numero di valori del rapporto m/n tra 0.5 e 8)

Al termine verranno mostrati due grafici:
1) Probabilità di soddisfacibilità P(soddisfacibile) vs m/n.
2) Numero medio di iterazioni di WalkSAT vs m/n.

Durante l'esecuzione vedrai una progress bar (tqdm). L'analisi può richiedere da qualche decina di secondi a diversi minuti a seconda dei parametri e della macchina.

## Come modificare i parametri
I parametri principali sono definiti in `phase_transition.py`:
- Funzione `run_analysis()`:
  ```python
  n = 50            # Numero di simboli proposizionali
  k = 3             # Numero di letterali per clausola (k-CNF)
  num_samples = 100 # Numero di formule per ciascun m/n
  num_ratios = 50   # Numero di rapporti m/n da campionare in [0.5, 8]
  ```
  Modifica questi valori per personalizzare l'esperimento.

- Funzione `analyze_phase_transition(num_symbols, len_clauses, num_samples, num_ratios)`:
  - Valida che `num_symbols > 0`, `len_clauses > 0`, `num_samples > 0`, `num_ratios >= 2`.
  - Per ogni rapporto `ratio` (m/n) calcola `num_clauses = int(ratio * num_symbols)` e:
    - genera una formula k-CNF con `KCNFGenerator(num_symbols, num_clauses, len_clauses)`,
    - risolve con `WalkSAT(formula, max_flips=2000, p=0.5)` (modificabile nel file se desideri),
    - raccoglie esito (soddisfacibile o no) e iterazioni impiegate.

- Parametri di WalkSAT (in `phase_transition.py`):
  ```python
  solver = WalkSAT(formula, 2000, 0.5)  # max_flips=2000, p=0.5
  ```
  Puoi aumentare `max_flips` o cambiare `p` (0..1) per esplorare comportamenti diversi.

## Esempi
- Eseguire con parametri più piccoli (più veloce):
  ```python
  # In phase_transition.py
  n = 30
  k = 3
  num_samples = 40
  num_ratios = 30
  ```
- Usare WalkSAT manualmente su una formula generata:
  ```python
  from kcnf_generator import KCNFGenerator
  from walksat import WalkSAT

  gen = KCNFGenerator(num_symbols=20, num_clauses=80, len_clause=3)
  formula = gen.formula

  solver = WalkSAT(formula, max_flips=5000, p=0.4)
  model, flips = solver.solve()
  if model is not None:
      print("Soddisfacibile in", flips, "flip")
  else:
      print("Non trovato assegnamento entro", flips, "flip")
  ```

## Rappresentazione delle formule
- Un letterale è una stringa: ad esempio `"A"` o `"¬B"` (il simbolo di negazione è `NEG = '¬'`).
- Una clausola è un `frozenset` di letterali distinti.
- Una formula è una lista di clausole.
- `KCNFGenerator` evita tautologie: non produce clausole con sia `X` sia `¬X`.

## Struttura della cartella
```
AI project/
├── common.py
├── kcnf_generator.py
├── walksat.py
├── phase_transition.py
└── README.md
```

## Output atteso
- Finestra grafica con due subplot:
  - P(soddisfacibile) vs m/n (linea blu con marker "+").
  - Iterazioni medie vs m/n (linea tratteggiata con marker "x").
- In console: messaggi di avanzamento e progress bar.

## Consigli e troubleshooting
- Esecuzione lenta: riduci `num_samples` e/o `num_ratios`, o abbassa `n`.
- Troppi insoddisfacibili nel regime denso: aumenta `max_flips` o cambia `p`.
- Errori su pacchetti mancanti: installa `numpy`, `matplotlib`, `tqdm` come indicato.
- Problemi con il simbolo `¬`: assicurati che il file sia in UTF-8 e il terminale supporti Unicode.