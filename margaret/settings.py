import os


__version__ = '0.0.0'


ENV_REF = os.environ.get('ENV_REF', 'development')
TOKEN = os.environ.get('TOKEN')
MYSQL_CONFIG = {
    'MYSQL_HOST': os.environ.get('MYSQL_HOST', 'localhost'),
    'MYSQL_USER': os.environ.get('MYSQL_USER', 'guest'),
    'MYSQL_PASSWORD': os.environ.get('MYSQL_PASSWORD', ''),
    'MYSQL_DATABASE': os.environ.get('MYSQL_DATABASE', ''),
    'MYSQL_ROOT_PASSWORD': os.environ.get('MYSQL_ROOT_PASSWORD', ''),
    'MYSQL_PORT': int(os.environ.get('MYSQL_PORT', 3306))
}

BANNER = f'''
========================
╔╦╗┌─┐┬─┐┌─┐┌─┐┬─┐┌─┐┌┬┐
║║║├─┤├┬┘│ ┬├─┤├┬┘├┤  │ 
╩ ╩┴ ┴┴└─└─┘┴ ┴┴└─└─┘ ┴ 
========================
Running Margaret version:
     {__version__}
________________________
'''


