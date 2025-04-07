from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



#  Initialize the database called inventory.db
engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


# Create a class called Product that passes in Base, which maps our model to the database
# set the table and columns in the table
# Strings are passed into each column to override how the column names are displayed in the database
# __repr__ sets format for product information
class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column('Product Name', String)
    product_price = Column('Price', Integer)
    product_quantity = Column('Quantity', Integer)    
    date_updated = Column('Date Updated', Date)

    def __repr__(self):
        return f'Product Name: {self.product_name} Quantity: {self.product_quantity} Price: {self.product_price} Updated: {self.date_updated}'
