user = 'confluent2'
pwd = 'confluent2'
db_name = 'default'
host = 'localhost'
port = '3307'


from sqlalchemy import create_engine, Column, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Connect to the database
engine = create_engine(f"mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{db_name}")

# ORM Base
Base = declarative_base()

# ORM Model for ticker_ethusdt
class TickerEthusdt(Base):
    __tablename__ = 'ticker_ethusdt'

    id = Column(Integer, primary_key=True, autoincrement=True)
    closeTime = Column(DateTime, nullable=False)
    count = Column(Float, nullable=False)
    firstId = Column(Float, nullable=False)
    highPrice = Column(Float, nullable=False)
    lastId = Column(Float, nullable=False)
    lastPrice = Column(Float, nullable=False)
    lowPrice = Column(Float, nullable=False)
    openPrice = Column(Float, nullable=False)
    openTime = Column(DateTime, nullable=False)
    priceChange = Column(Float, nullable=False)
    priceChangePercent = Column(Float, nullable=False)
    quoteVolume = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    weightedAvgPrice = Column(Float, nullable=False)

# Create the table in the database
Base.metadata.create_all(engine)


data = get_data()
# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert data into the table using ORM
ticker_entry = TickerEthusdt(**data)
session.add(ticker_entry)
session.commit()

# Close the session
session.close()
