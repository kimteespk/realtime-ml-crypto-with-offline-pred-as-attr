
USE default;

GRANT ALL PRIVILEGES ON `default`.* TO '%'@'%';

GRANT ALL PRIVILEGES ON `default`.* TO 'confluent2'@'%';

CREATE TABLE ticker_ethusdt (
    closeTime INTEGER,
    count DOUBLE,
    firstId DOUBLE,
    highPrice DOUBLE,
    lastId DOUBLE,
    lastPrice DOUBLE,
    lowPrice DOUBLE,
    openPrice DOUBLE,
    openTime INTEGER,
    priceChange DOUBLE,
    priceChangePercent DOUBLE,
    quoteVolume DOUBLE,
    volume DOUBLE,
    weightedAvgPrice DOUBLE
);
