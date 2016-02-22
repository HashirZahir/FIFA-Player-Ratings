# FIFA-Player-Ratings

This is a [scrapy](https://github.com/scrapy/scrapy) based tool can extract player statistics from futhead.com. EA has spent lots of money and time crafting individual statistics for thousands of players and these might be the closest representation of player statistics we have to do any analysis. Based on some reviews from websites, it also showed that FIFA Ultimate team player ratings are somewhat close (on average) to real life performance (but of course impossible to be precise). My aim is to provide a tool that can extract this data and make it available to all. Currently, I am only scraping data of non-in-form players (normal players, not legends or some old players) but this code can be easily modified to scrape other lists (mentioned below).

If you are just interested in the player statistics, you can have a look [here](player_stats.jl) (list is still being updated)


# Usage
Install the required packages (if not already installed) such as [pip](https://pip.pypa.io/en/latest/installing/), [setutptools](https://pypi.python.org/pypi/setuptools), [lxml](http://lxml.de/installation.html) and [OpenSSL](https://pypi.python.org/pypi/pyOpenSSL) as mentioned [here](http://doc.scrapy.org/en/latest/intro/install.html). After doing so, you can install Scrapy by typing
`pip install Scrapy` in the terminal.

If you are on Windows, watch this [youtube video](https://www.youtube.com/watch?v=eEK2kmmvIdw) which provides a detailed step by step guide on how to install Scrapy and should not take more than 10 minutes.

After installing Scrapy, you can clone this repo and run  
`scrapy crawl fifa -o player_stats.jl -s JOBDIR=attempt/spider1`  
in the root directory of the project (note: fifa is the name of the spider set in [fifa_spider.py](/FIFAscrape/spiders/fifa_spider.py)). 

An "attempt" directory will be created locally with spider settings to allow pausing and resuming of jobs. To pause the spider, press CRTL+C in the terminal/cmd once and wait for spider to shut down automatically. DO NOT press it twice as it will force shut the spider. To resume crawling, just enter the same command in the root directory again:  
`scrapy crawl fifa -o player_stats.jl -s JOBDIR=attempt/spider1`  
[Here](http://doc.scrapy.org/en/latest/topics/jobs.html) are the relavent scrapy docs for pausing and resuming jobs. 


If there are any issues, please report them or if you would like any additional features, please request them!

# Modifying Player List
Currently, the default start list has been set to [this page](http://www.futhead.com/16/players/?level=all_nif). To scrape through other lists, (for example, the data from [2013](http://www.futhead.com/13/players/?level=all_nif)), just go to the [fifa_spider.py](/FIFAscrape/spiders/fifa_spider.py) and modify the start_urls variable:  
```python
start_urls = [
        "http://www.futhead.com/16/players/?level=all_nif&bin_platform=ps"
    ]
```


# Important notes
1. [player_stats.jl](player_stats.jl) (in progress) contains all the player statistics from [here](http://www.futhead.com/16/players/?level=all_nif&bin_platform=ps)
2. This was run using Python 2.7
3. [JSON line exporter](http://doc.scrapy.org/en/latest/topics/exporters.html#json-with-large-data) setting was used in settings.py to handle large feeds 
4. I have modified it to run in DFS fashion (depth_priority=1) rather than the default BFS
5. [Long delays](http://doc.scrapy.org/en/latest/topics/autothrottle.html) were set for requests and number of concurrent requests are very low

# How it works
http://www.futhead.com/16/players/?level=all_nif contains a list of all normal FIFA 16 players. Each page contains about 40-50 players. My program will scan the html file of this page and take note of all the href attributes (links) of the players and yield a request to parse_playerURL to traverse to that link.

*Note: self.clean_str is a defined function which converts the unicode object to str and strips it of spaces and tab characters*
```python
#in parse function
url_list = sel.xpath('//tbody/tr/td[@class="player"]/a/@href')   #obtain a list of href links that contain relative links of players
        
        for i in url_list:
            relative_url = self.clean_str(i.extract())    
            #i is a selector and hence need to extract it to obtain unicode object and strip it of wierd characters
            req = Request(urljoin(response.url, relative_url),callback=self.parse_playerURL)   
            #pass on request with new urls to parse_playerURL
            yield req
```

Once the request has been yielded, scrapy will process these requests asynchronously (by default). When examining a player url (such as [this](http://www.futhead.com/16/players/26/zlatan-ibrahimovic/)), it will first create an item list which will contain all the player related attributes. The keys for this list (other than the name and overall attribute of player) are generated dynamically from the link. After all the attributes are collected, the list is returned and handled by the [item pipeline](http://doc.scrapy.org/en/latest/topics/item-pipeline.html) and [item exporter](http://doc.scrapy.org/en/latest/topics/exporters.html).

*Note: 1name was used as the key for the name attribute of players so that it would be the first key to populate in the json lines alphabetically.*
```python
#in parse_playerURL function
site = Selector(response)
items = []
item = PlayerItem()
item['1name'] = (response.url).rsplit("/")[-2].replace("-"," ")
title = self.clean_str(site.xpath('/html/head/title/text()').extract_first())
item['OVR'] = title.partition("FIFA")[0].split(" ")[-2]
stats = site.xpath('//div[@class="row player-center-container"]/div/a')
    for stat in stats:
         attr_name = self.clean_str(stat.xpath('.//text()').extract_first())
        item[attr_name] = self.clean_str(stat.xpath('.//div/text()').extract_first())
    
    items.append(item)
    return items
```
After all the players on 1 page have been scraped, the spider checks if a next page attribute exists. If it does, it will create a new request for the next page with a callback to the same parse function.
```python
#in parse function
next_url=sel.xpath('//div[@class="right-nav pull-right"]/a[@rel="next"]/@href').extract_first()  
        if(next_url):   #checks if next page exists
            clean_next_url = self.clean_str(next_url)
            reqNext = Request(urljoin(response.url, clean_next_url),callback=self.parse)    
            #calls back this function to repeat process on new list of links
            yield reqNext
```

# Disclaimer
I have set the spider settings in settings.py such that the load on the futhead.com website will be reduced to an absolute minimum. Moreover, I did not run this spider for extended periods of time to put stress on their server. You are free to tweak any settings to make the scraping faster or slower but proceed cautiously. Recklessly scraping their website could lead to bans from the website or even warnings from your ISP (Internet Service Provider).
