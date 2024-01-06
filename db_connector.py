
from sqlalchemy import create_engine, text, Column, Float, Integer, Double
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker




def my_engine(user= 'confluent2', pwd= 'confluent2', host= 'localhost', port= '3307', db_name= 'default'):
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


def db_insert(data, engine= None, Base= Base):
    if engine == None:
        engine = my_engine()
    # Create the table in the database
    Base.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Insert data into the table using ORM
    ticker_entry = TickerEthusdt(**data)
    session.add(ticker_entry)
    session.commit()

    # Close the session
    session.close()
    print('insert data to table complete')

    
if __name__ == '__main__':

    from get_ticker import get_data
    
    # table_name = 'ticker_ethusdt'


    data = get_data()
    db_insert(data)
    column, lst_row = db_select(table_name)
    print(len(lst_row))

