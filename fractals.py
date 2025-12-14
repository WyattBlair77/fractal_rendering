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

        self.edges = self.init_edges
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

    def compute_coordinates(self, edges, start_pos=(0, 0)):
        """Convert edges to absolute (x, y) coordinates using vectorized NumPy."""
        n = len(edges)

        # Extract angles and lengths as numpy arrays
        angles = np.array([e['angle'] for e in edges])
        lengths = np.array([e['length'] for e in edges])

        # Convert to radians
        radians = np.deg2rad(angles)

        # Compute dx, dy for each edge
        dx = lengths * np.cos(radians)
        dy = lengths * np.sin(radians)

        # Build coordinate arrays with start position
        x = np.zeros(n + 1)
        y = np.zeros(n + 1)
        x[0], y[0] = start_pos

        # Cumulative sum to get absolute positions
        x[1:] = x[0] + np.cumsum(dx)
        y[1:] = y[0] + np.cumsum(dy)

        return np.column_stack((x, y))

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

            if len(new_angles) > 0:

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


class DragonCurve(Fractal):
    """
    The Dragon Curve - a self-similar fractal that looks like a dragon
    viewed from above. Created by folding a strip of paper in half repeatedly.
    """

    def __init__(self, init_length):
        self.turns = []  # Will store turn directions: 1 = left, -1 = right
        super().__init__(
            init_length=init_length,
            init_angle=0,
            fractal_update_func=self.dragon_update,
            init_edges=[{'length': init_length, 'angle': 0}]
        )

    def dragon_update(self, edges: list[dict]) -> list[dict]:
        # Dragon curve rule: take existing turns, add a left turn,
        # then add the reverse of existing turns with flipped directions
        new_turns = self.turns + [1] + [-t for t in reversed(self.turns)]
        self.turns = new_turns

        # Convert turns to edges
        new_edges = []
        current_angle = 0
        for turn in new_turns:
            new_edges.append({'length': self.init_length, 'angle': current_angle})
            current_angle += turn * 90

        # Add final edge
        new_edges.append({'length': self.init_length, 'angle': current_angle})

        return new_edges


class LevyCCurve(Fractal):
    """
    The Levy C Curve (or Levy Dragon) - a self-similar fractal that creates
    beautiful symmetric tree-like patterns from a single line.
    """

    def __init__(self, init_length):
        super().__init__(
            init_length=init_length,
            init_angle=0,
            fractal_update_func=self.levy_update,
            init_edges=[{'length': init_length, 'angle': 0}]
        )

    def levy_update(self, edges: list[dict]) -> list[dict]:
        new_edges = []
        scale = 1 / np.sqrt(2)  # Each segment shrinks by sqrt(2)

        for edge in edges:
            # Each edge becomes two edges at 45-degree angles
            new_length = edge['length'] * scale
            new_edges.append({'length': new_length, 'angle': edge['angle'] + 45})
            new_edges.append({'length': new_length, 'angle': edge['angle'] - 45})

        return new_edges


class SierpinskiArrowhead(Fractal):
    """
    The Sierpinski Arrowhead Curve - draws the Sierpinski triangle
    as a single continuous line using 60-degree angles.
    """

    def __init__(self, init_length):
        self.iteration = 0
        super().__init__(
            init_length=init_length,
            init_angle=0,
            fractal_update_func=self.sierpinski_update,
            init_edges=[{'length': init_length, 'angle': 0}]
        )

    def sierpinski_update(self, edges: list[dict]) -> list[dict]:
        new_edges = []
        # Alternate the pattern based on iteration
        self.iteration += 1
        flip = 1 if self.iteration % 2 == 1 else -1

        for edge in edges:
            new_length = edge['length'] / 2
            base_angle = edge['angle']

            # Pattern: turn left 60, forward, turn right 60, forward, turn left 60
            new_edges.append({'length': new_length, 'angle': base_angle + flip * 60})
            new_edges.append({'length': new_length, 'angle': base_angle})
            new_edges.append({'length': new_length, 'angle': base_angle - flip * 60})

        return new_edges


class MooreCurve(Fractal):
    """
    The Moore Curve - a variant of the Hilbert curve that forms a closed loop.
    It's a space-filling curve that returns to its starting point.
    """

    def __init__(self, init_length):
        self.rules = {
            'L': 'LFL+F+LFL',
            'R': 'RFR-F-RFR'
        }
        # Start with the Moore curve axiom
        self.state = '-LFL+F+LFL-'
        super().__init__(
            init_length=init_length,
            init_angle=0,
            fractal_update_func=self.moore_update,
            init_edges=self._state_to_edges(init_length, '-LFL+F+LFL-')
        )

    def _state_to_edges(self, length, state):
        """Convert L-system state string to edge list."""
        edges = []
        current_angle = 90  # Start facing up

        for char in state:
            if char == 'F':
                edges.append({'length': length, 'angle': current_angle})
            elif char == '+':
                current_angle += 90
            elif char == '-':
                current_angle -= 90
            # L and R are just markers for rewriting, not drawing

        return edges

    def moore_update(self, edges: list[dict]) -> list[dict]:
        # Apply L-system rewriting rules
        new_state = ''
        for char in self.state:
            if char in self.rules:
                new_state += self.rules[char]
            else:
                new_state += char

        self.state = new_state
        return self._state_to_edges(self.init_length, self.state)


class GosperCurve(Fractal):
    """
    The Gosper Curve (Flowsnake) - a space-filling curve with hexagonal
    symmetry, using 60-degree angles for an organic, flowing appearance.
    """

    def __init__(self, init_length):
        # L-system: A -> A-B--B+A++AA+B-
        #           B -> +A-BB--B-A++A+B
        self.state = 'A'
        super().__init__(
            init_length=init_length,
            init_angle=0,
            fractal_update_func=self.gosper_update,
            init_edges=[{'length': init_length, 'angle': 0}]
        )

    def _state_to_edges(self, length, state):
        """Convert L-system state string to edge list."""
        edges = []
        current_angle = 0

        for char in state:
            if char in ('A', 'B'):  # Both A and B mean forward
                edges.append({'length': length, 'angle': current_angle})
            elif char == '+':
                current_angle += 60
            elif char == '-':
                current_angle -= 60

        return edges

    def gosper_update(self, edges: list[dict]) -> list[dict]:
        rules = {
            'A': 'A-B--B+A++AA+B-',
            'B': '+A-BB--B-A++A+B'
        }

        new_state = ''
        for char in self.state:
            if char in rules:
                new_state += rules[char]
            else:
                new_state += char

        self.state = new_state
        return self._state_to_edges(self.init_length, self.state)
