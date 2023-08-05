
# Medium module | Created by Markus Urban | 2020

from bs4 import BeautifulSoup

import requests

import json

import logging




def medium_search(query, result = "dict"):


    results = {}

    story = {} # Each individual story
    
    counter = 0


    URL = 'https://medium.com/search?q=' + query

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    articles = soup.find_all(class_='postArticle')


    # Title & Description
    
    for i in articles:

        title = i.find(class_='graf--title')

        title_txt = title.text.replace('\xa0', ' ')

        story["title"] = title_txt

        description = i.find(class_='graf--trailing')

        if title.text != description.text:

            description = description.text.replace('\xa0', ' ')

            story["description"] = description

        else:

            story["description"] = None



        # Author & Collection

        story["collection"] = "undefined" # We set a default value
        
        links = i.findAll(class_="ds-link")

        if links != None:

            for link in links:

                action = link.get("data-action")

                if action == "show-user-card":

                    story["author"] = link.text

                elif action == "show-collection-card":

                    story["collection"] = link.text


        # Claps
        
        claps = i.find(class_='js-actionMultirecommendCount')

        story["claps"] = claps.text


        # Date

        date = i.find("time")

        story["date"] = date.get("datetime")


        # Reading time

        readingtime = i.find("span", class_="readingTime")

        readingtime = readingtime.get("title")

        readingtime = readingtime.replace("min read", "")

        readingtime = int(readingtime)

        story["Readingtime"] = readingtime

        


        # Responses

        responses = i.findAll("a", class_="u-baseColor--buttonNormal")

        responses = responses[1].text

        responses = responses.replace("responses", "")

        responses = int(responses)

        story["responses"] = responses


        # URL

        readmore = i.findAll("a", class_="u-baseColor--buttonNormal")

        readmore = readmore[0]

        if readmore.get("data-action") == "open-post":

                readmore = readmore.get("href")

                story["link"] = readmore


        # Avatar Image

        avatar = i.find("img", class_="avatar-image")

        avatar = avatar.get("src")

        story["avatar"] = avatar



        # Story Image

        image = i.findAll("img")

        if len(image) >= 2:
            
            story["image"] = image[1].get("src")

        else:

            story["image"] = None;

        


       
        exec("results[" + str(counter) + "] = " + str(story))


        # We actualise the article counter

        counter = counter + 1




    if result == "json":

        results = json.dumps(results)

        return results

    elif result == "dict":

        return results

    else:

          logging.warning("Unrecognised result format - should be 'dict' or 'json'", exc_info=False)

    
