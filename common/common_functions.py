# sst imports
from sst.actions import (assert_text, click_element, get_current_url,
                         get_elements, get_elements_by_css,
                         get_elements_by_xpath, go_back, sleep, wait_for,
                         write_textfield)
# python imports
import random, string

class VerifyCommonLandingDashboard(object):
    def get_landing_dash_text(self):
        #returns "This app is designed and created for the sole use of screening
        # QA candidates for AvantCredit, any other use is prohibitted"
        return wait_for_element(ps='getting the landing page text', tag='a').text

    def verify_landing_dash_page_links(self, h1_index, expected_link_url,
                                       back=True):
        # used in both landing and dashboard verification
        link = self.h1.split(' | ')[h1_index]
        wait_click_url(ps='clicking "{0}" link'.format(link), tag='a', text=link)
        actual = get_current_url()
        self.assertIn(expected_link_url, actual,
                         msg='FAILED: expected "{0}" link to open url = {1}, got url = {2}'.format(link, expected_link_url, actual))
        test_print('Successfully opened the "{0}" link'.format(link), flash='!')
        if back:
            go_back() # cleanup step

class VerifyCommonErrorMsg(object):
    def verify_sign_up_label(self):
        expected = 'Sign up'
        actual = get_h2_label()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected h2 = "{0}", got h2 = "{1}" on url = {2}'.format(expected, actual, get_current_url()))
        test_print('Successfully verified h2 = "{0}"'.format(actual), flash='!')

    def verify_error_explanation(self, expected):
        actual = get_error_explanation()
        self.verify_sign_up_label()
        self.assertEqual(expected, actual,
                         msg='FAILED: expected error explanation = "{0}", got expected error explanation = "{1}" on url = {2}'.format(expected, actual, get_current_url()))
        test_print('Successfully verified expected error explanation = "{0}"'.format(actual), flash='!')

def create_valid_account():
        email = fake_valid_email()
        set_email_field(email)
        pw = valid_password()
        set_password_field(pw)
        set_password_confirmation_field(pw)
        set_sign_up_button()
        return email, pw

def fake_valid_email():
    # returns a valid email address not tied to any actual account
    return invalid_email() + '@fakedomain.com'

def get_dash_ep_text():
    # returns "You need to edit your profile before doing any querying"
    return wait_for_element(ps='getting the dashboard/edit profile page text',
                            tag='center').text

def get_error_explanation(expected=True):
    error_explanation = None
    if expected:
        error_explanation = wait_for_element(ps='getting error explanation label',
                                             css_select='div#error_explanation').text
    else:
        try:
            error_explanation = wait_for_element(ps='getting error explination label',
                                                 attempts=1, css_select='div#error_explanation').text
            raise ValueError('ERROR: received unexpected error message on the sign_up page = "{0}"'.format(error_explanation))
        except:
            test_print('Did not find an error explanation (expected)')
    return error_explanation

def get_h1():
    h1 = None
    try:
        h1 = wait_for_element(ps='getting the landing page h1 text', tag='h1').text
    except:
        pass
    return h1

def get_h2_label():
    return wait_for_element(ps='getting h2 label', tag='h2').text

def invalid_password():
    return valid_password()[:7]

def invalid_password_confirm(pw):
    """
    creates a different invalid password

    pw: original password you want to change
    type pw: string

    """
    pw2 = ''
    while True:
        pw2 = invalid_password()
        if pw2 != pw:
            break
    return pw2

def invalid_email():
    return random_word(random.randrange(5, 12), has_punc=False, has_upper=False)

def random_word(length, has_lower=True, has_upper=True, has_digits=True, has_punc=True):
    """
    creates randomly generated string

    has_upper: include upper case chars
    type has_upper: bool
    has_digits: include digits
    type has_digits: bool
    has_punc: include punctuation
    type has_punc: bool

    """
    char = ''
    if has_lower:
        char = string.ascii_lowercase
    if has_upper:
        char += string.ascii_uppercase
    if has_digits:
        char += string.digits
    if has_punc:
        char += string.punctuation
    return ''.join(random.choice(char) for _ in range(length))

def set_log_in_link():
    wait_click_url(ps='clicking the "Log in" link', text='Log in')

def set_email_field(email_text):
    """
    writes to email field

    email_text: email intended to be written to email field
    type email_text: string

    """
    wait_write(ps='writing "{0}" to "Email" field'.format(email_text),
               text_to_write=email_text, css_select='input#user_email')

def set_log_in_button():
    click_element(wait_for_element(value="Log in"))
    test_print('clicking the "Log in" button')

def set_password_field(password_text):
    """
    writes to password field

    password_text: password intended to be written to password field
    type password_text: string

    """
    wait_write(ps='writing "{0}" to "Password" field'.format(password_text),
               text_to_write=password_text, css_select='input#user_password')

def set_password_confirmation_field(password_text):
    """
    writes to password confirmation field

    password_text: password intended to be written to password field
    type password_text: string

    """
    wait_write(ps='writing "{0}" to "Password confirmation" field'.format(password_text),
               text_to_write=password_text, css_select='input#user_password_confirmation')

