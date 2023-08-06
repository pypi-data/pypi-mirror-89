import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH


class ProjectExpense(MWRAPBase):
    """
    Class for handling additional project expenses.

    An example for this would be when a third part product (one time cost) is bought for a specific customer project
    and then get billed to the project to regain the cost.

    .. seealso::

        :class:`moco_wrapper.models.ProjectRecurringExpense` for repeating expenses.
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def create(
        self,
        project_id: int,
        expense_date: datetime.date,
        title: str,
        quantity: float,
        unit: str,
        unit_price: float,
        unit_cost: float,
        description: str = None,
        billable: bool = True,
        budget_relevant: bool = False,
        custom_properties: dict = None
    ):
        """
        Create a project expense.

        :param project_id: Id of the project to create the expense for
        :param expense_date: Date of the expense
        :param title: Expense title
        :param quantity: Quantity (how much of ``unit`` was bought?)
        :param unit: Name of the unit (What was bought for the customer/project?)
        :param unit_price: Price of the unit that will be billed to the customer/project
        :param unit_cost: Cost that we had to pay
        :param description: Description of the expense (default ``None``)
        :param billable: If this expense billable (default ``True``)
        :param budget_relevant: If this expense is budget relevant (default ``False``)
        :param custom_properties: Additional fields as dictionary (default ``None``)

        :type project_id: int
        :type expense_date: datetime.date, str
        :type title: str
        :type quantity: float
        :type unit: str
        :type unit_price: float
        :type unit_cost: float
        :type description: str
        :type billable: bool
        :type budget_relevant: bool
        :type custom_properties: dict

        :returns: The created expense object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        data = {
            "date": expense_date,
            "title": title,
            "quantity": quantity,
            "unit": unit,
            "unit_price": unit_price,
            "unit_cost": unit_cost,
        }

        if isinstance(expense_date, datetime.date):
            data["date"] = self._convert_date_to_iso(expense_date)

        for key, value in (
            ("description", description),
            ("billable", billable),
            ("budget_relevant", budget_relevant),
            ("custom_properties", custom_properties),
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["project_expense_create"].format(project_id=project_id), data=data)

    def create_bulk(
        self,
        project_id: int,
        items: list,
    ):
        """
        Create multiple expenses for a project.

        :param project_id: Id of the project to created the expenses for
        :param items: Items to create bulk

        :type project_id: int
        :type items: list

        :returns: The created entries
        :rtype: :class:`moco_wrapper.util.response.ListResponse`

        .. seealso::
            :class:`moco_wrapper.util.generator.ProjectExpenseGenerator`
        """

        data = {
            "bulk_data": items
        }

        return self._moco.post(API_PATH["project_expense_create_bulk"].format(project_id=project_id), data=data)

    def update(
        self,
        project_id: int,
        expense_id: int,
        expense_date: datetime.date = None,
        title: str = None,
        quantity: float = None,
        unit: str = None,
        unit_price: float = None,
        unit_cost: float = None,
        description: str = None,
        billable: bool = None,
        budget_relevant: bool = None,
        custom_properties: dict = None
    ):
        """
        Update an existing project expense.

        :param project_id: Id of the project
        :param expense_id: id of the expense we want to update
        :param expense_date: Date of the expense (default ``None``)
        :param title: Expense title (default ``None``)
        :param quantity: Quantity (how much of ``unit`` was bought?) (default ``None``)
        :param unit: Name of the unit (What was bought for the customer/project?) (default ``None``)
        :param unit_price: Price of the unit that will be billed to the customer/project (default ``None``)
        :param unit_cost: Cost that we had to pay (default ``None``)
        :param description: Description of the expense (default ``None``)
        :param billable: If this expense billable (default ``None``)
        :param budget_relevant: If this expense is budget relevant (default ``None``)
        :param custom_properties: Additional fields as dictionary (default ``None``)

        :type project_id: int
        :type expense_id: int
        :type expense_date: datetime.date, str
        :type title: str
        :type quantity: float
        :type unit: str
        :type unit_price: float
        :type unit_cost: float
        :type description: str
        :type billable: bool
        :type budget_relevant: bool
        :type custom_properties: dict

        :returns: The updated expense object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        data = {}
        for key, value in (
            ("date", expense_date),
            ("title", title),
            ("quantity", quantity),
            ("unit", unit),
            ("unit_price", unit_price),
            ("unit_cost", unit_cost),
            ("description", description),
            ("billable", billable),
            ("budget_relevant", budget_relevant),
            ("custom_properties", custom_properties)
        ):
            if value is not None:
                if key in ["date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put(API_PATH["project_expense_update"].format(project_id=project_id, expense_id=expense_id),
                              data=data)

    def delete(
        self,
        project_id: int,
        expense_id: int
    ):
        """
        Deletes an expense.

        :param project_id: Id of the project the expense belongs to
        :param expense_id: Id of the expense to delete

        :type project_id: int
        :type expense_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """

        return self._moco.delete(
            API_PATH["project_expense_delete"].format(project_id=project_id, expense_id=expense_id))

    def disregard(
        self,
        project_id: int,
        expense_ids: list,
        reason: str
    ):
        """
        Disregard expenses

        :param project_id: Id of the project
        :param expense_ids: Array of expense ids to disregard
        :param reason: Reason for disregarding the expenses

        :type project_id: int
        :type expense_ids: list
        :type reason: str

        :returns: List of disregarded expense ids
        :rtype: :class:`moco_wrapper.util.response.ListResponse`

        Example usage:

        .. code-block:: python

            from moco_wrapper import Moco

            m = Moco()

            m.ProjectExpense.disregard(
                project_id=22,
                expense_ids=[444, 522, 893],
                reason="Expenses already billed"
            )
        """

        data = {
            "expense_ids": expense_ids,
            "reason": reason
        }

        return self._moco.post(API_PATH["project_expense_disregard"].format(project_id=project_id), data=data)

    def getall(
        self,
        from_date: datetime.date = None,
        to_date: datetime.date = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Get a list of all expenses.

        :param from_date: Start date (default ``None``)
        :param to_date: End date (default ``None``)
        :param sort_by: Sort results by field (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type from_date: datetime.date, str
        :type to_date: datetime.date, str
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of expense objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """

        params = {}
        for key, value in (
            ("from", from_date),
            ("to", to_date),
            ("page", page),
        ):
            if value is not None:
                if key in ["from_date", "to_date"] and isinstance(value, datetime.date):
                    params[key] = self._convert_date_to_iso(value)
                else:
                    params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["project_expense_getall"], params=params)

    def get(
        self,
        project_id: int,
        expense_id: int
    ):
        """
        Retrieve a single expense object.

        :param project_id: Id of the project
        :param expense_id: If of the expense to retrieve

        :type project_id: int
        :type expense_id: int

        :returns: Single expense object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        return self._moco.get(API_PATH["project_expense_get"].format(project_id=project_id, expense_id=expense_id))

    def getlist(
        self,
        project_id: int,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve all expenses of a project.

        :param project_id: Id of the project
        :param sort_by: Sort results by field (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type project_id: int
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of expense objects
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """

        params = {}

        for key, value in (
            ("page", page),
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["project_expense_getlist"].format(project_id=project_id), params=params)
