from os import getenv
import os
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

SESSION_STRING = getenv("SESSION_STRING", "session")
API_ID = int(getenv("API_ID", ""))
API_HASH = getenv("API_HASH")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
CHATS = list(map(int, getenv("CHATS").split()))
