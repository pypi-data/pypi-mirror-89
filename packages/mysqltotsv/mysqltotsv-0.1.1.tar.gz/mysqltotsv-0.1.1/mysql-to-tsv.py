#!/usr/bin/python3
import argparse
import os.path
import re
from mysqltotsv import Splitter, ExtractSchema, row_strip_quotes

def valid_file(inputfile):
    if not os.path.isfile(inputfile):
        raise argparse.ArgumentTypeError('mysql dump file does not exist')
    return inputfile

def valid_dir(outputdir):
    if not os.path.isdir(outputdir):
        raise argparse.ArgumentTypeError('output directory does not exist')
    return outputdir

arg_parser = argparse.ArgumentParser(description='Tool for conversion of large MySQL dumps to TSV format')
arg_parser.add_argument('--file', dest='file', action='store', required=True, type=valid_file, help='mysql dump file')
arg_parser.add_argument('--outdir', dest='outdir', action='store', required=True, type=valid_dir, help='output directory')
arg_parser.add_argument('--table-filter', dest='table_filter', action='store', required=False, type=str, help='filtered tables')
arg_parser.add_argument('--only-schema', dest='only_schema', action='store_true', help='write the schema to the output directory')
arg_parser.add_argument('--strip-quotes', dest='strip_quotes', action='store_true', help='strip quotes from values')

args   = arg_parser.parse_args()

if args.only_schema:
    extract = ExtractSchema(args)
    extract.doit()
else:
    splitter = Splitter(args)
    rows_written = 0
    seen_outfile = set()
    for batch in splitter.next_batch():
        outfile = os.path.join(args.outdir,batch["table_name"] + ".tsv")
        if os.path.exists(outfile) and outfile not in seen_outfile:
            os.remove(outfile)

        seen_outfile |= set([outfile])

        with open(outfile,"a") as fh_out:
            rows_written += len(batch["rows"])
            for r in batch["rows"]:
                if args.strip_quotes:
                    row_strip_quotes(r)
                fh_out.write("\t".join(map(str, r)) + "\n")
            print("rows written: ",rows_written)

