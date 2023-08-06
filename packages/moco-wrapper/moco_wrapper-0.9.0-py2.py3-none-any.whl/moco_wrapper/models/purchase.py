import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

from enum import Enum
from base64 import b64encode
from os.path import basename


class PurchaseStatus(str, Enum):
    """
    Enumeration for the allowed values that can be supplied for the ``status`` argument of
    :meth:`.Purchase.update_status`.

    Example usage:

    .. code-block:: python

        from moco_wrapper.models.purchase import PurchaseStatus
        from moco_wrapper import Moco

        m = Moco()
        m.Purchase.update_status(
            ..
            status = PurchaseStatus.APPROVED
        )
    """
    PENDING = "pending"
    APPROVED = "approved"


class PurchasePaymentMethod(str, Enum):
    """
    Enumeration for the allowed values than can be supplied for the ``payment_method`` argument of
    :meth:`.Purchase.create`.

    Example usage:

    .. code-block:: python

        from moco_wrapper.models.purchase import PurchasePaymentMethod
        from moco_wrapper import Moco

        m = Moco()
        new_purchase = m.Purchase.create(
            ..
            payment_method = PurchasePaymentMethod.CASH
        )
    """
    BANK_TRANSFER = "bank_transfer"
    DIRECT_DEBIT = "direct_debit"
    CREDIT_CARD = "credit_card"
    PAYPAL = "paypal"
    CASH = "cash"


class PurchaseFile(object):
    """
    Helper class for handling files in :meth:`.Purchase.create` and :meth:`.Purchase.store_document`.
    """

    def __init__(self, file_path, file_name=None):
        """
        Class Constructor

        :param file_path: Path to the file on disk
        :param file_name: Name of the file to be used when used by :class:`.Purchase` (default ``None``)

        :type file_path: str
        :type file_name: str

        .. node::
            When not supplying a ``file_name``, the basename of the file will be used
        """
        self.path = file_path
        self.name = file_name

        # if no name was set for the file, use the basename
        if file_name is None:
            with open(self.path, "r") as f:
                self.name = basename(f.name)

    def to_base64(self):
        """
        Converts the content of the file to its base64 representation.

        :returns: File content as base64
        :rtype: str
        """
        with open(self.path, "rb") as f:
            return b64encode(f.read()).decode("utf-8")

    @classmethod
    def load(cls, path):
        """
        Helper method to create a :class:`.PurchaseFile` object from a path.

        :returns: :class:`.PurchaseFile` object
        :rtype: :class:`.PurchaseFile`
        """
        return cls(path)


