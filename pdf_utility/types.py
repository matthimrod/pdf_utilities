"""
TypedDict classes for Matt's PDF Library
"""

from typing_extensions import TypedDict


class PdfDeleteKwargs(TypedDict):
    input: str
    output: str
    pages: list[int]


class PdfExtractKwargs(TypedDict):
    input: str
    output: str
    pages: list[int]


class PdfMergeKwargs(TypedDict):
    """ """

    inputs: list[str]
    output: str


class PdfRotateKwargs(TypedDict):
    input: str
    output: str
    pages: list[int]
