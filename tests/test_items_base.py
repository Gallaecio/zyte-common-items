from typing import Optional, Union

import attrs
import pytest

from zyte_common_items import Item, is_data_container


class NotConsideredAnItem:
    """It has to inherit from Item to be considered one."""

    pass


@attrs.define(slots=True)
class SubItem(Item):
    name: str


@attrs.define(slots=True)
class BigItem(Item):
    sub_item: Optional[SubItem] = None


@attrs.define(slots=True)
class BigItemIncorrect(Item):
    """This item is particularly incorrect since the annotation for its field
    belongs to multiple types.
    """

    sub_item: Union[SubItem, int, str]


def test_is_data_container():
    """It should be able to discern if a given class/instance is a data container
    that is defined inside this repository.
    """
    assert is_data_container(Item)
    assert is_data_container(SubItem)
    assert is_data_container(Item())
    assert is_data_container(SubItem(name="test"))

    assert not is_data_container(NotConsideredAnItem)
    assert not is_data_container(NotConsideredAnItem())


def test_item_from_dict():
    """Tests the annotation-aware behavior for correcty deriving the correct type
    in the sub fields.
    """

    assert BigItem(sub_item=None).sub_item is None

    item = BigItem.from_dict({"sub_item": {"name": "hello"}})
    type(item.sub_item) == SubItem  # noqa: B015


def test_item_from_dict_value_error():
    """Items with fields annotated with a Union of multiple different types should
    error out.
    """
    with pytest.raises(ValueError):
        BigItemIncorrect.from_dict({"sub_item": {"name": "hello"}})
