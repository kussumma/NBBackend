# NanoBeepa Backend

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Modules](#modules)
- [Features](#features)
- [API Docs](#api-docs)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

These instructions will help you set up and run the project on your local machine.

### Prerequisites

Before you begin, ensure you have met the following requirements:
- Python (version 3.11.x)
- [Poetry](https://pypi.org/project/poetry/)
- MySQL/MariaDB or PostgreSQL (require re-configuration)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/fokusuma/NBBackend.git
   ```

2. Install package:
    ```bash
    poetry install
    ```

3. Copy and fill the env
    ```bash
    cp .env.example .env
    ```

4. Run makemigrations
    ```bash
    python manage.py makemigrations
    ```

5. Run migration
    ```bash
    python manage.py migrate
    ```

6. Load all fixtures (per module, product as example)
    ```bash
    python manage.py loaddata fixtures/product/*.json
    ```

7. Create superuser
    ```bash
    python manage.py createsuperuser
    ```

8. Run the server on localhost:8000 (important: follow the frontend domain)
    ```bash
    python manage.py runserver localhost:8000
    ```

9. Go to [Django admin page](http://localhost:8000/admin)

10. Input or import all required master data (important: shipping routes)

## Modules
Coming soon

## Features
Coming soon

## API Docs
Coming Soon

## Contributing
Coming Soon

## License
Coming Soon



