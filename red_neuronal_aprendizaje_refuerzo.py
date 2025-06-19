# -*- coding: utf-8 -*-
"""
    Entrenamiento del agente en el entorno simulado.
    
    Este código entrena un agente para aprender a alcanzar una meta simple
    en un entorno simulado utilizando una red neuronal como modelo de Q-learning.
    
    El agente aprende a seleccionar acciones basadas en el estado actual y
    recibe recompensas por alcanzar la meta o penalizaciones por desviarse.
    
    El entrenamiento se realiza a través de múltiples episodios, donde el agente
    ajusta sus predicciones de Q-valor utilizando retropropagación y optimización.
    
    Al final del entrenamiento, se visualiza el rendimiento del agente a lo largo
    de los episodios mediante un gráfico de recompensas totales.
    
    Este código es un ejemplo básico de aprendizaje por refuerzo con redes neuronales
    y puede ser extendido o modificado para entornos más complejos.
    
Parte           Descripción
SimpleEnv	    Simula un entorno donde el objetivo es alcanzar un estado numérico.
DQN	            Red neuronal que aprende valores Q para cada acción.
select_action	Política ε-greedy: balancea exploración y explotación.
train()	        Ejecuta múltiples episodios, entrena usando DQN, y grafica progreso.
"""
# ==== 0. Librerias ====
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
import matplotlib.pyplot as plt

# ==== 1. Entorno simulado simple ====
class SimpleEnv:
    def __init__(self):
        self.state = 0  # Estado inicial (valor numérico)
        self.goal = 10  # Meta

    def reset(self):
        self.state = 0
        return np.array([self.state], dtype=np.float32)

    def step(self, action):
        # Acción 0: -1, Acción 1: +1
        if action == 0:
            self.state -= 1
        elif action == 1:
            self.state += 1

        reward = 1 if self.state == self.goal else -0.1
        done = self.state == self.goal
        return np.array([self.state], dtype=np.float32), reward, done

# ==== 2. Modelo de Red Neuronal ====
class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        self.fc = nn.Sequential(
            nn.Linear(1, 32),
            nn.ReLU(),
            nn.Linear(32, 2)  # Dos acciones: izquierda o derecha
        )

    def forward(self, x):
        return self.fc(x)

# ==== 3. Selección de acción (ε-greedy) ====
def select_action(model, state, epsilon):
    if random.random() < epsilon:
        return random.randint(0, 1)
    with torch.no_grad():
        state_tensor = torch.FloatTensor(state)
        q_values = model(state_tensor)
        return torch.argmax(q_values).item()

# ==== 4. Entrenamiento principal ====
def train():
    env = SimpleEnv()
    model = DQN()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    gamma = 0.9
    epsilon = 1.0
    epsilon_decay = 0.99
    min_epsilon = 0.01
    rewards_history = []

    for episode in range(200):
        state = env.reset()
        total_reward = 0

        for step in range(50):
            action = select_action(model, state, epsilon)
            next_state, reward, done = env.step(action)

            # Predicción actual
            q_values = model(torch.FloatTensor(state))
            q_value = q_values[action]

            with torch.no_grad():
                next_q = model(torch.FloatTensor(next_state))
                max_next_q = torch.max(next_q)
                expected_q = reward + gamma * max_next_q * (1 - int(done))

            loss = criterion(q_value, expected_q)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            state = next_state
            total_reward += reward

            if done:
                break

        epsilon = max(min_epsilon, epsilon * epsilon_decay)
        rewards_history.append(total_reward)
        print(f"Ep {episode+1}: Total Reward: {total_reward:.2f} Epsilon: {epsilon:.2f}")

    # Visualizar
    plt.plot(rewards_history)
    plt.xlabel("Episodios")
    plt.ylabel("Recompensa total")
    plt.title("Aprendizaje del agente")
    plt.grid()
    plt.show()

train()
