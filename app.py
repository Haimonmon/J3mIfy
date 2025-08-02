
import j3mify as jeje

# * External Libraries for Terminal style customization 🌾✨
from rich import box
from rich.panel import Panel
from rich.layout import Layout
from rich.console import Console
from rich.columns import Columns

from typing import Dict, Literal, List

console = Console()

layout = Layout(name="root")

ORIGINAL_COLOR: str = "#C3AD88"
NORMALIZED_CHAR_COLOR: str = "#AA5048"
TOKENIZATION_COLOR: str = "#E0A15E"
NORMALIZED_SENTENCE_COLOR: str = "#658963"

def display_debug_mode(original_sentence: str, normalized_characters: str, tokenization: str, normalized_sentence: str) -> None:
    """ for j3mify debug mode """

    # * For Original sentence
    box1: Panel = Panel.fit(original_sentence, title="🐞 ORIGINAL", 
                            title_align = "left", border_style = ORIGINAL_COLOR, padding = 2, box = box.ROUNDED)

    # * For normalization of characters sentence
    box2: Panel = Panel.fit(normalized_characters, title="♻️ NORMALIZED BY CHARACTERS", 
                            title_align = "left", border_style= NORMALIZED_CHAR_COLOR, padding = 2, box = box.ROUNDED)

    # * For tokenization
    box3: Panel = Panel.fit(" | ".join(tokenization), title="✂️ TOKENIZATION", 
                            title_align = "left", border_style = TOKENIZATION_COLOR, padding = 2, box = box.ROUNDED)

    # * For normalized sentence which is done 👌
    box4: Panel = Panel.fit(normalized_sentence, title = "🎉 NORMALIZED", 
                            title_align   = "left", border_style = NORMALIZED_SENTENCE_COLOR,  padding = 2, box = box.ROUNDED)

    console.print(Columns([box1, box2, box3, box4], equal=True))
    console.print("\n\n\n")


def display_presentation_mode(original_sentence: str, normalized_sentence: str) -> None:
    """ For j3mify presentation mode """
    # * For Original sentence
    box1: Panel = Panel.fit(original_sentence, title="🐞 ORIGINAL", 
                            title_align="left", border_style=ORIGINAL_COLOR, padding=2, box=box.ROUNDED)

    # * For normalized sentence which is done 👌
    box2: Panel = Panel.fit(normalized_sentence, title = "🎉 NORMALIZED", 
                            title_align   = "left", border_style = NORMALIZED_SENTENCE_COLOR,  padding = 2, box = box.ROUNDED)

    console.print(Columns([box1, box2], equal=True))
    console.print("\n\n\n")


def display_normal_mode(normalized_sentence: str) -> None:
    """ For j3mify normal mode """
    # * For normalized sentence which is done 👌
    box1: Panel = Panel.fit(normalized_sentence, title="🎉 NORMALIZED",
                            title_align="left", border_style=NORMALIZED_SENTENCE_COLOR,  padding=2, box=box.ROUNDED)

    console.print(box1)
    console.print("\n\n\n")


def choose(sentence: List[str] | str, mode: Literal["presentation", "debug"] = None) -> None:
    """ Wala nakong maisip na function description lmao """
    reply: Dict[str, str] | str = jeje.j3j3niZ3d(sentence, mode)

    if mode == "debug":
        display_debug_mode(
            original_sentence = reply.get("original_sentence"),
            normalized_characters = reply.get("character_normalization"),
            tokenization = reply.get("tokenization"),
            normalized_sentence = reply.get("normalized_sentence")
        )
        return

    if mode == "presentation":
        display_presentation_mode(
            original_sentence = reply.get("original_sentence"),
            normalized_sentence = reply.get("normalized_sentence")
        )
        return

    display_normal_mode(sentence)


def display_j3j3m0Nizer(sentence: List[str] | str, mode: Literal["presentation", "debug"] = None) -> None:
    """ User interface of the j3mify """
    if mode and mode not in ["presentation", "debug"]:
        print("[ 🍒 ]: Invalid Mode Choice.")
        return 

    if isinstance(sentence, list):
        for data in sentence:
            choose(data, mode = mode)
        return
    
    if isinstance(sentence, str):
        choose(sentence, mode = mode)
        return

    choose(sentence = sentence)
      
