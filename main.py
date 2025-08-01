import json
import j3mify as jeje

# * External Libraries for Terminal style customization 🌾✨
from rich.text import Text
from rich.panel import Panel
from rich.console import Console

from typing import Dict, List

console = Console()


def load_file(file_name: str) -> any:
    """ Loads data on the specified json file name. """
    with open(fr"{file_name}", "r", encoding="utf-8") as file:
        return json.load(file)


def generate_previous_chats(file_name: str, prompter_name: str, bot_name: str) -> None:
    """ loads chat head like terminal """
    # * Loads previous chat heads from the choosed json file.
    remembered_messages: List = load_file(file_name = file_name)

    for chat_head_response in remembered_messages:
        # * Checks if role and messages are not empty 
        if chat_head_response["role"] and chat_head_response["message"]:
            generate_chat_head(
                role = chat_head_response["role"],
                response = chat_head_response["message"],
                prompter_name = prompter_name,
                bot_name = bot_name
            )
            
            
def generate_chat_head(role: str, response: str, prompter_name: str = "", bot_name: str = "") -> None:
    """ Display single chat head for the given role. """
    chat_head_icons: Dict = {
        "saturn": f"👩 {prompter_name}",
        "zero": f"🧑 {bot_name}"
    }
    
    if role == "saturn":
          response = jeje.jejenized(
                sentence = response,
                mode = "debug"
                )
          
    chat_head_response: str = f"\n {response} \n"

    # * Each roles need to have unique color chat heads.
    if role == "saturn":
        chat_head_text = Text(chat_head_response, style="bold orange1")
        chat_head_panel = Panel.fit(chat_head_text, border_style="orange1", title = chat_head_icons[role], title_align = "right")
        console.print(chat_head_panel, justify="right")
    else:
        chat_head_text = Text(chat_head_response, style="bold magenta")
        chat_head_panel = Panel.fit(chat_head_text, border_style="magenta", title = chat_head_icons[role], title_align = "left")
        console.print(chat_head_panel, justify="left")
        
        
def main():
    """ main terminal 💀👌🥐✨ """
    generate_previous_chats(
          file_name = "presentation.json",
          prompter_name = "saturn",
          bot_name = "zero"
    )

if __name__ == "__main__":
    # main()

    # * Thanks to the alpha's and the source
    # * Jejemon Source: http://www.reyjr.com/2010/05/i-can-jejemon-write-lolz-jejejeje.html?m=1

    sentences: List[str] = [
        "L3t's g0 n0w 2h symb0ls! Try usin9 \"+\" in pl4c3 of \"t\" sinc3 i+ lo0ks th3 s4me anyw4y. R3pl4cing \"i\" wi+h \"!\" is jus+ w0nd3rfully art!st!c 4nd !ngen!0us, d0n't y0u 4gr33? By th3 w4y, an \"a\" c4n als0 be r3pl@c3d with an \"@\" symb0l, d3p3nd!ng 0n h0w difficult it will bec0me 2h c0mpr3hend. I m3@n, d0n'+ us3 \"@\" wh3n y0u're wr!tin9 an 3ma!l @dd3ss!",
        "So I started with the obvious ones, exchange letters for numbers - \"a\" can be \"4\", like with a sl4nted psychedelic look to it. Exchange \"e\" with \"3\", but not 4ll the tim3. You c4n still us3 the normal \"e\", sometim3s. 3xh4nge y0ur capital \"G\" with \"6\" and sm4ll \"g\" with \"9\" - it m4k3s s3nse ri9ht? You can use \"2\" in pl4ce of \"to\" or \4\" inste4d 0f \"for\" 4nytim3 y0u f33l like y0u n33d 2h do it... 4nd finally, us3 th3 numb3r \"0\" instead of the letter \"o\", just b3caus3 it's cut3r th4t w4y. Co0l! 63ttin9 th3 h4n9 0f it n0w?",
        "L@sTly, jej3m0nz aRe,, kN0wN 2h b v3rY~ k!nD 4nD r3speCtfUl, d3sp!te tHe!r wRiTin9 stYl3. It iz n0t uNuSuAl 4 j3jemonz 2h eNd aNy sent3nz wi+H \"po\" - a s!gn of~ r3spEct 4 Filipinos. TH3r ar sveral vRsi0ns- frm d s!mpl3 \"poh\" 2h d mor iNteRestn9 \"poewh\" 2h d fLaMboUyant~ \"phoewhzz\" - tAk3 ur piCk pohwzz!!!!~~~ jejeje!"
    ]

    for sentence in sentences:
        normalized: str = jeje.jejenized(
            sentence = sentence
        )

        print()
        print(normalized)

   


  
