from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from FIFAscrape.items import PlayerItem
from urlparse import urlparse, urljoin
from scrapy.http.request import Request
from scrapy.conf import settings
import random
import time

class fifaSpider(Spider):
    name = "fifa"
    allowed_domains = ["futhead.com"]
    start_urls = [
        "http://www.futhead.com/16/players/?level=all_nif&bin_platform=ps"
    ]
	

    def parse(self, response):
        #obtains links from page to page and passes links to parse_playerURL
        sel = Selector(response)    #define selector based on response object (points to urls in start_urls by default) 
        url_list = sel.xpath('//a[@class="display-block padding-0"]/@href')   #obtain a list of href links that contain relative links of players
        for i in url_list:
            relative_url = self.clean_str(i.extract())    #i is a selector and hence need to extract it to obtain unicode object
            print urljoin(response.url, relative_url)   #urljoin is able to merge absolute and relative paths to form 1 coherent link
            req = Request(urljoin(response.url, relative_url),callback=self.parse_playerURL)   #pass on request with new urls to parse_playerURL
            req.headers["User-Agent"] = self.random_ua()    
            yield req
        
        next_url=sel.xpath('//div[@class="right-nav pull-right"]/a[@rel="next"]/@href').extract_first()  
        if(next_url):                                                                       #checks if next page exists
            clean_next_url = self.clean_str(next_url)
            reqNext = Request(urljoin(response.url, clean_next_url),callback=self.parse)    #calls back this function to repeat process on new list of links
            yield reqNext
         
    def parse_playerURL(self, response):    
        #parses player specific data into items list
        site = Selector(response)
        items = []
        item = PlayerItem()
        item['1name'] = (response.url).rsplit("/")[-2].replace("-"," ")
        title = self.clean_str(site.xpath('/html/head/title/text()').extract_first())
        item['OVR'] = title.partition("FIFA 16 -")[1].split("-")[0]
        item['POS'] = self.clean_str(site.xpath('//div[@class="playercard-position"]/text()').extract_first())
        #stats = site.xpath('//div[@class="row player-center-container"]/div/a')
        stat_names = site.xpath('//span[@class="player-stat-title"]')
        stat_values = site.xpath('//span[contains(@class, "player-stat-value")]')
        for index in range(len(stat_names)):
            attr_name = stat_names[index].xpath('.//text()').extract_first()
            item[attr_name] = stat_values[index].xpath('.//text()').extract_first()
        items.append(item)
        return items
        
    def clean_str(self,ustring):    
        #removes wierd unicode chars (/u102 bla), whitespaces, tabspaces, etc to form clean string 
        return str(ustring.encode('ascii', 'replace')).strip()
        
    def random_ua(self):
        #randomise user-agent from list to reduce chance of being banned
        ua  = random.choice(settings.get('USER_AGENT_LIST'))
        if ua:
            ua='Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36'
        return ua
        
