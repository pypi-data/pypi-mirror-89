import unittest

from client import create_presence, process_ans
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE, ERROR


class TestMyClient(unittest.TestCase):

    def test_create_presence_positive(self):
        account_name_test = "Test_Guest"
        precence_test = create_presence(account_name_test)
        precence_test[TIME] = 1.1
        self.assertEqual(precence_test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Test_Guest'}})

    def test_create_presence_negativ(self):
        account_name_test = "Test_Guest"
        precence_test = create_presence(account_name_test)
        precence_test[TIME] = 1.1
        self.assertNotEqual(precence_test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_process_ans_positive(self):
        message_test = {
            RESPONSE: 400,
            ERROR: "error"
        }
        self.assertNotEqual(process_ans(message_test), "200 : OK")

    def test_process_ans_negative(self):
        message_test = {
            RESPONSE: 200,
            ERROR: "error"
        }
        self.assertEqual(process_ans(message_test), "200 : OK")

    def test_main_process_ans_msgError(self):
        error_test_ans = process_ans({RESPONSE: 300, ERROR: "error_value"})
        self.assertEqual(error_test_ans, "400 : error_value")


if __name__ == '__main__':
    unittest.main()
