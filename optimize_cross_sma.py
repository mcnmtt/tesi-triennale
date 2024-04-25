from operator import itemgetter
import warnings
warnings.filterwarnings("ignore")

from random import choices
import cross_sma_buysell as cross_sma

def genera_coppie_sma():

    coppie_valori_sma = []

    for sma1 in range(10,55,1):
        for sma2 in range(15,85,1):
            if sma2 > sma1:
                coppia_rsi = (sma1,sma2)
                coppie_valori_sma.append(coppia_rsi)

    return coppie_valori_sma

def inizializza(): # Genera la popolazione iniziale con genoma che rappresenta tutte le coppie (upperbound, lowerbound) con una votazione associata ad ogni coppia.

    coppie_sma = genera_coppie_sma()  # Contiene tutte le combinazioni di limite superiore (da 60 a 80 di 2 in 2) e limite inferiore (da 20 a 40 di 2 in 2) per l'RSI.

    popolazione = []

    for i in range(len(coppie_sma)):
        membro = {
        'genoma': coppie_sma[i],
        'voto': 0
        }
        popolazione.append(membro)
    return popolazione
  
def fitness(popolazione): # Assegna una votazione ad ogni genoma sulla base del rapporto tra "max drawdown","profitto finale","win rate" e "numero di trade".

    for i in range(len(popolazione)): # Itera ed assegna una votazione ad ogni coppia di valori di ogni membro della popolazione.

        membro_popolazione = popolazione[i]
        sma1, sma2 = membro_popolazione["genoma"]

        return_value = cross_sma.run_backtest(sma1=sma1, sma2=sma2)

        # Prendo i dati normalizzati risultanti dal backtesting e assegno un peso per fare incidere o meno un dato specifico. Infine li sommo per ottenere una votazione.

        membro_popolazione["voto"] = round(return_value, 2)

    return popolazione
  
def selezione(popolazione):
    
    # Filtra i valori negativi e "nan"
    popolazione_filtrata = [membro for membro in popolazione if membro["voto"] >= 0 and not isinstance(membro["voto"], str)]
    
    # Ordina la popolazione filtrata
    popolazione_ordinata = sorted(popolazione_filtrata, key=itemgetter("voto"), reverse=True)
    
    return popolazione_ordinata[:10]

def crossover(popolazione): # Utilizzo selezione ad un punto per effettuare il crossover.
    import itertools

    figli = []

    # Eseguo il crossover.

    for figlio in itertools.combinations(popolazione, 2):
        genoma1 = figlio[0]["genoma"]
        genoma2 = figlio[1]["genoma"]
        
        figlio1 = {"genoma": (genoma1[0], genoma2[1]), "voto": 0}
        figlio2 = {"genoma": (genoma2[0], genoma1[1]), "voto": 0}

        figli.append(figlio1)
        figli.append(figlio2)

    # Rimuovo membri della nuova popolazione ripetuti. Lasciando 1 sola ripetizione per ogni membro.
    
    figli_visti = set()
    figli_no_rip = []

    for figlio in figli:   
        genoma = figlio["genoma"]
        if genoma not in figli_visti:
            figli_visti.add(genoma)
            figli_no_rip.append(figlio)
    
    return figli_no_rip


def mutazione(popolazione):
    import random

    # Numero casuale di mutazioni da effettuare.
    num_mutazioni = random.randint(1, len(popolazione))

    for i in range(num_mutazioni):
        # Seleziono un figlio dalla popolazione in modo randomico
        random_figlio = random.choice(popolazione)
        indice_random_figlio = popolazione.index(random_figlio)

        genoma = random_figlio["genoma"]

        # Effettuo la mutazione sommando o sottraendo in modo randomico 2 ad uno dei due elementi che compongono il "genoma" di ogni figlio.
        indice_elemento = random.randint(0, 1)
        x = genoma[0]
        y = genoma[1]
        
        if indice_elemento == 0:
            if not x - 1 <= 0:
                x += random.choice([-1, 1])

        if indice_elemento == 1:
            if not y - 1 <= 0:
                y += random.choice([-1, 1])

        nuovo_genoma = (x,y)

        random_figlio["genoma"] = nuovo_genoma

        # Sostituisco il figlio mutato alla sua versione non mutata nella popolazione.
        popolazione[indice_random_figlio] = random_figlio

    return popolazione

def evoluzione():

    import time
    import math

    start_time = time.time()

    numero_generazioni = 20

    popolazione = inizializza()

    for i in range(numero_generazioni):

        popolazione = fitness(popolazione)
        
        popolazione = selezione(popolazione)
        popolazione = crossover(popolazione)

    fitness(popolazione=popolazione)

    popolazione_finale = sorted(filter(lambda x: not isinstance(x['voto'], float) or not math.isnan(x['voto']), popolazione), key=lambda x: x['voto'], reverse=True)

    end_time = time.time()
    exec_time = end_time - start_time

    print("sma1 ottimale: ", popolazione_finale[0]["genoma"][0])
    print("sma2 bound ottimale: ", popolazione_finale[0]["genoma"][1])
    print(round(exec_time,2), "secondi")

evoluzione()