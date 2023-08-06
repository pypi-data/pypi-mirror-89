from .helpers import DateHelper
from .resource import Resource


class TorExitNode(Resource):

    def __init__(self, api_key=None, api_url=None):
        """
        :param api_key: The API key.
        :param api_url: The Cyjax API url.
        """
        super(TorExitNode, self).__init__(api_key=api_key, api_url=api_url)

    def list(self, query=None, since=None, until=None):
        """
        Returns TOR exit nodes.
        :param query: The search query.
        :type query: str, optional
        :param since: The start date time.
        :type since: (datetime, timedelta, str), optional
        :param until: The end date time.
        :type until:  (datetime, timedelta, str), optional
        :return: The list of TOR exit nodes.
        :rtype list
        """

        params = DateHelper.build_date_params(since=since, until=until)
        if query:
            params.update({'query': query})

        return self.paginate(endpoint='blacklists/tor-node', params=params)

    def one(self, record_id):
        """
        Get one record by ID

        :param record_id: The record ID
        :type record_id: int, str

        :return: The record dictionary, raises exception if record not found
        :rtype: Dict[str, Any]:
        """
        return self.get_one_by_id(endpoint='blacklists/tor-node', record_id=record_id)
