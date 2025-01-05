"""
Test value object validation order.
"""

from typing import override

from value_object_pattern import ValueObject, process


class ValueObjectA(ValueObject[str]):
    """
    ValueObjectA value object class.
    """

    @process(order=0)
    def _concat_one(self, value: str) -> str:
        return value + 'A1'

    @process(order=1)
    def _concat_two(self, value: str) -> str:
        return value + 'A2'

    @process(order=2)
    def _aconcat_three(self, value: str) -> str:
        return value + 'A3'

    @process()
    def _aconcat_four(self, value: str) -> str:
        return value + 'A4'

    @process()
    def _concat_five(self, value: str) -> str:
        return value + 'A5'


class ValueObjectB(ValueObject[str]):
    """
    ValueObjectB value object class.
    """

    @process(order=0)
    def _concat_one(self, value: str) -> str:
        return value + 'B1'

    @process(order=1)
    def _concat_two(self, value: str) -> str:
        return value + 'B2'

    @process(order=2)
    def _aconcat_three(self, value: str) -> str:
        return value + 'B3'

    @process()
    def _concat_four(self, value: str) -> str:
        return value + 'B4'

    @process()
    def _aconcat_five(self, value: str) -> str:
        return value + 'B5'


class ValueObjectC(ValueObjectA, ValueObjectB):
    """
    ValueObjectC value object class.
    """

    @override
    @process(order=0)
    def _concat_one(self, value: str) -> str:
        return value + 'C1'

    @override
    @process(order=1)
    def _concat_two(self, value: str) -> str:
        return value + 'C2'

    @override
    @process(order=2)
    def _aconcat_three(self, value: str) -> str:
        return value + 'C3'

    @override
    @process()
    def _aconcat_four(self, value: str) -> str:
        return value + 'C4'

    @override
    @process()
    def _concat_five(self, value: str) -> str:
        return value + 'C5'


class ValueObjectD(ValueObjectB, ValueObjectA):
    """
    ValueObjectD value object class.
    """

    @override
    @process(order=0)
    def _concat_one(self, value: str) -> str:
        return value + 'D1'

    @override
    @process(order=1)
    def _concat_two(self, value: str) -> str:
        return value + 'D2'

    @override
    @process(order=2)
    def _aconcat_three(self, value: str) -> str:
        return value + 'D3'

    @override
    @process()
    def _aconcat_four(self, value: str) -> str:
        return value + 'D4'

    @override
    @process()
    def _concat_five(self, value: str) -> str:
        return value + 'D5'


def test_value_object_a_validation_order() -> None:
    """
    Test ValueObjectA validation order.
    """
    value_object_a = ValueObjectA(value='')
    assert value_object_a.value == 'A1A2A3A4A5'


def test_value_object_b_validation_order() -> None:
    """
    Test ValueObjectB validation order.
    """
    value_object_b = ValueObjectB(value='')
    assert value_object_b.value == 'B1B2B3B5B4'


def test_value_object_c_validation_order() -> None:
    """
    Test value object C validation order. The order should be class hierarchy, method order attribute, and method name.
    """
    value_object_c = ValueObjectC(value='')

    assert value_object_c.value == 'A1A2A3A4A5B1B2B3B5B4C1C2C3C4C5'


def test_value_object_d_validation_order() -> None:
    """
    Test value object D validation order. The order should be class hierarchy, method order attribute, and method name.
    """
    value_object_d = ValueObjectD(value='')

    assert value_object_d.value == 'B1B2B3B5B4A1A2A3A4A5D1D2D3D4D5'
