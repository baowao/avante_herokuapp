# common_functions imports
from common.common_functions import (create_valid_account,
                                     get_error_explanation, get_h1,
                                     get_h2_label, invalid_email,
                                     invalid_password, set_email_field,
                                     set_log_in_button, set_log_in_link,
                                     set_password_field, set_sign_up_link,
                                     test_print, VerifyCommonErrorMsg,
                                     wait_click_url)
# sst imports
from sst.actions import get_current_url, go_back, go_to, stop
# python imports
import unittest

#===============================================================================
# setters
#===============================================================================
def set_forgot_your_password():
    wait_click_url(ps='clicking the "Forgot your password?" link', text='Forgot your password?')

def set_forgot_your_password_send_password_button():
    wait_click_url(ps='clicking the "Send me reset password instructions" link', value="Send me reset password instructions")

#===============================================================================
# tests
#===============================================================================
class SignIn(VerifyCommonErrorMsg, unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.chk_url = 'https://avant-qa-screening.herokuapp.com/users/sign_in'
        go_to(self.chk_url)
        set_sign_up_link()
        self.valid_email, self.valid_pw = create_valid_account()
        stop()

    def setUp(self):
        go_to(self.chk_url)

    def test_valid_email_valid_pw(self):
        set_email_field(self.valid_email)
        set_password_field(self.valid_pw)
        set_log_in_button()
        expected = 'https://avant-qa-screening.herokuapp.com/dashboard'
        actual = get_current_url()
        self.assertEqual(expected, actual,
                         msg='FAILED: url expected after login = {0}, got url = {1}'.format(expected, actual))
        test_print('Successfully verified login', flash='!')

    def test_forgot_password_verify_label(self):
        set_forgot_your_password()
        expected = 'Forgot your password?'
        actual = get_h2_label()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected label = "{0}", got = "{1}"'.format(expected, actual))
        test_print('Successfully verified label = "{0}"'.format(actual), flash='!')

    def test_forgot_password_login_link(self):
        set_forgot_your_password()
        set_log_in_link()
        expected_login_url = 'https://avant-qa-screening.herokuapp.com/users/sign_in'
        actual_url = get_current_url()
        self.assertEqual(expected_login_url, actual_url,
                     msg='FAILED: expected login url = {0}, got url = {1}'.format(expected_login_url, actual_url))
        test_print('Successfully verified the "log in" link', flash='!')
        go_back() # cleanup step

    def test_forgot_password_sign_up_link(self):
        set_forgot_your_password()
        set_sign_up_link()
        expected_signup_url ='https://avant-qa-screening.herokuapp.com/users/sign_up'
        actual_url = get_current_url()
        self.assertEqual(expected_signup_url, actual_url,
                     msg='FAILED: expected login url = {0}, got url = {1}'.format(expected_signup_url, actual_url))
        test_print('Successfully verified the "Sign up" link', flash='!')
        go_back()

    def test_valid_email_forgot_password_send_password_button(self):
        set_forgot_your_password()
        set_email_field(self.valid_email)
        set_forgot_your_password_send_password_button()
        actual = get_h1()
        error_dialog = "We're sorry, but something went wrong."
        if actual == error_dialog:
            raise ValueError('ERROR: clicking the "Send me reset password instructions" button opens up an error page!')
        # not sure what the expected behavior is here, so skipping further
        # verification

    def test_blank_email_forgot_password_send_password_button(self):
        set_forgot_your_password()
        set_forgot_your_password_send_password_button()
        expected = "1 error prohibited this user from being saved:\nEmail can't be blank"
        self.verify_error_explanation(expected)

    def test_invalid_email_forgot_password_send_password_button(self):
        set_forgot_your_password()
        url = get_current_url()
        set_email_field(invalid_email())
        actual = get_error_explanation(False)
        self.verify_sign_up_label()
        self.assertFalse(actual,
                         msg='FAILED: expected no error explanation, but got error explanation = "{0}" on url = {1}'.format(actual, get_current_url()))
        test_print('Successfully verified no error explanation'.format(actual), flash='!')
        self.assertEqual(url, get_current_url(),
                         msg='FAILED: expected url = {0}, got url = {1}'.format(url, get_current_url()))
        test_print('Successfully verified login was unsuccessful, user is still on the sign_up page', flash='!')

    def test_remember_me(self):
        self.skipTest('See manual test in test plan!')

    #===========================================================================
    # valid email
    #===========================================================================
    def test_valid_email_invalid_pw(self):
        set_email_field(self.valid_email)
        set_password_field(invalid_password())
        set_log_in_button()
        self.verify_invalid_sign_in()

    def test_valid_email_blank_pw(self):
        set_email_field(self.valid_email)
        set_log_in_button()
        self.verify_invalid_sign_in()

    #===========================================================================
    # invalid email
    #===========================================================================
    def test_invalid_email_valid_pw(self):
        set_email_field(invalid_email())
        set_password_field(self.valid_pw)
        set_log_in_button()
        self.verify_invalid_sign_in()

    def test_invalid_email_invalid_pw(self):
        set_email_field(invalid_email())
        set_password_field(invalid_password())
        set_log_in_button()
        self.verify_invalid_sign_in()

    def test_invalid_email_blank_pw(self):
        set_email_field(invalid_email())
        set_log_in_button()
        self.verify_invalid_sign_in()

    #===========================================================================
    # blank email
    #===========================================================================
    def test_blank_email_valid_pw(self):
        set_password_field(self.valid_pw)
        set_log_in_button()
        self.verify_invalid_sign_in()

    def test_blank_email_invalid_pw(self):
        set_password_field(invalid_password())
        set_log_in_button()
        self.verify_invalid_sign_in()

    def test_blank_email_blank_pw(self):
        set_log_in_button()
        self.verify_invalid_sign_in()

    #===========================================================================
    # module common functions
    #===========================================================================
    def verify_log_in_label(self):
        expected = 'Log in'
        actual = get_h2_label()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected h2 = "{0}", got h2 = "{1}" on url = {2}'.format(expected, actual, get_current_url()))
        test_print('Successfully verified h2 = "{0}"'.format(actual), flash='!')

    def verify_invalid_sign_in(self):
        self.verify_log_in_label()
        self.assertEqual(self.chk_url, get_current_url(),
                         msg='FAILED: expected url = {0}, got url = {1}'.format(self.chk_url, get_current_url()))
        test_print('Successfully verified login was unsuccessful, user is still on the sign_in page', flash='!')

    def verify_sign_up_label(self):
        expected = 'Forgot your password?'
        actual = get_h2_label()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected h2 = "{0}", got h2 = "{1}" on url = {2}'.format(expected, actual, get_current_url()))
        test_print('Successfully verified h2 = "{0}"'.format(actual), flash='!')

if __name__ == "__main__":

    unittest.main()