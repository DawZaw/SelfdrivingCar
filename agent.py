from __future__ import annotations

from collections import deque
import random
import torch
import numpy as np
from model import QNet, QTrainer

from typing import TYPE_CHECKING

from settings import *

if TYPE_CHECKING:
    from game import Game


class Agent:
    n_games: int
    epsilon: float
    gamma: float
    memory: deque
    model: QNet
    trainer: QTrainer

    def __init__(self, input_size: int) -> None:
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = QNet(input_size, 256, 3)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game: Game) -> np.ndarray:
        state: list[float] = []
        for sensor in game.car.sensors:
            state.append(sensor.length)
        return np.array(state, dtype=np.float32)

    def remember(
        self,
        state: np.ndarray,
        action: list[int],
        reward: int,
        next_state: np.ndarray,
        done: bool,
    ) -> None:
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self) -> None:
        if len(self.memory) > BATCH_SIZE:
            sample: list[deque] | deque = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = self.memory
        states, actions, rewards, next_states, dones = zip(*sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(
        self,
        state: np.ndarray,
        action: list[int],
        reward: int,
        next_state: np.ndarray,
        done: bool,
    ) -> None:
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state: np.ndarray) -> list[int]:
        self.epsilon = 200 - self.n_games
        final_move: list[int] = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move: int = random.randint(0, 2)
        else:
            state0: torch.Tensor = torch.tensor(state, dtype=torch.float32)
            prediction: torch.Tensor = self.model(state0)
            move = int(torch.argmax(prediction).item())
        final_move[move] = 1
        return final_move
