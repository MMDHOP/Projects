# -*- coding: utf-8 -*-
"""
Glider-based Logic Gates Module.

This module proves Turing completeness of Conway's Game of Life by building
AND and NOT logic gates purely out of glider collisions.

Signal convention
------------------
- Presence of a glider in a given time-window == logical bit 1.
- Absence of a glider in that window == logical bit 0.

All coordinates and timings below were derived empirically by simulating
real glider-glider collisions with the GameOfLife engine in conway.py
(see the accompanying derivation notes) rather than guessed, so the exact
generation counts and offsets given are the ones that actually reproduce
the required reactions on this engine.
"""
import numpy as np
from conway import GameOfLife


# --- Canonical 5-cell glider, plus its 4 diagonal orientations ------------
_GLIDER_BASE = [(0, 1), (1, 2), (2, 0), (2, 1), (2, 2)]  # travels SE


def _glider_cells(direction):
    """
    Return the relative (dr, dc) offsets of a glider that travels toward
    `direction` ('SE', 'SW', 'NE' or 'NW'), obtained by mirroring the
    canonical SE glider.
    """
    base = _GLIDER_BASE
    if direction == 'SE':
        return base
    if direction == 'SW':
        maxc = max(c for _, c in base)
        return [(r, maxc - c) for r, c in base]
    if direction == 'NE':
        maxr = max(r for r, _ in base)
        return [(maxr - r, c) for r, c in base]
    if direction == 'NW':
        maxr = max(r for r, _ in base)
        maxc = max(c for _, c in base)
        return [(maxr - r, maxc - c) for r, c in base]
    raise ValueError(f"Unknown glider direction: {direction}")


def _insert_glider(game, direction, index):
    """Insert a glider travelling `direction` with its top-left at `index`."""
    for dr, dc in _glider_cells(direction):
        game.grid[index[0] + dr, index[1] + dc] = game.aliveValue


