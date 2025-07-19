import json
import j3mify as jeje

# * External Libraries for Terminal style customization 🌾✨
from pyfiglet import Figlet

from rich.text import Text
from rich.live import Live
from rich.panel import Panel
from rich.console import Console

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
    """
    Display single chat head for the given role.
    """
    chat_head_icons: Dict = {
        "saturn": f"👩 {prompter_name}",
        "zero": f"🧑 {bot_name}"
    }
    
    if role == "saturn":
          response = jeje.jejenized(response)
          
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
    main()