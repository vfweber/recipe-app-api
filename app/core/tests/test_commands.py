from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class TestCommands(SimpleTestCase):

    def test_wait_for_db_ready(self, mock_check):
        mock_check.return_value = True
        call_command('wait_for_db')
        mock_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self,  mock_sleep, mock_check):
        mock_check.side_effect = ([Psycopg2Error] * 2 +
                                  [OperationalError] * 3 + [True])
        call_command('wait_for_db')

        self.assertEqual(mock_check.call_count, 6)
        mock_check.assert_called_with(databases=['default'])
