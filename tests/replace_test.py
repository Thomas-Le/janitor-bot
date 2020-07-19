#!/usr/bin/env python

import os
import sys
import pytest

from janitor_bot.cogs.replace import setReplacement, sendReplacement, keywords


def test_setKeyword():
    assert setReplacement("test", "pass") == {"test": "pass"}
    assert setReplacement("test123", "pass321") == {
        "test123": "pass321",
        "test": "pass",
    }
    assert setReplacement("Trump", "2020") == {
        "test123": "pass321",
        "Trump": "2020",
        "test": "pass",
    }
    assert setReplacement("2020", "1920") == {
        "test123": "pass321",
        "Trump": "2020",
        "2020": "1920",
        "test": "pass",
    }


def test_sendReplacement():
    assert sendReplacement("test") == "pass"
    assert sendReplacement("asdftest123jkl;") == "asdfpass321jkl;"
    assert sendReplacement("asdftest123jklTrump 2020;") == "asdfpass321jkl1920 1920;"
