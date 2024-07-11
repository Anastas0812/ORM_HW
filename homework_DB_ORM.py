import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
driver = config['Driver']['driver']
login = config['Log']['login']
password = config['Passw']['password']
host = config['Host']['host']
db = config['DataBase']['db']

DSN = f"{driver}://{login}:{password}@localhost:{host}/{db}"

engine = sqlalchemy.create_engine(DSN)
create_tables(engine)
Session = sessionmaker(bind=engine)
session = Session()

publisher_1 = Publisher(name='Уильям', surname='Шекспир')
publisher_2 = Publisher(name='Александр Сергеевич', surname='Пушкин')
book_1 = Book(title='Ромео и Джульетта', publisher=publisher_1)
book_2 = Book(title='Оттело', publisher=publisher_1)
book_3 = Book(title='Капитанская дочка', publisher=publisher_2)
book_4 = Book(title='Руслан и Людмила', publisher=publisher_2)
book_5 = Book(title='Евгений Онегин', publisher=publisher_2)
shop_1 = Shop(name='ЛитреС')
shop_2 = Shop(name='Читай-город')
shop_3 = Shop(name='Буквоед')
shop_4 = Shop(name='Лабиринт')
shop_5 = Shop(name='Книжный дом')
stock_1 = Stock(book=book_1, shop=shop_1)
stock_2 = Stock(book=book_2, shop=shop_2)
stock_3 = Stock(book=book_3, shop=shop_3)
stock_4 = Stock(book=book_4, shop=shop_3)
stock_5 = Stock(book=book_3, shop=shop_4)
stock_6 = Stock(book=book_5, shop=shop_5)
stock_7 = Stock(book=book_3, shop=shop_3)
sale_1 = Sale(price='999', date_sale='2024-01-01', stock=stock_1, count='12')
sale_2 = Sale(price='850', date_sale='2024-01-13', stock=stock_2, count='14')
sale_3 = Sale(price='600', date_sale='2022-11-09', stock=stock_3, count='10')
sale_4 = Sale(price='500', date_sale='2022-11-08', stock=stock_4, count='9')
sale_5 = Sale(price='580', date_sale='2022-11-05', stock=stock_5, count='22')
sale_6 = Sale(price='490', date_sale='2022-11-02', stock=stock_6, count='9')
sale_7 = Sale(price='600', date_sale='2022-10-26', stock=stock_7, count='3')

session.add_all([publisher_1, publisher_2, book_1, book_2, book_3, book_4, book_5, shop_1, shop_2, shop_3, shop_4, shop_5, stock_1, stock_2, stock_3, stock_4, stock_5, stock_6, stock_7, sale_1, sale_2, sale_3, sale_4, sale_5, sale_6, sale_7])
session.commit()
surnames = []
list_p = session.query(Publisher.surname)
for p in list_p:
    surnames.append(', '.join(p))
input_publisher = input('Введите фамилию автора: ')
if input_publisher in surnames:
    result = (session.query(Book).with_entities(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher, Publisher.id == Book.id_publisher).join(Stock, Stock.id_book == Book.id).join(Shop, Shop.id == Stock.id_shop).join(Sale, Sale.id_stock == Stock.id).filter(Publisher.surname == input_publisher).all())
    for book_title, shop_name, price, date_ in result:
        print(f'{book_title} | {shop_name} | {price} | {date_}')
else:
    print('Пока книг этого автора нет в наличии')

session.close()
