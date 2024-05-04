from typing import Callable
from tqdm.auto import tqdm
import numpy as np

class Fractal:

    def __init__(self, init_length: int, init_angle: int, fractal_update_func: Callable, init_edges: list[dict]=None):

        self.init_length = init_length
        self.init_angle = init_angle

        if init_edges is None:
            self.init_edges = [{'length': self.init_length, 'angle': self.init_angle}]
        else:
            self.init_edges = init_edges

        self.edges = self.init_edges.copy()
        self.fractal_update_func = fractal_update_func
        self.current_recursion_level = 0

    def reset(self):

        self.edges = [{'length': self.init_length, 'angle': self.init_angle}]
        self.current_recursion_level = 0

    def update(self):

        starting_edges = self.edges.copy()

        if self.current_recursion_level == 0:
            print(f'Current Recursion Level: {self.current_recursion_level+1}', end='')
        else:
            print(f'-->{self.current_recursion_level+1}', end='')

        new_edges = self.fractal_update_func(starting_edges)

        self.edges = new_edges
        self.current_recursion_level += 1

    def generate(self, desired_recursion_level):

        if desired_recursion_level == self.current_recursion_level:
            print()

            finished_edges = self.edges.copy()
            self.reset()

            return finished_edges
        
        else:
            self.update()
            return self.generate(
                desired_recursion_level=desired_recursion_level,
            )

class KochCurve(Fractal):

    def __init__(self, init_length, init_angle):
        super().__init__(init_length=init_length, init_angle=init_angle, fractal_update_func=self.koch_update)

    def koch_update(self, edges: list[dict]) -> list[dict]:
        new_edges = []

        for edge in edges:
            
            new_edges.append({'length': edge['length']/2, 'angle': edge['angle'] + 45})
            new_edges.append({'length': edge['length']/2, 'angle': edge['angle'] - 45})

        return new_edges
    
class HilbertCurve(Fractal):

    def __init__(self, init_length):
        
        self.triplet_map = {
            'D': np.array([0  , 90 , 180]),
            'A': np.array([90 , 0  , -90]),
            'B': np.array([180, -90, 0  ]),
            'C': np.array([-90, 180, 90 ]),
        }

        super().__init__(init_length=init_length, init_angle=90, fractal_update_func=self.hilbert_update, init_edges=self.get_init_edges(init_length, 90))

    def get_init_edges(self, init_length, init_angle):

        edge_1 = {'length': init_length, 'angle': init_angle    }
        edge_2 = {'length': init_length, 'angle': init_angle-90 }
        edge_3 = {'length': init_length, 'angle': init_angle-180}

        init_edges = [edge_1, edge_2, edge_3]
        return init_edges

    def get_letter(self, triplet_angles):

        which_triplet = np.all(np.array(list(self.triplet_map.values())) == np.broadcast_to(triplet_angles, shape=(4, 3)), axis=1)
        letters = np.array(list(self.triplet_map.keys()))[:, np.newaxis]

        letter = letters[which_triplet].squeeze().tolist()

        return letter

    def get_new_angles(self, triplet_letter):

        angle_map = {
            'A': np.concatenate(
                [
                    self.triplet_map['D'], 
                    [90], 
                    self.triplet_map['A'], 
                    [0], 
                    self.triplet_map['A'], 
                    [270], 
                    self.triplet_map['B']
                ]
            ),
            'B': np.concatenate(
                [
                    self.triplet_map['C'], 
                    [180], 
                    self.triplet_map['B'], 
                    [270], 
                    self.triplet_map['B'], 
                    [0], 
                    self.triplet_map['A']
                ]
            ),
            'C': np.concatenate(
                [
                    self.triplet_map['B'], 
                    [270], 
                    self.triplet_map['C'], 
                    [180], 
                    self.triplet_map['C'], 
                    [90], 
                    self.triplet_map['D']
                ]
            ),
            'D': np.concatenate(
                [
                    self.triplet_map['A'], 
                    [0], 
                    self.triplet_map['D'], 
                    [90], 
                    self.triplet_map['D'], 
                    [180], 
                    self.triplet_map['C']
                ]
            ),
        }

        if triplet_letter:
            new_angles = angle_map[triplet_letter]

        else:
            new_angles = []

        return new_angles

    def hilbert_update(self, edges: list[dict]) -> list[dict]:
        
        # based on this very helpful diagram: https://en.wikipedia.org/wiki/Hilbert_curve#/media/File:Hilbert_curve_production_rules!.svg
        angles = np.array([edge['angle'] for edge in edges])

        new_edges = []
        i = 0

        while i < len(angles)-2:

            triplet = angles[i:i+3]
            letter = self.get_letter(triplet)
            new_angles = self.get_new_angles(letter)

            if new_angles != []:

                new_triplet_edges = [
                    {'length': self.init_length, 'angle': angle}
                    for angle in new_angles
                ]

                if len(angles) > 3 and (i + 3) < len(angles):
                    new_triplet_edges += [{'length': self.init_length, 'angle': angles[i+3]}]

                new_edges += new_triplet_edges
                i += 4
            
            else:
                continue

        return new_edges
