# importing config data
from config import PATH_DB

# importing library for ORM system
from sqlalchemy import ForeignKey, String, Integer, Column, DateTime,\
     Boolean, Table, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class City(Base):
    __tablename__ = 'city'

    id = Column(Integer, primary_key=True)
    name = Column(String(90), nullable=False)
    warehouses = relationship('Warehouse', back_populates='city')

    def json(self):
        return {'id': self.id, 'name': self.name}


class Warehouse(Base):
    __tablename__ = 'warehouse'

    id = Column(Integer, primary_key=True)
    name = Column(String(90), nullable=False)
    adress = Column(String(90), nullable=False)
    id_city = Column(Integer, ForeignKey('city.id'), nullable=False)
    city = relationship('City', back_populates='warehouses')
    supplyses = relationship('Supply', back_populates='warehouse')


class Supplier(Base):
    __tablename__ = 'supplier'

    id = Column(Integer, primary_key=True)
    name = Column(String(90), nullable=False)
    supplyses = relationship('Supply', back_populates='supplier')
    product = relationship('Product')


class Supply(Base):
    __tablename__ = 'supply'

    id = Column(Integer, primary_key=True)
    date_register = Column(DateTime(timezone=True), server_default=func.now())
    date_delivery = Column(DateTime(timezone=True))
    id_warehouse = Column(Integer, ForeignKey('warehouse.id'), nullable=False)
    id_supplier = Column(Integer, ForeignKey('supplier.id'), nullable=False)
    warehouse = relationship('Warehouse', back_populates='supplyses')
    supplier = relationship('Supplier', back_populates='supplyses')
    is_product = relationship('IsProduct', back_populates='supply')


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(90), nullable=False, unique=True)
    product = relationship('Product')


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String(90), nullable=False, unique=True)
    price = Column(Integer)
    description = Column(String(260))
    category = Column(Integer, ForeignKey('category.id'), nullable=False)
    supplier = Column(Integer, ForeignKey('supplier.id'), nullable=False)
    is_product = relationship(
        'IsProduct', 
        back_populates='product', 
        cascade='all, delete')


class IsProduct(Base):
    __tablename__ = 'is_product'

    id = Column(Integer, primary_key=True)
    number_product = Column(Integer, unique=True, nullable=False)
    id_product = Column(Integer, ForeignKey('product.id'), nullable=False)
    id_supply = Column(Integer, ForeignKey('supply.id'))
    present = Column(Boolean, default=True)
    product = relationship('Product', back_populates='is_product')
    supply = relationship('Supply', back_populates='is_product')
    sales = relationship('Sales', back_populates='is_product', uselist=False)


class ChekForCustomer(Base):
    __tablename__ = 'chek_for_customer'

    id = Column(Integer, primary_key=True)
    datetime_sale = Column(
        DateTime(timezone=True),
        server_default=func.now())
    sales = relationship('Sales', back_populates='chek_for_customer')


class Sales(Base):
    __tablename__ = 'customer'

    id = Column(Integer, primary_key=True)
    id_is_product = Column(Integer, ForeignKey(
        'is_product.id'),
        nullable=False,
        unique=True)
    chek_for_customer_id = Column(Integer,\
     ForeignKey('chek_for_customer.id'), nullable=False)
    chek_for_customer = relationship('ChekForCustomer', back_populates='sales')
    is_product = relationship('IsProduct', back_populates='sales')


def create_models():
    Base.metadata.create_all(bind=create_engine(PATH_DB, echo=True))