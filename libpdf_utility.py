import argparse
import re
import sys
import PyPDF2

argparser = argparse.ArgumentParser(description="A simple Python PDF utility that probably already exists.")

argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)

    if   args.command == "merge"     : cmd_merge(args)
    elif args.command == "extract"   : cmd_extract(args)
    elif args.command == "rotate"    : cmd_rotate(args)

def parse_ranges(pageString: str): 
    result = re.search(r'(\d+)-(\d+)', pageString)
    if result:
        a = result.group(1)
        b = result.group(2)
        return list(range(int(a) - 1, int(b)))
    else:
        return int(pageString) - 1

def flatten(input: list): 
    result = []
    for x in input:
        if type(x) is list:
            for y in x:
                result.append(y)
        else:
            result.append(x)
    return result

argsp = argsubparsers.add_parser("merge", help="Merge two or more PDFs.")
argsp.add_argument('-i', '--input', 
                   help='Input file(s).', 
                   nargs='+', 
                   default=[])
argsp.add_argument('-o', '--output', 
                   help='Output PDF file name. Default: output.pdf',
                   default='output.pdf')

def cmd_merge(args):
    merger = PyPDF2.PdfFileMerger()
    for filename in args.input:
        print(f'Reading {filename}')
        merger.append(PyPDF2.PdfFileReader(open(filename, 'rb')))

    print(f'Writing {args.output}')
    merger.write(args.output)

argsp = argsubparsers.add_parser("extract", help="Extract one or more pages from a PDF.")
argsp.add_argument('-o', '--output', 
                   help='Output PDF file name. Default: output.pdf',
                   default='output.pdf')
argsp.add_argument('-i', '--input', 
                   help='Input file.')
argsp.add_argument('-p', '--pages', 
                   help='Page(s) to rotate.', 
                   nargs='+', 
                   default=[])

def cmd_extract(args):
    pages_to_extract = flatten(list(map(lambda n: parse_ranges(n), args.pages)))
    reader = PyPDF2.PdfFileReader(args.input)
    writer = PyPDF2.PdfFileWriter()

    for pageNum in range(reader.numPages):
        if pageNum in pages_to_extract:
            page = reader.getPage(pageNum)
            writer.addPage(page)

    writer.write(args.output)

argsp = argsubparsers.add_parser("rotate", help="Rotate one or more pages in a PDF.")
argsp.add_argument('-o', '--output', 
                    help='Output PDF file name. Default: output.pdf',
                    default='output.pdf')
argsp.add_argument('-i', '--input', 
                    help='Input file.')
argsp.add_argument('-p', '--pages', 
                    help='Page(s) to rotate.', 
                    nargs='+', 
                    default=[])

def cmd_rotate(args):
    pages_to_rotate = flatten(list(map(lambda n: parse_ranges(n), args.pages)))
    reader = PyPDF2.PdfFileReader(args.input)
    writer = PyPDF2.PdfFileWriter()
    
    for pageNum in range(reader.numPages):
        page = reader.getPage(pageNum)
        if pageNum in pages_to_rotate:
            page.rotate(90)
        writer.addPage(page)

    writer.write(args.output)