def set_sign_up_button():
    click_element(wait_for_element(value="Sign up"))
    test_print('clicking the "Sign up" button')

def set_sign_up_link():
    wait_click_url(ps='clicking the "Sign up" link', text='Sign up')

def test_print(print_statement, flash='#'):
    """
    console logging utitlity.

    print_statement: statement to console
    type print_statement: string
    flash: accentuates your print statement in the console
    type flash: string

    """
    print len(print_statement) * flash
    print print_statement
    print len(print_statement) * flash

def valid_password():
    # returns password 8 chars (up to 20)
    return random_word(random.randrange(8,20))

def wait_click_url(ps=None, flash='#', attempts=10, index=0, element=None,
                   css_select=None, *args, **kwargs):
    """
    clicks url AND waits for url to change

    ps: logging message of your choosing
    type ps: string
    flash: accentuates your print statement in the console
    type flash: string
    index: will return the elment you specify by index
    type index: int
    attempts: number of tries, seperated by a 1 second sleep to get the elements
    type attempts: int
    xpath: an xpath like you would pass into get_element_by_xpath()
    type xpath: string
    css_select: a css selector like you would pass into get_element_by_css()
    type css_select: string
     *args, **kwargs: any element pair you would pass into get_element()
         e.g tag='some_tag_type', css_class='some_class_name'

    """
    chk_url = get_current_url()
    counter = 1
    while chk_url == get_current_url():
        if element:
            wait_for(click_element, element)
        elif css_select:
            try:
                wait_for(click_element, get_elements_by_css(css_select)[index])
            except Exception as e:
                if counter > 2:
                    test_print('ERROR: "{0}". Attempt {1} of {2}'.format(e, counter, attempts))
        else:
            try:
                wait_for(click_element, get_elements(*args, **kwargs)[index])
            except Exception as e:
                if counter > 2:
                    test_print('ERROR: "{0}". Attempt {1} of {2}'.format(e, counter, attempts))
        if counter == attempts:
            raise Exception('Error: The url did not change after {0} attempts'.format(attempts))
            break
        else:
            sleep(1)
        counter += 1
    if ps:
        test_print(ps, flash)

def wait_for_element(ps=None, flash='#', index=0, attempts=10, xpath=None,
                     css_select=None, *args, **kwargs):
    """
    Waits for one specific elements. Returns an element

    ps: logging message of your choosing
    type ps: string
    flash: accentuates your print statement in the console
    type flash: string
    index: will return the elment you specify by index
    type index: int
    attempts: number of tries, seperated by a 1 second sleep to get the elements
    type attempts: int
    xpath: an xpath like you would pass into get_element_by_xpath()
    type xpath: string
    css_select: a css selector like you would pass into get_element_by_css()
    type css_select: string
     *args, **kwargs: any element pair you would pass into get_element()
         e.g tag='some_tag_type', css_class='some_class_name'

    """
    some_element = None
    counter = 1
    while not some_element:
        try:
            if xpath:
                some_element = get_elements_by_xpath(xpath)[index]
            elif css_select:
                some_element = get_elements_by_css(css_select)[index]
            else:
                some_element = get_elements(*args, **kwargs)[index]

        except Exception as e:
            if counter > 2:
                test_print('ERROR: {0}. Attempt {1} of {2}'.format(e, counter, attempts))
            sleep(1)

        counter += 1
        if counter > attempts and not some_element:
            raise e
            break

    if some_element and ps:
        test_print(ps, flash)
    return some_element

def wait_write(text_to_write, attempts=10, ps=None, flash='#', index=0, css_select=None, *args, **kwargs):
    """
    writes to a text field

    text_to_write: text intended to be written to text field
    type text_to_write: string
    attempts: number of tries, seperated by a 1 second sleep to get the elements
    type attempts: int
    ps: logging message of your choosing
    type ps: string
    flash: accentuates your print statement in the console
    type flash: string
    index: will return the elment you specify by index
    type index: int
    xpath: an xpath like you would pass into get_element_by_xpath()
    type xpath: string
    css_select: a css selector like you would pass into get_element_by_css()
    type css_select: string
     *args, **kwargs: any element pair you would pass into get_element()
         e.g tag='some_tag_type', css_class='some_class_name'

    """
    if css_select:
        wait_for_element(css_select=css_select)
    else:
        wait_for_element(*args, **kwargs)
    while attempts > 0:
        try:
            if css_select:
                write_textfield(get_elements_by_css(css_select)[index], text_to_write)
                assert_text(get_elements_by_css(css_select)[index], text_to_write)
                break
            else:
                write_textfield(get_elements(*args, **kwargs)[index], text_to_write)
                assert_text(get_elements(*args, **kwargs)[index], text_to_write)
                break
        except Exception as e:
            attempts -= 1
            sleep(1)
        if attempts == 0:
            raise e
    if ps:
        test_print(ps, flash)