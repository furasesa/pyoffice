import argparse
import logging
import re
import textwrap as _textwrap
from prompt_toolkit import prompt
import getpass

log = logging.getLogger(__name__)

class LineWrapRawTextHelpFormatter(argparse.RawTextHelpFormatter):
    def __add_whitespace(self, idx, iw_space, text):
        if idx == 0:
            return text
        return (" " * iw_space) + text

    def _split_lines(self, text, width):
        text_rows = text.splitlines()
        for idx, line in enumerate(text_rows):
            search = re.search('\s*[0-9\-]{0,}\.?\s*', line)
            if line.strip() == "":
                text_rows[idx] = " "
            elif search:
                lw_space = search.end()
                lines = [self.__add_whitespace(i, lw_space, x) for i, x in enumerate(_textwrap.wrap(line, width))]
                text_rows[idx] = lines

        return [item for sublist in text_rows for item in sublist]

def parse_option():
    parser = argparse.ArgumentParser(
        formatter_class=LineWrapRawTextHelpFormatter, )
    # global options
    setting_args = parser.add_argument_group('global options')
    # Add the arguments
    setting_args.add_argument('-d',
                              dest='directory',
                              action='store',
                              help='set database directory',
                              )
    setting_args.add_argument('-u',
                              dest='user',
                              action='store',
                              help='set user login',
                              default=getpass.getuser()
                              )
    setting_args.add_argument('-p',
                              dest='passwd',
                              action='store',
                              help='set user password',
                              )

    return parser.parse_args()

setting_args = {}
options = parse_option()

def validation(group_args, key):
    v = vars(options).get(key)
    if v is not None:
        log.info('%s : %s ' % (key, v))
        group_args.update({key: v})
    return


def get_setting_args():
    validation(setting_args, 'directory')
    validation(setting_args, 'user')
    validation(setting_args, 'passwd')
    return setting_args





