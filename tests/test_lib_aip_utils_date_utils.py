import unittest
import logging
from datetime import date
from datetime import timedelta
from lib.aip.utils.date_utils import validate_and_convert_date


# Suppress logging messages below CRITICAL level
# to just get the result of the tests.
logging.disable(logging.CRITICAL)

class TestValidateAndConvertDate(unittest.TestCase):

    def test_valid_date(self):
        # Test with a valid date
        self.assertEqual(validate_and_convert_date("2024-10-27"), date(2024, 10, 27))

    def test_empty_string(self):
        # Test with an empty string
        with self.assertRaises(ValueError):
            validate_and_convert_date("")

    def test_invalid_format(self):
        # Test with various invalid formats
        with self.assertRaises(ValueError):
            validate_and_convert_date("2024/10/27")

        with self.assertRaises(ValueError):
            validate_and_convert_date("27-10-2024")

        with self.assertRaises(ValueError):
            validate_and_convert_date("October 27, 2024")

    def test_nonexistent_date(self):
        # Test not existing date Feb 30th
        with self.assertRaises(ValueError):
            validate_and_convert_date("2024-02-30")

        # Test not existing month 13
        with self.assertRaises(ValueError):
            validate_and_convert_date("2024-13-01")

    def test_none_value(self):
        # Test with None as input
        with self.assertRaises(TypeError):
            validate_and_convert_date(None)

    def test_edge_case(self):
        # Test leap years
        self.assertEqual(validate_and_convert_date("2024-02-29"), date(2024, 2, 29))

    def test_future_date(self):
        # Test future date raises exception
        future_date = (date.today() + timedelta(days=1)).isoformat()

        with self.assertRaises(ValueError):
            validate_and_convert_date(future_date)


if __name__ == '__main__':
    unittest.main()
