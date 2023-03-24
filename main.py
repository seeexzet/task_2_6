import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publiser(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    # books = relationship("", back_populates="publisers")

class Bookk(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisers = relationship(Publiser, backref="books")
    #publisers = relationship(Publiser, back_populates="books")

class Shop(Base):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=40), nullable=False)

class Sale(Base):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.String(length=12))
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer)

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)

    books2 = relationship(Bookk, backref="stocks")
    shops = relationship(Shop, backref="stocks2")
    sales = relationship(Sale, backref="stock3")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


DSN = "postgresql://postgres:387987@localhost:5432/task6_db" # строка подключения к источнику данных
engine = sqlalchemy.create_engine(DSN) # движок-абстракция, который может подключиться
create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()

# создание объектов
push = Publiser(name="Пушкин")

kd = Bookk(title="Капитанская дочка", publisers=push)
ril = Bookk(title="Руслан и Людмила", publisers=push)
eo = Bookk(title="Евгений Онегин", publisers=push)

bkv = Shop(title="Буквоед")
lbr = Shop(title="Лабиринт")
knd = Shop(title="Книжный дом")

kd1 = Stock(count = 1, books2=kd, shops = bkv)
ril1 = Stock(count = 1, books2=ril, shops = bkv)
kd2 = Stock(count = 1, books2=kd, shops = lbr)
eo1 = Stock(count = 1, books2=kd, shops = knd)

sale_kd1_1 = Sale(price = 600, date_sale='09-11-2022', stock3 = kd1)
sale_ril = Sale(price = 500, date_sale='08-11-2022', stock3 = ril1)
sale_kd2 = Sale(price = 580, date_sale='05-11-2022', stock3 = kd2)
sale_eo = Sale(price = 490, date_sale='02-11-2022', stock3 = eo1)
sale_kd1_2 = Sale(price = 600, date_sale='26-10-2022', stock3 = kd1)

session.add_all([push, kd, ril, eo, bkv, lbr, knd, kd1, ril1, kd2, eo1, sale_kd1_1, sale_ril, sale_kd2, sale_eo, sale_kd1_2])
session.commit() # фиксируем изменения
print(push.id)
print(kd.id)

# запросы
 
q = session.query(Bookk.title, Shop.title, Sale.price, Sale.date_sale).join(Publiser).join(Stock).join(Shop).join(Sale).filter(Publiser.name == 'Пушкин')
print(q)

for book, shop, price, date_sale in q:
    print(f'| {book} | {shop} | {price} | {date_sale} |')