class Purchase(MWRAPBase):

    def __init__(self, moco):
        """
        Class constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        purchase_id: int = None,
        category_id: int = None,
        term: str = None,
        company_id: int = None,
        status: PurchaseStatus = None,
        tags: list = None,
        start_date: datetime.date = None,
        end_date: datetime.date = None,
        unpaid: bool = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of purchases.

        :param purchase_id: Id of the purchase (default ``None``)
        :param category_id: Id of the category the purchase belongs to  (default ``None``)
        :param term: Full text search  (default ``None``)
        :param company_id: Company id of the supplier (default ``None``)
        :param status: Status of the purchases
        :param tags: List of tags (default ``None``)
        :param start_date: Start date filter
            (if ``start_date`` is supplied, ``end_date`` must also be supplied) (default ``None``)
        :param end_date: End date filter
            (if ``end_date`` is supplied, ``start_date`` must also be supplied) (default ``None``)
        :param unpaid: Filter only purchases without a payment (default ``None``)
        :param sort_by: Field to sort results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type purchase_id: int
        :type category_id: int
        :type term: str
        :type company_id: int
        :type status: :class:`.PurchaseStatus`, str
        :type tags: list
        :type start_date: datetime.date, str
        :type end_date: datetime.date, str
        :type unpaid: bool
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of purchases
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """

        if start_date is not None and end_date is None:
            raise ValueError("If start_date is set, so must be end_date")

        if end_date is not None and start_date is None:
            raise ValueError("If end_date is set, so must be start_date")

        params = {}

        if start_date is not None and end_date is not None:
            start_date_formatted = ""
            if isinstance(start_date, datetime.date):
                start_date_formatted = self._convert_date_to_iso(start_date)
            else:
                start_date_formatted = start_date

            end_date_formatted = ""
            if isinstance(end_date, datetime.date):
                end_date_formatted = self._convert_date_to_iso(end_date)
            else:
                end_date_formatted = end_date

            params["date"] = "{}:{}".format(start_date_formatted, end_date_formatted)

        for key, value in (
            ("id", purchase_id),
            ("category_id", category_id),
            ("term", term),
            ("company_id", company_id),
            ("status", status),
            ("tags", tags),
            ("unpaid", unpaid),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["purchase_getlist"], params=params)

    def get(
        self,
        purchase_id: int
    ):
        """
        Retrieve a single purchase.

        :param purchase_id: The id of the purchase

        :type purchase_id: int

        :returns: A single purchase
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        return self._moco.get(API_PATH["purchase_get"].format(id=purchase_id))

    def create(
        self,
        purchase_date: datetime.date,
        currency: str,
        payment_method: PurchasePaymentMethod,
        items: list,
        due_date: datetime.date = None,
        service_period_from: datetime.date = None,
        service_period_to: datetime.date = None,
        company_id: int = None,
        receipt_identifier: str = None,
        info: str = None,
        iban: str = None,
        reference: str = None,
        custom_properties: dict = None,
        file: PurchaseFile = None,
        tags: list = None
    ):
        """
        Create a new purchase.

        :param purchase_date: Date of the purchase
        :param currency: Currency
        :param payment_method: Method of payment that was used
        :param items: List of items that were purchased (minimum 1 item required)
        :param due_date: Date the purchase is due (default ``None``)
        :param service_period_from: Service period start date (default ``None``)
        :param service_period_to: Service period end date (default ``None``)
        :param company_id: Id of the supplier company (default ``None``)
        :param receipt_identifier: Receipt string (default ``None``)
        :param info: Info text (default ``None``)
        :param iban: Iban  (default ``None``)
        :param reference: Reference text (default ``None``)
        :param custom_properties: Custom Properties (default ``None``)
        :param file: File attached to the purchase (default ``None``)
        :param tags: List of tags  (default ``None``)

        :type purchase_date: datetime.date, str
        :type currency: str
        :type payment_method: :class:`.PurchasePaymentMethod`, str
        :type items: List
        :type due_date: datetime.date, str
        :type service_period_from: datetime.date, str
        :type service_period_to: datetime.date, str
        :type company_id: int
        :type receipt_identifier: str
        :type info: str
        :type iban: str
        :type reference: str
        :type custom_properties: dict
        :type file: :class:`.PurchaseFile`
        :type tags: list

        :returns: The created purchase
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        data = {
            "date": purchase_date,
            "currency": currency,
            "payment_method": payment_method,
            "items": items,
        }

        if isinstance(data["date"], datetime.date):
            data["date"] = self._convert_date_to_iso(data["date"])

        for key, value in (
            ("due_date", due_date),
            ("service_period_from", service_period_from),
            ("service_period_to", service_period_to),
            ("company_id", company_id),
            ("receipt_identifier", receipt_identifier),
            ("info", info),
            ("iban", iban),
            ("reference", reference),
            ("custom_properties", custom_properties),
            ("file", file),
            ("tags", tags),
        ):
            if value is not None:
                # check if value is a date
                if key in ["due_date", "service_period_from", "service_period_to"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                elif isinstance(value, PurchaseFile):  # check if value is a file
                    data[key] = {
                        "filename": value.name,
                        "base64": value.to_base64()
                    }
                else:
                    data[key] = value

        return self._moco.post(API_PATH["purchase_create"], data=data)

    def delete(
        self,
        purchase_id: int
    ):
        """
        Deletes a purchase.

        :param purchase_id: Id of the purchase to delete

        :type purchase_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`

        .. warning::
            Deletion of a purchase is only possible if the state of the purchase is :attr:`.PurchaseStatus.PENDING`
            and no payments have been registered to the purchase yet

        """
        return self._moco.delete(API_PATH["purchase_delete"].format(id=purchase_id))

    def update_status(
        self,
        purchase_id: int,
        status: PurchaseStatus,
    ):
        """
        Updates the state of a purchase.

        :param purchase_id: Id of the purchase to update
        :param status: New status

        :type purchase_id: int
        :type status: :class:`.PurchaseStatus`, str

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """
        data = {
            "status": status
        }

        return self._moco.patch(API_PATH["purchase_update_status"].format(id=purchase_id), data=data)

    def store_document(
        self,
        purchase_id,
        file,
    ):
        """
        Stores the document for a purchase.

        :param purchase_id: Id of the purchase
        :param file: Purchase file

        :type purchase_id: int
        :type file: :class:`.PurchaseFile`

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """

        # overwrite content-type with None so content-type can be set by the requests module
        # the content-type will be multipart/form-data. For multipart/form-data a boundary parameter also has to be set
        # we cannot set this parameter at this stage, so we clear the content-type and let the content-type be
        # automatically be determined by the requests module
        # for more info see https://www.w3.org/Protocols/rfc1341/7_2_Multipart.html
        headers = {
            "Content-Type": None
        }

        files = {
            "file": (file.name, open(file.path, "rb"))
        }

        return self._moco.patch(API_PATH["purchase_store_document"].format(id=purchase_id),
                                headers=headers, data=None, files=files)
