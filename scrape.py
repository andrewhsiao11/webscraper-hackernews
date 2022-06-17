import requests
from bs4 import BeautifulSoup
# print nicely to terminal
import pprint

# can decide how many pages of site to scrape with range
def get_page_info(numPages):
    links = []
    subtext = []
    for page in range(1, numPages+1):
        res = requests.get('https://news.ycombinator.com/news?p=' + str(page))
        # turn this data into html object that we can use (can return tags in a list form)
        soup = BeautifulSoup(res.text, 'html.parser')
        # soup.select() allows access using CSS selectors (like .class or #id)
        links += soup.select(".titlelink")
        subtext += soup.select(".subtext")
    return links, subtext


def sort_stories_by_votes(hnlist):
    # telling sorted what we want to sort by in dict
    return sorted(hnlist, key=lambda key: key["votes"], reverse=True)

# get title and link that has at least 100 votes("points")
def curate_hackernews(numPages=1):
    links, subtext = get_page_info(numPages)
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        # second param is default if no href
        href = item.get('href', None)
        # get the ele with class = score which is where votes are contained
        # .select() always returns a list even if one element
        vote = subtext[idx].select(".score")
        # will return a list with ele inside if it exists (i.e. if the post has at least 1 vote)
        if len(vote):
            # get integer val of points
            points = int(vote[0].getText().replace(" points", ""))
            if points > 99:
                # put into dict of {title, link}
                hn.append({'title': title, "link": href, "votes": points})
    return sort_stories_by_votes(hn)


pprint.pprint(curate_hackernews(2))
