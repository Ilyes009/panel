import panel as pn
from src.gui.marketplace_panel import MarketplacePanel
from src.utils.system import clear_screen, set_terminal_title
from src.config import BANNER
import hashlib
import sys
from keyauth import api
import os

def getchecksum():
    md5_hash = hashlib.md5()
    with open(''.join(sys.argv), "rb") as file:
        md5_hash.update(file.read())
    return md5_hash.hexdigest()

def main():
    set_terminal_title("Hydra #1 - @planoea on discord")
    print(BANNER)
    
    keyauthapp = api(
        name="HydraV1",
        ownerid="fV0uvYnrch",
        version="1.0",
        hash_to_check=getchecksum()
    )
    
    key = pn.widgets.PasswordInput(name="Authorization Key", placeholder="Enter your key...")
    
    def validate_key(event):
        try:
            keyauthapp.license(key.value)
            clear_screen()
            marketplace = MarketplacePanel()
            pn.serve(marketplace.show())
        except Exception as e:
            print(f"Authentication failed: {str(e)}")
    
    auth_button = pn.widgets.Button(name="Login", button_type="primary")
    auth_button.on_click(validate_key)
    
    layout = pn.Column(
        pn.pane.Markdown("# Welcome To Hydra HQ"),
        pn.pane.Markdown("Input Valid Authorization Key"),
        key,
        auth_button
    )
    
    pn.serve(layout)

if __name__ == "__main__":
    main()