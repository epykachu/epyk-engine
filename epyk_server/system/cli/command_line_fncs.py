"""
"""
import sys
import argparse
import pkg_resources
import shutil
import os



def main():
  """"""
  parser_map = {}
  arg_parser = argparse.ArgumentParser(prog='epyk-engine')
  subparser = arg_parser.add_subparsers(title='Commands', dest='command')
  subparser.required = True
  for func, parser_init in parser_map.items():
    new_parser = subparser.add_parser(func, help=parser_init[1])
    parser_init[0](new_parser)
  args = arg_parser.parse_args(sys.argv[1:])
  return args.func(args)



if __name__ == '__main__':
  main()
