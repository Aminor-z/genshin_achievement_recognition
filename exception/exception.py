# coding=utf-8
class GameCaptureException(Exception):
    def __str__(self):
        return f"I cannot see your game~ (Maybe your genshin window was minimized)"


class WhereIsYourGameException(Exception):
    def __init__(self, game_name):
        self.game_name = game_name

    def __str__(self):
        return f"I cannot find the game called {self.game_name}."


class ConfigFileErrorException(Exception):
    def __str__(self):
        return f"The config file is corrupted."


class GamtFileErrorException(Exception):
    def __str__(self):
        return f"The gamt file maybe incorrect."
