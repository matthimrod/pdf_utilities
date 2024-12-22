"""
Matt's Really Cool PDF Utility
"""

import argparse
import sys

from . import main


def run(argv: list[str]) -> None:
    """
    Run Function
    :param argv: Command line arguments
    :type argv: list[str]
    """
    arg_parser = argparse.ArgumentParser(description="A simple Python PDF utility that probably "
                                                     "already exists.")

    arg_subparsers = arg_parser.add_subparsers(title="Commands", dest="command")
    arg_subparsers.required = True

    merge_subparser = arg_subparsers.add_parser("merge",
                                                help="Merge two or more PDFs.")
    merge_subparser.add_argument('-i', '--input',
                                 help='Input file(s).',
                                 nargs='+',
                                 default=[])
    merge_subparser.add_argument('-o', '--output',
                                 help='Output PDF file name. Default: output.pdf',
                                 default='output.pdf')

    extract_subparser = arg_subparsers.add_parser("extract",
                                                  help="Extract one or more pages from a PDF.")
    extract_subparser.add_argument('-o', '--output',
                                   help='Output PDF file name. Default: output.pdf',
                                   default='output.pdf')
    extract_subparser.add_argument('-i', '--input',
                                   help='Input file.')
    extract_subparser.add_argument('-p', '--pages',
                                   help='Page(s) to rotate.',
                                   nargs='+',
                                   default=[])

    rotate_subparser = arg_subparsers.add_parser("rotate",
                                                 help="Rotate one or more pages in a PDF.")
    rotate_subparser.add_argument('-o', '--output',
                                  help='Output PDF file name. Default: output.pdf',
                                  default='output.pdf')
    rotate_subparser.add_argument('-i', '--input',
                                  help='Input file.')
    rotate_subparser.add_argument('-p', '--pages',
                                  help='Page(s) to rotate.',
                                  nargs='+',
                                  default=[])

    delete_subparser = arg_subparsers.add_parser("delete",
                                                 help="Delete one or more pages from a PDF.")
    delete_subparser.add_argument('-o', '--output',
                                  help='Output PDF file name. Default: output.pdf',
                                  default='output.pdf')
    delete_subparser.add_argument('-i', '--input',
                                  help='Input file.')
    delete_subparser.add_argument('-p', '--pages',
                                  help='Page(s) to delete.',
                                  nargs='+',
                                  default=[])

    main(arg_parser.parse_args(argv))


if __name__ == '__main__':
    run(sys.argv[1:])
