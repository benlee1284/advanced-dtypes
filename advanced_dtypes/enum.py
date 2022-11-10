from __future__ import annotations

from typing import Any, Iterator, Tuple


def _is_descriptor(obj: Any) -> bool:
	return hasattr(obj, '__get__') or hasattr(obj, '__set__') or hasattr(obj, '__delete__')


class FastEnumMeta(type):
	@classmethod
	def __prepare__(mcs, cls: type, bases: Tuple[type, ...]) -> dict:
		return dict()

	def __new__(
		mcs,
		cls: str,
		bases: Tuple[type, ...],
		classdict: dict,
	) -> FastEnumMeta:
		enum_class = super().__new__(mcs, cls, bases, classdict)

		enum_class._element_map = dict()
		enum_class._reverse_element_map = dict()

		for name, value in classdict.items():
			if not name.startswith('_') and not _is_descriptor(value):
				member = enum_class.__new__(enum_class)
				member.name = name
				member.value = value

				member._hash = hash(name)

				member.__init__()
				setattr(enum_class, name, member)
				enum_class._element_map[name] = member
				try:
					# Value may not be hashable
					enum_class._reverse_element_map[value] = member
				except TypeError:
					pass

		enum_class.__slots__ = tuple(name for name in classdict) + ("_element_map", "_reverse_element_map")

		return enum_class

	def __call__(cls, value: Any) -> FastEnum:
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

	def __getitem__(cls, name: str) -> FastEnum:
		return cls._element_map[name]

	def __iter__(cls) -> Iterator[FastEnum]:
		return (v for v in cls._element_map.values())

	def __reversed__(cls) -> Iterator[FastEnum]:
		return reversed(list(cls))

	def __len__(cls) -> int:
		return len(cls._element_map)


class FastEnum(metaclass=FastEnumMeta):
	__slots__ = ("_hash", "name", "value")

	_hash: int

	def __repr__(self) -> str:
		return f'{self.__class__.__name__}.{self.name}'

	def __hash__(self) -> int:
		return self._hash

	def __eq__(self, other: Any) -> bool:
		if isinstance(other, FastEnum):
			return self.value == other.value
		else:
			return self.value == other
