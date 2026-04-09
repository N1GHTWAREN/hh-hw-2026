import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_creates_both_local_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "3,Ivan Ivanov,+79990000000,4,John Smith,+75551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, LocalUser)
    assert active_call.caller.id == 3
    assert active_call.receiver.id == 4


def test_register_call_creates_both_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "5,Ivan Ivanov,+19990000000,6,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, ForeignUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 5
    assert active_call.receiver.id == 6


def test_register_call_creates_foreign_and_local_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "7,Ivan Ivanov,+19990000000,8,John Smith,+75551234567"
    )

    assert isinstance(active_call.caller, ForeignUser)
    assert isinstance(active_call.receiver, LocalUser)
    assert active_call.caller.id == 7
    assert active_call.receiver.id == 8


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_initial_active_calls_count_is_zero():
    switchboard = Switchboard()

    assert switchboard.get_active_calls_count() == 0


def test_register_calls_accumulate():
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )

    assert switchboard.get_active_calls_count() == 1

    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_multiple_switchboards_independent():
    s1 = Switchboard()
    s2 = Switchboard()

    s1.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )

    assert s1.get_active_calls_count() == 1
    assert s2.get_active_calls_count() == 0


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1


def test_initial_cross_border_calls_count_is_zero():
    switchboard = Switchboard()

    assert switchboard.get_cross_border_calls_count() == 0


def test_cross_border_count_without_cross_border_calls():
    switchboard = Switchboard()

    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_cross_border_calls_count() == 0


def test_cross_border_register_calls_accumulate():
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )

    assert switchboard.get_cross_border_calls_count() == 0

    switchboard.register_call(
        "3,John Smith,+75551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_cross_border_calls_count() == 1

    switchboard.register_call(
        "5,Maria Petrova,+79991112233,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_cross_border_calls_count() == 2


def test_missing_fields_raises():
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="Ожидалось 6"):
        switchboard.register_call("1,Ivan Ivanov,+79990000000,2,John Smith")



def test_extra_fields_raises():
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="Ожидалось 6"):
        switchboard.register_call("1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567,дополнительная_информация")


def test_non_numeric_caller_id_raises():
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="caller_id"):
        switchboard.register_call("abc,Ivan Ivanov,+79990000000,2,John Smith,+15551234567")


def test_negative_caller_id_raises():
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="caller_id"):
        switchboard.register_call("-1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567")


def test_non_numeric_receiver_id_raises():
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="receiver_id"):
        switchboard.register_call("1,Ivan Ivanov,+79990000000,xyz,John Smith,+15551234567")


def test_single_word_caller_name_raises():
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="caller_name"):
        switchboard.register_call("1,Ivan,+79990000000,2,John Smith,+15551234567")


def test_name_with_digits_raises():
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="caller_name"):
        switchboard.register_call("1,Ivan123 Ivanov,+79990000000,2,John Smith,+15551234567")


def test_empty_name_raises():
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="caller_name"):
        switchboard.register_call("1,,+79990000000,2,John Smith,+15551234567")


def test_phone_with_letters_raises():
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="caller_phone"):
        switchboard.register_call("1,Ivan Ivanov,+7ABCDEFGH,2,John Smith,+15551234567")


def test_too_short_phone_raises():
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="caller_phone"):
        switchboard.register_call("1,Ivan Ivanov,+7123,2,John Smith,+15551234567")


def test_receiver_phone_invalid_raises():
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="receiver_phone"):
        switchboard.register_call("1,Ivan Ivanov,+79990000000,2,John Smith,+1ABC")
