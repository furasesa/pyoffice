import sqlite3
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, merge_completers
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import SqlLexer
from .config import sql_completer, style

from typing import Union, List

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


class Database:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.session = PromptSession(
            lexer=PygmentsLexer(SqlLexer), completer=sql_completer, style=style)
        self.console = Console()
        self.cursor = self.connection.cursor()

        # fixed table
        self.tbl_table = Table(show_header=True, header_style="bold magenta")
        self.tbl_table.add_column('Tables')
        self.tbl_table.add_column('Description')
        print('[bold]get table list[/bold]')
        # print available tables
        cur = self.cursor.execute('SELECT name FROM sqlite_master WHERE type=\'table\'')
        table_list = list(map(lambda x: x[0], cur))
        # logging.debug(f'list table: {table_list}')
        self.table_list = table_list
        for tbl in self.table_list:
            cur = self.cursor.execute(f'SELECT * FROM {tbl}')
            description = list(map(lambda x: x[0], cur.description))
            logging.debug(f'table: {tbl} {description}')
            self.tbl_table.add_row(tbl, str(description))  # for printing

        # init
        self.print_table()

    def print_table(self):
        self.console.print(self.tbl_table)

    def cli(self):
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
        basic_cmd = WordCompleter(['help', 'list'])
        table_list = WordCompleter(self.table_list)
        search_completer = merge_completers([basic_cmd, table_list])
        self.session = PromptSession(
            lexer=PygmentsLexer(SqlLexer), completer=search_completer, style=style)
        while True:
            try:
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

            with self.connection:
                try:
                    tbl = Table(show_header=True, header_style="bold magenta")
                    search_str = f'SELECT * FROM {s_table} WHERE {s_key} LIKE \'%{s_string}%\''
                    logging.debug(search_str)
                    commands = self.connection.execute(search_str)
                    cur = self.cursor.execute(f'SELECT * FROM {s_table}')
                    description = list(map(lambda x: x[0], cur.description))
                    for des in description:
                        tbl.add_column(des)

                except Exception as e:
                    print(repr(e))
                else:
                    for result in commands:
                        logging.debug(f'search result: {result}')
                        row_container = (str(x) for x in result)  # force elements to string
                        tbl.add_row(*row_container)
                    self.console.print(tbl)

        print('[bold red]GoodBye![/bold red]')


        # for table_name in table_list:
        #     print(f'search looking in {table_name}')
        #     search_str = f'SELECT * FROM {table_name} WHERE name LIKE {keywords}'
        #     print(f'search string: {search_str}')
        #     c_t = cursor.execute(search_str)
        #     # print(f'search result: {c_t}')
        #     for res in c_t:
        #         print(f'result: {res}')




