import json
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

def load_config():
    with open('config.json', 'r') as file:
        data = json.load(file)
    return data

def bd():
    data = load_config()
    db_information = data['bd']
    bd_type= db_information['bd_type']
    user= db_information["user"]
    pastword= db_information["pastword"]
    host= db_information["host"]
    port= db_information["port"]
    name= db_information["name"]

    return f"{bd_type}://{user}:{pastword}@{host}:{port}/{name}"




Base = declarative_base()
data = load_config()
type1 = data['table']["product_type"]
class ProductType(Base):
    __tablename__ = type1[0]
    id = Column(eval(type1[1]['id']["type"]), primary_key=True)
    name = Column(eval(type1[1]['name']["type"])(type1[1]['name']["count"]))

type2 = data['table']["product_gender"]
class ProductGender(Base):
    __tablename__ = type2[0]
    id = Column(eval(type2[1]['id']["type"]), primary_key=True)
    name = Column(eval(type2[1]['name']["type"])(type2[1]['name']["count"]))
type3 = data['table']["product_size"]
class ProductSize(Base):
    __tablename__ = type3[0]
    id = Column(eval(type3[1]['id']["type"]), primary_key=True)
    name = Column(eval(type3[1]['name']["type"])(type3[1]['name']["count"]))

product = data['table']["product"]
class Product(Base):
    __tablename__ = product[0]
    id = Column(eval(product[1]['id']["type"]), primary_key=True)
    name = Column(eval(product[1]['name']["type"])(product[1]['name']["count"]))
    type = Column(eval(product[1]['type']["type"]), ForeignKey(product[1]['type']["ForeignKey"]))
    gender = Column(eval(product[1]['gender']["type"]), ForeignKey(product[1]['gender']["ForeignKey"]))
    size = Column(eval(product[1]['size']["type"]), ForeignKey(product[1]['size']["ForeignKey"]))
    price = Column(eval(product[1]['price']["type"]))
customer=data['table']["customer"]
class Customer(Base):
    __tablename__ = customer[0]
    id = Column(eval(customer[1]['id']["type"]), primary_key=True)
    name = Column(eval(customer[1]['name']["type"])(customer[1]['name']["count"]))
    surname = Column(eval(customer[1]['surname']["type"])(customer[1]['surname']["count"]))
    mail = Column(eval(customer[1]['mail']["type"])(customer[1]['mail']["count"]))
    phone = Column(eval(customer[1]['phone']["type"]))
    adres = Column(eval(customer[1]['adres']["type"])(customer[1]['adres']["count"]))

purchase=data['table']["purchase"]
class Purchase(Base):
    __tablename__ = purchase[0]
    id = Column(eval(purchase[1]['id']["type"]), primary_key=True)
    date_order = Column(eval(purchase[1]['date_order']["type"]))
    id_customer = Column(eval(purchase[1]['id_customer']["type"]), ForeignKey(purchase[1]['id_customer']["ForeignKey"]))
    discount = Column(eval(purchase[1]['discount']["type"]))

purchase_list=data['table']["purchase_list"]
class PurchaseList(Base):
    __tablename__ = purchase_list[0]
    id = Column(eval(purchase_list[1]['id']["type"]), primary_key=True)
    id_purchase = Column(eval(purchase_list[1]['id_purchase']["type"]), ForeignKey(purchase_list[1]['id_purchase']["ForeignKey"]))
    id_product = Column(eval(purchase_list[1]['id_product']["type"]), ForeignKey(purchase_list[1]['id_product']["ForeignKey"]))
    count_product = Column(eval(purchase_list[1]['count_product']["type"]))



class Data:
    url=bd()
    engine = create_engine(url)
    # print(url)
    Base.metadata.create_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()




# Base = declarative_base()
# class ProductType(Base):
#     __tablename__ = 'product_type'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#
# class ProductGender(Base):
#     __tablename__ = 'product_gender'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#
# class ProductSize(Base):
#     __tablename__ = 'product_size'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#
# class Customer(Base):
#     __tablename__ = 'customer'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#     surname = Column(String(100))
#     mail = Column(String(100))
#     phone = Column(Integer)
#     adres = Column(String(200))
# class Product(Base):
#     __tablename__ = 'product'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(100))
#     type = Column(Integer, ForeignKey('product_type.id'))
#     gender = Column(Integer, ForeignKey('product_gender.id'))
#     size = Column(Integer, ForeignKey('product_size.id'))
#     price = Column(Float)
# class Purchase(Base):
#     __tablename__ = 'purchase'
#     id = Column(Integer, primary_key=True)
#     date_order = Column(DateTime)
#     id_customer = Column(Integer, ForeignKey('customer.id'))
#     discount = Column(Float)
# class PurchaseList(Base):
#     __tablename__ = 'purchase_list'
#     id = Column(Integer, primary_key=True)
#     id_purchase = Column(Integer, ForeignKey('purchase.id'))
#     id_product = Column(Integer, ForeignKey('product.id'))
#     count_product = Column(Integer)