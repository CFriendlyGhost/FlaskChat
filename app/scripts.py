import random
import string
from typing import Dict, List, Any, Tuple


def create_room_id(id_length: int) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = "".join(random.choice(characters) for _ in range(id_length))
    return random_string


def change_dict_format(messages_dict: Dict[str, List[Tuple[str, Any]]]) -> List[Dict[str, Any]]:
    formatted_messages = []

    for user, messages in messages_dict.items():
        for content, send_time in messages:
            formatted_message = {"user": user, "date": send_time, "message": content}
            formatted_messages.append(formatted_message)
    formatted_messages.sort(key=lambda x: x["date"], reverse=True)
    return formatted_messages


def rooms_to_codes(rooms: List[Any]) -> List[str]:
    codes_list = []
    for room in rooms:
        codes_list.append(room.room_code)
    return codes_list
