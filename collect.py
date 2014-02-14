#import logging
#import os

from backdrop.collector import arguments
#from backdrop.collector.logging_setup import set_up_logging

from collector.trending import compute

if __name__ == '__main__':
    #logfile_path = os.path.join(
    #    os.path.dirname(os.path.realpath(__file__)), 'log')
    #set_up_logging('ga_trending_collector', logging.DEBUG, logfile_path)

    args = arguments.parse_args('Google Analytics Trending')

    compute(vars(args))
