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

    @classmethod
    def get_aggregated_logs(
        cls,
        start_time,
        end_time,
        aggregator_type="minutes",
        optional_query_parameters=None,
    ):
        """Returns the list of aggregated logs in your account.

        Required Query Parameters

        ======================== ===========
        Field                    Description
        ======================== ===========
        start_time               Start date and time. Format used is ISO 8601 as YYYYMMDDThhmmssZ , ISO 8601 format without - and :
        end_time                 End date and time. Format used is ISO 8601 as YYYYMMDDThhmmssZ , ISO 8601 format without - and :
        aggregator_type          Default value: "minutes". Valid values are: minutes, hours, days, months, years
        ======================== ===========

        Optional Query Parameters

        ======================== ===========
        Field                    Description
        ======================== ===========
        log_type                 The log type, as a string. log-types are typically of the form ITEM_TYPE.ACTION, where ITEM_TYPE is the type of item that was affected and ACTION is what happened to it. A valid list of log_ytpes: message.queued, message.undelivered, message.failed, message.received, webhook.error, number.purchased, number.released, user.login, user.login_success
        operator_id              Unique id of operator that caused this log.
        limit                    Used for pagination, number of log records to return.
        start_key                Used for pagination, value of last_key from previous response.
        ======================== ===========
        """
        query_string = {
            "start_time": start_time,
            "end_time": end_time,
            "aggregator_type": aggregator_type,
        }
        if optional_query_parameters is not None:
            for key, value in optional_query_parameters.items():
                query_string[key] = value
        response = Log.get(custom_path="/aggregate", **query_string)
        return response

    @classmethod
    def find(cls, id_=None, path=None, **kwargs):
        """
             Get logs related to an user account.

             This method returns a tuple with the following values:
                - last_key: Used for pagination. Can be sent with next request as start_key to get next set of results.
                - logs: list of log entries.
        """
        url = cls._collection_path(path=path, options=None) + cls._query_string(kwargs)
        response = cls.request.get(url)
        last_key = response.get("last_key")
        logs = cls._build_list(response["log_items"])
        return last_key, logs
