import torch
import numpy as np

from actor import Actor, preprocessing
from environment import Environment

num_epochs = 10000
games_in_epoch = 40

best_score = 0

def train_epoch(env, model):
    states_per_game = []
    actions_per_game = []
    rewards_per_game = []
    for i in range(games_in_epoch):
        env.reset()
        states = []
        actions = []
        state, reward, finished = env.observation()
        moves_left = 1000
        while not finished and moves_left:
            states.append(preprocessing(state))
            action = model.act(states[-1])
            state, reward, finished = env.step(action)
            actions.append(action)
            moves_left -= 1
        states_per_game.append(torch.cat(states))
        actions_per_game.append(torch.tensor(actions, dtype=torch.int))
        rewards_per_game.append(reward)
        # print(f"Game {1 + i} finished with score {reward}")
    rewards = np.array(rewards_per_game)
    rewards_norm = (rewards - rewards.mean()) / rewards.std()
    for state_batch, action_batch, norm_reward in zip(states_per_game, actions_per_game, rewards_norm):
        model.learn_game(state_batch, action_batch, norm_reward)
    print(f"Average score: {rewards.mean()}")
    global best_score
    if rewards.mean() > best_score:
        best_score = rewards.mean()
        print("New best, saving model...")
        model.save_scripted()
    print()
    return rewards.mean()


def save(mean_rewards, reward_log_path="/results/reward_curve"):
    open(reward_log_path, "w").write("\n".join([str(x) for x in mean_rewards]))

def main():
    env = Environment(invalid_move_penalty=.5)
    model = Actor(lr=0.0003)
    mean_rewards = []
    for i in range(num_epochs):
        print(f"Epoch {1 + i} started")
        mean_rewards.append(train_epoch(env, model))
        if i % 10 == 0:
            save(mean_rewards)


if __name__ == "__main__":
    main()