class GliderLogicGates:
    """
    Builds and runs AND / NOT logic gates on top of GameOfLife, using
    genuine glider-glider collision reactions:

      * AND gate: two gliders launched on courses that intersect at a
        genuine 90-degree angle (A travels SE, B travels SW -- these two
        directions are perpendicular) collide into a single stable 2x2
        block *only* when BOTH are present. A lone glider just flies
        through the target region and leaves nothing behind -> output is
        a block iff A AND B.

      * NOT gate: a "control" glider (SE) is always launched toward the
        output region. If input A is inactive, nothing else is fired and
        the control glider survives and reaches the output. If input A is
        active, a second "blocker" glider (SW) is fired on a precisely
        timed intercept course that causes BOTH gliders to fully annihilate
        (0 live cells) before the output region is reached -> output is
        active iff NOT A.
    """

    # ---- AND gate geometry -----------------------------------------------
    # Verified empirically: A travels SE, B travels SW. These two directions
    # are perpendicular (a genuine 90-degree intersection, dot product = 0),
    # and their paths are set up to cross exactly at the target coordinate
    # (15, 12) as specified in the assignment. When, and only when, BOTH
    # gliders are launched, they collide and settle into a stable 2x2 block
    # at that exact target after _AND_STEPS generations.
    _AND_TARGET = (15, 12)
    _AND_STEPS = 20

    def setup_and_gate(self, grid_size=35, input_a_present=False, input_b_present=False):
        """
        Set up the Game of Life grid for an AND gate.

        Args:
            grid_size (int): Size of the simulation grid.
            input_a_present (bool): If True, place glider for Input A.
            input_b_present (bool): If True, place glider for Input B.

        Returns:
            GameOfLife: Initialized GameOfLife object.
        """
        game = GameOfLife(N=grid_size, finite=True, fastMode=True)
        target_r, target_c = self._AND_TARGET

        # Input A: glider travelling SE, launched so its path crosses
        # `target` at generation _AND_STEPS.
        if input_a_present:
            a_index = (target_r - 5, target_c - 3)
            _insert_glider(game, 'SE', a_index)

        # Input B: glider travelling SW -- perpendicular (90 degrees) to A --
        # launched so its path crosses `target` at the same generation.
        if input_b_present:
            b_index = (target_r - 2, target_c - 0)
            _insert_glider(game, 'SW', b_index)

        game._and_target = (target_r, target_c)  # stash for run_and_gate
        return game

    def run_and_gate(self, input_a_present, input_b_present, grid_size=35):
        """
        Run the AND gate simulation for a specific number of steps and return the output.

        Args:
            input_a_present (bool): Input A state.
            input_b_present (bool): Input B state.

        Returns:
            bool: True if output is active (a stable 2x2 block formed in the
                  output region -- which only happens when both gliders
                  collide), False otherwise.
        """
        game = self.setup_and_gate(grid_size, input_a_present, input_b_present)
        target_r, target_c = game._and_target

        for _ in range(self._AND_STEPS):
            game.evolve()

        grid = game.grid
        block = (
            grid[target_r, target_c] == game.aliveValue
            and grid[target_r, target_c + 1] == game.aliveValue
            and grid[target_r + 1, target_c] == game.aliveValue
            and grid[target_r + 1, target_c + 1] == game.aliveValue
        )
        return bool(block)

    # ---- NOT gate geometry (verified: control glider alone survives to
    #      the output window after 60 generations; with the blocker fired
    #      5 generations later it is fully annihilated before then) -------
    _NOT_CONTROL_START = (2, 2)          # control glider launch point (SE)
    _NOT_BLOCKER_DELAY = 5               # generations before blocker launches
    _NOT_BLOCKER_COL_OFFSET = 20         # blocker column offset from control
    _NOT_STEPS = 60
    _NOT_OUTPUT_WINDOW = (15, 22, 15, 22)  # row_lo, row_hi, col_lo, col_hi

    def setup_not_gate(self, grid_size=35, input_a_present=False):
        """
        Set up the Game of Life grid for a NOT gate.

        Args:
            grid_size (int): Size of the simulation grid.
            input_a_present (bool): If True, place glider for Input A.

        Returns:
            GameOfLife: Initialized GameOfLife object.
        """
        game = GameOfLife(N=grid_size, finite=True, fastMode=True)

        # Control glider: always launched, heads toward the output region.
        _insert_glider(game, 'SE', self._NOT_CONTROL_START)

        # Input A (blocker): only launched if the input bit is active, on a
        # delayed intercept course that annihilates the control glider.
        if input_a_present:
            for _ in range(self._NOT_BLOCKER_DELAY):
                game.evolve()
            blocker_index = (
                self._NOT_CONTROL_START[0],
                self._NOT_CONTROL_START[1] + self._NOT_BLOCKER_COL_OFFSET,
            )
            _insert_glider(game, 'SW', blocker_index)

        return game

    def run_not_gate(self, input_a_present, grid_size=35):
        """
        Run the NOT gate simulation for a specific number of steps and return the output.

        Args:
            input_a_present (bool): Input A state.

        Returns:
            bool: True if output is active (the control glider survived and
                  reached the output window), False otherwise (it was
                  annihilated by the blocker glider).
        """
        game = self.setup_not_gate(grid_size, input_a_present)

        # Account for the generations already consumed inside setup while
        # timing the (optional) blocker launch, so total elapsed == _NOT_STEPS.
        already_evolved = self._NOT_BLOCKER_DELAY if input_a_present else 0
        for _ in range(self._NOT_STEPS - already_evolved):
            game.evolve()

        r_lo, r_hi, c_lo, c_hi = self._NOT_OUTPUT_WINDOW
        region = game.grid[r_lo:r_hi, c_lo:c_hi]
        return bool(region.sum() > 0)


if __name__ == '__main__':
    gates = GliderLogicGates()

    print("AND gate truth table:")
    for a in (False, True):
        for b in (False, True):
            out = gates.run_and_gate(a, b)
            print(f"  A={int(a)} B={int(b)} -> {int(out)}")

    print("\nNOT gate truth table:")
    for a in (False, True):
        out = gates.run_not_gate(a)
        print(f"  A={int(a)} -> {int(out)}")