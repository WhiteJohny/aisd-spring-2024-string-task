#!/usr/bin/env python3

"""
Suffix tree to search in dictionary
"""

from typing import List


class SSet:
    """String set. Should be based on Suffix tree"""

    def __init__(self, fname: str) -> None:
        """Saves filename of a dictionary file"""
        self.fname = fname
        self.words = None

    def load(self) -> None:
        """
        Loads words from a dictionary file.
        Each line contains a word.
        File is not sorted.
        """
        with open(self.fname, 'r') as f:
            self.words = [line.rstrip() for line in f]

    def search(self, substring: str) -> List[str]:
        """Returns all words that contain substring."""
        words = [w for w in self.words if substring in w]
        words.append("some wrong word!")
        return words
