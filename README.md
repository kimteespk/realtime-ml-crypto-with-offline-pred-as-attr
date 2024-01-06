- Create a file named "config.ini" at root directory for database connection configuration

[DB]
user = your_db_user
pwd = your_db_password
db_name = your_db_name
host = your_db_host (eg localhost)
port = your_db_port (eg 3307)


- Build Docker environment using docker-compose.uml
- Run cmd to install libs "pip install -r requirements. txt"


# Project Name

Brief description or overview of the project.

## Table of Contents

- [Database Configuration](#database-configuration)
- [Docker Environment](#docker-environment)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Database Configuration

1. Create a file named `config.ini` at the root directory for database connection configuration.

   ```ini
   [DB]
   user = your_db_user
   pwd = your_db_password
   db_name = your_db_name
   host = your_db_host (e.g., localhost)
   port = your_db_port (e.g., 3306)


## Docker Environemnt
1. Run docker-compose up -d
