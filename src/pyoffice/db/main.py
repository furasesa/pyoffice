import sqlite3
import locale
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, merge_completers
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer

from rich import print
from rich.console import Console
from rich.table import Table
from rich.progress import track
from time import sleep
import os
import sys
from rich.columns import Columns
from rich.markdown import Markdown
from rich.syntax import Syntax

import logging
locale.setlocale(locale.LC_ALL, '')

from .config import sql_completer, style, basic_command
from .config import row_filter, col_filter
from .commands import cmd_parse


class Database:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.session = None
        self.console = Console()
        self.cursor = self.connection.cursor()

        self.table_list = []

        # read config
        # Completer


        logging.debug(f'end init')

    def get_cursor_raw(self, args):
        """
        @brief SELECT * FROM <table>
        @return cursor
        @extract using loop
        """
        try:
            a = self.cursor.execute(args)
            logging.debug(f'get_cursor_raw: {a}')
            return a
        except Exception as e:
            logging.error(repr(f'Error occurs: {e}'))

    def get_cursor_data(self, args) -> list:
        """
        @brief SELECT <col> from <table>. do not use *
        @Example:
        SELECT name from lt;
        @return list
        """
        try:
            a = self.cursor.execute(args)
            lst_a = list(map(lambda x: x[0], a))
            logging.debug(f'get_cursor_data: {lst_a}')
            return lst_a
        except Exception as e:
            logging.error(repr(f'Error occurs: {e}'))

    def get_cursor_description(self, args) -> list:
        """
        @brief: SELECT * from <table>;
        @return column list
        """
        try:
            a = self.cursor.execute(args)
            des_lst = list(map(lambda x: x[0], a.description))
            logging.debug(f'get_cursor_description: {des_lst}')
            return des_lst
        except Exception as e:
            logging.error(repr(f'Error occurs: {e}'))

    def print_table(self):
        tbl = Table(show_header=True, header_style="bold magenta")
        tbl.add_column('Tables')
        tbl.add_column('Description')
        print('[bold]get table list[/bold]')
        self.table_list = self.get_cursor_data('SELECT name FROM sqlite_master WHERE type=\'table\'')
        for table in self.table_list:
            table_des = self.get_cursor_description(f'SELECT * FROM {table}')
            tbl.add_row(table, str(table_des))

        self.console.print(tbl)
        return self.table_list

    def cli(self):
        self.session = PromptSession(
            lexer=PygmentsLexer(SqlLexer), completer=sql_completer, style=style)
        print('[bold red]Control-D to quit[/bold red]')
        print('[bold red]Control-C to retry[/bold red]')

        while True:
            try:
                text = self.session.prompt('pyoffice> ')
                logging.debug(f'execute: {text}')
            except KeyboardInterrupt:
                continue  # Control-C pressed. Try again.
            except EOFError:
                break  # Control-D pressed.

            with self.connection:
                try:
                    messages = self.connection.execute(text)
                except Exception as e:
                    print(repr(e))
                else:
                    for message in messages:
                        print(message)

        print('[bold red]GoodBye![/bold red]')

    def search(self, config):
        self.print_table()
        database_completer = []
        if 'Completer' in config:
            col = config['Completer']['col'].split(',')
            tbl = config['Completer']['tbl'].split(',')
            gen_data = (self.get_cursor_data(f'SELECT {c} FROM {t}') for c in col for t in tbl)
            for x in gen_data:
                database_completer += x
            logging.debug(f'Completer from config: {database_completer}')

        table_list = WordCompleter(self.table_list, ignore_case=True)
        in_db_data = WordCompleter(database_completer, ignore_case=True)
        search_completer = merge_completers([basic_command, table_list, in_db_data])
        self.session = PromptSession(
            lexer=PygmentsLexer(SqlLexer), completer=search_completer, style=style)
        while True:
            try:
                tbl = Table(show_header=True, header_style="bold magenta")
                cmd = self.session.prompt('search> ')
                cmd_array = cmd.split(' ')
                if cmd_array[0] == 'help':
                    print('[bold red]Control-D to quit[/bold red]')
                    print('[bold red]Control-C to retry[/bold red]')
                    print('[bold]command: <table> <col> <keyword>')
                    continue
                elif cmd_array[0] == 'list':
                    self.print_table()
                    continue
                else:
                    s_table = cmd_array[0]
                    s_key = cmd_array[1]
                    s_string = cmd_array[2]
                    if s_table not in self.table_list:
                        logging.error(f'{s_table} not in {self.table_list}')
                # logging.debug(f'execute: {cmd}')
            except KeyboardInterrupt:
                continue  # Control-C pressed. Try again.
            except EOFError:
                break  # Control-D pressed.

            col_list = self.get_cursor_description(f'SELECT * FROM {s_table}')
            search_result = self.get_cursor_raw(f'SELECT * '
                                                f'FROM {s_table} '
                                                f'WHERE {s_key} '
                                                f'LIKE \'%{s_string}%\'')

            col_filter(tbl, col_list)
            row_filter(tbl, search_result)

            self.console.print(tbl)
        print('[bold red]GoodBye![/bold red]')

    def query(self, query_dictionary):
        # building WordCompleter
        query_list = query_dictionary.keys()  # look in config['Query']['list']
        where_key = []
        equation = []
        print(f'dict keys: {query_dictionary.keys()}')
        for k, v in query_dictionary.items():
            print(f'k: {k}, v: {v}')
            if 'filter' in v:
                print(f"filter found: {v['filter']}")
                where_key += v['filter']
                for vv in v['filter']:
                    val = vv.split('.')
                    equation += self.get_cursor_data(f"SELECT {val[1]} FROM {val[0]};")

        logging.debug(f'query list: {query_list}')
        logging.debug(f'where: {where_key}')
        logging.debug(f'equal: {equation}')

        query_cmd = WordCompleter(query_list)
        where_cmd = WordCompleter(where_key)
        equation_cmd = WordCompleter(equation)

        query_completer = merge_completers([basic_command, query_cmd, where_cmd, equation_cmd])
        self.session = PromptSession(
            lexer=PygmentsLexer(SqlLexer), completer=query_completer, style=style)
        while True:
            try:
                tbl = Table(show_header=True, header_style="bold magenta")
                cmd = [x for x in self.session.prompt('query> ').split()]
                # build command dictionary
                cmd_valid = {
                    'query': query_list,
                    'filter': where_key,
                    'filter_name': equation
                }
                valid_cmd = cmd_parse('query', cmd, cmd_valid)
                if valid_cmd == 1:
                    continue
                try:
                    search_str = f"{query_dictionary[valid_cmd['query']]['query']} " \
                                 f"WHERE {valid_cmd['filter']} = \'{valid_cmd['filter_name']}\';"
                    logging.debug(f"using filter: {valid_cmd['filter']} filter name: {valid_cmd['filter_name']}")
                except KeyError:
                    try:
                        search_str = f"{query_dictionary[valid_cmd['query']]['query']};"
                    except KeyError:
                        raise ValueError(f'Query {query_list} please use one of them')

                logging.debug(f'search string: {search_str}')
                query_result = self.get_cursor_raw(search_str) if search_str is not None \
                    else ValueError('Query String is None')

            except KeyboardInterrupt:
                continue  # Control-C pressed. Try again.
            except EOFError:
                break  # Control-D pressed.

            query_used = valid_cmd['query']
            column = query_dictionary[query_used]['column']
            logging.debug(f'column list: {column}')

            col_filter(tbl, column)
            row_filter(tbl, query_result)
            self.console.print(tbl)
        print('[bold red]GoodBye![/bold red]')



