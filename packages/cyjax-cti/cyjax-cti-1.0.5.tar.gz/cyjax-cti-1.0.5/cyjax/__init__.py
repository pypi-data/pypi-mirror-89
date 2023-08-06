from .data_leak import LeakedEmail
from .exceptions import ResponseErrorException, InvalidDateFormatException, ApiKeyNotFoundException
from .incident_report import IncidentReport
from .indicator_of_compromise import IndicatorOfCompromise
from .malicious_domain import MaliciousDomain
from .my_report import MyReport
from .paste import Paste
from .tor_exit_node import TorExitNode
from .tweet import Tweet


api_key = None
api_url = None
proxy_settings = None
verify_ssl = True
