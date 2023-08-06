from moco_wrapper.models.base import MWRAPBase
from moco_wrapper.const import API_PATH


class UserHoliday(MWRAPBase):
    """
    Class for handling users holiday/vacation credits.

    Every user that can take vacation has a number of vacation credits. These can be manged with this model.

    Example usage:

    .. code-block:: python

        from moco_wrapper import Moco

        m = Moco()

        # this user gets extra vacation in 2020
        m.UserHoliday.create(
            year = 2020,
            title = "extra vacation day",
            user_id = 22,
            hours = 8
        )

    .. note::
        Please not that the base unit for holiday credits is hours. So if your typical workday contains 8 hours,
        8 holiday credits means one day off.
    """

    def __init__(self, moco):
        """
        Class Constructor

        :param moco: An instance of :class:`moco_wrapper.Moco`
        """
        self._moco = moco

    def getlist(
        self,
        year: int = None,
        user_id: int = None,
        sort_by: str = None,
        sort_order: str = 'asc',
        page: int = 1
    ):
        """
        Retrieve a list of holiday entries.

        :param year: Show only this year (e.g. 2019) (default ``None``)
        :param user_id: Show only holidays from this user (e.g. 5) (default ``None``)
        :param sort_by: field to sort results by (default ``None``)
        :param sort_order: asc or desc (default ``"asc"``)
        :param page: Page number (default ``1``)

        :type year: int
        :type user_id: int
        :type sort_by: str
        :type sort_order: str
        :type page: int

        :returns: List of holiday entries
        :rtype: :class:`moco_wrapper.util.response.PagedListResponse`
        """
        params = {}
        for key, value in (
            ("year", year),
            ("user_id", user_id),
            ("page", page)
        ):
            if value is not None:
                params[key] = value

        if sort_by is not None:
            params["sort_by"] = "{} {}".format(sort_by, sort_order)

        return self._moco.get(API_PATH["holiday_getlist"], params=params)

    def get(
        self,
        holiday_id: int
    ):
        """
        Retrieve single holiday entry

        :param holiday_id: Id of the holiday

        :type holiday_id: int

        :returns: The holiday object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """
        return self._moco.get(API_PATH["holiday_get"].format(id=holiday_id))

    def create(
        self,
        year: int,
        title: str,
        user_id: int,
        hours: float = None,
        days: float = None,
    ):
        """
        Create an users entitlement for holidays/vacation (either by hours or days).

        :param year: Year the holiday credits are for
        :param title: Title
        :param user_id: Id of the user these holiday credits belongs to
        :param hours: Hours (specify either hours or days) (default ``None``)
        :param days: Days (specify either hours or days) (default ``None``)

        :type year: int
        :type title: str
        :type user_id: int
        :type hours: float
        :type days: float

        :returns: The created holiday object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        if days is None and hours is None:
            raise ValueError("Either the hours or days parameter must be specified")

        if days is not None and hours is not None:
            raise ValueError("Specify either hours or the days parameter (not both)")

        data = {
            "year": year,
            "title": title,
            "user_id": user_id,
        }

        for key, value in (
            ("days", days),
            ("hours", hours)
        ):
            if value is not None:
                data[key] = value

        return self._moco.post(API_PATH["holiday_create"], data=data)

    def update(
        self,
        holiday_id: int,
        year: int = None,
        title: str = None,
        user_id: int = None,
        hours: float = None,
        days: float = None,
    ):
        """
        Update a holiday entry

        :param holiday_id: Id of the holiday entry
        :param year:  Year the holiday credits are for (default ``None``)
        :param title: Title (default ``None``)
        :param user_id: User this holiday entry belongs to (default ``None``)
        :param hours: Hours (specify either hours or days) (default ``None``)
        :param days: Days (specify either hours or days) (default ``None``)

        :type holiday_id: int
        :type year: int
        :type title: str
        :type user_id: int
        :type hours: float
        :type days: float

        :returns: The updated holiday object
        :rtype: :class:`moco_wrapper.util.response.ObjectResponse`
        """

        if days is None and hours is None:
            raise ValueError("Either the hours or days parameter must be specified")

        if days is not None and hours is not None:
            raise ValueError("Specify either hours or the days parameter (not both)")

        data = {}
        for key, value in (
            ("year", year),
            ("title", title),
            ("hours", hours),
            ("days", days),
            ("user_id", user_id)
        ):
            if value is not None:
                data[key] = value

        return self._moco.put(API_PATH["holiday_update"].format(id=holiday_id), data=data)

    def delete(
        self,
        holiday_id: int
    ):
        """
        Delete a holiday entry

        :param holiday_id: Id of the holiday entry to delete

        :type holiday_id: int

        :returns: Empty response on success
        :rtype: :class:`moco_wrapper.util.response.EmptyResponse`
        """
        return self._moco.delete(API_PATH["holiday_delete"].format(id=holiday_id))
