import pandas as pd
import isbnlib
from newspaper import Article
import matplotlib.pyplot as plt
plt.style.use('ggplot')
from progressbar import ProgressBar
import re
import goodreads_api_client as gr

goodreads = pd.read_csv('/Users/ngohoanganh/Desktop/Goodreads Kaggle project/books.csv', error_bad_lines = False)

client = gr.Client(developer_key= 'fgwnppR6Q1wpFt0n6umUQ') #API given in the reference notebook on Kaggle

def html(isbn):
    url = 'https://isbndb.com/book/'+isbn
    article = Article(url)
    article.download()
    article.parse()
    ar = article.html
    ar = ar[9300:9900]
    return ar

def reg(l):
    return re.search(r'(\b\d{4})\b',l).groups()[0]
    
def bookdata(df):
    year=[]
    pbar = ProgressBar()
    for isbn in pbar(df.isbn13):
        try:
            details = isbnlib.meta(isbn)
            year.append(details['Year'])
        except :
            try: 
                book_detail = client.Book.show_by_isbn(isbn)
                keys_wanted = ['publication_year']
                reduced_book = {k:v for k,v in book_detail.items() if k in keys_wanted}
                year.append((reduced_book['publication_year']))
            
            except: 
                try:
                    y = html(isbn)
                    year_extracted = reg(y) 
                    year.append(y)
                except:
                    year.append('0')
                
    return year

def new_data(df):
    year = bookdata(df)
    year_df = pd.DataFrame(year, columns=['Year'])
    new_df = df.join(year_df)
    new_df.dropna(0, inplace=True)
    new_df = new_df[new_df['Year'].str.isnumeric()]
    new_df = new_df[new_df.Year !='0']
    return new_df

goodreads_year = new_data(goodreads)

goodreads_year.to_csv('/Users/ngohoanganh/Desktop/Goodreads Kaggle project/goodreads_year.csv', sep=',', encoding = 'UTF-16', index = False)





