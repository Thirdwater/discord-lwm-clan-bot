#!/usr/bin/env python3


from dotenv import load_dotenv
from model import Model
from view import View
from controller import Controller


def main():
    load_dotenv()
    model = Model()
    view = View()
    controller = Controller(model, view)


if __name__ == '__main__':
    main()
