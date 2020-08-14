#!/usr/bin/env python

import os
import sys
import pytest

from janitor_bot.cogs.replace import set_replacement, send_replacement, remove_replacement, get_keywords

@pytest.mark.parametrize("keyword, value, expected_result", [
    ("test", "pass", {"test": "pass"}),
    ("test123", "pass321", {"test123": "pass321", "test": "pass"}),
    ("Trump", "2020", {"test123": "pass321", "Trump": "2020", "test": "pass"}),
    ("2020", "1920", {"test123": "pass321", "Trump": "2020", "2020": "1920", "test": "pass"}),
    ])
def test_setKeyword(keyword, value, expected_result):
    set_replacement(keyword, value) 
    assert get_keywords() == expected_result

@pytest.mark.parametrize("message, new_message", [
    ("test", "pass"),
    ("asdftest123jkl;", "asdfpass321jkl;"),
    ("asdftest123jklTrump 2020;", "asdfpass321jkl1920 1920;"),
    ])
def test_send_replacement(message, new_message):
    assert send_replacement(message) == new_message

@pytest.mark.parametrize("keyword, expected_result", [
    ("2020", {"test123": "pass321", "Trump": "2020", "test": "pass"}),
    ("test123", {"Trump": "2020", "test": "pass"}),
    ("Trump", {"test": "pass"}),
    ])
def test_remove_replacement(keyword, expected_result):
    remove_replacement(keyword) 
    assert get_keywords() == expected_result

def test_removeReplacementErr():
    with pytest.raises(Exception):
        removeReplacement("word not in dict")

