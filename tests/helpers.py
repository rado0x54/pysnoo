# -*- coding: utf-8 -*-
"""Helper Module for the PySnoo tests."""
import os


def load_fixture(folder, filename, mode='r'):
    """Load a fixture."""
    path = os.path.join(os.path.dirname(__file__),
                        'fixtures', folder, filename)
    with open(path, mode) as fdp:
        return fdp.read()
