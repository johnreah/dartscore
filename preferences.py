import os
from pathlib import Path
import configparser
from typing import Any

class Preferences:
    """Centralised, type-aware configuration with safe defaults."""

    DEFAULTS = {
        "TextToSpeech": {
            "voice": "en_GB-alba-medium",
            "say_totals": True,
            "say_score_required": True
        },
        "Sound": {
            "button_clicks": True
        },
        "Players": {
            "player1": "Player 1",
            "player2": "Player 2"
        },
        "Game": {
            "start_from": 501
        }
    }

    def __init__(self, filename: str = ".dartscore.ini"):
        self.path = Path(os.path.join(Path().home(), filename))
        self.config = configparser.ConfigParser(
            defaults=None,           # we handle defaults ourselves
            interpolation=None,      # usually safest choice nowadays
            allow_no_value=False,
        )

        for section, options in self.DEFAULTS.items():
            self.config[section] = options.copy()

        if self.path.is_file():
            self.config.read(self.path)
        else:
            self.save()

    def get(self, section: str, key: str, fallback: Any = None) -> str:
        return self.config.get(section, key, fallback=fallback)

    def getint(self, section: str, key: str, fallback: int = 0) -> int:
        return self.config.getint(section, key, fallback=fallback)

    def getfloat(self, section: str, key: str, fallback: float = 0.0) -> float:
        return self.config.getfloat(section, key, fallback=fallback)

    def getboolean(self, section: str, key: str, fallback: bool = False) -> bool:
        return self.config.getboolean(section, key, fallback=fallback)

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as f:
            self.config.write(f, space_around_delimiters=False)

    #-----------
    # Properties
    #-----------

    @property
    def tts_voice(self) -> str:
        return self.get("TextToSpeech", "voice")

    @tts_voice.setter
    def tts_voice(self, value: str) -> None:
        self.config["TextToSpeech"]["voice"] = value
        self.save()

    @property
    def tts_say_totals(self) -> bool:
        return self.getboolean("TextToSpeech", "say_totals", False)

    @tts_say_totals.setter
    def tts_say_totals(self, value: bool) -> None:
        self.config["TextToSpeech"]["say_totals"] = str(value).lower()
        self.save()

    @property
    def tts_say_score_required(self) -> bool:
        return self.getboolean("TextToSpeech", "say_score_required", False)

    @tts_say_score_required.setter
    def tts_say_score_required(self, value: bool) -> None:
        self.config["TextToSpeech"]["say_score_required"] = str(value).lower()
        self.save()

    @property
    def sound_button_clicks(self) -> bool:
        return self.getboolean("Sound", "button_clicks", False)

    @sound_button_clicks.setter
    def sound_button_clicks(self, value: bool) -> None:
        self.config["Sound"]["button_clicks"] = str(value).lower()
        self.save()

    @property
    def players_player1(self) -> str:
        return self.get("Players", "player1")

    @players_player1.setter
    def players_player1(self, value: str) -> None:
        self.config["Players"]["player1"] = value
        self.save()

    @property
    def players_player2(self) -> str:
        return self.get("Players", "player2")

    @players_player2.setter
    def players_player2(self, value: str) -> None:
        self.config["Players"]["player2"] = value
        self.save()

    @property
    def game_start_from(self) -> int:
        return self.get("Game", "start_from")

    @game_start_from.setter
    def game_start_from(self, value: int) -> None:
        self.config["Game"]["start_from"] = str(value)
        self.save()

