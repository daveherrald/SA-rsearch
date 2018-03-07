#!/usr/bin/env python

from splunklib.searchcommands import dispatch, ReportingCommand, Configuration, Option, validators
import splunklib.results as results
import splunklib.client as client
from splunk.appserver.mrsparkle.lib.util import make_splunkhome_path
import logging
import ConfigParser
import sys
import json
import time
import keyring
import os
from rsearch_utils import utils

def setup_logger(level, filename):
    '''
    Setup a logger for the custom search command.
    '''
    logger = logging.getLogger('splunk.appserver.customsearch.rsearch.' + filename)
    logger.propagate = False
    logger.setLevel(level)

    file_handler = logging.handlers.RotatingFileHandler(make_splunkhome_path(['var', 'log', 'splunk', filename]), maxBytes=25000000, backupCount=5)

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger

'''
Configure logging.
'''
logger_admin = setup_logger(logging.INFO, 'rsearch.log')

@Configuration()
class rinputlookupCommand(ReportingCommand):
    @Configuration()
    def map(self, records):
        return records

    def reduce(self, records):
        '''
        Determine the Splunk user, session key, and app
        '''
        user = self._metadata.searchinfo.username
        session_key = self._metadata.searchinfo.session_key
        app = self._metadata.searchinfo.app

        '''
        Read the username, password, and connection details for a more privileged Splunk account from a config file. 
        This more privileged account will be used to connect to Splunk and retrieve data not available to the user 
        who originally ran the custom search command.

        WARNING: The credentials for the more privileged account are stored in plain text on the file system of 
        the Splunk search head where this app is installed.
        '''
        CONF_FILE = make_splunkhome_path(['etc', 'apps', 'SA-rsearch', 'bin', 'rsearch.config'])
        parsed_config = utils._parse_config(CONF_FILE)
        PASSWORD = utils._get_password(parsed_config.get('SERVICE'), parsed_config.get('USER'))
        resultstoreturn = []

        try:
            searchquery = """
            | inputlookup employeeinfo.csv | search user={}
            """.format(user)
            kwargs_oneshot = {'count': 0}
            service = client.connect(host=parsed_config.get('HOST'),
                                     port=parsed_config.get('PORT'),
                                     username=parsed_config.get('USER'),
                                     password=PASSWORD)
            searchresults = service.jobs.oneshot(searchquery, **kwargs_oneshot)
            reader = results.ResultsReader(searchresults)
            if reader:
                for item in reader:
                    resultstoreturn.append(item)
        except:
            logger_admin.exception('Error executing search.')

        return resultstoreturn

    
if __name__ == "__main__":
    dispatch(rinputlookupCommand, sys.argv, sys.stdin, sys.stdout, __name__)
