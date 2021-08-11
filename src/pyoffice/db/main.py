import sqlite3
import locale
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, merge_completers
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer
from .config import sql_completer, style, basic_command
from .config import row_filter


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


class Database:
    def __init__(self, database, config):
        self.connection = sqlite3.connect(database)
        self.session = None
        self.console = Console()
        self.cursor = self.connection.cursor()
        self.database_completer = []

        # fixed table
        self.tbl_table = Table(show_header=True, header_style="bold magenta")
        self.tbl_table.add_column('Tables')
        self.tbl_table.add_column('Description')
        print('[bold]get table list[/bold]')

        with self.connection:
            self.table_list = self.get_cursor_data('SELECT name FROM sqlite_master WHERE type=\'table\'')
            for tbl in self.table_list:
                table_des = self.get_cursor_description(f'SELECT * FROM {tbl}')
                # for printing
                self.tbl_table.add_row(tbl, str(table_des))
            self.print_table()
            # read config
            # Completer
            if 'Completer' in config:
                col = config['Completer']['col'].split(',')
                tbl = config['Completer']['tbl'].split(',')
                gen_data = (self.get_cursor_data(f'SELECT {c} FROM {t}') for c in col for t in tbl)
                for x in gen_data:
                    self.database_completer += x
                logging.debug(f'Completer from config: {self.database_completer}')
        logging.debug(f'end init')

    def print_table(self):
        self.console.print(self.tbl_table)

    def get_cursor_raw(self, args):
        try:
            a = self.cursor.execute(args)
            logging.debug(f'get_cursor_raw: {a}')
            return a
        except Exception as e:
            logging.error(repr(f'Error occurs: {e}'))

    def get_cursor_data(self, args) -> list:
        try:
            a = self.cursor.execute(args)
            lst_a = list(map(lambda x: x[0], a))
            logging.debug(f'get_cursor_data: {lst_a}')
            return lst_a
        except Exception as e:
            logging.error(repr(f'Error occurs: {e}'))

    def get_cursor_description(self, args) -> list:
        try:
            a = self.cursor.execute(args)
            des_lst = list(map(lambda x: x[0], a.description))
            logging.debug(f'get_cursor_description: {des_lst}')
            return des_lst
        except Exception as e:
            logging.error(repr(f'Error occurs: {e}'))

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

    def search(self):
        table_list = WordCompleter(self.table_list, ignore_case=True)
        in_db_data = WordCompleter(self.database_completer, ignore_case=True)
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
                    logging.info('print table list')
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

            search_des = self.get_cursor_description(f'SELECT * FROM {s_table}')
            for des in search_des:
                tbl.add_column(des)

            search_result = self.get_cursor_raw(f'SELECT * '
                                                f'FROM {s_table} '
                                                f'WHERE {s_key} '
                                                f'LIKE \'%{s_string}%\'')

            for result in search_result:
                logging.debug(f'search result: {result}')
                # because of locale
                row_container = ()
                for x in result:
                    if type(x) == int:
                        row_container = (*row_container, f'{x:n}')
                    else:
                        row_container = (*row_container, f'{x}')
                # logging.debug(f'add {row_container}')
                # row_container = (str(x) for x in result)  # force elements to string
                tbl.add_row(*row_container)
            self.console.print(tbl)
        print('[bold red]GoodBye![/bold red]')

    def query(self, query_dictionary, column, q_filter):
        query_list = query_dictionary.keys()
        query_cmd = WordCompleter(query_dictionary.keys())
        filter_list = []
        if q_filter is not None:
            for f in q_filter:
                sel = f.split('.')
                filter_list += self.get_cursor_data(f'SELECT {sel[1]} FROM {sel[0]};')

        filter_cmd = WordCompleter(filter_list)
        logging.debug(f'query list: {query_list}')
        filter_tbl = WordCompleter(q_filter)
        query_completer = merge_completers([basic_command, query_cmd, filter_tbl, filter_cmd])
        self.session = PromptSession(
            lexer=PygmentsLexer(SqlLexer), completer=query_completer, style=style)
        while True:
            try:
                tbl = Table(show_header=True, header_style="bold magenta")
                cmd = self.session.prompt('query> ')
                cmd_array = cmd.split(' ')
                if cmd_array[0] == 'help':
                    print('[bold red]Control-D to quit[/bold red]')
                    print('[bold red]Control-C to retry[/bold red]')
                    print(f'[bold]query list: {query_list} project.id {filter_list}')
                    continue
                elif cmd_array[0] == 'list':
                    logging.info('print table list')
                    self.print_table()
                    continue
                else:
                    s_query = cmd_array[0]
                    s_filter = None
                    s_str = None
                    if len(cmd_array) > 1:
                        s_filter = cmd_array[1]
                        s_str = cmd_array[2]
                    if s_query not in query_list:
                        logging.error(f'{s_query} not in {query_list}')
                # logging.debug(f'execute: {cmd}')
            except KeyboardInterrupt:
                continue  # Control-C pressed. Try again.
            except EOFError:
                break  # Control-D pressed.

            if s_filter is not None:
                search_str = f'{query_dictionary.get(s_query)} WHERE {s_filter} = \'{s_str}\';'
            else:
                search_str = query_dictionary.get(s_query)
            query_result = self.get_cursor_raw(search_str)
            if column is not None:
                for col in column:
                    if col == 'price' or col == 'amount':
                        tbl.add_column(col, justify='right')
                    else:
                        tbl.add_column(col)

            for result in query_result:
                logging.debug(f'query result: {result}')
                row_container = row_filter(result)
                tbl.add_row(*row_container)
            self.console.print(tbl)

        print('[bold red]GoodBye![/bold red]')



