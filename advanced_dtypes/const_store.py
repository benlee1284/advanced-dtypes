from __future__ import annotations

from typing import Any, Iterator, Tuple


def _is_descriptor(obj: Any) -> bool:
    return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')


class ConstStoreMeta(type):
    @classmethod
    def __prepare__(mcs, cls: type, bases: Tuple[type, ...]) -> dict:
        return dict()

    def __new__(
        mcs,
        cls: str,
        bases: Tuple[type, ...],
        classdict: dict,
    ) -> ConstStoreMeta:
        const_class = super().__new__(mcs, cls, bases, classdict)

        const_class._element_keys_set = set()
        const_class._element_map = dict()
        const_class._reverse_element_map = dict()

        for name, value in classdict.items():
            if not name.startswith('_') and not _is_descriptor(value):
                setattr(const_class, name, value)
                try:
                    const_class._element_keys_set.add(value)
                    const_class._element_map[name] = value
                    const_class._reverse_element_map[value] = name
                except TypeError:
                    ...

        const_class.__slots__ = tuple(name for name in classdict) + ("_element_keys_set", "_element_map", "_reverse_element_map")

        return const_class

    def __call__(cls, value: Any) -> ConstStore:
        if isinstance(value, cls):
            return value

        try:
            return cls._reverse_element_map[value]
        except TypeError:
            # for non-hashable items
            for member in cls._element_map.values():
                if member.value == value:
                    return member
        except KeyError:
            ...
        raise LookupError(f"No member found with value {value}")

    def __getitem__(cls, name: str) -> ConstStore:
        return cls._element_map[name]

    def __iter__(cls) -> Iterator[ConstStore]:
        return (v for v in cls._element_map.values())

    def __reversed__(cls) -> Iterator[ConstStore]:
        return reversed(list(cls))

    def __len__(cls) -> int:
        return len(cls._element_map)

    def __contains__(cls, element: Any) -> bool:
        # Use set where possible otherwise use list
        return element in cls._element_keys_set or element in cls._element_map.values()


class ConstStore(metaclass=ConstStoreMeta):
    ...
