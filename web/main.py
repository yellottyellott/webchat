#!/usr/bin/env python
import logging
import sys

import dashboard.app


def main():
    logging.basicConfig(level=logging.DEBUG)
    dashboard.app.run(8001)


if __name__ == '__main__':
    try:
        main()
        exit_code = 0
    except Exception:
        logging.exception("uncaught error")
        exit_code = 1

    sys.exit(exit_code)
