from typing import Optional, List, Dict
import os
import json

from core.signals import on_shutdown


class Storage:
    _storage: Dict[str, Dict[str, str]] = {}

    @classmethod
    def get_user(cls, username: str) -> Optional[Dict]:
        return cls._storage.get(username, None)

    @classmethod
    def save_user(cls, username: str, data: Dict[str, str]) -> None:
        if type(username) != str or len(username) == 0:
            return

        cls._storage[username] = data
        return

    @classmethod
    def load_storage(cls) -> None:
        if not os.path.exists(".user_storage.json"):
            return
        with open(".user_storage.json", "r") as fd:
            cls._storage = json.load(fd)

    @classmethod
    def save_storage(cls) -> None:
        print("Saving the storage...")
        with open(".user_storage.json", "w") as fd:
            json.dump(cls._storage, fd)


Storage.load_storage()


@on_shutdown
def shutdown_save_storage():
    Storage.save_storage()
