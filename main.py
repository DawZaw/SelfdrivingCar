import numpy as np
import pygame as pg
from agent import Agent
from game import Game
from settings import *

game: Game = Game()
agent: Agent = Agent(input_size=len(game.car.sensors))


def main() -> None:
    highscore: int = 0
    while True:
        CLOCK.tick(FPS)
        fps: str = str(int(CLOCK.get_fps()))
        pg.display.set_caption("Selfdriving Car | FPS: " + fps)
        game.handle_events()

        # Get initial state
        state_old: np.ndarray = agent.get_state(game)
        # Get move
        final_move: list[int] = agent.get_action(state_old)
        # Performe move and get new state
        reward: int
        done: bool
        score: int
        reward, done, score = game.update(final_move)
        state_new: np.ndarray = agent.get_state(game)

        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # Remember
        agent.remember(state_old, final_move, reward, state_new, done)

        # Train long memory if game over
        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > highscore:
                highscore = score

        game.draw()
        game.display_text("Generation", agent.n_games, 15, 15)
        game.display_text("Highscore", highscore, 15, 40)
        game.display_text("Score", game.car.score, 15, 65)
        pg.display.update()


if __name__ == "__main__":
    main()
else:
    pass
