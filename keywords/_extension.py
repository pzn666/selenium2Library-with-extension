from __future__ import division
from __future__ import absolute_import
from builtins import str
from builtins import chr
from past.builtins import basestring
from past.utils import old_div
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from Selenium2Library import utils
from Selenium2Library.locators import ElementFinder
from Selenium2Library.locators import CustomLocator
from .keywordgroup import KeywordGroup
from selenium.common.exceptions import StaleElementReferenceException
import urllib.request
import ssl
import time

try:
    basestring  # attempt to evaluate basestring
    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)

class _ExtensionKeywords(KeywordGroup):

    def __init__(self):
        self._element_finder = ElementFinder()

    # Click 
    def click_element_by_id(self, id):
        xpath = "//*[@id=" + "'" +  id + "'" + "]"
        elems = self._element_find("xpath=" + xpath, False, False)
        self.__click_displayed_element(elems)

    def click_element_by_class(self, css_class):
        """
        Click element by text
        """
        self._info("Clicking button with class '%s'." % css_class)
        elems = self._element_find("css=" + css_class, False, False)
        self.__click_displayed_element(elems)

    def click_element_by_text(self, text):
        """
        Click element by text
        """
        self._info("Clicking element with text '%s'." % text)
        xpath = "//*[text()=" + "'" +  text + "'" + "]"
        elems = self._element_find("xpath=" + xpath, False, False)
        self.__click_displayed_element(elems)

    def click_element_by_title(self, title):
        xpath = "//*[@title=" + "'" +  title + "'" + "]"
        elems = self._element_find("xpath=" + xpath, False, False)
        self.__click_displayed_element(elems)

    def click_element_when_attribute(self, locator, attribute, attr_value):
        elem = None
        if type(locator) is str:
            temp_elems = self._element_find(locator, False, False)
            if type(temp_elems) is list:
                for temp_elem in temp_elems:
                    if temp_elem.is_displayed():
                        elem = temp_elem
                        break
        else:
            elem = locator
        real_value = elem.get_attribute(attribute)
        if real_value == attr_value:
            elem.click()
    
    def click_element_until_target_is_visible(self, click_locator, visible_locator, timeout=None, interval=None, error=None):
        innter_interval = 0
        if interval is not None:
            innter_interval = int(interval[:-1])
        def click_until_visible():
            try:
                if innter_interval > 0:
                    time.sleep(innter_interval)
                click_elem = self._element_find(click_locator, True, False)
                visible_elem = self._element_find(visible_locator, True, False)
                visible = self._is_visible(visible_elem)
                if visible:
                    return
                elif visible is None:
                    return error or "Element locator '%s' did not match any elements after %s" % (visible_locator, self._format_timeout(timeout))
                else:
                    click_elem.click()
                    return error or "Element '%s' was not visible in %s" % (visible_locator, self._format_timeout(timeout))
            except Exception as e:
                message = ('click_locator: ' + click_locator + ", visible_locator: " + visible_locator + ' ')
                if click_elem is None:
                    message += 'click_elem is None'
                if visible_elem is None:
                    message += 'visible_elem is None'
                raise AssertionError(message)

        self._wait_until_no_error(timeout, click_until_visible)

    def click_button_by_id(self, id):
        xpath = "//button[@id=" + "'" +  id + "'" + "]"
        btns = self._element_find("xpath=" + xpath, False, False)
        self.__click_displayed_element(btns)

    def click_button_by_class(self, css_class):
        """
        Click link by CSS class
        """
        self._info("Clicking button with class '%s'." % css_class)
        btns = self._element_find("css=" + css_class, False, False)
        self.__click_displayed_element(btns)

    def click_button_by_text(self, text):
        """
        Click button by text
        """
        self._info("Clicking button with text '%s'." % text)
        xpath = "//button[text()=" + "'" +  text + "'" + "]"
        btns = self._element_find("xpath=" + xpath, False, False)
        self.__click_displayed_element(btns)

    def click_link_by_id(self, id):
        xpath = "//a[@id=" + "'" +  id + "'" + "]"
        links = self._element_find("xpath=" + xpath, False, False)
        self.__click_displayed_element(links)

    def click_link_by_class(self, css_class):
        """
        Click link by CSS class
        """
        self._info("Clicking link with class '%s'." % css_class)
        links = self._element_find("css=" + css_class, False, False)
        self.__click_displayed_element(links)

    def click_link_by_text(self, text):
        """
        Click link by text 
        """
        self._info("Clicking link with text '%s'." % text)
        xpath = "//a[text()=" + "'" +  text + "'" + "]"
        links = self._element_find("xpath=" + xpath, False, False)
        self.__click_displayed_element(links)

    def click_link_by_title(self, title):
        """
        Click link by title attribute of a link
        """
        self._info("Clicking link with title '%s'." % title)
        xpath = "//a[@title=" + "'" +  title + "'" + "]"
        links = self._element_find("xpath=" + xpath, False, False)
        self.__click_displayed_element(links)

    def click_link_by_attribute(self, attr_name, attr_value):
        xpath = "//a[@" + attr_name + "=" + attr_value + "]"
        links = self._element_find("xpath=" + xpath, False, False)
        self.__click_displayed_element(links)

    def __click_displayed_element(self, elements):
        if type(elements) is list:
            for element in elements:
                if element.is_displayed():
                    element.click()
                    break
        else:
            elements.click()

    # Compate element title/text
    def compare_elements_text_by_id(self, id, text, without_space="False"):
        locator = "xpath=//*[@id=" + "'" +  id + "'" + "]"
        elems = self._element_find(locator, False, False)
        self.__compare_text(text, elems, without_space)

    def compare_elements_text_by_class(self, css_class, text, first_only, without_space="False"):
        """
        Compare all elements' text which find by css calss
        """
        self._info("Compare elements text with class '%s'." % css_class)
        if first_only == 'True':
            elems = self._element_find("css=" + css_class, True, False)
        else:
            elems = self._element_find("css=" + css_class, False, False)
        if elems is not None:
            self.__compare_text(text, elems, without_space)
        else:
            message = "Cannot get elements in compare_elements_text_by_class"
            raise AssertionError(message)

    def compare_elements_title_by_class(self, css_class, text, first_only, without_space="False"):
        """
        Compare all elements' title which find by cas class
        """
        self._info("Compare elements title with class '%s'." % css_class)
        elems = None
        if first_only == 'True':
            elems = self._element_find("css=" + css_class, True, False)
        else:
            elems = self._element_find("css=" + css_class, False, False)
        self.__compare_title(text, elems, without_space)

    def compare_elements_title_by_id(self, id, text):
        locator = "xpath=//*[@id=" + "'" +  id + "'" + "]"
        elems = self._element_find(locator, False, False)
        self.__compare_title(text, elems)
    
    def element_should_contain_text(self, locator, expected, without_space="False"):
        actual = self._get_text(locator)
        if without_space == 'True':
            expected = expected.replace(" ", "")
            actual = actual.replace(" ", "")
        if not expected in actual:
            message = "Element '%s' should have contained text '%s' but its text was '%s'." % (locator, expected, actual)
            raise AssertionError(message)

    def __compare_title(self, text, elems, without_space):
        if type(elems) is list:
            for index, elem in enumerate(elems):
                if not elem.is_displayed():
                    continue
                elem_title = elem.get_attribute('title').encode('UTF-8').decode('UTF-8')
                elem_title = self.__trim_space(elem_title)
                text = self.__trim_space(text)
                if elem_title != text:
                    message = "Title should be '%s' the same, but it's '%s'" % (text, elem_title)
                    raise AssertionError(message)
        else:
            if not elems.is_displayed():
                message = "Element found but is not displayed"
                raise AssertionError(message)
            elem_title = elems.get_attribute('title').encode('UTF-8').decode('UTF-8')
            elem_title = self.__trim_space(elem_title)
            text = self.__trim_space(text)
            if elem_title != text:
                message = "Title should be '%s' the same, but it's '%s'" % (text, elem_title)
                raise AssertionError(message)

    def __compare_text(self, text, elems, without_space):
        if type(elems) is list:
            for index, elem in enumerate(elems):
                if not elem.is_displayed():
                    continue
                actual_text = elem.text
                if without_space == 'True':
                    text = self.__trim_space(text)
                    actual_text = self.__trim_space(actual_text)
                if actual_text != text:
                    message = "Text should be '%s', but it's '%s' at elem in elems, and without_space is '%s'" % (text, actual_text, without_space)
                    raise AssertionError(message)
        else:
            actual_text = elems.text
            if not elems.is_displayed():
                message = "Element found but is not displayed"
                raise AssertionError(message)
            if without_space == 'True':
                actual_text = actual_text.replace(" ", "")
                text = text.replace(" ", "")
            if actual_text != text:
                message = "Text should be '%s', but it's '%s'" % (text, actual_text)
                raise AssertionError(message)

    def __trim_space(self, text):
        text = text.replace(" ","")
        text = text.replace(u"\xa0", "")
        return text
    # Compare images
    def compare_images(self, imgs_path_list_a, imgs_path_list_b):
        """
        Compare two list of images are the same or not
        """
        if '' in imgs_path_list_a:
            imgs_path_list_a.remove('')
        if '' in imgs_path_list_b:
            imgs_path_list_b.remove('')
        if len(imgs_path_list_a) != len(imgs_path_list_b):
            message = "Two lists' length are not match"
            raise AssertionError(message)
        for path_a, path_b in zip(imgs_path_list_a, imgs_path_list_b):
            self.compare_image(path_a, path_b)

    def compare_image(self, img_path_a, img_path_b):
        """
        Compare two images is the same or not
        """
        img_a = self.__image_source(img_path_a)
        img_b = self.__image_source(img_path_b)
        if bytearray(img_a) != bytearray(img_b):
            message = "File at '%s' and '%s' should be the same, but it's not." % (img_path_a, img_path_b)
            raise AssertionError(message)


    def __image_source(self, path):
        result_file = None
        if 'http' in path:
            context = ssl._create_unverified_context()
            result_file = urllib.request.urlopen(path, context=context)
        else:
            result_file = open(path, 'rb')
        if result_file is None:
            message = "Cannot read files at '%s'." % (path)
            raise AssertionError(message)
        result_bytearray = result_file.read()
        return result_bytearray

    # Waits
    def wait_until_element_is_visible_by_id(self, id, timeout=None, error=None):
        def check_visibility_by_css():
            locator = "xpath=//*[@id=" + "'" +  id + "'" + "]"
            visible = self._is_visible(locator)
            if visible:
                return
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" % (locator, self._format_timeout(timeout))
            else:
                return error or "Element '%s' was not visible in %s" % (locator, self._format_timeout(timeout))

        self._wait_until_no_error(timeout, check_visibility_by_css)

    def wait_until_element_is_visible_by_class(self, css_class, timeout=None, error=None):
        def check_visibility_by_css():
            locator = "css=" + css_class
            visible = self._is_visible(locator)
            if visible:
                return
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" % (locator, self._format_timeout(timeout))
            else:
                return error or "Element '%s' was not visible in %s" % (locator, self._format_timeout(timeout))

        self._wait_until_no_error(timeout, check_visibility_by_css)

    def wait_until_element_is_visible_by_title(self, title, timeout=None, error=None):
        def check_visibility_by_title():
            locator = "xpath=//*[@title=" + "'" +  title + "'" + "]"
            visible = self._is_visible(locator)
            if visible:
                return
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" % (locator, self._format_timeout(timeout))
            else:
                return error or "Element '%s' was not visible in %s" % (locator, self._format_timeout(timeout))

        self._wait_until_no_error(timeout, check_visibility_by_title)

    def wait_until_element_is_visible_by_text(self, text, timeout=None, error=None):
        def check_visibility_by_text():
            locator = "xpath=//*[text()=" + "'" +  text + "'" + "]"
            visible = self._is_visible(locator)
            if visible:
                return
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" % (locator, self._format_timeout(timeout))
            else:
                return error or "Element '%s' was not visible in %s" % (locator, self._format_timeout(timeout))

        self._wait_until_no_error(timeout, check_visibility_by_text)

    def wait_until_browser_title_is(self, title, timeout=None, error=None):
        def check_browser_title():
            if title == self.get_title():
                return
            else:
                return error or "Title was not %s in %s" % (title, self._format_timeout(timeout))
        self._wait_until_no_error(timeout, check_browser_title)

    def wait_until_element_text_changed(self, locator, timeout=None, error=None):
        elements = self._element_find(locator, False, False)
        original_text = ''
        for element in elements:
            if element.is_displayed():
                original_text = element.text
                break
        def element_text_changed():
            elements = self._element_find(locator, False, False)
            for element in elements:
                if element.is_displayed():
                    target_element = element
                    break
            if target_element is not None:
                if target_element.text != original_text:
                    return
                else:
                    return error or "Element text '%s' did not change after %s and is '%s'" % (locator, self._format_timeout(timeout), original_text)
            else:
                return error or "Element '%s' was not found in %s" % (locator, self._format_timeout(timeout))

        self._wait_until_no_error(timeout, element_text_changed)

    # Checks
    def check_link_parent_attr_by_text(self, text, parent_tag, target_attr, expect_value):
        xpath = "//a[text()=" + "'" +  text + "'" + "]"
        link = self._element_find("xpath=" + xpath, True, False)
        parent = link.find_elements_by_xpath(".//ancestor::" + parent_tag)[0]
        if parent is None:
            message = "Can't find parent of '%s', which tag is '%s'" % (text, parent_tag)
            raise AssertionError(message)
        real_value = parent.get_attribute(target_attr) 
        if real_value == expect_value:
            return True
        else:
            return False

    def check_element_attribute(self, locator, attr_name, expect_value):
        elements = self._element_find(locator, False, False)
        for element in elements:
            if element.is_displayed():
                element_attr_value = element.get_attribute(attr_name)
                if element_attr_value == expect_value:
                    return True
                else:
                    return False

    # Gets
    def get_background_img_paths_by_class(self, css_class, first_only):
        """
        Get links' background image from css property
        """
        if first_only == 'False':
            img_paths = []
            links = self._element_find("css=" + css_class, False, False)
            if type(links) is list:
                for link in links:
                    img_path = link.value_of_css_property("background-image")
                    img_path = img_path[5:len(img_path) - 2]
                    img_paths.append(img_path)
            else:
                img_path = links.value_of_css_property("background-image")
                img_path = img_path[5:len(img_path) - 2]
                img_paths.append(img_path)
            return img_paths
        else:
            link = self._element_find("css=" + css_class, True, False)
            img_path = link.value_of_css_property("background-image")
            img_path = img_path[5:len(img_path) - 2]
            return img_path

    def get_all_element_title_or_text_with(self, locator):
        elems = self._element_find(locator, False, False)
        text_title_list = []
        for elem in elems:
            if not elem.is_displayed():
                continue
            element_title = elem.get_attribute('title')
            if element_title != '':
                text_title_list.append(elem.get_attribute('title').encode('UTF-8').decode('UTF-8'))
            elif elem.text != '':
                text_title_list.append(elem.text.encode('UTF-8').decode('UTF-8'))
        if not text_title_list:
            message = "No elem found in '%s'" % (locator)
            raise AssertionError(message)
        return text_title_list

    def get_all_element_text_from(self, locator):
        elems = self._element_find(locator, False, False)
        text_list = []
        for elem in elems:
            text_list.append(elem.text)
        if not text_list:
            message = "Nothing found in '%s'" % (locator)
            raise AssertionError(message)
        return text_list

    def get_all_element_text_from_with_tag(self, locator, tag):
        elems = self._element_find(locator, False, False)
        results = []
        for elem in elems:
            for elem_tag in elem.find_elements_by_tag_name(tag):
                results.append(elem_tag.text)
        if not results:
            message = "Nothing found in '%s'" % (locator)
            raise AssertionError(message)
        return results
                
    def get_all_links_text_or_title_from(self, locator):
        """
        Return a list containing texts of all links found in certain element
        """
        elems = self._element_find(locator, False, False)
        links = []
        for elem in elems:
            if not elem.is_displayed():
                continue
            for elem_link in elem.find_elements_by_tag_name('a'):
                if not elem.is_displayed():
                    continue
                element_link_title = elem_link.get_attribute('title')
                if element_link_title != '':
                    links.append(elem_link.get_attribute('title').encode('UTF-8').decode('UTF-8'))
                elif elem_link.text != '':
                    links.append(elem_link.text.encode('UTF-8').decode('UTF-8'))
        if not links:
            message = "No links found in '%s'" % (locator)
            raise AssertionError(message)
        return links

    def get_all_links_text_from(self, locator):
        elems = self._element_find(locator, False, False)
        links = []
        for elem in elems:
            if not elem.is_displayed():
                continue
            for elem_link in elem.find_elements_by_tag_name('a'):
                if not elem.is_displayed():
                    continue
                if elem_link.text != '':
                    links.append(elem_link.text.encode('UTF-8').decode('UTF-8'))
        if not links:
            message = "No links found in '%s'" % (locator)
            raise AssertionError(message)
        return links

    def get_all_links_title_from(self, locator):
        elems = self._element_find(locator, False, False)
        links = []
        for elem in elems:
            if not elem.is_displayed():
                continue
            for elem_link in elem.find_elements_by_tag_name('a'):
                if not elem.is_displayed():
                    continue
                element_link_title = elem_link.get_attribute('title')
                if element_link_title != '':
                    links.append(elem_link.get_attribute('title').encode('UTF-8').decode('UTF-8'))
        if not links:
            message = "No links found in '%s'" % (locator)
            raise AssertionError(message)
        return links

    def get_substring(self, text, start, end):
        """
        Get substring
        """
        return text[int(start):int(end)]
