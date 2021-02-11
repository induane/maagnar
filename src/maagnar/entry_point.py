# Standard
import argparse
import errno
import logging
import os
import pkg_resources
from pkg_resources import get_distribution
import sys
from logging.config import dictConfig

# Third Party
from log_color import ColorFormatter, ColorStripper

# Project
from maagnar import lib

LOG = logging.getLogger(__name__)

# Setup the version string globally
try:
    pkg_version = f'%(prog)s {get_distribution("maagnar").version}'
except pkg_resources.DistributionNotFound:
    pkg_version = "%(prog)s Development"
except Exception:
    pkg_version = "%(prog)s Unknown"


def cli():
    parser = argparse.ArgumentParser(description="Anagram generator")
    parser.add_argument("SEED", nargs=1)
    parser.add_argument(
        "-l",
        "--log-level",
        default="INFO",
        choices=("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
        help="Logging level for Montana Scripts.",
    )
    parser.add_argument(
        "-L",
        "--logfile",
        dest="logfile",
        default=None,
        help="Location to place a log of the process output",
    )
    parsed_args = parser.parse_args()

    # Get logging related arguments & the configure logging
    if parsed_args.logfile:
        logfile = os.path.abspath(parsed_args.logfile)
    else:
        logfile = None

    # Don't bother with a file handler if we're not logging to a file
    handlers = (
        ["console", "filehandler"]
        if logfile
        else [
            "console",
        ]
    )

    # The base logging configuration
    BASE_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "ConsoleFormatter": {
                "()": ColorFormatter,
                "format": "%(levelname)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "FileFormatter": {
                "()": ColorStripper,
                "format": ("%(levelname)-8s: %(asctime)s '%(message)s' %(name)s:%(lineno)s"),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "ConsoleFormatter",
            },
        },
        "loggers": {
            "maagnar": {
                "handlers": handlers,
                "level": parsed_args.log_level,
            },
        },
    }

    # If we have a log file, modify the dict to add in the filehandler conf
    if logfile:
        BASE_CONFIG["handlers"]["filehandler"] = {
            "level": parsed_args.log_level,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": logfile,
            "formatter": "FileFormatter",
        }

    # Setup the loggers
    dictConfig(BASE_CONFIG)
    LOG.info("Generating anagrams from #c<%s>", parsed_args.SEED[0])
    total = lib.calculate_total_permutations(parsed_args.SEED[0])
    padding = len(str(total))  # Used for progress indicator
    LOG.info("Possible combinations: #c<%s>", total)
    for idx, val in enumerate(lib.permutations(parsed_args.SEED[0]), start=1):
        LOG.info("[#m<%s/%s>] Found: #g<'%s>'", str(idx).zfill(padding), total, val)

    LOG.debug("#g<\u2713> Process complete!")


def main():
    try:
        cli()
    except KeyboardInterrupt:
        # Write a nice message to stderr
        sys.stderr.write("\n\033[91m\u2717 Operation canceled by user.\033[0m\n")
        sys.exit(errno.EINTR)


if __name__ == "__main__":
    main()
