import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
from IPython.display import display, Image

total_pages = int(input('How many pages to scrape: '))
books_data = pd.DataFrame(columns = ['title','book_cover_url','price','description','upc_id','product_type','availability','reviews'])


# for web pages number a loop is given
for index in range(1,total_pages + 1):
    url = 'https://books.toscrape.com/catalogue/page-'+ str(index) +'.html'
    response = requests.get(url)
    book_tags = BeautifulSoup(response.text, 'html.parser')

    # find all list of books info on one web page
    info = book_tags.find_all('article', class_ = 'product_pod')

    books_lists = []
    
    # fetch the books information
    for i in range(len(info)):
        book_url = title_tags = info[i].select('h3 a')[0].attrs['href']
        
        # open the specific book url
        book_url_response = requests.get('https://books.toscrape.com/catalogue/' + book_url)
        
        # create a parser for a single book titled url
        get_book_tags = BeautifulSoup(book_url_response.text,'html.parser')
        get_info = get_book_tags.find_all('article', class_ = 'product_page')

        # book title
        book_title = get_info[0].select('h1')[0].text
        print(book_title)

        # book img url
        book_img = get_info[0].select('img')[0].attrs['src']
        book_cover_url = book_img.replace('../../', 'https://books.toscrape.com/')

        # book price
        book_price = get_info[0].select('.price_color')[0].text

        # book description
        book_description = get_info[0].select('p')[3].text

        book_info = get_info[0].select('table td')
        book_upc = book_info[0].text
        book_product_type = book_info[1].text
        book_availibility = book_info[5].text
        book_reviews = book_info[6].text

        book = [book_title, book_cover_url, book_price, book_description,\
                           book_upc, book_product_type, book_availibility, book_reviews]
        
        books_data.loc[len(books_data)] = book



books_data.to_csv('Books.csv')
    
    
