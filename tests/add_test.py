#!/usr/bin/env python

import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../janitor-bot")
from add import add


def test_add():
    assert add(3, 5) == 8
