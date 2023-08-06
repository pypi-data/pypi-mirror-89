import datetime

from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH

from enum import Enum


class ProjectRecurringExpensePeriod(str, Enum):
    """
    Enumeration for allowed values of ``period`` argument of :meth:`.ProjectRecurringExpense.create`.

    Example usage:

    .. code-block:: python

        from moco_wrapper.models.project_recurring_expense import ProjectRecurringExpensePeriod
        from moco_wrapper import Moco

        m = Moco()
        recur_expense = m.ProjectRecurringExpense.create(
            ..
            period = ProjectRecurringExpensePeriod.WEEKLY
        )

    """
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    BIANNUAL = "biannual"
    ANNUAL = "annual"


class ProjectRecurringExpense(MWRAPBase):
    """
    Class for handling recurring expenses of a project.

    An example for this would be when a third part subscription (repeat cost) is bought for a specific customer project
    and then get billed to the project to regain the cost.

    .. seealso::
        :class:`moco_wrapper.models.ProjectExpense` for one time expenses.
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        project_id: int,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of recurring expenses for a project.

        :param project_id: Id of the project the expenses belong to
        :param sort_by: Field to sort results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type project_id: int
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of recurring expenses
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

        return self._moco.get(API_PATH["project_recurring_expense_getlist"].format(project_id=project_id),
                              params=params)

    def get(
        self,
        project_id: int,
        recurring_expense_id: int,
    ):
        """
        Retrieve a single recurring expense

        :param project_id: Id of the project the expense belongs to
        :param recurring_expense_id: iI of the recurring expense

        :type project_id: int
        :type recurring_expense_id: int

        :returns: Single recurring expense object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        return self._moco.get(API_PATH["project_recurring_expense_get"]
                              .format(project_id=project_id, recurring_expense_id=recurring_expense_id))

    def create(
        self,
        project_id: int,
        start_date: datetime.date,
        period: ProjectRecurringExpensePeriod,
        title: str,
        quantity: float,
        unit: str,
        unit_price: float,
        unit_cost: float,
        finish_date: datetime.date = None,
        description: str = None,
        billable: bool = True,
        budget_relevant: bool = False,
        custom_properties: dict = None,
    ):
        """
        Create a new recurring expense for a project.

        :param project_id: Id of the project to create the expense for
        :param start_date: Starting date of the expense
        :param period: period of the expense
        :param title: Title of the expense
        :param quantity: Quantity (how much of ``unit`` was bought?)
        :param unit: Name of the unit (What was bought for the customer/project?)
        :param unit_price: Price of the unit that will be billed to the customer/project
        :param unit_cost: Cost that we had to pay
        :param finish_date: Finish date, (if None: unlimited) (default ``None``)
        :param description: Description of the expense (default ``None``)
        :param billable: If this expense billable (default ``True``)
        :param budget_relevant: If this expense is budget relevant (default ``False``)
        :param custom_properties: Additional fields as dictionary (default ``None``)

        :type project_id: int
        :type start_date: datetime.date, str
        :type period: :class:`.ProjectRecurringExpensePeriod`, str
        :type title: str
        :type quantity: float
        :type unit: str
        :type unit_price: float
        :type unit_cost: float
        :type finish_date: datetime.date, str
        :type description: str
        :type billable: bool
        :type budget_relevant: bool
        :type custom_properties: dict

        :returns: The created recurring expense object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        data = {
            "start_date": start_date,
            "period": period,
            "title": title,
            "quantity": quantity,
            "unit": unit,
            "unit_price": unit_price,
            "unit_cost": unit_cost
        }

        for date_key in ["start_date"]:
            if isinstance(data[date_key], datetime.date):
                data[date_key] = self._convert_date_to_iso(data[date_key])

        for key, value in (
            ("finish_date", finish_date),
            ("description", description),
            ("billable", billable),
            ("budget_relevant", budget_relevant),
            ("custom_properties", custom_properties)
        ):
            if value is not None:
                if key in ["finish_date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.post(API_PATH["project_recurring_expense_create"].format(project_id=project_id), data=data)

    def update(
        self,
        project_id: int,
        recurring_expense_id: int,
        title: str = None,
        quantity: float = None,
        unit: str = None,
        unit_price: float = None,
        unit_cost: float = None,
        finish_date: datetime.date = None,
        description: str = None,
        billable: bool = None,
        budget_relevant: bool = None,
        custom_properties: dict = None,
    ):
        """
        Update an existing recurring expense.

        :param project_id: Id of the project
        :param recurring_expense_id: Id of the recurring expense to update
        :param title: Title of the expense (default ``None``)
        :param quantity: Quantity (how much of ``unit`` was bought?) (default ``None``)
        :param unit: Name of the unit (What was bought for the customer/project?) (default ``None``)
        :param unit_price: Price of the unit that will be billed to the customer/project (default ``None``)
        :param unit_cost: Cost that we had to pay (default ``None``)
        :param finish_date: Finish date, (if None: unlimited) (default ``None``)
        :param description: Description of the expense (default ``None``)
        :param billable: If this expense billable (default ``None``)
        :param budget_relevant: If this expense is budget relevant (default ``None``)
        :param custom_properties: Additional fields as dictionary (default ``None``)

        :type project_id: int
        :type recurring_expense_id: int
        :type title: str
        :type quantity: int
        :type unit: str
        :type unit_price: float
        :type unit_cost: float
        :type finish_date: datetime.date, str
        :type description: str
        :type billable: bool
        :type custom_properties: dict

        :returns: The updated recurring expense object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        data = {}
        for key, value in (
            ("title", title),
            ("quantity", quantity),
            ("unit", unit),
            ("unit_price", unit_price),
            ("unit_cost", unit_cost),
            ("finish_date", finish_date),
            ("description", description),
            ("billable", billable),
            ("budget_relevant", budget_relevant),
            ("custom_properties", custom_properties)
        ):
            if value is not None:
                if key in ["finish_date"] and isinstance(value, datetime.date):
                    data[key] = self._convert_date_to_iso(value)
                else:
                    data[key] = value

        return self._moco.put(API_PATH["project_recurring_expense_update"]
                              .format(project_id=project_id, recurring_expense_id=recurring_expense_id), data=data)

    def delete(
        self,
        project_id: int,
        recurring_expense_id: int,
    ):
        """
        Deletes an existing recurring expense.

        :param project_id: Project id the expense belongs to
        :param recurring_expense_id: Id of the expense to delete

        :type project_id: int
        :type recurring_expense_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """
        return self._moco.delete(API_PATH["project_recurring_expense_delete"]
                                 .format(project_id=project_id, recurring_expense_id=recurring_expense_id))
