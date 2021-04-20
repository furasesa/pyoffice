import logging
import secrets
import string

from prompt_toolkit.shortcuts.prompt import PromptSession, prompt
from .db.connector import OfficeData
from .options import get_setting_args

import sys
import platform

from pathlib import Path


# getpass.getpass(prompt='Password: ', stream=None)
# getpass.getuser()

log = logging.getLogger('main')
os_platform = platform.system()


def setting_validation(setting):
    # use session
    session = PromptSession()
    # init variables
    _user = setting.get('user')
    _passwd = setting.get('passwd')
    _directory = setting.get('directory')

    # validations
    _passwd = _passwd if _passwd is not None \
        else session.prompt('Enter Password:> ', is_password=True)
    
    _directory = Path.home()/'.config'/'pyoffice' \
        if os_platform == 'Linux' else Path('.')

    # fix FileNotFoundError
    _directory.mkdir(parents=True, exist_ok=True)

    return _user, _passwd, _directory

if __name__ == '__main__':
    log.info('platform: %s' %os_platform )
    settings = get_setting_args()
    user, passwd, directory = setting_validation(settings)
    log.debug('\nuser: %s\npass: %s\ndir: %s' %(user, passwd, directory))

    # database begin:
    data = OfficeData(directory, user, passwd)
    data.test_save_setting()


    
    # user_ch = input('Login as %s (y/n)?' %user)
    # bool_user = True if user_ch in ['y', 'Y', 'yes', 'Yes'] else False
    # user = user if bool_user else input('set username :>')

    # while len(user) < 3:
    #     log.error('username must not to be less than 3')
    #     user = input('set username :>')
        

    # log.info('user : %s' %user)

    sys.exit('trial done')
    

    data = OfficeData()
    # data.test()
    alphabet = string.ascii_letters + string.digits
    log.info('alphabet : %s' % alphabet )
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(8))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    
    log.info('password : %s' % password)
    



