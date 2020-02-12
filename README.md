# WTF! Console POST
Yet another cURL but using JSON files. WTF! could also be used to assert API results

## Demo
[![asciicast](https://asciinema.org/a/300449.svg)](https://asciinema.org/a/300449)

## Prerequisites
Before you continue, ensure you have met the following requirements:

- You have installed Python ^3.6
- You have install poetry

## Installation
```sh
# Clone repository
git clone https://github.com/jabernardo/wtf
cd wtf
# Install dependencies using poetry
poetry install
# Make it install!
make install
# Test
wtf --help
```

## How to use?
1. First you need to create a JSON file containing the details of your request. See `examples` folder for more details.

```json
{
    "label": "Get YCombinator Article",
    "url": "https://hacker-news.firebaseio.com/v0/item/8863.json?print=pretty"
}

```

2. Run application
```sh
wtf -f ycombinator.json
```

## Contibuting to WTF!
To contribute to WTF! Make sure to give a star and forked this repository.

Alternatively see the GitHub documentation on [creating a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## License
The `wtf` is open-sourced software licensed under the [MIT license](http://opensource.org/licenses/MIT).
