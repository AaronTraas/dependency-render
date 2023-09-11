from argparse import ArgumentParser

from ._version import __version__
from .dep_render import render_output
from .dep_render import Config

logger = logging.getLogger(__name__)

def parse_args(argv):
    '''
    parse command-line args.
    '''
    parser = ArgumentParser(description='Dependency graph generator')
    parser.add_argument('input_csv',
        help='The CSV to parse')
    parser.add_argument('--output-type', choices=['pdf','png','svg'], default='pdf',
        help='Output file type for the graph to render.')
    args = parser.parse_args()

    return Config(args.input_csv, args.output_type)


def main(): # pragma: no cover
    render_output(parse_args(sys.argv[1:]))
