## DeepCrawl Robots.txt live checker

```shell script
> cat urls.txt

https://www.ebay.at/
https://www.ebay.at/adchoice
https://www.ebay.at/sl/sell
https://www.ebay.at/mye/myebay/watchlist
https://www.ebay.at/sch/ebayadvsearch
https://www.ebay.at/sch/Kleidung-Accessoires-/11450/i.html
https://www.ebay.at/sch/Auto-Tuning-Styling-/107059/i.html
https://www.ebay.at/sch/Modeschmuck-/10968/i.html
https://www.ebay.at/sch/Damenschuhe-/3034/i.html
```

```shell script
> cat robots.txt

User-agent: *
Disallow: /sch/
```

```
pip install deepcrawl_robots
```

```python
from deepcrawl_robots import Processor

urls_path = "Path to urls file"
robots_txt_path = "Path to robots.txt file"
processor = Processor(
    user_agent="User agent",
    urls_file_path=urls_path,
    robots_file_path=robots_txt_path
)
```

```shell script
> cat result.txt

https://www.ebay.at/mye/myebay/watchlist,true
https://www.ebay.at/adchoice,true
https://www.ebay.at/,true
https://www.ebay.at/sl/sell,true
https://www.ebay.at/sch/Kleidung-Accessoires-/11450/i.html,false
https://www.ebay.at/sch/ebayadvsearch,true
https://www.ebay.at/sch/Modeschmuck-/10968/i.html,false
https://www.ebay.at/sch/Auto-Tuning-Styling-/107059/i.html,false
https://www.ebay.at/sch/Damenschuhe-/3034/i.html,false
```
