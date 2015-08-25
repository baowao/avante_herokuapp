# common_functions imports
from common.common_functions import (create_valid_account, get_h1,
                                     get_dash_ep_text, set_sign_up_link,
                                     set_email_field, set_log_in_button,
                                     set_password_field, test_print,
                                     VerifyCommonLandingDashboard)
# sst imports
from sst.actions import go_to
# python imports
import unittest

#===============================================================================
# tests
#===============================================================================
class Dashboard(VerifyCommonLandingDashboard, unittest.TestCase):
    @classmethod
    def setUpClass(self):
        go_to('https://avant-qa-screening.herokuapp.com/users/sign_in')
        set_sign_up_link()
        self.valid_email, self.valid_pw = create_valid_account()
        self.h1 = get_h1()

    def test_dashboard_text(self):
        expected = 'This app is designed and created for the sole use of screening QA candidates for AvantCredit, any other use is prohibitted'
        actual = self.get_landing_dash_text()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected text on dashboard page = "{0}", got = "{1}"'.format(expected, actual))
        test_print('Successfully verified dashboard page text = "{0}"'.format(actual), flash='!')

    def test_dashboard_text2(self):
        expected = 'You need to edit your profile before doing any querying'
        actual = get_dash_ep_text()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected text on dashboard page = "{0}", got = "{1}"'.format(expected, actual))
        test_print('Successfully verified dashboard page text = "{0}"'.format(actual), flash='!')

    def test_h1(self):
        expected = 'Sign out | Edit Profile'
        self.assertEqual(expected, self.h1,
                         msg='FAILED: expected h1 text on dashboard page = "{0}", got = "{1}"'.format(expected, self.h1))
        test_print('Successfully verified h1 text = "{0}"'.format(self.h1), flash='!')

    def test_sign_out_link(self):
        expected = 'https://avant-qa-screening.herokuapp.com/'
        self.verify_landing_dash_page_links(0, expected, False)

        # clean up steps (this test only) logs back in
        go_to('https://avant-qa-screening.herokuapp.com/users/sign_in')
        set_email_field(self.valid_email)
        set_password_field(self.valid_pw)
        set_log_in_button()

    def test_edit_profile_link(self):
        expected = 'https://avant-qa-screening.herokuapp.com/profiles/'
        self.verify_landing_dash_page_links(1, expected)

if __name__ == "__main__":

    unittest.main()