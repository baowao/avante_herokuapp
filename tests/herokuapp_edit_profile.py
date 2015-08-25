# common_functions imports
from common.common_functions import (create_valid_account, get_dash_ep_text,
                                     get_h1, get_h2_label, random_word,
                                     set_sign_up_link, test_print,
                                     VerifyCommonLandingDashboard,
                                     wait_click_url, wait_for_element,
                                     wait_write)
# sst imports
from sst.actions import (assert_displayed, click_element, get_element_by_css,
                         get_elements_by_css, go_to, simulate_keys)
# python imports
import random, unittest

#===============================================================================
# getters
#===============================================================================
def get_field_labels():
    return [x.text for x in get_elements_by_css('.sr-only.control-label') if x.text not in (None, '')]

#===============================================================================
# setters
#===============================================================================
def set_random_first_name():
    random_name = random_word(random.randrange(2,10))
    wait_write(random_name, ps='writing "{0}" to the first name field'.format(random_name),
               css_select='input#profile_first_name')
    return random_name

def set_random_last_name():
    random_name = random_word(random.randrange(2,10))
    wait_write(random_name, ps='writing "{0}" to the last name field'.format(random_name),
               css_select='input#profile_last_name')
    return random_name

def set_random_city():
    random_city = random_word(random.randrange(2,10))
    wait_write(random_city, ps='writing "{0}" to the city field'.format(random_city),
               css_select='input#profile_city')
    return random_city

def set_random_zip():
    random_zip = random_word(random.randrange(2,10), has_punc=False)
    wait_write(random_zip, ps='writing "{0}" to the zip field'.format(random_zip),
               css_select='input#profile_zip')
    return random_zip

def set_random_zip2():
    random_zip = '60625'
    wait_write(random_zip, ps='writing "{0}" to the zip field'.format(random_zip),
               css_select='input#profile_zip')
    return random_zip

def set_random_birthdate():
    random_birthdate = random_word(random.randrange(2,10))
    wait_write(random_birthdate, ps='writing "{0}" to the birthdate field'.format(random_birthdate),
               css_select='input#profile_birthdate')
    return random_birthdate

def set_edit_profile_link():
    wait_click_url(ps='clicking the "Edit Profile" link', text='Edit Profile')

def set_random_state_dropdown():
    try:
        click_element(get_element_by_css('select#profile_state'))
        states = get_element_by_css('select#profile_state').text.split('\n')
        if (len(states)) < 51:
            raise ValueError('ERROR: did not find 51 states')
        random_state = states[random.randrange(len(states))]
        state_index = states.index(random_state)
        for _ in xrange(state_index):
            simulate_keys(get_element_by_css('select#profile_state'), 'DOWN')
        simulate_keys(get_element_by_css('select#profile_state'), 'ENTER')
        test_print('clicking state = "{0}"'.format(random_state))
    except:
        random_state = 'AL'
    return random_state

def set_update_personal_button():
    click_element(wait_for_element(ps='clicking "Update Personal" button', css_select='input.btn.btn-primary'))

