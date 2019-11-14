from neat.reporting import BaseReporter
from neat.nn import FeedForwardNetwork
from agents import RandomAgent
import pickle       # pip install cloudpickle

class OpponentTracker(BaseReporter):

    def __init__(self, reset_number=10, save_opponents=True):
        self._generations = 0
        self._best_net = None
        self._best_fitness = None
        self._reset_number = reset_number
        self._current_opponent = RandomAgent()
        self._last_fitness = None
        self._best_ever = None
        self._save_opponents = save_opponents

    def post_evaluate(self, config, population, species, best_genome):
        if self._best_net is None or best_genome.fitness > self._best_fitness:
            self._best_net = FeedForwardNetwork.create(best_genome, config)
            self._best_fitness = best_genome.fitness
            if self._best_ever is None or self._best_fitness > self._best_ever:
                self._best_ever = self._best_fitness
        print("Best fitness so far in this cycle", self._best_fitness, ", Best fitness ever", self._best_ever, ", Currently used agent:", "random" if self._last_fitness is None else self._last_fitness)
        self._generations += 1
        if self._generations >= self._reset_number:
            is_random = self._last_fitness is not None and self._best_fitness < self._last_fitness
            print("Resetting opponent, last fitness was",
                    "random" if self._last_fitness is None else self._last_fitness,
                    "new fitness is",
                    "random" if is_random else self._best_fitness)
            if is_random:
                self._current_opponent = RandomAgent()
                self._last_fitness = None
            else:
                self._current_opponent = self._best_net
                self._last_fitness = self._best_fitness
                self._best_fitness = None
                self._best_net = None
                if self._save_opponents:
                    with open('opponent-net-{}.pkl'.format(self._last_fitness), 'wb') as output:
                        pickle.dump(self._current_opponent, output, 1)

            self._generations = 0

    @property
    def current_opponent(self):
        return self._current_opponent
