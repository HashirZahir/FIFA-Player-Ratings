# FIFA-Player-Ratings

This is a [scrapy](https://github.com/scrapy/scrapy) based tool can extract player statistics from futhead.com. EA has spent lots of money and time crafting individual statistics for thousands of players and these might be the closest representation of player statistics we have to do any analysis. Based on some reviews from websites, it also showed that FIFA Ultimate team player ratings are somewhat close (on average) to real life performance (but of course impossible to be precise). My aim is to provide a tool that can extract this data and make it available to all. Currently, I am only scraping data of non-in-form players (normal players, not legends or some old players) but this code can be easily modified to scrape other lists (simply modify start_urls).

# Important notes
1. [player_stats.jl](player_stats.jl) (in progress) contains all the player statistics from [here](http://www.futhead.com/16/players/?level=all_nif&bin_platform=ps)
2. This was run using Python 2.7
3. [JSON line exporter] (http://doc.scrapy.org/en/latest/topics/exporters.html#json-with-large-data) setting was used in settings.py to handle large feeds 
4. I have modified it to run in DFS fashion (depth_priority=1) rather than the default BFS
5. [Long delays](http://doc.scrapy.org/en/latest/topics/autothrottle.html) were set for requests and number of concurrent requests are very low

# Usage
Run "scrapy crawl fifa -o player_stats.jl -s JOBDIR=attempt/spider1" in the root directory of the project. An "attempt" directory will be created locally with spider settings to allow pausing and resuming of jobs. To pause spider, press CRTL+C in the shell/cmd and wait for spider to shut down automatically. DO NOT press it twice as it will force shut the spider. To resume crawling, just enter the same command in the root directory again: "scrapy crawl fifa -o player_stats.jl -s JOBDIR=attempt/spider1". [Here](http://doc.scrapy.org/en/latest/topics/jobs.html) are the relavent scrapy docs. 
If you have no idea what I'm talking about, you can take a look [here](http://doc.scrapy.org/en/master/intro/overview.html) to setup scrapy. 

If there are any issues, please report them or if you would like any additional features, please request them!

# Disclaimer
I have set the spider settings in settings.py such that the load on the futhead.com website will be reduced to an absolute minimum. Moreover, I did not run this spider for extended periods of time to put stress on their server. You are free to tweak any settings to make the scraping faster or slower but proceed cautiously. Recklessly scraping their website could lead to bans from the website or even warnings from your ISP (Internet Service Provider).
