"""
.. module:: countable
   :synopsis: Countable module.
"""

from vivialconnect.common.util import Util


class Countable(object):
    """Use this class to view the total number of resources.
    """

    @classmethod
    def count(cls, opts=None, **kwargs):
        """Use this method to view the total number of resources
        in your account.
        """
        if opts is None:
            opts = kwargs
        return int(Util.remove_root(cls.get(custom_path="/count", **opts)))
