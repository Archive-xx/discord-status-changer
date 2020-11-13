try:
    import os
    import json
    import time
    import requests

    from colorama import Fore, init
except ModuleNotFoundError:
    os.system("pip3 install colorama requests")

init()

errors = 0
succeses = 0

os.system("cls" if os.name == "nt" else "clear") # so it should work on windows and linux

with open("configs/words.txt", "r", encoding="UTF-8") as f:
    words = []
    for word in f.read().splitlines():
        words.append(word)


with open("configs/config.json", encoding="UTF-8") as f:
    config = json.load(f)

headers = {
    "Authorization": config["token"],
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.287 Chrome/85.0.4183.121 Electron/10.1.5 Safari/537.36",
    "Accept": "*/*"
}


while True:
    for i in range(len(words)):
        try:
            json = {"custom_status": {"text": words[i], "emoji_name": config["emoji_name"], "emoji_id": config["emoji_id"]}}
            r = requests.patch("https://canary.discord.com/api/v8/users/@me/settings", headers=headers, json=json)

            if r.status_code == 401: # UNAUTHORIZED
                print(f"{Fore.RED}Invalid token...{Fore.RESET}")
                os.system("pause >NUL")
                os._exit(0)

            elif config["log_changes"] == True:
                print(f"{Fore.GREEN}>{Fore.RESET} Changed status to: {Fore.GREEN}{words[i]}{Fore.RESET}")
            succeses += 1
            os.system(f"title [Discord-status-changer] - errors: {errors} ^| status changed: {succeses}")

            time.sleep(int(config["timeout"]))
        except:
            errors += 1
