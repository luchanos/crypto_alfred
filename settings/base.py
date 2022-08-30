import os

from envparse import Env


env = Env()

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
