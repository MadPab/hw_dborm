from sqlalchemy import *
from sqlalchemy.orm import *

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    books = relationship("Book", back_populates="publisher")

class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)

    publisher = relationship("Publisher", back_populates="books")
    stocks = relationship("Stock", back_populates="book")

class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)

    stocks = relationship("Stock", back_populates="shop")

class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)

    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop", back_populates="stocks")
    sales = relationship("Sale", back_populates="stock")

class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Numeric(10, 2), nullable=False)
    date_sale = Column(Date, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False)

    stock = relationship("Stock", back_populates="sales")

DATABASE_URL = 'postgresql://postgres:123@localhost:5432/bookstore'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


# new_publisher = Publisher(name="Пушкин")
# new_book = Book(title="Капитанская дочка", publisher=new_publisher)
# new_shop = Shop(name="Буквоед")
# new_stock = Stock(book=new_book, shop=new_shop, count=10)
# new_sale = Sale(stock=new_stock, price=600, date_sale='26-10-2022', count=1)

# session.add(new_publisher)
# session.add(new_book)
# session.add(new_shop)
# session.add(new_stock)
# session.add(new_sale)
# session.commit()

publisher_name = input("Введите имя автора\издателя: ")

results = session.query(
    Book.title,
    Shop.name,
    Sale.price,
    Sale.date_sale
).select_from(Book).join(
    Stock, Stock.id_book == Book.id
).join(
    Publisher, Publisher.id == Book.id_publisher
).join(
    Sale, Sale.id_stock == Stock.id
).join(
    Shop, Shop.id == Stock.id_shop
).filter(Publisher.name == publisher_name).all()


for title, shop_name, price, date_sale in results:
    print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")

session.close()
