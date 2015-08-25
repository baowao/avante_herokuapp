# common_functions imports
from common.common_functions import (create_valid_account, fake_valid_email,
                                     get_error_explanation, invalid_email,
                                     invalid_password, set_email_field,
                                     set_password_confirmation_field,
                                     set_password_field, set_log_in_link,
                                     set_sign_up_button, test_print,
                                     VerifyCommonErrorMsg, valid_password)
# sst imports
from sst.actions import get_current_url, go_to, stop
# python imports
import unittest

#===============================================================================
# tests
#===============================================================================
class SignUp(VerifyCommonErrorMsg, unittest.TestCase):
    def setUp(self):
        # open the sign_up page directly
        self.chk_url = 'https://avant-qa-screening.herokuapp.com/users/sign_up'
        go_to(self.chk_url)

    def test_sign_up_label(self):
        self.verify_sign_up_label()

    def test_existing_user(self):
        email, pw = create_valid_account()
        stop() # cleanup step
        go_to(self.chk_url)
        set_email_field(email)
        set_password_field(pw)
        set_password_confirmation_field(pw)
        set_sign_up_button()
        expected = "1 error prohibited this user from being saved:\nEmail has already been taken"
        self.verify_error_explanation(expected)
        stop() # cleanup step

    def test_login_link(self):
        set_log_in_link()
        expected_login_url = 'https://avant-qa-screening.herokuapp.com/users/sign_in'
        actual_url = get_current_url()
        self.assertEqual(expected_login_url, actual_url,
                     msg='FAILED: expected login url = {0}, got url = {1}'.format(expected_login_url, actual_url))
        test_print('Successfully verified the "Log in" link', flash='!')
        stop() # cleanup step

    #===========================================================================
    # valid_email
    #===========================================================================
    def test_valid_email_valid_pw_valid_cpw(self):
        create_valid_account()
        self.assertNotEqual(self.chk_url, get_current_url(),
                         msg='FAILED: url = {0} - did not change after login'.format(get_current_url()))
        test_print('Successfully verified sign up', flash='!')
        stop() # cleanup step

    def test_valid_email_valid_pw_invalid_cpw(self):
        set_email_field(fake_valid_email())
        set_password_field(valid_password())
        set_password_confirmation_field(invalid_password())
        set_sign_up_button()
        expected = "1 error prohibited this user from being saved:\nPassword confirmation doesn't match Password"
        self.verify_error_explanation(expected)

    def test_valid_email_valid_pw_blank_cpw(self):
        set_email_field(fake_valid_email())
        set_password_field(valid_password())
        set_sign_up_button()
        expected = "1 error prohibited this user from being saved:\nPassword confirmation doesn't match Password"
        self.verify_error_explanation(expected)

    def test_valid_email_invalid_pw_valid_cpw(self):
        set_email_field(fake_valid_email())
        set_password_field(invalid_password())
        set_password_confirmation_field(valid_password())
        set_sign_up_button()
        expected = "2 errors prohibited this user from being saved:\nPassword confirmation doesn't match Password\nPassword is too short (minimum is 8 characters)"
        self.verify_error_explanation(expected)

    def test_valid_email_invalid_pw_invalid_cpw(self):
        set_email_field(fake_valid_email())
        pw = invalid_password()
        set_password_field(pw)
        set_password_confirmation_field(pw)
        set_sign_up_button()
        expected = "1 error prohibited this user from being saved:\nPassword is too short (minimum is 8 characters)"
        self.verify_error_explanation(expected)

    def test_valid_email_invalid_pw_blank_cpw(self):
        set_email_field(fake_valid_email())
        set_password_field(invalid_password())
        set_sign_up_button()
        expected = "2 errors prohibited this user from being saved:\nPassword confirmation doesn't match Password\nPassword is too short (minimum is 8 characters)"
        self.verify_error_explanation(expected)

    def test_valid_email_blank_pw_valid_cpw(self):
        set_email_field(fake_valid_email())
        set_password_confirmation_field(valid_password())
        set_sign_up_button()
        expected = "2 errors prohibited this user from being saved:\nPassword can't be blank\nPassword confirmation doesn't match Password"
        self.verify_error_explanation(expected)

    def test_valid_email_blank_pw_invalid_cpw(self):
        set_email_field(fake_valid_email())
        set_password_confirmation_field(invalid_password())
        set_sign_up_button()
        expected = "2 errors prohibited this user from being saved:\nPassword can't be blank\nPassword confirmation doesn't match Password"
        self.verify_error_explanation(expected)

    def test_valid_email_blank_pw_blank_cpw(self):
        set_email_field(fake_valid_email())
        set_sign_up_button()
        expected = "1 error prohibited this user from being saved:\nPassword can't be blank"
        self.verify_error_explanation(expected)

    #===========================================================================
    # invalid email
    #===========================================================================
    def test_invalid_email_valid_pw_valid_cpw(self):
        pw = valid_password()
        set_password_field(pw)
        set_password_confirmation_field(pw)
        set_email_field(invalid_email())
        set_sign_up_button()
        self.verify_invalid_email()

    def test_invalid_email_valid_pw_invalid_cpw(self):
        set_password_field(valid_password())
        set_password_confirmation_field(invalid_password())
        set_email_field(invalid_email())
        set_sign_up_button()
        self.verify_invalid_email()

    def test_invalid_email_valid_pw_blank_cpw(self):
        set_password_field(valid_password())
        set_email_field(invalid_email())
        set_sign_up_button()
        self.verify_invalid_email()

    def test_invalid_email_invalid_pw_valid_cpw(self):
        set_password_field(invalid_password())
        set_password_confirmation_field(valid_password())
        set_email_field(invalid_email())
        set_sign_up_button()
        self.verify_invalid_email()

    def test_invalid_email_invalid_pw_invalid_cpw(self):
        pw = invalid_password()
        set_password_field(pw)
        set_password_confirmation_field(pw)
        set_email_field(invalid_email())
        set_sign_up_button()
        self.verify_invalid_email()

    def test_invalid_email_invalid_pw_blank_cpw(self):
        set_password_field(invalid_password())
        set_email_field(invalid_email())
        set_sign_up_button()
        self.verify_invalid_email()

    def test_invalid_email_blank_pw_valid_cpw(self):
        set_password_confirmation_field(valid_password())
        set_email_field(invalid_email())
        set_sign_up_button()
        self.verify_invalid_email()

    def test_invalid_email_blank_pw_invalid_cpw(self):
        set_password_confirmation_field(invalid_password())
        set_email_field(invalid_email())
        set_sign_up_button()
        self.verify_invalid_email()

    def test_invalid_email_blank_pw_blank_cpw(self):
        set_email_field(invalid_email())
        set_sign_up_button()
        self.verify_invalid_email()

    #===========================================================================
    # blank email
    #===========================================================================
    def test_blank_email_valid_pw_valid_cpw(self):
        pw = valid_password()
        set_password_field(pw)
        set_password_confirmation_field(pw)
        set_sign_up_button()
        expected = "1 error prohibited this user from being saved:\nEmail can't be blank"
        self.verify_error_explanation(expected)

    def test_blank_email_valid_pw_invalid_cpw(self):
        set_password_field(valid_password())
        set_password_confirmation_field(invalid_password())
        set_sign_up_button()
        expected = "2 errors prohibited this user from being saved:\nEmail can't be blank\nPassword confirmation doesn't match Password"
        self.verify_error_explanation(expected)

    def test_blank_email_valid_pw_blank_cpw(self):
        pw = valid_password()
        set_password_field(pw)
        set_sign_up_button()
        expected = "2 errors prohibited this user from being saved:\nEmail can't be blank\nPassword confirmation doesn't match Password"
        self.verify_error_explanation(expected)

    def test_blank_email_invalid_pw_valid_cpw(self):
        set_password_field(invalid_password())
        set_password_confirmation_field(valid_password())
        set_sign_up_button()
        expected = "3 errors prohibited this user from being saved:\nEmail can't be blank\nPassword confirmation doesn't match Password\nPassword is too short (minimum is 8 characters)"
        self.verify_error_explanation(expected)

    def test_blank_email_invalid_pw_invalid_cpw(self):
        pw = invalid_password()
        set_password_field(pw)
        set_password_confirmation_field(pw)
        set_sign_up_button()
        expected = "2 errors prohibited this user from being saved:\nEmail can't be blank\nPassword is too short (minimum is 8 characters)"
        self.verify_error_explanation(expected)

    def test_blank_email_invalid_pw_blank_cpw(self):
        set_password_field(invalid_password())
        set_sign_up_button()
        expected = "3 errors prohibited this user from being saved:\nEmail can't be blank\nPassword confirmation doesn't match Password\nPassword is too short (minimum is 8 characters)"
        self.verify_error_explanation(expected)

    def test_blank_email_blank_pw_valid_cpw(self):
        set_password_confirmation_field(invalid_password())
        set_sign_up_button()
        expected = "3 errors prohibited this user from being saved:\nEmail can't be blank\nPassword can't be blank\nPassword confirmation doesn't match Password"
        self.verify_error_explanation(expected)

    def test_blank_email_blank_pw_invalid_cpw(self):
        set_password_confirmation_field(invalid_password())
        set_sign_up_button()
        expected = "3 errors prohibited this user from being saved:\nEmail can't be blank\nPassword can't be blank\nPassword confirmation doesn't match Password"
        self.verify_error_explanation(expected)

    def test_blank_email_blank_pw_blank_cpw(self):
        set_sign_up_button()
        expected = "2 errors prohibited this user from being saved:\nEmail can't be blank\nPassword can't be blank"
        self.verify_error_explanation(expected)

    #===========================================================================
    # module common function
    #===========================================================================
    def verify_invalid_email(self):
        actual = get_error_explanation(False)
        self.verify_sign_up_label()
        self.assertFalse(actual,
                         msg='FAILED: expected no error explanation, but got error explanation = "{0}" on url = {1}'.format(actual, get_current_url()))
        test_print('Successfully verified no error explanation'.format(actual), flash='!')
        self.assertEqual(self.chk_url, get_current_url(),
                         msg='FAILED: expected url = {0}, got url = {1}'.format(self.chk_url, get_current_url()))
        test_print('Successfully verified login was unsuccessful, user is still on the sign_up page', flash='!')

if __name__ == "__main__":

    unittest.main()