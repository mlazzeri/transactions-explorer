import unittest

from hamcrest import *
from nose.tools import nottest

from test.features import BrowserTest


class test_create_pages(BrowserTest):

    def test_about_page(self):
        self.browser.visit("http://0.0.0.0:8000/high-volume-services/"
                           "by-transactions-per-year/descending")
        assert_that(self.browser.find_by_css('#wrapper h1').text,
                    is_('High-volume services'))

    def test_home_page(self):
        self.browser.visit("http://0.0.0.0:8000/")

        headlines = self.browser.find_by_css('.headline')

        departments = headlines[0].text
        services = headlines[1].text
        transactions = headlines[2].text

        assert_that(departments, contains_string('4'))
        assert_that(services, contains_string('11'))
        assert_that(transactions, contains_string('4.85b'))

    def test_all_services(self):
        self.browser.visit("http://0.0.0.0:8000/all-services/by-transactions-per-year/descending")
        assert_that(self.browser.find_by_css('#wrapper h1').text, is_("Transactions Explorer"))
        assert_that(self.browser.find_by_css('.explanatory').text, is_("Compare all government transactional services grouped by the department providing them. You can also see just the high-volume services, or read more about the data and how it is collected."))
