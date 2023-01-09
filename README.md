# Search Engine

## Authors

Ryan Wang and John Lu

## Description

This application scrapes websites and allows you to search with query to find ten most similar pages from your the crawled

## Executable Files

Executable files in this program include our code, librabry code and test code

### Our Code
- crawler.py
- searchdata.py
- search.py

### Librabry Code
- webdev.py
- testingtools.py
- matmult.py

### Test Code
- fruits-all-test.py
- fruits-idf-test.py
- fruits-incoming-links-test.py
- fruits-outgoing-links-test.py
- fruits-page-rank-test.py
- fruits-search-test.py
- fruits-tf-test.py
- fruits-tfidf-test.py

> ... and other tests which replace 'fruits' with 'fruits2'/'fruits3'/'fruits4'/'fruits5'/'tinyfruits'

## How to Use this Project?

### Approach 1 - search based on the websites you want

1. Include Our Code and Librabry Code to your project and import crawler and search modules: `$ import crawler, search`

2. Run the crawler with the website you want: `$ crawler.crawl('[the website you want to crawl]')`

3. Start the search with the query and whether considering page rank in your search. You will receive a list of most likely pages by running the following code: `$ print(search.search('[the search query]', True/False))`

### Approach 2 - search based on the websites provided (run tests)

1. In the command line, while you are in the project directory, run the 'fruits-all-test' test or any other test in Test Code: `$ python3 fruits-all-test.py`

2. Check with the output text files to tell whether the crawling and the search is succssful