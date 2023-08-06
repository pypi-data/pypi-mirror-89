from abc import ABC, abstractmethod

import attr

import numpy as np

from .ast.node import TooManyShapesError
from .ast.expression import Variable, Constant
from .ast.drawing import Primitive
from .grammar import grammar
from .renderer import forward_transform


class Sampler(ABC):
    def __init__(self, rng):
        self.rng = rng

    @abstractmethod
    def sample(self, variables, production="D", depth=0):
        pass

    def sample_inputs(self, variables):
        inputs = {}
        for variable in variables:
            inputs[variable] = self.sample({}, production=Constant).value
        return inputs


def probabilities_for_weights(items, weights):
    probs = []
    for item in items:
        if isinstance(item, list):
            item = item[0]
        probs.append(weights.get(item, 1))
    probs = np.array(probs, dtype=np.float64)
    probs /= probs.sum()
    return probs


class PCFGSampler(Sampler):
    def __init__(self, rng, grammar=grammar, weights={}, max_depth=float("inf")):
        super().__init__(rng)
        self.weights = weights
        self.grammar = grammar
        self.max_depth = max_depth

    def sample_from_list(self, items):
        probs = probabilities_for_weights(items, self.weights)
        idx = self.rng.choice(len(probs), p=probs)
        return items[idx]

    def sample(self, variables, production="D", depth=0):
        if depth > self.max_depth:
            raise DepthExceededError
        variables = set(variables)
        if production == Variable:
            return Variable.parse(self.sample_from_list(sorted(variables)))
        if isinstance(production, type):
            tag = self.sample_from_list(production.tags())
            return production.parse(tag)

        if isinstance(production, list):
            start, *rules = production
            tag = self.sample_from_list(start.tags())
            return start.parse(
                tag, [self.sample(variables, rule, depth + 1) for rule in rules]
            )

        assert isinstance(production, str)
        rule = self.sample_from_list(self.grammar[production])
        if isinstance(rule, list):
            start = rule[0]
        else:
            start = rule
        custom_sample = start.custom_sample(self, variables, depth)
        if custom_sample is not None:
            return custom_sample
        return self.sample(variables, rule, depth)


class DepthExceededError(Exception):
    pass


def item_within_bounding_box(item, size):
    if np.linalg.det(item.transform[:2, :2]) < 1e-7:
        return False  # degenerate
    points_of_interest = (
        np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
        .astype(np.float)
        .T.reshape(2, -1, 1)
    )
    new_pois = forward_transform(item.transform, points_of_interest)
    return (new_pois <= size).all()


class InputSampler:
    def __init__(self, underlying, *, image_size, num_inputs):
        self.underlying = underlying
        self.image_size = image_size
        self.num_inputs = num_inputs

    def sample(self, variables, silent=True):
        while True:
            try:
                program = self.underlying.sample(variables)
            except DepthExceededError:
                continue
            io = self.sample_inputs(program, variables, silent=silent)
            if io is not None:
                return (program, *io)

    def sample_inputs(self, program, variables, silent=True):
        tokens = set(program.code)
        if isinstance(program, Primitive):
            return
        for var in variables:
            if var not in tokens:
                return
        if "white" in tokens:
            return
        if not ("combine" in tokens or "repeat" in tokens):
            return
        if not silent:
            print("considering: ", " ".join(program.code))

        inputs = [
            self.underlying.sample_inputs(variables) for _ in range(self.num_inputs)
        ]
        try:
            outputs = [program.evaluate(inp) for inp in inputs]
        except ZeroDivisionError:
            return
        except TooManyShapesError:
            return

        bad = 0
        for o in outputs:
            within, not_within = 0, 0
            for item in o:
                if item_within_bounding_box(item, self.image_size / 2):
                    within += 1
                else:
                    not_within += 1
            if within <= 1 or not_within / len(o) > 0.5:
                bad += 1
        if bad > 0:
            return

        return inputs, outputs
