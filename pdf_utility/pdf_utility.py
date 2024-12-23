"""
Matt's Really Cool PDF Utility
"""

import argparse
import re
import sys

from pypdf import PdfReader, PdfWriter
from typing_extensions import TypedDict, Unpack


class PdfDeleteKwargs(TypedDict):
    """
    Keyword Arguments for pdf_delete()
    """

    input: str
    output: str
    pages: list[int]


class PdfExtractKwargs(TypedDict):
    """
    Keyword Arguments for pdf_extract()
    """

    input: str
    output: str
    pages: list[int]


class PdfMergeKwargs(TypedDict):
    """
    Keyword Arguments for pdf_merge()
    """

    inputs: list[str]
    output: str


class PdfRotateKwargs(TypedDict):
    """
    Keyword Arguments for pdf_rotate()
    """

    input: str
    output: str
    pages: list[int]


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


def run(argv: list[str]) -> None:
    """
    Run Function
    :param argv: Command line arguments
    :type argv: list[str]
    """
    arg_parser = argparse.ArgumentParser(
        description="A simple Python PDF utility that probably " "already exists."
    )

    arg_subparsers = arg_parser.add_subparsers(title="Commands", dest="command")
    arg_subparsers.required = True

    merge_subparser = arg_subparsers.add_parser("merge", help="Merge two or more PDFs.")
    merge_subparser.add_argument(
        "-i", "--input", help="Input file(s).", nargs="+", default=[]
    )
    merge_subparser.add_argument(
        "-o",
        "--output",
        help="Output PDF file name. Default: output.pdf",
        default="output.pdf",
    )

    extract_subparser = arg_subparsers.add_parser(
        "extract", help="Extract one or more pages from a PDF."
    )
    extract_subparser.add_argument(
        "-o",
        "--output",
        help="Output PDF file name. Default: output.pdf",
        default="output.pdf",
    )
    extract_subparser.add_argument("-i", "--input", help="Input file.")
    extract_subparser.add_argument(
        "-p", "--pages", help="Page(s) to rotate.", nargs="+", default=[]
    )

    rotate_subparser = arg_subparsers.add_parser(
        "rotate", help="Rotate one or more pages in a PDF."
    )
    rotate_subparser.add_argument(
        "-o",
        "--output",
        help="Output PDF file name. Default: output.pdf",
        default="output.pdf",
    )
    rotate_subparser.add_argument("-i", "--input", help="Input file.")
    rotate_subparser.add_argument(
        "-p", "--pages", help="Page(s) to rotate.", nargs="+", default=[]
    )

    delete_subparser = arg_subparsers.add_parser(
        "delete", help="Delete one or more pages from a PDF."
    )
    delete_subparser.add_argument(
        "-o",
        "--output",
        help="Output PDF file name. Default: output.pdf",
        default="output.pdf",
    )
    delete_subparser.add_argument("-i", "--input", help="Input file.")
    delete_subparser.add_argument(
        "-p", "--pages", help="Page(s) to delete.", nargs="+", default=[]
    )

    args = arg_parser.parse_args(argv)

    if args.command == "merge":
        pdf_merge(inputs=args.input, output=args.output)
    elif args.command == "extract":
        pdf_extract(
            input=args.input,
            output=args.output,
            pages=flatten(list(map(parse_ranges, args.pages))),
        )
    elif args.command == "rotate":
        pdf_rotate(
            input=args.input,
            output=args.output,
            pages=flatten(list(map(parse_ranges, args.pages))),
        )
    elif args.command == "delete":
        pdf_delete(
            input=args.input,
            output=args.output,
            pages=flatten(list(map(parse_ranges, args.pages))),
        )


if __name__ == "__main__":
    run(sys.argv[1:])
