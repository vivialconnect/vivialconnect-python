import abc
import collections

from weakref import WeakKeyDictionary
from vivialconnect.resources.resource import BaseField, SubordinateResource
from six import with_metaclass


class SimpleResourceList(collections.MutableSequence):
    """A simple list wrapper that only takes SubordinateResource or dict instances."""

    def __init__(self, owner, member_type, raw_items):
        self.member_type = member_type
        self.owner = owner
        self._items = list()
        self.extend(list(raw_items))

    def check(self, value):
        if isinstance(value, self.member_type):
            if (
                isinstance(value, SubordinateResource)
                and value.parent_resource
                and value.parent_resource != self.owner
            ):
                raise TypeError(
                    "Cannot add subordinate types to lists belonging to different parents."
                )
        elif not isinstance(value, dict):
            raise TypeError(
                "Value must be a {tp} instance or dict. Got {cl}".format(
                    tp=self.member_type, cl=type(value)
                )
            )

    def insert(self, index, value):
        self.check(value)
        if isinstance(value, dict):
            value = self.member_type(attributes=value)
        value.parent_resource = self.owner
        self._items.insert(index, value)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, i):
        return self._items[i]

    def __delitem__(self, i):
        del self._items[i]

    def __setitem__(self, i, v):
        self.check(v)
        self._items[i] = v

    def __repr__(self):
        return str(self._items)


class Field(with_metaclass(abc.ABCMeta, BaseField)):
    """Abstract field type defining a common interface."""

    def __init__(self, name):
        self.name = name
        self.owner_map = WeakKeyDictionary()

    def __get__(self, obj, obj_type):
        if obj is None:
            # Return the descriptor if no instance is given, as in getattr(type(obj), desc_name)
            return self
        if obj not in self.owner_map:
            self.owner_map[obj] = self.initialized_value(obj)
        return self.owner_map[obj]

    def __set__(self, obj, value):
        self.owner_map[obj] = value

    @abc.abstractmethod
    def initialized_value(self, obj, value=None):
        raise NotImplementedError


class ResourceField(Field):
    """A field containing a reference to a single SubordinateResource instance."""

    def __init__(self, name, member_type):
        if not issubclass(member_type, SubordinateResource):
            raise ValueError("member_type must be a SubordinateResource subclass")
        self.member_type = member_type
        super(ResourceField, self).__init__(name)

    def __set__(self, obj, value):
        if issubclass(self.member_type, SubordinateResource):
            if value.parent_resource and value.parent_resource != obj:
                raise TypeError(
                    "Cannot set subordinate resource to a value from another parent"
                )
            value.parent_resource = obj
        Field.__set__(self, obj, value)

    def initialized_value(self, obj, value=None):
        return None


class ResourceListingField(ResourceField):
    """A field containing a list of SubordinateResource instances."""

    def __init__(self, name, member_type, iterable_type=SimpleResourceList):
        self.iterable_type = iterable_type
        super(ResourceListingField, self).__init__(name, member_type)

    def __set__(self, obj, value):
        if not isinstance(value, self.iterable_type):
            value = self.initialized_value(obj, value)
        elif issubclass(self.member_type, SubordinateResource):
            for item in value:
                if item.parent_resource and item.parent_resource != obj:
                    raise TypeError(
                        "Cannot set listing of subordinate resources containing items from different parents."
                    )
                item.parent_resource = obj
        Field.__set__(self, obj, value)

    def initialized_value(self, obj, value=None):
        return self.iterable_type(obj, self.member_type, value or [])
