#!/usr/bin/env python3


from dotenv import load_dotenv
from controller import BotController


def main():
    load_dotenv()
    bot_controller = BotController(None, None)


if __name__ == '__main__':
    main()
