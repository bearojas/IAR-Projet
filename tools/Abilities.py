#!/usr/bin/python3
# -*-coding: utf-8 -*

from enum import Enum, auto


class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Abilities(AutoName):
    DEFAULT = auto()
    NO_SELECTION = auto()
    SELECTION = auto()
    NO_SWITCHING = auto()
    SWITCHING = auto()