#===============================================================================
# tests
#===============================================================================
class EditProfile(VerifyCommonLandingDashboard, unittest.TestCase):
    @classmethod
    def setUpClass(self):
        go_to('https://avant-qa-screening.herokuapp.com/users/sign_in')
        set_sign_up_link()
        self.valid_email, self.valid_pw = create_valid_account()
        self.h1 = get_h1()
        set_edit_profile_link()

    def test_edit_profile_text(self):
        expected = 'This app is designed and created for the sole use of screening QA candidates for AvantCredit, any other use is prohibitted'
        actual = self.get_landing_dash_text()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected text on dashboard page = "{0}", got = "{1}"'.format(expected, actual))
        test_print('Successfully verified dashboard page text = "{0}"'.format(actual), flash='!')

    def test_edit_profile_text2(self):
        expected = 'You need to edit your profile before doing any querying'
        actual = get_dash_ep_text()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected text on dashboard page = "{0}", got = "{1}"'.format(expected, actual))
        test_print('Successfully verified dashboard page text = "{0}"'.format(actual), flash='!')

    def test_edit_your_profile_label(self):
        expected = 'Edit your Profile:'
        actual = get_h2_label()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected label = "{0}", got = "{1}"'.format(expected, actual))
        test_print('Successfully verified label = "{0}"'.format(actual), flash='!')

    def test_ep_field_labels(self):
        expected_labels = [u'First name', u'Last name', u'City', u'State',
                           u'Zip', u'Birthdate']
        self.assertListEqual(expected_labels, get_field_labels())
        test_print('Successfully verified the following labels;', flash='!')
        for index, label in enumerate(expected_labels, 1):
            print '{0}) {1}'.format(index, label)

    def test_ep_fields_fails(self):
        # This test fails... See bug #1 report
        funcs = [set_random_first_name, set_random_last_name, set_random_city,
                 set_random_state_dropdown, set_random_zip,
                 set_random_birthdate]
        selected = [None]
        for _ in funcs:
            random_index = None
            while random_index in selected:
                random_index = random.randrange(len(funcs))
            selected.append(random_index)
            funcs[random_index]()
        set_update_personal_button()
        set_edit_profile_link()

    def test_ep_fields_workaround(self):
        # This test is a workaround for test_ep_fields_fails
        # This test can also fail based on issues detailed in bug #2 report
        funcs = [set_random_first_name, set_random_last_name, set_random_city,
                 set_random_state_dropdown, set_random_zip2,
                 set_random_birthdate]
        selected = [None]

        # write fields in random order
        random_last_name = None
        random_city = None
        random_state_dropdown = None
        random_zip = None
        random_birthdate = None
        set_update_personal_button()
        for _ in funcs:
            random_index = None
            while random_index in selected:
                random_index = random.randrange(len(funcs))
            val = funcs[random_index]()
            selected.append(random_index)

            # check profile values
            if random_index == 0:
                random_first_name = val
            elif random_index == 1:
                random_last_name = val
            elif random_index == 2:
                random_city = val
            elif random_index == 3:
                random_state_dropdown = val
            elif random_index == 4:
                random_zip = val
            else:
                random_birthdate = val
            set_update_personal_button()

        # confirm dashboard messages, links
        expected = 'This app is designed and created for the sole use of screening QA candidates for AvantCredit, any other use is prohibitted'
        actual = self.get_landing_dash_text()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected text on dashboard page = "{0}", got = "{1}"'.format(expected, actual))
        test_print('Successfully verified dashboard page text = "{0}"'.format(actual), flash='!')
        expected = 'Succesfully updated profile'
        actual = get_dash_ep_text()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected text on dashboard page = "{0}", got = "{1}"'.format(expected, actual))
        test_print('Successfully verified dashboard page text = "{0}"'.format(actual), flash='!')
        expected = 'Sign out | Edit Profile'
        self.assertEqual(expected, self.h1,
                         msg='FAILED: expected h1 text on dashboard page = "{0}", got = "{1}"'.format(expected, self.h1))
        test_print('Successfully verified h1 text = "{0}"'.format(self.h1), flash='!')

        # click edit profile and confirm values
        set_edit_profile_link()

        # fn
        self.assertTrue(assert_displayed(wait_for_element(value=random_first_name)))
        test_print('Successfully verified "{0}" in the first name field'.format(random_first_name), flash='!')

        # ln
        self.assertTrue(assert_displayed(wait_for_element(value=random_last_name)))
        test_print('Successfully verified "{0}" in the last name field'.format(random_last_name), flash='!')

        # city
        self.assertTrue(assert_displayed(wait_for_element(value=random_city)))
        test_print('Successfully verified "{0}" in the city field'.format(random_city), flash='!')

        # state
        self.assertTrue(assert_displayed(wait_for_element(value=str(random_state_dropdown))))
        test_print('Successfully verified "{0}" in the state field'.format(random_state_dropdown), flash='!')

        # zip
        self.assertTrue(assert_displayed(wait_for_element(value=random_zip)))
        test_print('Successfully verified "{0}" in the zip field'.format(random_zip), flash='!')

        # birthdate
        self.assertTrue(assert_displayed(wait_for_element(value=random_birthdate)))
        test_print('Successfully verified "{0}" in the birthdate field'.format(random_birthdate), flash='!')

if __name__ == "__main__":

    unittest.main()