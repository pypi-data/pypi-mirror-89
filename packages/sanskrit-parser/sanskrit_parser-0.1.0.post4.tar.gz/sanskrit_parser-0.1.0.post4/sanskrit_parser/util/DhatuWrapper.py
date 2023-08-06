#!/usr/bin/env python
"""
Wrapper around  kRShNamAchArya dhAtupATha to extract simple dhAtu attributes
@author: Karthikeyan Madathil (@kmadathil)
"""
from __future__ import print_function

import logging
import os

import requests
from tinydb import TinyDB, Query

from sanskrit_parser.base.sanskrit_base import SanskritImmutableString, SCHEMES


class DhatuWrapper(object):
    """
    Class to interface with the kRShNamAchArya dhAtupATha
    https://github.com/sanskrit-coders/stardict-sanskrit/tree/master/sa-vyAkaraNa/dhAtu-pATha-kRShNAchArya
    """
    # Moved to our own repo
    git_url = 'https://raw.githubusercontent.com/kmadathil/sanskrit_parser/master/data/dhAtu-pATha-kRShNAchArya.json'
    base_dir = os.path.expanduser("~/.sanskrit_parser/data")
    db_file = "dhAtu-pATha-kRShNAchArya.json"
    q = Query()

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self._get_file()
        self.db = TinyDB(os.path.join(self.base_dir, self.db_file))
        # Check if db is empty
        if len(self.db.all()) == 0:
            self._generate_db()

    def _get_file(self):
        """ Download file if not present in cache """
        if not os.path.exists(self.base_dir):
            self.logger.debug("Data cache not found. Creating.")
            os.makedirs(self.base_dir)
        if not os.path.exists(os.path.join(self.base_dir, self.db_file)):
            self.logger.debug("%s not found. Downloading it", self.db_file)
            r = requests.get(self.git_url, stream=True)
            assert r.status_code != 404, \
                "Could not download file {}".format(self.git_url)
            with open(os.path.join(self.base_dir, self.db_file), "wb") as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)

    def _get_dhatus(self, d):
        """ Get all tags for a dhatu d """
        if d is None:
            return None
        else:
            return self.db.search(self.q.DAtuH == d)

    def is_sakarmaka(self, d):
        """ Is d sakarmaka? """
        # Tags
        tl = self._get_dhatus(d)
        if len(tl) != 0:
            supported_karmakas = {'sakarmakaH', 'dvikarmakaH'}
            return any([t['karmakatvaM'] in supported_karmakas for t in tl])
        else:
            self.logger.debug("Couldn't find dhatu {} in database".format(d))
            return False


if __name__ == "__main__":
    from argparse import ArgumentParser

    def getArgs():
        """
          Argparse routine.
          Returns args variable
        """
        # Parser Setup
        parser = ArgumentParser(description='Dhatu Wrapper')
        # String to encode
        parser.add_argument('dhatu', nargs="?", type=str, default="kf")
        # Input Encoding (autodetect by default)
        parser.add_argument('--input-encoding', type=str, default=None)
        parser.add_argument('--tags', type=str,
                            choices=["all", u'DAtuH', u'mUlaDAtuH',
                                     u'DAtvarTaH', u'gaRaH', u'karmakatvaM',
                                     u'iwtvaM', u'padam-upagrahaH', u'rUpam'],
                            default=u'karmakatvaM')
        parser.add_argument('--debug', action='store_true')
        return parser.parse_args()

    def main():
        args = getArgs()
        print("Input Dhatu:", args.dhatu)
        if args.debug:
            logging.basicConfig(filename='DhatuWrapper.log', filemode='w', level=logging.DEBUG)
        else:
            logging.basicConfig(filename='DhatuWrapper.log', filemode='w', level=logging.INFO)
        logger = logging.getLogger(__name__)
        if args.input_encoding is None:
            ie = None
        else:
            ie = SCHEMES[args.input_encoding]
        i = SanskritImmutableString(args.dhatu, encoding=ie)
        it = i.canonical()
        print("Input String in SLP1:", it)
        logger.info("Input String in SLP1: {}".format(it))
        w = DhatuWrapper(logger=logger)
        if args.tags == "all":
            res = w._get_dhatus(it)
        else:
            res = map(lambda x: x[args.tags], w._get_dhatus(it))
        print(res)
        print("Is {} sakarmaka?: {}".format(it, w.is_sakarmaka(it)))
        logger.info("Reported {}".format(res))

    main()
