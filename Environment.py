import numpy as np
import pygame
import gymnasium as gym
from gymnasium import spaces


class HideAndSeekEnv(gym.Env): # type: ignore
    def __init__(self, file_path : str):
        self.action_space = spaces.Discrete(8)
        self.action_to_directions ={
            0: np.array([0, -1]),
            1: np.array([1, -1]),
            2: np.array([1, 0]),
            3: np.array([1, 1]),
            4: np.array([0, 1]),
            5: np.array([-1, 1]),
            6: np.array([-1, 0]),
            7: np.array([-1, -1])
        }
        self.observation_space = spaces.Dict(
            {
                "seeker" : spaces.Box(low=0, high=7, shape=(2,), dtype = np.int8),
                "hider" : spaces.Box(low=0, high=5, shape=(2,), dtype = np.int8),
            }
        )
        self.window : None | pygame.Surface = None
        self.clock : None | pygame.time.Clock = None

        with open(file_path, "r") as f:
            self._n, self._m = [int (x) for x in f.readline().split()]
            self._map = np.array([[int(x) for x in line[:-1]] for line in f.readlines()])
            self._instance_map = np.array(self._map)

    def _obs(self): 
        hider = np.array([])
        seeker = np.array([])
        for i in range(self._n):
            for j in range(self._m):
                if self._map[i, j] == 3:
                    seeker = np.array([i, j])
                elif self._map[i, j] == 2:
                    np.append(hider, np.array([i, j]))
        return {"seeker": seeker, "hider": hider}

    def reset(self):
        self._map = np.array(self._instance_map)
        return self._obs()

if __name__ == "__main__":
    env = HideAndSeekEnv("map.txt")

