#!/usr/bin/env python
import logging
import sys

import worker


def main():
    logging.basicConfig(level=logging.DEBUG)
    worker.run()


if __name__ == '__main__':
    try:
        main()
        exit_code = 0
    except Exception:
        logging.exception("uncaught error")
        exit_code = 1

    sys.exit(exit_code)
