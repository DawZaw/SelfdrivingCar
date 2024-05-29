# Selfdriving Car using DQN

## Description
This project showcases Deep Q-Network (DQN) capabilities to teach agent how to steer a car based on detected distance from a car to the edge of a track.
DQN is a type of reinforcement learning algorithm, where agent is placed in certain environment, and is capable of performing specified actions.
Based on reward and punishment system, agent tries to maximize rewards, while avoiding punishments. In this example reward is given for every frame the car is driving, while punishment is given when car touches edge of a track.

### Features
- procedurally generated track on every episode
- raycasting for detecting edges of a track
- DQN model 

### Built with
- Pygame
- PyTorch

#### Start of learning process
At the beginning agent is exploring new environment, a lot of crashes are expected.
<div align="center">
    <img src="images/first_episodes.gif" />
</div>

#### After 200 episodes
After some episodes agent adapts his driving skill to stay on track for longer period of time.
<div align="center">
    <img src="images/200_episode.gif" />
</div>

