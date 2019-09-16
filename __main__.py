# -*- coding: utf-8 -*
import sys
import logging
from logging.handlers import RotatingFileHandler
import optparse

from controllers.main import QtMainController


def main(argv=None):
    if argv is None:
        argv = sys.argv

    usage = "usage: %prog [options] [workflow_file]"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-l", "--log-level", help="Logging level (0, 1, 2, 3, 4)", type="int", default=1)

    (options, args) = parser.parse_args(argv[1:])

    levels = [logging.CRITICAL, logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]

    # File handler should always be at least INFO level so we need the application root level to be at least at INFO.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s/%(funcName)s - %(message)s')
    root_level = min(levels[options.log_level], logging.INFO)
    logger = logging.getLogger("PlottingApp")
    logger.setLevel(root_level)
    log_handler = RotatingFileHandler('PlottingApp.log', maxBytes=500000, backupCount=2)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.info(f"logging level: {root_level}")

    mc = QtMainController(sys.argv)
    mc()


if __name__ == "__main__":
    sys.exit(main())
