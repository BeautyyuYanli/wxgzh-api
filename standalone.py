import os
import argparse
from wxgzh_api.updater import Updater
from wxgzh_api.updater.exceptions import CookieException

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--cookiefile', type=str,
                           default=os.getenv('COOKIE_FILE'))
    argparser.add_argument('--target', type=str, nargs='+', default=[])
    args = argparser.parse_args()
    updater = Updater(cookiefile=args.cookiefile)
    result = updater.update(args.target)
    print(result)
