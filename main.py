from margaret.settings import BANNER, TOKEN
from src.commands import client


if __name__ == '__main__':
    print(BANNER)
    client.run(TOKEN)
