from __future__ import annotations

from dataclasses import dataclass

from app.users import User, LocalUser, ForeignUser

import re

LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    _NAME_PATTERN = re.compile(r"^[A-Za-zА-Яа-яЁё]+ [A-Za-zА-Яа-яЁё]+$")
    _PHONE_PATTERN = re.compile(r"^\+?\d{7,15}$")
    _FIELDS_NUMBER = 6

    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._cross_border_calls: list[ActiveCall] = []

    def register_call(self, raw_call: str) -> ActiveCall:
        split_call = raw_call.split(',')
        if len(split_call) != self._FIELDS_NUMBER:
            raise ValueError(f"Ожидалось {self._FIELDS_NUMBER} полей, было получено {len(split_call)}")
        caller_id, caller_name, caller_phone, receiver_id, receiver_name, receiver_phone = split_call
        self._validate_id(caller_id, "caller_id")
        self._validate_id(receiver_id, "receiver_id")
        self._validate_name(self, caller_name, "caller_name")
        self._validate_name(self, receiver_name, "receiver_name")
        self._validate_phone(self, caller_phone, "caller_phone")
        self._validate_phone(self, receiver_phone, "receiver_phone")
        caller = self._create_user(caller_id, caller_name, caller_phone)
        receiver = self._create_user(receiver_id, receiver_name, receiver_phone)
        call = ActiveCall(caller, receiver)
        self._active_calls.append(call)
        if call.is_cross_border:
            self._cross_border_calls.append(call)
        return call

    @staticmethod
    def _create_user(user_id: str, name: str, phone: str) -> LocalUser | ForeignUser:
        cls = LocalUser if phone[:2] == LOCAL_PHONE_PREFIX else ForeignUser
        return cls(int(user_id), name, phone)

    @staticmethod
    def _validate_id(value: str, field: str) -> None:
        if not value.isdigit():
            raise ValueError(f"{field} должен быть положительным числом, было получено {value}")

    @staticmethod
    def _validate_name(self, value: str, field: str) -> None:
        if not self._NAME_PATTERN.match(value):
            raise ValueError(f"{field} должен быть строкой в виде 'Имя Фамилия', было получено {value}")

    @staticmethod
    def _validate_phone(self, value: str, field: str) -> None:
        if not self._PHONE_PATTERN.match(value):
            raise ValueError(f"{field} должен быть строкой в виде '+*', где * - 7-15 чисел, было получено {value}")

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return len(self._cross_border_calls)
