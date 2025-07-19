import numpy as np
from hmmlearn import hmm

""""
necessario rodar o comando `pip install hmmlearn`, caso não tiver instalado essa biblioteca
"""



"""
Matriz de Probabilidades de Transição (A)
A[i, j] = P(estado_proximo=j | estado_atual=i)
Estados: 0 = 'Andando', 1 = 'Parado'
Se Andando (0): 80% de chance de continuar Andando, 20% de ir para Parado
Se Parado (1): 10% de chance de ir para Andando, 90% de continuar Parado

"""
trans_matrix = np.array([
    [0.8, 0.2],  # De 'Andando' para 'Andando', 'Parado'
    [0.1, 0.9]   # De 'Parado' para 'Andando', 'Parado'
])

"""
Matriz de Probabilidades de Emissão (B)
B[i, j] = P(observacao=j | estado_atual=i)
Observações: 0 = 'Movimento Detectado', 1 = 'Sem Movimento'
Se Andando (0): 70% de chance de Detectar Movimento, 30% de Não Detectar
Se Parado (1): 5% de chance de Detectar Movimento, 95% de Não Detectar

"""

emission_matrix = np.array([
    [0.7, 0.3],  # De 'Andando' para 'Detectado', 'Não Detectado'
    [0.05, 0.95] # De 'Parado' para 'Detectado', 'Não Detectado'
])

"""
Probabilidades Iniciais do Estado (pi)
P(estado_inicial=i)
60% de chance de começar Andando, 40% de começar Parado
"""

start_probs = np.array([0.6, 0.4])

"""
Criar o modelo HMM
n_components: número de estados ocultos
n_iter: número de iterações para o algoritmo de aprendizado (se estivéssemos treinando)
verbose: para ver o progresso (coloque True para depuração)
"""
model = hmm.CategoricalHMM(n_components=2, random_state=42, n_iter=100)
model.startprob_ = start_probs
model.transmat_ = trans_matrix
model.emissionprob_ = emission_matrix

# Simular uma sequência de observações (o que o sensor detecta)
# Uma sequência de 5 minutos, a cada minuto
# 0 = 'Movimento Detectado', 1 = 'Sem Movimento'
# Observações: [Detectado, Não Detectado, Detectado, Detectado, Não Detectado]

observations = np.array([[0], [1], [0], [0], [1]])

print("Sequência de Observações (0=Detectado, 1=Não Detectado):\n", observations.T)

# aqui prever a sequência de estados ocultos mais provável
# O metodo predict usa o algoritmo de Viterbi para encontrar a sequência mais provável.
logprob, hidden_states = model.decode(observations, algorithm="viterbi")

print("\nLog-probabilidade da sequência observada:", logprob)
print("Sequência de Estados Ocultos Inferred (0=Andando, 1=Parado):\n", hidden_states)

# Traduzir os estados para algo legivel
state_map = {0: 'Andando', 1: 'Parado'}
inferred_activity = [state_map[s] for s in hidden_states]
print("\nAtividade Inferida (mais provável):\n", inferred_activity)
