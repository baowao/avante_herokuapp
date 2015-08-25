# common_functions imports
from common.common_functions import get_h1, test_print, VerifyCommonLandingDashboard
# sst imports
from sst.actions import go_to
# python imports
import unittest

#===============================================================================
# tests
#===============================================================================
class Landing(VerifyCommonLandingDashboard, unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.chk_url = 'https://avant-qa-screening.herokuapp.com/'
        go_to(self.chk_url)
        self.h1 = get_h1()

    def test_landing_text(self):
        expected = 'This app is designed and created for the sole use of screening QA candidates for AvantCredit, any other use is prohibitted'
        actual = self.get_landing_dash_text()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected text on landing page = "{0}", got = "{1}"'.format(expected, actual))
        test_print('Successfully verified landing page text = "{0}"'.format(actual), flash='!')

    def test_h1(self):
        expected = 'Sign Up | Sign In'
        self.assertEqual(expected, self.h1,
                         msg='FAILED: expected h1 text on landing page = "{0}", got = "{1}"'.format(expected, self.h1))
        test_print('Successfully verified h1 text = "{0}"'.format(self.h1), flash='!')

    def test_sign_up_link(self):
        expected = 'https://avant-qa-screening.herokuapp.com/users/sign_up'
        self.verify_landing_dash_page_links(0, expected)

    def test_sign_in_link(self):
        expected = 'https://avant-qa-screening.herokuapp.com/users/sign_in'
        self.verify_landing_dash_page_links(1, expected)

if __name__ == "__main__":

    unittest.main()