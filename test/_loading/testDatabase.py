import unittest
from unittest.mock import patch, MagicMock

from sqlalchemy import Engine

from etlsus.loading.database import create_db_engine, insert_into_db
from config import get_database_config


class TestDatabase(unittest.TestCase):

    @patch('etlsus.loading.database.get_database_config')
    def test_create_db_engine_success(self, mock_config):
        mock_config.return_value = get_database_config(env='test')

        engine = create_db_engine()

        self.assertIsInstance(engine, Engine)
        self.assertIn(
            "postgresql+psycopg2://test_user:***"
            "@localhost:12345/test_db",
            str(engine)
        )

    def test_insert_into_db_calls_to_sql(self):
        mock_conn = MagicMock()
        mock_df = MagicMock()
        mock_df.to_sql = MagicMock()

        insert_into_db(mock_conn, mock_df, "test_table", if_exists="append",
                       index=False)

        mock_df.to_sql.assert_called_once_with(
            "test_table",
            con=mock_conn,
            if_exists="append",
            index=False
        )


if __name__ == '__main__':
    unittest.main()
