from moco_wrapper.const import API_PATH
from moco_wrapper import models, util, exceptions
from moco_wrapper.util import requestor, objector, response

from requests import get, post, put, delete


class Moco(object):
    """
    Main Moco class for handling authentication, object conversion, requesting ressources with the moco api

    :param auth: Dictionary containing authentication information, see :ref:`authentication`
    :param objector: objector object (see :ref:`objector`, default: :class:`moco_wrapper.util.objector.DefaultObjector`)
    :param requestor: requestor object (see :ref:`requestor`, default: :class:`moco_wrapper.util.requestor.DefaultRequestor`)
    :param impersonate_user_id: user id the client should impersonate (default: None, see https://github.com/hundertzehn/mocoapp-api-docs#impersonation)

    :type auth: dict
    :type impersonate_user_id: int

    .. code-block:: python

        import moco_wrapper
        moco = moco_wrapper.Moco(
            auth = {
                "api_key": "<TOKEN>",
                "domain": "<DOMAIN>"
            }
        )
    """

    def __init__(
        self,
        auth={},
        objector=objector.DefaultObjector(),
        requestor=requestor.DefaultRequestor(),
        impersonate_user_id: int = None,
        **kwargs):

        self.auth = auth
        """
        Authentication information

        It either contains an api key and and domain

        .. code-block:: python

            from moco_wrapper import Moco

            m = Moco(
                auth={"api_key": "here is my key", "domain": "testdomain"}
            )

        Or it contains domain, email and password

        .. code-block:: python

            from moco_wrapper import Moco

            m = Moco(
                auth={"domain": "testdomain", "email": "testemail@mycompany.com", "password": "test"}
            )

        """

        self.Activity = models.Activity(self)
        self.Contact = models.Contact(self)
        self.Company = models.Company(self)
        self.Comment = models.Comment(self)
        self.Unit = models.Unit(self)

        self.User = models.User(self)
        self.UserPresence = models.UserPresence(self)
        self.UserHoliday = models.UserHoliday(self)
        self.UserEmployment = models.UserEmployment(self)

        self.Schedule = models.Schedule(self)  # old way for handling planning + absenses
        self.PlanningEntry = models.PlanningEntry(self)  # new way for handling planning

        self.Project = models.Project(self)
        self.ProjectContract = models.ProjectContract(self)
        self.ProjectExpense = models.ProjectExpense(self)
        self.ProjectTask = models.ProjectTask(self)
        self.ProjectRecurringExpense = models.ProjectRecurringExpense(self)
        self.ProjectPaymentSchedule = models.ProjectPaymentSchedule(self)

        self.Deal = models.Deal(self)
        self.DealCategory = models.DealCategory(self)

        self.Invoice = models.Invoice(self)
        self.InvoicePayment = models.InvoicePayment(self)
        self.Offer = models.Offer(self)

        self.Session = models.Session(self)

        self.PurchaseCategory = models.PurchaseCategory(self)
        self.Purchase = models.Purchase(self)

        self.HourlyRate = models.HourlyRate(self)
        self.Tagging = models.Tagging(self)

        self._requestor = requestor
        self._objector = objector

        # set default values if not already set
        if self._requestor is None:
            self._requestor = util.requestor.DefaultRequestor()

        if self._objector is None:
            self._objector = util.objector.DefaultObjector()

        self._impersonation_user_id = impersonate_user_id

        # these will be (re)set on the first request
        self.api_key = None
        self.domain = None

        if "api_key" in self.auth.keys():
            self.api_key = self.auth["api_key"]

        if "domain" in self.auth.keys():
            self.domain = self.auth["domain"]

    def request(
        self,
        method: str,
        path: str,
        params: dict = None,
        data: dict = None,
        bypass_auth: bool = False,
        **kwargs
    ):
        """
        Requests the given resource with the assigned requestor

        :param method: HTTP Method (eg. POST, GET, PUT, DELETE)
        :param path: path of the resource (e.g. ``/projects``)
        :param params: url parameters (e.g. ``page=1``, query parameters)
        :param data: dictionary with data (http body)
        :param bypass_auth: If authentication checks should be skipped (default False)

        The request will be given to the currently assigned requestor (see :ref:`requestor`).
        The response will then be given to the currently assigned objector (see :ref:`objector`)

        The *possibly* modified response will then be returned
        """

        full_path = self.full_domain + path
        requestor_response = None

        if not bypass_auth:
            self.authenticate()

        # merge headers if set in model
        headers = self.headers
        if "headers" in kwargs.keys():
            for key, value in kwargs["headers"].items():
                headers[key] = value

            del kwargs["headers"]

        # pass request making to the requestor object
        if method == "GET":
            requestor_response = self._requestor.get(full_path, params=params, data=data, headers=headers, **kwargs)
        elif method == "PUT":
            requestor_response = self._requestor.put(full_path, params=params, data=data, headers=headers, **kwargs)
        elif method == "POST":
            requestor_response = self._requestor.post(full_path, params=params, data=data, headers=headers, **kwargs)
        elif method == "DELETE":
            requestor_response = self._requestor.delete(full_path, params=params, data=data, headers=headers, **kwargs)
        elif method == "PATCH":
            requestor_response = self._requestor.patch(full_path, params=params, data=data, headers=headers, **kwargs)

        # push the response to the current objector
        objector_result = self._objector.convert(requestor_response)

        # if the result is an exception we raise it, otherwise return it
        if isinstance(objector_result, response.ErrorResponse) and isinstance(objector_result.data,
                                                                              exceptions.MocoException):
            raise objector_result.data

        # return the objector result by default
        return objector_result

    def get(self, path, params=None, data=None, **kwargs):
        """
        Helper function for GET requests
        """
        return self.request("GET", path, params=params, data=data, **kwargs)

    def post(self, path, params=None, data=None, **kwargs):
        """
        Helper function for POST requests
        """
        return self.request("POST", path, params=params, data=data, **kwargs)

    def put(self, path, params=None, data=None, **kwargs):
        """
        Helper function for PUT requests
        """
        return self.request("PUT", path, params=params, data=data, **kwargs)

    def delete(self, path, params=None, data=None, **kwargs):
        """
        Helper function for DELETE requests
        """
        return self.request("DELETE", path, params=params, data=data, **kwargs)

    def patch(self, path, params=None, data=None, **kwargs):
        """
        Helper function for PATCH requests
        """
        return self.request("PATCH", path, params=params, data=data, **kwargs)

    def impersonate(
        self,
        user_id: int
    ):
        """
        Impersonates the user with the supplied user id

        :param user_id: user id to impersonate

        .. seealso::

            :meth:`clear_impersonation` to end impersonation of ``user_id``

        """
        self._impersonation_user_id = user_id

    def clear_impersonation(self):
        """
        Ends impersonation

        .. seealso::

            :meth:`impersonate`

        """
        self._impersonation_user_id = None

    @property
    def headers(self):
        """
        Returns all http headers to be used by the assigned requestor
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Token token={}'.format(self.api_key)
        }

        if self._impersonation_user_id is not None:
            headers["X-IMPERSONATE-USER-ID"] = str(self._impersonation_user_id)

        return headers

    @property
    def full_domain(self) -> str:
        """
        Returns the full url of the moco api

        .. code-block:: python

            >> m = Moco(auth={"domain": "testabcd", ..})
            >> print(m.full_domain)
            https://testabcd.mocoapp.com/api/v1

        """
        return "https://{}.mocoapp.com/api/v1".format(self.domain)

    @property
    def session(self):
        """
        Get the http.session object of the current requestor (None if the requestor does not have a session)
        """
        return self._requestor.session

    @property
    def objector(self):
        """
        Get the currently assigned objector object

        .. seealso::

            :ref:`objector`
        """
        return self._objector

    @property
    def requestor(self):
        """
        Get the currently assigned requestor object

        .. seealso::

            :ref:`requestor`
        """
        return self._requestor

    def authenticate(self):
        """
        Performs any action necessary to be authenticated against the moco api.

        This method gets invoked automatically, on the very first request you send against the api.
        """
        if self.api_key is not None and self.domain is not None:
            return  # already authenticated

        if all(x in self.auth.keys() for x in ['api_key', 'domain']):
            # authentication with api key
            self.api_key = self.auth["api_key"]
            self.domain = self.auth["domain"]
            del self.auth
        elif all(x in self.auth.keys() for x in ['domain', 'email', 'password']):
            # authentication with username/password
            self.domain = self.auth["domain"]

            email, password = self.auth["email"], self.auth["password"]
            session = self.Session.authenticate(email, password).data

            self.api_key = session.api_key
            del self.auth
        else:
            # raise error authentication information is very likely invalid
            raise ValueError("Invalid authentication information given")
