import logging
from rich import print


def cmd_parse(cmd_type, cmd_list, dict_cmd: dict):
    args_valid = {}
    if cmd_type == 'query':
        if cmd_list[0] == 'help':
            print('[bold red]Control-D to quit[/bold red]')
            print('[bold red]Control-C to retry[/bold red]')
            print(f'command: {dict_cmd}')
            return 1
        if cmd_list[0] == 'list':
            print(f"main query: {dict_cmd['query']}")
            return 1
        else:
            for k, v in dict_cmd.items():
                if k == 'query':
                    args_valid.update({'query': z for z in v if z in cmd_list})
                elif k == 'filter':
                    args_valid.update({'filter': z for z in v if z in cmd_list})
                elif k == 'filter_name':
                    args_valid.update({'filter_name': z for z in v if z in cmd_list})
            logging.debug(f'args_valid: {args_valid}')
            return args_valid








