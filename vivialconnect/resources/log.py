"""
.. module:: configuration
   :synopsis: Log module.
"""

from vivialconnect.resources.resource import Resource


class Log(Resource):
	"""Returns the list of logs in your account.

    Required Query Parameters

    ======================== ===========
    Field                    Description
    ======================== ===========
    start_time               Start date and time. Format used is ISO 8601 as YYYYMMDDThhmmssZ , ISO 8601 format without - and :
    end_time                 End date and time. Format used is ISO 8601 as YYYYMMDDThhmmssZ , ISO 8601 format without - and :
    ======================== ===========

    Optional Query Parameters

    ======================== ===========
    Field                    Description
    ======================== ===========
    log_type                 The log type, as a string. log-types are typically of the form ITEM_TYPE.ACTION, where ITEM_TYPE is the type of item that was affected and ACTION is what happened to it. For example, message.queued.                                                   |
    item_id                  Unique id of item that was affected.
    operator_id              Unique id of operator that caused this log.
    limit                    Used for pagination, number of log records to return.
    start_key                Used for pagination, value of last_key from previous response.
    ======================== ===========
	"""
	pass
