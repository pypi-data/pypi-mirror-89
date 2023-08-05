# -*- python -*-
"""
djfim.management.commands.fim
"""

from django.core.management.base import BaseCommand, CommandError


from djfim.base import Actuator


class Command(BaseCommand):
    help = ''

    def add_parser(self, parser):
        parser.add_argument(
            '--',
            vars='datafile',
            metavars='fixture.dat',
            help=''
        )

    def handle(self, *args, **opts):
        act = Actuator()
        
        with open(opts['datafile'], 'r') as datafile:
            act.loadFromFile(datafile)

        act.applyRelease()
