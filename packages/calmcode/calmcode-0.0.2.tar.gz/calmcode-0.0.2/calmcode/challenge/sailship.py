from collections import Counter
import numpy as np
from scipy.spatial import distance_matrix


class TravellingSalesmanShip:
    def __init__(self, n_ports=250, shape="uniform", angle_penalty=1.75, seed=42):
        self.seed = seed
        self.n_ports = n_ports
        self.shape = shape
        self.angle_penalty = angle_penalty
        np.random.seed(self.seed)
        self.coordinates = np.random.uniform(0, 1, size=(self.n_ports, 2))
        self.distance_matrix = distance_matrix(self.coordinates, self.coordinates)

    @staticmethod
    def angle_between(v1, v2):
        """Returns the angle in radians between vectors 'v1' and 'v2'"""
        v1_u = v1 / v1.sum()
        v2_u = v2 / v2.sum()
        return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    def score(self, solution):
        """
        Calculates a score for a given solution.
        """
        self.check_solution(solution=solution)
        tour = solution["tour"]
        total_distance, total_angle, total_score = 0, 0, 0
        for i in range(self.n_ports):
            a, b, c = tour[i - 2], tour[i - 1], tour[i]
            delta_dist = self.distance_matrix[a, b] / 2 + self.distance_matrix[b, c] / 2
            v1 = self.coordinates[b] - self.coordinates[a]
            v2 = self.coordinates[b] - self.coordinates[c]
            delta_angle = self.angle_between(v1, v2) * self.angle_penalty
            total_distance += delta_dist
            total_angle += delta_angle
            total_score += delta_angle + delta_dist
        return {
            "score": total_score,
            "total_distance": total_distance,
            "total_angle": total_angle,
        }

    def check_solution(self, solution):
        """
        Checks if a solution is feasible.
        """
        tour = solution["tour"]
        all_ports = [i for i in range(self.n_ports)]
        double = Counter(tour + all_ports)
        if not all([v == 2 for v in double.values()]):
            missing = [p for p in all_ports if p not in tour]
            extra = [k for k, v in Counter(all_ports).items() if v > 1]
            report = f"""Incorrect submission.\nThe following ports were visited more than once: {extra}.\nThe following ports were missing {missing}."""
            raise ValueError(report)
