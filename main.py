from margaret.settings import BANNER, TOKEN, ENV_REF
from src.commands import client
from src.keep_alive import keep_alive


if __name__ == '__main__':
    print(BANNER)
    if ENV_REF == 'replit':
        keep_alive()
    client.run(TOKEN)
