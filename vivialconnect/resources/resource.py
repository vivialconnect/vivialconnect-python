"""
.. module:: resource
   :synopsis: Resource module.
"""
# Inspired by https://github.com/Shopify/pyactiveresource

import sys

from collections import MutableSequence, MutableMapping
from itertools import chain

from vivialconnect.common.requestor import Requestor
from vivialconnect.common.error import ResourceError
from vivialconnect.common.util import Util
import six


class BaseField(object):
    pass


class ResourceAttributeStorage(MutableMapping):
    def __init__(self, parent, attributes=None, backing_type=dict):
        if not isinstance(parent, Resource):
            raise ValueError("Parent should be a Resource instance")
        self.parent_resource = parent
        self._items = backing_type()
        self._fields = parent.declared_fields
        if isinstance(attributes, dict):
            self.update(attributes)

    def __getitem__(self, key):
        if key in self._fields:
            return getattr(self.parent_resource, key)
        return self._items[key]

    def __iter__(self):
        return chain(self._items, self._fields)

    def __len__(self):
        return len(self._items) + len(self._fields)

    def __delitem__(self, key):
        if key in self._fields:
            delattr(self.parent_resource, key)
        del self._items[key]

    def __setitem__(self, key, value):
        if key in self._fields:
            setattr(self.parent_resource, key, value)
        else:
            self._items[key] = value


class ResourceMeta(type):
    """A metaclass for :class:`Resource` objects.

    This class provides a way for configuration of API properties (user, password, account_id, etc).
    """

    def __new__(mcs, name, bases, new_attrs):
        if "_singular" not in new_attrs or not new_attrs["_singular"]:
            new_attrs["_singular"] = Util.underscore(name)
        if "_plural" not in new_attrs or not new_attrs["_plural"]:
            new_attrs["_plural"] = Util.pluralize(new_attrs["_singular"])
        klass = type.__new__(mcs, name, bases, new_attrs)
        klass._fields = {}
        for attr, val in new_attrs.items():
            if isinstance(val, BaseField):
                klass._fields[attr] = val
        return klass

    def get_plural(cls):
        return cls._plural

    def set_plural(cls, value):
        cls._plural = value

    plural = property(
        get_plural, set_plural, None, "The plural name of this object type"
    )

    def get_singular(cls):
        return cls._singular

    def set_singular(cls, value):
        cls._singular = value

    singular = property(
        get_singular, set_singular, None, "The singular name of this object type"
    )

    def get_primary_key(cls):
        return cls._primary_key

    def set_primary_key(cls, value):
        cls._primary_key = value

    primary_key = property(
        get_primary_key,
        set_primary_key,
        None,
        "Name of attribute that uniquely identies the resource",
    )

    @property
    def request(cls):
        super_class = cls.__mro__[1]
        if super_class == object or "_request" in cls.__dict__:
            if cls._request is None:
                cls._request = Requestor(
                    api_key=cls.api_key,
                    api_secret=cls.api_secret,
                    api_base_url=cls.api_base_url,
                    api_account_id=cls.api_account_id,
                    verify_request=cls._verify_request,
                    request_timeout=cls._request_timeout,
                )
            return cls._request
        else:
            return super_class.request

    def get_api_key(cls):
        return cls._api_key

    def set_api_key(cls, value):
        cls._request = None
        cls._api_key = value

    api_key = property(
        get_api_key, set_api_key, None, "An API key used for HMAC authentication"
    )

    def get_api_secret(cls):
        return cls._api_secret

    def set_api_secret(cls, value):
        cls._request = None
        cls._api_secret = value

    api_secret = property(
        get_api_secret,
        set_api_secret,
        None,
        "An API secret used for HMAC authentication",
    )

    def get_api_account_id(cls):
        return cls._api_account_id

    def set_api_account_id(cls, value):
        cls._request = None
        cls._api_account_id = value

    api_account_id = property(
        get_api_account_id, set_api_account_id, None, "An API account id"
    )

    def get_api_base_url(cls):
        return cls._api_base_url

    def set_api_base_url(cls, value):
        cls._request = None
        cls._api_base_url = value

    api_base_url = property(
        get_api_base_url,
        set_api_base_url,
        None,
        "An API base_url used for HMAC authentication",
    )

    def get_verify_request(cls):
        return cls._verify_request

    def set_verify_request(cls, value):
        cls._request = None
        cls._verify_request = value

    api_verify_request = property(
        get_verify_request, set_verify_request, None, "Verify SSL certs"
    )

    def get_request_timeout(cls):
        return cls._request_timeout

    def set_request_timeout(cls, value):
        cls._request_timeout = value

    request_timeout = property(
        get_request_timeout, set_request_timeout, None, "Request Timeout"
    )


