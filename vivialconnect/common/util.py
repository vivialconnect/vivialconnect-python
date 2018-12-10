"""
.. module:: util
   :synopsis: Various utility functions shipped with Vivial Connect
              Python API.

"""
# Inspired by https://github.com/Shopify/pyactiveresource

import re
import json

import six
from six.moves.urllib.parse import urlencode


# Patterns blatantly stolen from Rails' Inflector
PLURALIZE_PATTERNS = [
    (r"(quiz)$", r"\1zes"),
    (r"^(ox)$", r"\1en"),
    (r"([m|l])ouse$", r"\1ice"),
    (r"(matr|vert|ind)(?:ix|ex)$", r"\1ices"),
    (r"(x|ch|ss|sh)$", r"\1es"),
    (r"([^aeiouy]|qu)y$", r"\1ies"),
    (r"(hive)$", r"1s"),
    (r"(?:([^f])fe|([lr])f)$", r"\1\2ves"),
    (r"sis$", r"ses"),
    (r"([ti])um$", r"\1a"),
    (r"(buffal|tomat)o$", r"\1oes"),
    (r"(bu)s$", r"\1ses"),
    (r"(alias|status)$", r"\1es"),
    (r"(octop|vir)us$", r"\1i"),
    (r"(ax|test)is$", r"\1es"),
    (r"s$", "s"),
    (r"$", "s"),
]

SINGULARIZE_PATTERNS = [
    (r"(quiz)zes$", r"\1"),
    (r"(matr)ices$", r"\1ix"),
    (r"(vert|ind)ices$", r"\1ex"),
    (r"^(ox)en", r"\1"),
    (r"(alias|status)es$", r"\1"),
    (r"(octop|vir)i$", r"\1us"),
    (r"(cris|ax|test)es$", r"\1is"),
    (r"(shoe)s$", r"\1"),
    (r"(o)es$", r"\1"),
    (r"(bus)es$", r"\1"),
    (r"([m|l])ice$", r"\1ouse"),
    (r"(x|ch|ss|sh)es$", r"\1"),
    (r"(m)ovies$", r"\1ovie"),
    (r"(s)eries$", r"\1eries"),
    (r"([^aeiouy]|qu)ies$", r"\1y"),
    (r"([lr])ves$", r"\1f"),
    (r"(tive)s$", r"\1"),
    (r"(hive)s$", r"\1"),
    (r"([^f])ves$", r"\1fe"),
    (r"(^analy)ses$", r"\1sis"),
    (r"((a)naly|(b)a|(d)iagno|(p)arenthe|(p)rogno|(s)ynop|(t)he)ses$", r"\1\2sis"),
    (r"([ti])a$", r"\1um"),
    (r"(n)ews$", r"\1ews"),
    (r"s$", r""),
]

IRREGULAR = [
    ("person", "people"),
    ("man", "men"),
    ("child", "children"),
    ("sex", "sexes"),
    ("move", "moves"),
    # ('cow', 'kine') WTF?
]

UNCOUNTABLES = [
    "equipment",
    "information",
    "rice",
    "money",
    "species",
    "series",
    "fish",
    "sheep",
    "billing",
]


class Util(object):
    """Various utility functions shipped with Vivial Connect Python API.
    """

    @staticmethod
    def pluralize(singular):
        """Convert singular word to its plural form.

        :param singular: A word in its singular form.
        :type singular: `str`.
        :returns:  `str` -- the word in its plural form.
        """
        if singular in UNCOUNTABLES:
            return singular
        for i in IRREGULAR:
            if i[0] == singular:
                return i[1]
        for i in PLURALIZE_PATTERNS:
            if re.search(i[0], singular):
                return re.sub(i[0], i[1], singular)

    @staticmethod
    def singularize(plural):
        """Convert plural word to its singular form.

        :param plural: A word in its plural form.
        :type plural: `str`.
        :returns:  `str` -- the word in its singular form.
        """
        if plural in UNCOUNTABLES:
            return plural
        for i in IRREGULAR:
            if i[1] == plural:
                return i[0]
        for i in SINGULARIZE_PATTERNS:
            if re.search(i[0], plural):
                return re.sub(i[0], i[1], plural)
        return plural

    @staticmethod
    def camelize(word):
        """Convert a word from lower_with_underscores to CamelCase.

        :param word: The string to convert.
        :type word: `str`.
        :returns:  `str` -- the modified string.
        """
        return "".join(
            w[0].upper() + w[1:]
            for w in re.sub("[^A-Z^a-z^0-9^:]+", " ", word).split(" ")
        )

    @staticmethod
    def underscore(word):
        """Convert a word from CamelCase to lower_with_underscores.

        :param word: The string to convert.
        :type word: `str`.
        :returns:  `str` -- the modified string.
        """
        return re.sub(r"\B((?<=[a-z])[A-Z]|[A-Z](?=[a-z]))", r"_\1", word).lower()

    @staticmethod
    def to_query(query_params):
        """Convert a dictionary to url query parameters.

        :param query_params: A dictionary of arguments.
        :type query_params: `dict`.
        :returns:  `str` -- a string of query parameters.
        """

        def annotate_params(params):
            annotated = {}
            for key, value in six.iteritems(params):
                if isinstance(value, list):
                    key = "%s[]" % key
                elif isinstance(value, dict):
                    dict_options = {}
                    for dk, dv in six.iteritems(value):
                        dict_options["%s[%s]" % (key, dk)] = dv
                    annotated.update(annotate_params(dict_options))
                    continue
                elif isinstance(value, six.text_type):
                    value = value.encode("utf-8")
                else:
                    value = str(value)
                annotated[key] = value
            return annotated

        annotated = annotate_params(query_params)
        return urlencode(annotated, True)

    @staticmethod
    def to_json(obj, root="object"):
        """Convert a dictionary or list to an JSON string.

        :param obj: The object to serialize.
        :returns:  `str` -- a JSON string.
        """
        if root:
            obj = {root: obj}
        return json.dumps(obj, separators=(",", ":"))

    @staticmethod
    def json_to_dict(jsonstr):
        """Parse the json into a dictionary of attributes.

        :param jsonstr: A JSON formatted string.
        :type jsonstr: `str`.
        :returns:  `str` -- the deserialized object.
        """
        return json.loads(jsonstr)

    @staticmethod
    def remove_root(data):
        """Removes root key from dictionary.

        :param data: A dict to remove root key from.
        :type data: `dict`.
        :returns:  `dict` -- a new dictionary without root key.
        """
        if isinstance(data, dict) and len(data) == 1:
            return list(data.values())[0]
        return data
