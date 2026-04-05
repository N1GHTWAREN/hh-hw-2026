from __future__ import annotations

from dataclasses import dataclass

from app.users import User


LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []

    def register_call(self, raw_call: str) -> ActiveCall:
        from app import LocalUser, ForeignUser
        def create_user(user_id, name, phone):
            cls = LocalUser if phone[:2] == LOCAL_PHONE_PREFIX else ForeignUser
            return cls(int(user_id), name, phone)
        caller_id, caller_name, caller_phone, receiver_id, receiver_name, receiver_phone = raw_call.split(',')
        caller = create_user(caller_id, caller_name, caller_phone)
        receiver = create_user(receiver_id, receiver_name, receiver_phone)
        return ActiveCall(caller, receiver)

    def get_active_calls_count(self) -> int:
        pass  # Удалите `pass` и пишите ваш код

    def get_cross_border_calls_count(self) -> int:
        pass  # Удалите `pass` и пишите ваш код
