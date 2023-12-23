import pytest
from unittest.mock import patch
from fe.access.new_seller import register_new_seller
import uuid
import psycopg2

class TestCreateStore:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.user_id = "test_create_store_user_{}".format(str(uuid.uuid1()))
        self.store_id = "test_create_store_store_{}".format(str(uuid.uuid1()))
        self.password = self.user_id
        yield

    def test_ok(self):
        self.seller = register_new_seller(self.user_id, self.password)
        code = self.seller.create_store(self.store_id)
        assert code == 200

    # def test_database_error(self, mocker):
    #     self.seller = register_new_seller(self.user_id, self.password)

    #     mock_connect = mocker.patch('be.model.store.psycopg2.connect')
    #     mock_cursor = mock_connect.return_value.cursor.return_value
    #     mock_cursor.execute.side_effect = psycopg2.Error('Test error')

    #     code = self.seller.create_store(self.store_id)
    #     assert code == 528

    def test_error_exist_store_id(self):
        self.seller = register_new_seller(self.user_id, self.password)
        code = self.seller.create_store(self.store_id)
        assert code == 200

        code = self.seller.create_store(self.store_id)
        assert code != 200

    def test_error_authorization_fail(self):
        self.seller = register_new_seller(self.user_id, self.password)
        self.seller.token += "_x"
        code = self.seller.create_store(self.store_id)
        assert code == 401
