# Silene

Silene is an open source web crawler framework built upon [Pyppeteer](https://github.com/pyppeteer/pyppeteer).

## Getting started

Each crawler must subclass the `Crawler` class and implement the abstract `configure` method. The `CrawlerConfiguration`
specifies the initial requests to make and other properties of the crawler. Once a request is processed, the appropriate
callback will be invoked. By default, in case of a successful request the
`on_response_success` callback will be executed. This is where you can interact with the page content. You can also
specify custom callbacks for your requests.

Below you can find a very simple implementation.

### Example code snippet

```python
from silene.crawl_request import CrawlRequest
from silene.crawl_response import CrawlResponse
from silene.crawler import Crawler
from silene.crawler_configuration import CrawlerConfiguration


class MyCrawler(Crawler):
    def configure(self) -> CrawlerConfiguration:
        return CrawlerConfiguration([CrawlRequest('https://example.com')])

    def on_response_success(self, response: CrawlResponse) -> None:
        # Do something with the response...
        pass
```

## Development instructions

### Prerequisite

This project requires [Pipenv](https://docs.pipenv.org/) to be installed.

### Create environment

Run `pipenv install --dev` to create a new virtual environment and install the necessary packages.

### Run tests

Run `pytest` in the project root folder.

### Run tests with coverage

Run `pytest --cov=silene` in the project root folder.

## License

The source code of Silene is made available under
the [Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0).
