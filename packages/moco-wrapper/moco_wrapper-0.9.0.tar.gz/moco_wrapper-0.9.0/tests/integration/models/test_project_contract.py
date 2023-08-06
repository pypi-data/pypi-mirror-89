from moco_wrapper.util.response import ObjectResponse, PagedListResponse, EmptyResponse
from moco_wrapper.models.company import CompanyType

import string
import random

from datetime import date
from .. import IntegrationTest


class TestProjectContract(IntegrationTest):
    def get_unit(self):
        with self.recorder.use_cassette("TestProjectContract.get_unit"):
            unit = self.moco.Unit.getlist().items[0]
            return unit

    def get_customer(self):
        with self.recorder.use_cassette("TestProjectContract.get_customer"):
            customer_create = self.moco.Company.create(
                name="TestProjectContract.get_customer",
                company_type=CompanyType.CUSTOMER
            )

            return customer_create.data

    def get_user(self):
        with self.recorder.use_cassette("TestProjectContract.get_user"):
            user = self.moco.User.getlist().items[0]
            return user

    def get_other_user(self):
        unit = self.get_unit()

        with self.recorder.use_cassette("TestProjectContract.get_other_user"):
            user_create = self.moco.User.create(
                firstname="-",
                lastname="TestProjectContract.get_other_user",
                email="{}@example.org".format(self.id_generator()),
                password=self.id_generator(),
                unit_id=unit.id,
                active=True,
            )

            return user_create.data

    def test_getlist(self):
        user = self.get_user()
        customer = self.get_customer()

        with self.recorder.use_cassette("TestProjectContract.test_getlist"):
            project_create = self.moco.Project.create(
                name="TestProjectContract.test_getlist_project_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            contract_list = self.moco.ProjectContract.getlist(
                project_id=project_create.data.id
            )

            assert project_create.response.status_code == 200
            assert contract_list.response.status_code == 200

            assert type(contract_list) is PagedListResponse

            assert contract_list.current_page == 1
            assert contract_list.is_last is not None
            assert contract_list.next_page is not None
            assert contract_list.total is not None
            assert contract_list.page_size is not None

    def test_create(self):
        user = self.get_user()
        customer = self.get_customer()
        other_user = self.get_other_user()  # created user for assigning to project

        with self.recorder.use_cassette("TestProjectContract.test_create"):
            project_create = self.moco.Project.create(
                name="TestProjectContract.test_create_project_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            billable = False
            active = True
            budget = 9900
            hourly_rate = 100

            contract_create = self.moco.ProjectContract.create(
                project_id=project_create.data.id,
                user_id=other_user.id,
                billable=billable,
                active=active,
                budget=budget,
                hourly_rate=hourly_rate
            )

            assert project_create.response.status_code == 200
            assert contract_create.response.status_code == 200

            assert type(project_create) is ObjectResponse
            assert type(contract_create) is ObjectResponse

            assert contract_create.data.firstname == other_user.firstname
            assert contract_create.data.lastname == other_user.lastname
            assert contract_create.data.billable == billable
            assert contract_create.data.budget == budget
            assert contract_create.data.user_id == other_user.id
            assert contract_create.data.hourly_rate == hourly_rate
            assert contract_create.data.active == active

    def test_get(self):
        user = self.get_user()
        customer = self.get_customer()
        other_user = self.get_other_user()  # created user for assigning to project

        with self.recorder.use_cassette("TestProjectContract.test_get"):
            project_create = self.moco.Project.create(
                name="TestProjectContract.test_get_project_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            billable = False
            active = True
            budget = 9900
            hourly_rate = 100

            contract_create = self.moco.ProjectContract.create(
                project_id=project_create.data.id,
                user_id=other_user.id,
                billable=billable,
                active=active,
                budget=budget,
                hourly_rate=hourly_rate
            )

            contract_get = self.moco.ProjectContract.get(
                project_id=project_create.data.id,
                contract_id=contract_create.data.id
            )

            assert project_create.response.status_code == 200
            assert contract_create.response.status_code == 200
            assert contract_get.response.status_code == 200

            assert type(project_create) is ObjectResponse
            assert type(contract_create) is ObjectResponse
            assert type(contract_get) is ObjectResponse

            assert contract_get.data.firstname == other_user.firstname
            assert contract_get.data.lastname == other_user.lastname
            assert contract_get.data.billable == billable
            assert contract_get.data.budget == budget
            assert contract_get.data.user_id == other_user.id
            assert contract_get.data.hourly_rate == hourly_rate
            assert contract_get.data.active == active

    def test_update(self):
        user = self.get_user()
        customer = self.get_customer()
        other_user = self.get_other_user()  # created user for assigning to project

        with self.recorder.use_cassette("TestProjectContract.test_update"):
            project_create = self.moco.Project.create(
                name="TestProjectContract.test_update_project_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            billable = False
            active = True
            budget = 9900.5
            hourly_rate = 100.2

            contract_create = self.moco.ProjectContract.create(
                project_id=project_create.data.id,
                user_id=other_user.id,
                billable=True,
                budget=1,
                hourly_rate=2,
            )

            contract_update = self.moco.ProjectContract.update(
                project_id=project_create.data.id,
                contract_id=contract_create.data.id,
                billable=billable,
                active=active,
                budget=budget,
                hourly_rate=hourly_rate
            )

            assert project_create.response.status_code == 200
            assert contract_create.response.status_code == 200
            assert contract_update.response.status_code == 200

            assert type(project_create) is ObjectResponse
            assert type(contract_create) is ObjectResponse
            assert type(contract_update) is ObjectResponse

            assert contract_update.data.firstname == other_user.firstname
            assert contract_update.data.lastname == other_user.lastname
            assert contract_update.data.billable == billable
            assert contract_update.data.budget == budget
            assert contract_update.data.user_id == other_user.id
            assert contract_update.data.hourly_rate == hourly_rate
            assert contract_update.data.active == active

    def test_delete(self):
        user = self.get_user()
        customer = self.get_customer()
        other_user = self.get_other_user()  # created user for assigning to project

        with self.recorder.use_cassette("TestProjectContract.test_delete"):
            project_create = self.moco.Project.create(
                name="TestProjectContract.test_delete_project_create",
                currency="EUR",
                leader_id=user.id,
                customer_id=customer.id,
                finish_date=date(2020, 1, 1),
            )

            billable = False
            active = True
            budget = 9900
            hourly_rate = 100

            contract_create = self.moco.ProjectContract.create(
                project_id=project_create.data.id,
                user_id=other_user.id,
                billable=billable,
                active=active,
                budget=budget,
                hourly_rate=hourly_rate
            )

            contract_delete = self.moco.ProjectContract.delete(
                project_id=project_create.data.id,
                contract_id=contract_create.data.id
            )

            assert project_create.response.status_code == 200
            assert contract_create.response.status_code == 200
            assert contract_delete.response.status_code == 204

            assert type(project_create) is ObjectResponse
            assert type(contract_create) is ObjectResponse
            assert type(contract_delete) is EmptyResponse
