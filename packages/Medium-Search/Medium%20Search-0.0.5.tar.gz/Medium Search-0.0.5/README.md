# Medium search

![](https://miro.medium.com/max/8978/1*s986xIGqhfsN8U--09_AdA.png)

### Features

- Search for Medium stories
- Get story title, description, link, image, author, claps and more
- Get the results in  JSON format or as a Python Dictionary

## Installation

To install this package, run the following statement on your console
```
pip install medium-search
```

After that, you can import the module in your program using the following statement:
```
from medium-search import medium-search
```


## Basic usage


To search Medium stories, use the `medium_search()` function.

This function requires an argument where you must specify your search query:

```
medium-search("query")
```
You can also define the format of the function result:

| Type | Description                    |
| ------------- | ------------------------------ |
| `json`      | JSON object      |
| `dict`   | Python dictionary (default)     |

To set it, use the `result` argument:

```
medium-search("query", result="json")
```
## The result

The function returns a dictionary that contains the information of each Medium story inside another dictionary. The result is structured like the following:

`{0: {information} , 1: {information}, 2: {information} ... }`

If you want to access the information of the first story, for example, you can use the following code:
```
stories = medium_search("php")
first_story = stories[0]
print(first_story)
```
The result of the code above is going to be something like the following:
```
{'title': 'The Future of PHP', 'description': 'Is it a dead programming language?', 'collection': 'Better Programming', 'author': 'Daan', 'claps': '3.3K', 'date': '2019-08-27T15:28:40.277Z', 'Readingtime': 5, 'responses': 50, 'link': 'https://medium.com/better-programming/does-php-have-a-future-6756f166ba8?source=search_post---------5', 'avatar': 'https://cdn-images-1.medium.com/fit/c/72/72/1*_aBlvaUgbJgSEI2fdRj9MQ.png', 'image': 'https://cdn-images-1.medium.com/fit/t/1600/480/1*DhrEoZfrQ7u1B7JVdKe1jA.png'}
```

From each story, you can get the following information:

| Name | Type | Description |
| ------------- | ------------------------------ |
| `title`      | string      | The title of the story
| `description`   | string     | The description of the story
| `collection`   | string    | The collection of the story
| `author`   | string     | The author of the story
| `claps`   | string    | The number of claps the story has
| `date`   | date     | The publishing date
| `readingtime`   | integer    | The average reading time (in minutes)
| `responses`   | integer    | The number of responses (comments)
| `link`   | string     | The link of the story
| `avatar`   | string     | The link to the profile image of the author
| `image`   |  string    | The link to the article header image

To get any of this items separately, you could use:

```
stories = medium_search("php")
first_story = stories[0]
author = first_story["author"]
print(author)
```
In this case, the ouput of the program would be something like this:

```
Keith Adams
```

## Bugs & Errors

This package is in developement, so I expect to find bugs and errors in some cases. If you find one, you can contact me sending an email to **murbanlavalira()gmail.com**

## License

Feel free to use this package in any of your projects, and to modify it  if you want to. This package is free to use.


