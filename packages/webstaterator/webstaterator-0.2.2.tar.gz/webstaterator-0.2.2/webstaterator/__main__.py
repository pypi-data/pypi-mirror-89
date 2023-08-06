"""
Webstaterator

A Python tool for generating static websites based on object models

Documentation: TBA
Gitlab: https://gitlab.com/Jon.Keatley.Folio/webstaterator
PyPi: Some day!

Created by Jon Keatley (http://jon-keatley.com)
Named by Sasha Siegel. It is her fault!

Copyright Jon Keatley 2020

"""

import sys
import argparse

from webstaterator import Webstaterator

DESCRIPTION = """A Python tool for generating static websites based on object models"""


def get_parser_options():
    """ Generate CLI options """
    parser = argparse.ArgumentParser(
        prog='webstaterator',
        description=DESCRIPTION
    )

    arg_website_short = '-w'
    arg_website_long = '--website'
    arg_website_desc = 'Website decription file'

    arg_output_short = '-o'
    arg_output_long = '--output'
    arg_output_desc = 'Output path'

    action_parser = parser.add_subparsers(
        title='Actions',
        description='Webstaterator actions',
        dest='action'
    )
    action_validate = action_parser.add_parser(
        'validate',
        help='Validates the provided website description file'
    )
    action_validate.add_argument(
        arg_website_short,
        arg_website_long,
        help=arg_website_desc,
        required = True
    )

    action_build = action_parser.add_parser(
        'build',
        help="""Builds a website in the given folder based
on the provided website description file"""
        )
    action_build.add_argument(
        arg_website_short,
        arg_website_long,
        help=arg_website_desc,
        required = True,
    )
    action_build.add_argument(
        arg_output_short,
        arg_output_long,
        help=arg_output_desc,
        required = True,
    )

    action_template = action_parser.add_parser(
        'template',
        help='Generates a blank website description file'
    )

    action_template.add_argument(
        arg_output_short,
        arg_output_long,
        help=arg_output_desc,
        required = True,
    )

    return parser

def run(args):
    """ Execute webstaterators CLI """
    pargs = get_parser_options().parse_args(args)

    if pargs.action is None:
        get_parser_options().parse_args(["-h"])
        sys.exit(0)

    ws_obj = Webstaterator()

    if pargs.action == 'validate':
        ws_obj.validate(pargs.website)
    elif pargs.action == 'build':
        ws_obj.build(pargs.website, pargs.output)
    elif pargs.action == 'template':
        ws_obj.template(pargs.output)

def execute():
    """ wrapper method that calls run with sys.argv[1:] """
    run(sys.argv[1:])

if __name__ == '__main__':
    execute()
