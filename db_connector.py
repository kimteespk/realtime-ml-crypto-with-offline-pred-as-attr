
from sqlalchemy import create_engine, text, Column, Float, Integer, Double, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
cfg = config['DB']
user = cfg['user']
pwd = cfg['pwd']
db_name = cfg['db_name']
host = cfg['host']
port = cfg['port']


# def my_engine(user= 'confluent2', pwd= 'confluent2', host= 'localhost', port= '3307', db_name= 'default'):
def my_engine(user= user, pwd= pwd, host= host, port= port, db_name= db_name):
    # Connect to the database
    engine = create_engine(f"mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{db_name}")
    return engine




def db_select(table_name, engine= None):
    if engine == None:
        engine = my_engine()

    connection = engine.connect()
    # Execute a SQL query using text
    query = text(f'SELECT * FROM {table_name}')
    result = connection.execute(query)
    keys= result.keys()
    # Fetch the results
    rows = result.fetchall()

    # Close the connection
    connection.close()
    
    return keys._keys ,rows
    



# ORM Base
Base = declarative_base()

# ORM Model for ticker_ethusdt
class TickerEthusdt(Base):
    __tablename__ = 'ticker_ethusdt'

    id = Column(Integer, primary_key=True, autoincrement=True)
    closeTime = Column(Integer, nullable=False)
    count = Column(Float, nullable=False)
    firstId = Column(Float, nullable=False)
    highPrice = Column(Float, nullable=False)
    lastId = Column(Float, nullable=False)
    lastPrice = Column(Float, nullable=False)
    lowPrice = Column(Float, nullable=False)
    openPrice = Column(Float, nullable=False)
    openTime = Column(Integer, nullable=False)
    priceChange = Column(Float, nullable=False)
    priceChangePercent = Column(Float, nullable=False)
    quoteVolume = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    weightedAvgPrice = Column(Float, nullable=False)
    
class OhlcvETH(Base):
    __tablename__ = 'ohlcv_ethusdt'
    # print('\n\nCONNECT :', __tablename__)
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(BigInteger, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    
class OhlcvBNB(Base):
    __tablename__ = 'ohlcv_bnbusdt'
    # print('\n\nCONNECT :', __tablename__)
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(BigInteger, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)




def db_insert(data, engine= None, Base= Base, ORMclass= TickerEthusdt):
    if engine == None:
        engine = my_engine()
    # Create the table in the database
    Base.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    try:

        # Insert data into the table using ORM
        if isinstance(data, dict):
            ticker_entry = ORMclass(**data)
            session.add(ticker_entry)
            count = 1
        elif isinstance(data, list):
            # [session.add(ORMclass(**x)) for x in data]
            for dct_data in data:
                entry = ORMclass(**dct_data)
                session.add(entry)
                # [session.add(ORMclass(**x)) for x in data]
            count = len(data)

        session.commit()
        print(f'\n\ninsert data {count} records to table {ORMclass.__tablename__} complete')
    
    except Exception as e:
        print('\n\n Error inserting data :{e}')
    
    finally:
        # Close the session
        session.close()
    
    



    

    
if __name__ == '__main__':

    from get_ticker import get_data
    
    # table_name = 'ticker_ethusdt'


    data = get_data()
    db_insert(data)
    column, lst_row = db_select(table_name)
    print(len(lst_row))

