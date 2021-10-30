__all__ = ["Chatroom"]

import datetime
from .constants import *
from .waobject import WaObject
from selenium.webdriver.common.keys import Keys


class Chatroom(WaObject):
    def __init__(self, browser=None):
        super().__init__(browser)

    def open_chat_to(self, nameornumber, _shouldoutput=(True, True)):
        if _shouldoutput[0] and DEFAULT_SHOULD_OUTPUT:
            print(f'Opening chatroom to "{nameornumber}"', end="... ")
        self._search_and_open_chat_by_number(nameornumber)
        if _shouldoutput[1] and DEFAULT_SHOULD_OUTPUT:
            print(f'{STRINGS.CHECK_CHAR} Done')

    def open_chat_to_number_using_url(self, number, _shouldoutput=(True, True)):
        if _shouldoutput[0] and DEFAULT_SHOULD_OUTPUT:
            print(f'Opening chatroom to "{number}"', end="... ")
        self.browser.get("https://web.whatsapp.com/send?phone=" + number)
        self._wait_for_presence_of_an_element(SELECTORS.MAIN_SEARCH_BAR)
        if _shouldoutput[1] and DEFAULT_SHOULD_OUTPUT:
            print(f'{STRINGS.CHECK_CHAR} Done')

    def send_message_to(self, nameornumber, message, _shouldoutput=(True, True)):
        if _shouldoutput[0] and DEFAULT_SHOULD_OUTPUT:
            print(f'Sending message "{message}" to "{nameornumber}"...', end="... ")
        self.open_chat_to(nameornumber)
        self._send_message(message)
        if _shouldoutput[1] and DEFAULT_SHOULD_OUTPUT:
            print(f'{STRINGS.CHECK_CHAR} Done')

    def send_message_to_multiple_chats(self, namesornumbers, message):
        for nameornumber in namesornumbers:
            self.send_message_to(nameornumber, message)

    def send_message_at_time_to(self, nameornumberlist, message, time='03:00:00', _shouldoutput=(True, True)):
        if _shouldoutput[0] and DEFAULT_SHOULD_OUTPUT:
            print(f'Sending message "{message}" to "{nameornumberlist}" on time {time}...')
        h, m, s = map(int, time.split(':'))
        given_time = str(datetime.time(hour=h, minute=m, second=s))
        while True:
            now = datetime.datetime.now()
            time_now = "%0.2d:%0.2d:%0.2d" % (now.hour, now.minute, now.second)
            if given_time == time_now:
                self.send_message_to_multiple_chats(nameornumberlist, message)
                break
                
    def clear_all_chats(self):
        self._wait_for_presence_of_an_element(SELECTORS.GROUPS__NAME_IN_CHATS)
        self._wait_for_an_element_to_be_clickable(SELECTORS.MAIN_SEARCH_BAR).click()
        preactive = None
        self.browser.switch_to.active_element.send_keys(Keys.ARROW_DOWN)
        curractive = self.browser.switch_to.active_element
        pregroupname = None
        while curractive != preactive:
            self._wait_for_presence_of_an_element(SELECTORS.CHATROOM__OPTIONS)
            
            for i in range(3):
                self.browser.switch_to.active_element.send_keys(Keys.ARROW_DOWN)
            self.browser.switch_to.active_element.send_keys(Keys.ENTER)
            self._wait_for_presence_of_an_element(SELECTORS.OVERLAY)
            self._wait_for_an_element_to_be_clickable(SELECTORS.OVERLAY_OK).click()      
            
            self._close_info()
            
            preactive = curractive
            pregroupname = self._wait_for_presence_of_an_element(SELECTORS.CHATROOM__NAME)
            curractive.send_keys(Keys.ARROW_DOWN)
            curractive = self.browser.switch_to.active_element
            
    def _open_chat_info(self):
        self._wait_for_an_element_to_be_clickable(SELECTORS.CHATROOM__NAME).click()

    def _close_chat_info(self):
        self._wait_for_an_element_to_be_clickable(SELECTORS.CHATROOM__CLOSE_INFO).click()

    def _send_message(self, message):
        self._wait_for_an_element_to_be_clickable(SELECTORS.MESSAGE_INPUT_BOX).send_keys(message + Keys.ENTER)

