from __future__ import annotations
from typing import List, Dict
import json

from fibers.tree import Node


class Document:
    def __init__(self, title="", content="", sections=None):
        self.title = title
        self.content = content
        self.sections: List[Document] = sections if sections is not None else []

    def iter_sections(self, root_path="") -> (Document, str):
        # TODO this is not tested
        if len(self.content) > 0:
            yield self, root_path + "\\" + self.title
        for section in self.sections:
            yield from section.iter_sections(root_path=root_path + "\\" + self.title)

    @classmethod
    def from_dict(cls, d: Dict):
        return cls(d.get("title", ""), d.get("content", ""),
                   [cls.from_dict(sub) for sub in d.get("sections", [])])

    @classmethod
    def from_json(cls, file_path: str):
        with open(file_path, "r") as f:
            d = json.load(f)
        return cls.from_dict(d)
    
    def __repr__(self):
        return f"<{self.__class__.__name__}> {self.title!r}"

    def to_tree(self):
        root = Node()
        self._to_tree(root)
        return root

    def _to_tree(self, root: Node):
        root = root.s(self.title)
        root.content = self.content
        for section in self.sections:
            section._to_tree(root)

    def display(self):
        self.to_tree().display()