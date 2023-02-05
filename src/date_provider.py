import re

import lxml.html
import requests
from waste_type import WasteType
from invalid_address_exception import InvalidAddressException


class DateProvider:
    ENDPOINT = 'https://web6.karlsruhe.de/service/abfall/akal/akal.php'

    REST_XPATH = '/html/body/section/div/div[3]/div[3]'
    BIO_XPATH = '/html/body/section/div/div[4]'
    WERTSTOFF_XPATH = '/html/body/section/div/div[5]'
    PAPIER_XPATH = '/html/body/section/div/div[6]'
    SPERRMUELL_XPATH = '/html/body/section/div/div[8]/div[3]'

    DATE_REGEX = '[0-9]{2}\\.[0-9]{2}\\.[0-9]{4}'

    def __init__(self, street, street_number):
        self.street = street
        self.street_number = street_number

    def extract_dates(self, text):
        return re.findall(self.DATE_REGEX, text)

    @staticmethod
    def read_xpath(html, xpath):
        tree = lxml.html.fromstring(html)
        element = tree.xpath(xpath)[0]
        return lxml.html.tostring(element).decode("utf-8")

    def fetch_dates(self):
        payload = {
            'strasse_n': self.street,
            'hausnr': self.street_number,
            'anzeigen': 'anzeigen'
        }

        response = requests.post(self.ENDPOINT, data=payload).text

        if "Die ausgewählte Adresse ist unbekannt" in response:
            raise InvalidAddressException(self.street, self.street_number)

        return {
            WasteType.RESIDUAL_WASTE: self.extract_dates(self.read_xpath(response, self.REST_XPATH)),
            WasteType.ORGANIC_WASTE: self.extract_dates(self.read_xpath(response, self.BIO_XPATH)),
            WasteType.RECYCLABLE_WASTE: self.extract_dates(self.read_xpath(response, self.WERTSTOFF_XPATH)),
            WasteType.PAPER_WASTE: self.extract_dates(self.read_xpath(response, self.PAPIER_XPATH)),
            WasteType.BULKY_WASTE: self.extract_dates(self.read_xpath(response, self.SPERRMUELL_XPATH))
        }
