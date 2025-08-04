from src.server.app import app

from colorama import Fore, Style, init
import os
from src.agent.main_agent import main_agent
import webbrowser
import threading

init(autoreset=True)

def banner():
    print(
        Fore.GREEN + r"""
        
 /$$$$$$$  /$$     /$$ /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$  /$$   /$$        /$$$$$$  /$$$$$$
| $$__  $$|  $$   /$$/| $$__  $$ /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$| $$$ | $$       /$$__  $$|_  $$_/
| $$  \ $$ \  $$ /$$/ | $$  \ $$| $$  \ $$| $$  \__/| $$  \__/| $$  \ $$| $$$$| $$      | $$  \ $$  | $$  
| $$$$$$$/  \  $$$$/  | $$$$$$$/| $$  | $$|  $$$$$$ | $$      | $$$$$$$$| $$ $$ $$      | $$$$$$$$  | $$  
| $$____/    \  $$/   | $$__  $$| $$  | $$ \____  $$| $$      | $$__  $$| $$  $$$$      | $$__  $$  | $$  
| $$          | $$    | $$  \ $$| $$  | $$ /$$  \ $$| $$    $$| $$  | $$| $$\  $$$      | $$  | $$  | $$  
| $$          | $$    | $$  | $$|  $$$$$$/|  $$$$$$/|  $$$$$$/| $$  | $$| $$ \  $$      | $$  | $$ /$$$$$$
|__/          |__/    |__/  |__/ \______/  \______/  \______/ |__/  |__/|__/  \__/      |__/  |__/|______/

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=
""" + Fore.YELLOW + Style.BRIGHT + """
Contributers: 
    - Sreehari
    - Aromal 
    
Star us on GitHub if you like it! \n
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=
                                                                                                                                                                                      
        """ + Style.RESET_ALL
    )


# if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
# banner()
# # executable()
# # main_agent()


# webbrowser.open("http://127.0.0.1:5500/src/presentation/index.html")

# if __name__ == "__main__":
    
    
#     app.run(host="0.0.0.0", port=8434, debug=True)
if __name__ == "__main__":
    banner()

    # Start main_agent in a separate thread so Flask can run concurrently
    agent_thread = threading.Thread(target=main_agent, daemon=True)
    agent_thread.start()

    try:
        webbrowser.open("http://127.0.0.1:5500/src/presentation/index.html")
    except Exception as e:
        print(Fore.RED + f"Failed to open browser: {e}")

    app.run(host="0.0.0.0", port=8434, debug=True)