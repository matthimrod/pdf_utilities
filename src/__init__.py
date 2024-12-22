"""
Matt's PDF Library of Functions That Probably Already Exist Elsewhere
"""

import re
from argparse import Namespace

from pypdf import PdfReader, PdfWriter


def main(args: Namespace) -> None:
    """
    Main Function; Calls the appropriate command function
    :param args: Argparse Results
    :type args: Namespace
    """
    if args.command == "merge":
        pdf_merge(args)
    elif args.command == "extract":
        pdf_extract(args)
    elif args.command == "rotate":
        pdf_rotate(args)
    elif args.command == "delete":
        pdf_delete(args)


def parse_ranges(page_string: str) -> list | int:
    """
    Parses page ranges
    :param page_string: The page rage as a string ##-##
    :type page_string: str
    :return: A list of pages or an int for a single page
    :rtype: list | int
    """
    result = re.search(r'(\d+)-(\d+)', page_string)
    if result:
        a = result.group(1)
        b = result.group(2)
        return list(range(int(a) - 1, int(b)))
    return int(page_string) - 1


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


def pdf_merge(args: Namespace) -> None:
    """
    Merge two or more PDFs
    :param args: Argparse Results
    :type args: Namespace
    """
    merger = PdfWriter()
    for filename in args.input:
        print(f'Reading {filename}')
        merger.append(PdfReader(filename))

    print(f'Writing {args.output}')
    merger.write(args.output)


def pdf_extract(args: Namespace) -> None:
    """
    Extract one or more pages from a PDF
    :param args: Argparse Results
    :type args: Namespace
    """
    pages_to_extract = flatten(list(map(parse_ranges, args.pages)))
    reader = PdfReader(args.input)
    writer = PdfWriter()

    for page_num, page in enumerate(reader.pages):
        if page_num in pages_to_extract:
            writer.add_page(page)

    writer.write(args.output)


def pdf_rotate(args: Namespace) -> None:
    """
    Rotate one or more pages in a PDF
    :param args: Argparse Results
    :type args: Namespace
    """
    pages_to_rotate = flatten(list(map(parse_ranges, args.pages)))
    pdf = PdfWriter(args.input)

    for page_num in pages_to_rotate:
        pdf.pages[page_num].rotate(90)

    pdf.write(args.output)


def pdf_delete(args: Namespace) -> None:
    """
    Delete one or more pages from a PDF
    :param args: Argparse Results
    :type args: Namespace
    """
    pages_to_delete = flatten(list(map(parse_ranges, args.pages)))
    pdf = PdfWriter(args.input)

    for page_num in pages_to_delete:
        pdf.remove_page(page_num)

    pdf.write(args.output)
