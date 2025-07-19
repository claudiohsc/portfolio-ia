import numpy as np
import matplotlib.pyplot as plt

""""
necessario rodar o comando `pip install matplotlib`, caso não tiver instalado essa biblioteca
"""

# Temperatura verdadeira (que não conhecemos diretamente)
true_temp = 22.5 #  Celsius
num_steps = 50   # Numero de medições ao longo do tempo

# Matriz de Transicao de Estado (A) - Temperatura constante
A = np.array([[1.0]])

# Matriz de Observacao (C) - Medimos diretamente a temperatura
C = np.array([[1.0]])


# Pequena incerteza no modelo (a temp pode variar um pouco)
Q = np.array([[0.01]]) # Variacao de 0.01 graus a cada passo


# Grande incerteza do sensor (medicao ruidosa)
R = np.array([[1.0]]) # Variacao de 1.0 graus no ruído do sensor

# Inicializacao do Filtro de Kalmann

# Estimativa inicial do estado (temperatura)
x_hat_k = np.array([[20.0]]) # Chute 

# Covariância de erro inicial (P)
# Alta incerteza no nosso chute inicial
P_k = np.array([[1000.0]])

# Listas para armazenar os resultados para plotagem
true_temps = []
noisy_measurements = []
estimated_temps = []

# Simulacao e Aplicacao do Filtro de Kalman
for k in range(num_steps):
    # Simular a temperatura "verdadeira" com pequena variacao
    true_temp_actual = true_temp + np.random.normal(0, np.sqrt(Q[0,0]))
    true_temps.append(true_temp_actual)

    # Simular a medicao ruidosa do sensor
    measurement = true_temp_actual + np.random.normal(0, np.sqrt(R[0,0]))
    noisy_measurements.append(measurement)

    

    # Etapa de Tempo
    
    x_pred = A @ x_hat_k # @ para multiplicacao de matrizes

    
    P_pred = A @ P_k @ A.T + Q

    # Etapa de Medicao
    # Ganho de Kalman (K)
    
    K = P_pred @ C.T @ np.linalg.inv(C @ P_pred @ C.T + R)

    # Estado estimado atualizado
   
    x_hat_k = x_pred + K @ (measurement - C @ x_pred)

    # Covariância de erro atualizada
    # P_k = (I - K * C) * P_pred
    P_k = (np.eye(A.shape[0]) - K @ C) @ P_pred

    # Armazenar a estimativa para plotagem
    estimated_temps.append(x_hat_k[0,0])

# Plota os resultados
plt.figure(figsize=(10, 6))
plt.plot(true_temps, label='Temperatura Verdadeira', color='green', linestyle='--')
plt.plot(noisy_measurements, 'x', label='Medições Ruidosas', color='red', alpha=0.6)
plt.plot(estimated_temps, label='Estimativa do Filtro de Kalman', color='blue')
plt.title('Estimativa de Temperatura da Sala com Filtro de Kalman')
plt.xlabel('Passo de Tempo')
plt.ylabel('Temperatura (°C)')
plt.legend()
plt.grid(True)
plt.show()