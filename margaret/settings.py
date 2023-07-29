import os


__version__ = '0.0.0'

TOKEN = os.environ.get('TOKEN')

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