class Resource(six.with_metaclass(ResourceMeta, object)):
    """This class represents a base :class:`Resource` object.
    """

    _request = None
    _api_key = None
    _api_secret = None
    _api_account_id = None
    _api_base_url = None
    _verify_request = True
    _primary_key = "id"
    _request_timeout = 30

    API_ACCOUNT_PREFIX = "/accounts/%(account_id)s"

    def __init__(self, attributes=None, prefix_options=None):
        if attributes is None:
            attributes = {}
        if prefix_options:
            self._prefix_options = prefix_options
        else:
            self._prefix_options = []
        self.klass = self.__class__
        self.attributes = ResourceAttributeStorage(self, attributes)
        self._initialized = True

    # Public class methods which act as factory functions
    @classmethod
    def find(cls, id_=None, path=None, **kwargs):
        """Find resources.

        :param id_: A specific resource to retrieve.
        :type id_: ``int``.
        :param path: The path that resources will be fetched from.
        :type path: ``str``.
        :param \**kwargs: Any keyword arguments used for forming a query.
        :returns: :class:`Resource` -- a Resource object.
        :raises: :class:`RequestorError`: On any communications errors.
                 :class:`ResourceError`: On any other errors.
        """
        if id_:
            return cls._find_single(id_, path=path, **kwargs)
        return cls._find_every(path=path, **kwargs)

    @classmethod
    def find_first(cls, path=None, **kwargs):
        """Find first available resource from the list.

        :param path: The path that resources will be fetched from.
        :type path: ``str``.
        :param \**kwargs: Any keyword arguments used for forming a query. Valid query keywords include: search, order, limit, page
        :returns: The first found resource from the list of returned resources, otherwise ``None``.
        :raises: :class:`RequestorError`: On any communications errors.
                 :class:`ResourceError`: On any other errors.
        """
        resources = cls._find_every(path=path, **kwargs)
        if resources:
            return resources[0]

    @classmethod
    def create(cls, attributes):
        """Creates and saves a resource with the given attributes.

        :param attributes: A dictionary of attributes which represent this object.
        :type attributes: ``dict``.
        :returns: :class:`Resource` -- a newly created :class:`Resource` object.
        """
        resource = cls(attributes)
        resource.save()
        return resource

    def save(self):
        """Saves :class:`Resource` object to the server.

        :returns: ``True`` on success, or throws an error.
        :raises: :class:`RequestorError`: On any communications errors.
            :class:`ResourceError`: On any other errors.
        """
        attributes = self._wrap_attributes(root=self._singular)
        if self.id:
            response = self.klass.request.put(
                self._element_path(self.id, path=None, options=self._prefix_options),
                attributes,
            )
        else:
            response = self.klass.request.post(
                self._collection_path(path=None, options=self._prefix_options),
                params=attributes,
            )
        self._update(Util.remove_root(response))
        return True

    def reload(self):
        """Reloads :class:`Resource` object from the server.

        :raises: :class:`RequestorError`: On any communications errors.
            :class:`ResourceError`: On any other errors.
        """
        attributes = self.klass.request.get(
            self._element_path(self.id, path=None, options=self._prefix_options)
        )
        self._update(attributes)

    def destroy(self):
        """Deletes :class:`Resource` object from the server.

        :raises: :class:`RequestorError`: On any communications errors.
            :class:`ResourceError`: On any other errors.
        """
        self.klass.request.delete(
            self._element_path(self.id, path=None, options=self._prefix_options)
        )

    def is_new(self):
        """Returns True if resource is new and have not been saved.

        :returns: ``True`` if resource is new, ``False`` otherwise.
        """
        return not self.id

    @classmethod
    def get(cls, id_=None, path=None, custom_path="", **kwargs):
        url = cls._custom_path(
            id_=id_, path=path, custom_path=custom_path, options=None
        ) + cls._query_string(kwargs)
        return cls.request.get(url)

    @classmethod
    def post(cls, id_=None, path=None, custom_path="", params=None, **kwargs):
        url = cls._custom_path(
            id_=id_, path=path, custom_path=custom_path, options=None
        ) + cls._query_string(kwargs)
        return cls.request.post(url, params=params)

    @classmethod
    def _find_single(cls, id_, path=None, **kwargs):
        url = cls._element_path(id_, path=path, options=None) + cls._query_string(
            kwargs
        )
        response = cls.request.get(url)
        return cls._build_object(response)

    @classmethod
    def _find_every(cls, path=None, **kwargs):
        url = cls._collection_path(path=path, options=None) + cls._query_string(kwargs)
        response = cls.request.get(url)
        return cls._build_list(response)

    @classmethod
    def _build_object(cls, attributes):
        return cls(Util.remove_root(attributes))

    @classmethod
    def _build_list(cls, attributes):
        resources = []
        elements = Util.remove_root(attributes)
        if isinstance(elements, dict):
            elements = [elements]
        for element in elements:
            resources.append(cls(Util.remove_root(element)))
        return resources

    def _update(self, attributes):
        if not isinstance(attributes, dict):
            return
        for key, value in six.iteritems(attributes):
            desc = self.declared_fields.get(key)
            if isinstance(value, dict):
                klass = self._find_class_for(key)
                attr = klass(value)
            elif isinstance(value, list):
                klass = None
                attr = []
                for child in value:
                    if isinstance(child, dict):
                        if klass is None:
                            # Figure out the class based on the descriptor, if any
                            if desc:
                                klass = desc.member_type
                            else:
                                # Guess the subclass
                                klass = self._find_class_for_collection(key)
                        if issubclass(klass, SubordinateResource):
                            attr.append(klass(child, parent_resource=self))
                        else:
                            attr.append(klass(child))
                    else:
                        attr.append(child)
                if klass and issubclass(klass, SubordinateResource):
                    setattr(self, key, attr)
            else:
                attr = value
            # Store the actual value in the attributes dictionary
            self.attributes[key] = attr

    @classmethod
    def _find_class_for_collection(cls, collection_name):
        return cls._find_class_for(Util.singularize(collection_name))

    @classmethod
    def _find_class_for(cls, element_name=None, class_name=None, create_missing=True):
        if not element_name and not class_name:
            raise ResourceError("element_name or class_name must be specified")
        elif not element_name:
            element_name = Util.underscore(class_name)
        elif not class_name:
            class_name = Util.camelize(element_name)

        module_path = cls.__module__.split(".")
        for depth in range(len(module_path), 0, -1):
            try:
                __import__(".".join(module_path[:depth]))
                module = sys.modules[".".join(module_path[:depth])]
            except ImportError:
                continue
            try:
                klass = getattr(module, class_name)
                return klass
            except AttributeError:
                try:
                    __import__(".".join([module.__name__, element_name]))
                    submodule = sys.modules[".".join([module.__name__, element_name])]
                except ImportError:
                    continue
                try:
                    klass = getattr(submodule, class_name)
                    return klass
                except AttributeError:
                    continue

        # Woow, we made it this far, and no class was found
        if create_missing:
            return type(str(class_name), (cls,), {"__module__": cls.__module__})

    @property
    def declared_fields(self):
        return self._fields

    def _to_dict(self):
        attributes = {}
        for key, value in six.iteritems(self.attributes):
            if isinstance(value, MutableSequence):
                new_value = []
                for item in value:
                    if isinstance(item, Resource):
                        new_value.append(item._to_dict())
                    else:
                        new_value.append(item)
                attributes[key] = new_value
            elif isinstance(value, Resource):
                attributes[key] = value._to_dict()
            else:
                attributes[key] = value
        return attributes

    def _wrap_attributes(self, root="object"):
        if root:
            return {root: self._to_dict()}
        return self._to_dict()

    def get_id(self):
        return self.attributes.get(self.klass.primary_key)

    def set_id(self, value):
        self.attributes[self.klass.primary_key] = value

    id = property(get_id, set_id, None, "Value stored in the primary key")

    def _attr_valid(self, name):
        if "attributes" in self.__dict__:
            if name in self.attributes:
                return True
        return False

    def __getattr__(self, name):
        if "attributes" in self.__dict__:
            if name in self.attributes:
                return self.attributes[name]
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if "_initialized" in self.__dict__:
            if name in self.__dict__ or getattr(self.__class__, name, None):
                # Update a normal attribute
                object.__setattr__(self, name, value)
            else:
                # Add/update an attribute
                self.attributes[name] = value
        else:
            object.__setattr__(self, name, value)

    def __repr__(self):
        return "%s(%s)" % (self._singular, self.id)

    if six.PY2:
        # pylint: disable=undefined-variable
        def __cmp__(self, other):
            if isinstance(other, self.__class__):
                return cmp(self.id, other.id)
            else:
                return cmp(self.id, other)

    else:

        def __eq__(self, other):
            return (
                other.__class__ == self.__class__
                and self.id == other.id
                and self._prefix_options == other._prefix_options
            )

    def __hash__(self):
        return id(self)

    @classmethod
    def _prefix(cls, path=None, options=None):
        prefix = ""
        if path:
            prefix = path
        if options and isinstance(options, list) and len(options) > 0:
            prefix = prefix + ("/%s/%s" % tuple(options))
        return prefix

    @classmethod
    def _element_path(cls, id_, path=None, options=None, ext=".json"):
        return (cls.API_ACCOUNT_PREFIX + "%(prefix)s/%(plural)s/%(id)s%(ext)s") % {
            "account_id": cls._api_account_id,
            "prefix": cls._prefix(path, options),
            "plural": cls._plural,
            "id": id_,
            "ext": ext,
        }

    @classmethod
    def _collection_path(cls, path=None, options=None, ext=".json"):
        return (cls.API_ACCOUNT_PREFIX + "%(prefix)s/%(plural)s%(ext)s") % {
            "account_id": cls._api_account_id,
            "prefix": cls._prefix(path, options),
            "plural": cls._plural,
            "ext": ext,
        }

    @classmethod
    def _custom_path(
        cls, id_=None, path=None, custom_path="", options=None, ext=".json"
    ):
        if id_:
            return (
                cls.API_ACCOUNT_PREFIX + "%(prefix)s/%(plural)s/%(id)s%(custom)s%(ext)s"
            ) % {
                "account_id": cls._api_account_id,
                "prefix": cls._prefix(path, options),
                "plural": cls._plural,
                "id": id_,
                "custom": custom_path,
                "ext": ext,
            }
        else:
            return (
                cls.API_ACCOUNT_PREFIX + "%(prefix)s/%(plural)s%(custom)s%(ext)s"
            ) % {
                "account_id": cls._api_account_id,
                "prefix": cls._prefix(path, options),
                "plural": cls._plural,
                "custom": custom_path,
                "ext": ext,
            }

    @classmethod
    def _query_string(cls, query_options=None):
        if query_options:
            return "?" + Util.to_query(query_options)
        else:
            return ""


class SubordinateResource(Resource):
    def __init__(self, attributes=None, prefix_options=None, parent_resource=None):
        self.parent_resource = parent_resource
        super(SubordinateResource, self).__init__(attributes, prefix_options)

    @classmethod
    def find(cls, *args, **kwargs):
        raise NotImplementedError("Cannot find subordinate resources.")

    def __repr__(self):
        try:
            identity = "({})".format(self.identity)
        except AttributeError:
            identity = ""
        return "{}.{}{}".format(self.parent_resource, self._singular, identity)
