"""
Matt's PDF Library of Functions That Probably Already Exist Elsewhere
"""

import re

from pypdf import PdfReader, PdfWriter
from typing_extensions import Unpack

from types import PdfDeleteKwargs, PdfExtractKwargs, PdfMergeKwargs, PdfRotateKwargs


def parse_ranges(page_string: str) -> list:
    """
    Parses page ranges and returns the indices of the pages as they would
    be found in a zero-indexed array.
    :param page_string: The page rage as a string ##-##
    :type page_string: str
    :return: A list of pages
    :rtype: list
    """
    result = re.search(r"(\d+)-(\d+)", page_string)
    if result:
        a = result.group(1)
        b = result.group(2)
        return list(range(int(a) - 1, int(b)))
    return [int(page_string) - 1]


def flatten(input_list: list) -> list:
    """
    Flattens nested lists into a single list
    :param input_list: A list that may contain other lists
    :type input_list: list
    :return: The list, flattened
    :rtype: list
    """
    result = []
    for x in input_list:
        if isinstance(x, list):
            for y in x:
                result.append(y)
        else:
            result.append(x)
    return result


def pdf_merge(**kwargs: Unpack[PdfMergeKwargs]) -> None:
    """
    Merge two or more PDFs
    :keyword input: Input PDF name/path
    :keyword output: Output PDF name/path
    """
    with PdfWriter() as writer:
        for filename in kwargs["inputs"]:
            writer.append(PdfReader(filename))

        writer.write(kwargs["output"])


def pdf_extract(**kwargs: Unpack[PdfExtractKwargs]) -> None:
    """
    Extract one or more pages from a PDF
    :keyword input: Input PDF name/path
    :keyword output: Output PDF name/path
    :keyword pages: list of page numbers to extract
    """
    source_pdf = PdfReader(kwargs["input"])
    target_pdf = PdfWriter()

    for page_num, page in enumerate(source_pdf.pages):
        if page_num in kwargs["pages"]:
            target_pdf.add_page(page)

    target_pdf.write(kwargs["output"])


def pdf_rotate(**kwargs: Unpack[PdfRotateKwargs]) -> None:
    """
    Rotate one or more pages in a PDF
    :keyword input: Input PDF name/path
    :keyword output: Output PDF name/path
    :keyword pages: list of page numbers to rotate
    """
    pdf = PdfWriter(kwargs["input"])

    for page_num in kwargs["pages"]:
        pdf.pages[page_num].rotate(90)

    pdf.write(kwargs["output"])


def pdf_delete(**kwargs: Unpack[PdfDeleteKwargs]) -> None:
    """
    Delete one or more pages from a PDF
    :keyword input: Input PDF name/path
    :keyword output: Output PDF name/path
    :keyword pages: list of page numbers to delete
    """
    pdf = PdfWriter(kwargs["input"])

    for page_num in kwargs["pages"]:
        pdf.remove_page(page_num)

    pdf.write(kwargs["output"])
