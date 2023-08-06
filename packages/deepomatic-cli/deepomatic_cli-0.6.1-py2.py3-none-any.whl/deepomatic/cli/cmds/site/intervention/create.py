from ...utils import Command, BuildDict
from ..utils import SiteManager


class CreateCommand(Command):
    """
        Create a new intervention
    """

    def setup(self, subparsers):
        parser = super(CreateCommand, self).setup(subparsers)
        parser.add_argument('-u', "--api_url", required=True, type=str, help="url of your Customer api")
        parser.add_argument('-n', '--name', required=True, type=str, help="Intervention name")
        parser.add_argument('-m', "--metadata", dest='metadata',
                            action=BuildDict, nargs="+", metavar="NAME:VAL", required=True,
                            help='Metadata for the intervention in format name:value')
        return parser

    def run(self, api_url, name, metadata, **kwargs):
        return SiteManager().create_intervention(api_url, name, metadata)
