from typing import List


class Node:
    def __init__(self, suffix: str, word_id: int = -1) -> None:
        self.suffix = suffix
        self.children = []
        self.word_id = word_id

    def insert(self, word: str, word_id: int) -> None:
        if word == "$":
            self.children.append(Node(suffix=word, word_id=word_id))
            return None

        for child in self.children:
            s = child.suffix

            if s == "$" or word[0] != s[0]:
                continue

            for i in range(1, min(len(word), len(s))):
                if word[i] != s[i] or s[i] == "$":
                    node = Node(s[i:], child.word_id)
                    node.children = child.children
                    child.suffix = s[:i]
                    child.children = [node, Node(word[i:], word_id)]
                    child.word_id = -1
                    return None

            child.insert(word[len(s):], word_id)
            return None

        self.children.append(Node(word, word_id))
        return None


def get_word_ids(node):
    if node.word_id != -1:
        return {node.word_id}

    res = set()
    for child in node.children:
        res.update(get_word_ids(child))

    return res


class SSet:
    def __init__(self, fname: str) -> None:
        self.fname = fname
        self.words = None
        self.root = None

    def load(self) -> None:
        with open(self.fname, 'r') as f:
            self.words = [line.rstrip() for line in f]
            self.root = Node("")
            for word_id in range(len(self.words)):
                word = self.words[word_id] + "$"
                for i in range(len(word) - 1, -1, -1):
                    self.root.insert(word[i:], word_id)

    def search(self, substring: str) -> List[str]:
        root = self.root
        while True:
            for i in range(len(root .children)):
                s = root.children[i].suffix

                if substring.startswith(s):
                    substring = substring[len(s):]
                    root = root.children[i]
                    break

                if s.startswith(substring):
                    return [self.words[j] for j in get_word_ids(root)]
            else:
                return []
