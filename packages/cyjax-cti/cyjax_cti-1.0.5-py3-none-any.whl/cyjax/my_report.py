from .helpers import DateHelper
from .resource import Resource


class MyReport(Resource):

    def __init__(self, api_key=None, api_url=None):
        """
        :param api_key: The API key.
        :param api_url: The API URL.
        """
        super(MyReport, self).__init__(api_key=api_key, api_url=api_url)

    def list(self, query=None, since=None, until=None):
        """
        Returns my reports.

        :param query: The search query.
        :type query: str, optional

        :param since: The start date time.
        :type since: (datetime, timedelta, str), optional

        :param until: The end date time.
        :type until:  (datetime, timedelta, str), optional

        :return: The list of incident reports.
        :rtype list
        """
        params = DateHelper.build_date_params(since=since, until=until)
        if query:
            params.update({'query': query})

        return self.paginate(endpoint='report/my-report', params=params)

    def one(self, report_id):
        """
        Get one record by ID

        :param report_id: The my report ID
        :type report_id: int, str

        :return: The record dictionary, raises exception if record not found
        :rtype: Dict[str, Any]:
        """
        return self.get_one_by_id(endpoint='report/my-report', record_id=report_id)
