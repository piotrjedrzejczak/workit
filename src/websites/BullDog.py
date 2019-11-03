from requests import get
from src.model.Offer import Offer
from src.model.Website import Website
from bs4 import BeautifulSoup as BSoup
from re import compile

class BullDogJobs(Website):

    __get_offers_url = 'https://bulldogjob.pl/companies/jobs?mode=plain&page='

    def __init__(self):
        self.offers = []


    def create_offers(self):
        '''This method creates Offers from BullDogJobs'''
        
        last_page = 1
        if (response := get(self.__get_offers_url, headers={'User-Agent': 'Mozilla/5.0'})).status_code == 200:
            html = BSoup(response.text, 'html.parser')
            last_page += int(self._get_html_text(html, classname='pagination', by_attr=True, attr='data-total'))
            for listing in html.find_all(class_=compile(r'results-list-item')):
                    offer = self._parse_offer(listing)
                    if offer[3] == '':
                        # If Offer URL was not found, it means that the listing is invalid. Move on to the next listing.
                        continue
                    else:
                        self.offers.append(Offer(*offer))
            for page in range(2, last_page):
                response = get(f'{self.__get_offers_url}{str(page)}', headers={'User-Agent': 'Mozilla/5.0'})
                html = BSoup(response.text, 'html.parser')
                for listing in html.find_all(class_=compile(r'results-list-item')):
                    offer = self._parse_offer(listing)
                    if offer[3] == '':
                        # If Offer URL was not found, it means that the listing is invalid. Move on to the next listing.
                        continue
                    else:
                        self.offers.append(Offer(*offer))
    
        return f'Created {len(self.offers)} offers.'


    def _parse_offer(self, offer):         
        ''' This method extracts all the necessary information from HTML element to create a Offer object.
            It returns a tuple, sorted according to the Offer Class API. '''

        title = self._get_html_text(offer, classname='result-header-name')
        company = self._get_html_text(offer, classname='pop-black desktop')
        city = self._get_html_text(offer, classname='pop-mobile')
        salary = self._get_html_text(offer, classname='pop-green')
        experience = [] # No experiance information avaliable
        techstack = self._get_html_text(offer, classname='btn btn-sm btn-default nohover', multiple=True)
        offerurl = self._get_html_text(offer, classname='result-header-name', by_attr=True, attr='href')
        logourl = self._get_html_text(offer, classname='logo-img', by_attr=True, attr='src')
        
        return title, company, city, offerurl, salary, techstack, experience, logourl
   

    def _get_html_text(self, html, classname, by_attr=False, multiple=False, attr=''):
        ''' Given an bs4.element.Tag object from BeautifulSoup, it extracts raw text or specified HTML attribute.
            If your element contains more than one object, set multiple=True and you'll receive a list of strings.
            If the specified element doesn't exist you'll receive an empty string '''
        try:
            if by_attr:
                return html.find(class_=classname)[attr]

            if multiple:
                return [elem.text.strip() for elem in html.find_all(class_=classname)]

            return html.find(class_=classname).text.strip()

        except AttributeError:
            return ''
        except TypeError:
            return ''


x = BullDogJobs()
x.create_offers()
pass