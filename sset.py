from typing import List


class Node:
    def __init__(self, suffix: str, suffix_id: int = -1) -> None:
        self.suffix = suffix
        self.children = []
        self.suffix_id = suffix_id

    def insert(self, suffix: str, suffix_id: int) -> None:
        if suffix == "$":
            self.children.append(Node(suffix=suffix, suffix_id=suffix_id))
            return None

        for child in self.children:
            s = child.suffix

            if s == "$" or suffix[0] != s[0]:
                continue

            for i in range(1, min(len(suffix), len(s))):
                if suffix[i] != s[i] or s[i] == "$":
                    node = Node(s[i:], child.suffix_id)
                    node.children = child.children
                    child.suffix = s[:i]
                    child.children = [node, Node(suffix[i:], suffix_id)]
                    child.suffix_id = -1
                    return None

            child.insert(suffix[len(s):], suffix_id)
            return None

        self.children.append(Node(suffix, suffix_id))
        return None


def get_suffix_ids(node):
    if node.suffix_id != -1:
        return {node.suffix_id}

    res = set()
    for child in node.children:
        res.update(get_suffix_ids(child))

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
                    return [self.words[j] for j in get_suffix_ids(root)]
            else:
                return []
