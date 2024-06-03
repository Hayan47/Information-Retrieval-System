# Information Retrieval System

This is an information retrieval system built with Python Django using a Service Oriented Architecture. It uses PostgreSQL as the database backend and Tailwind CSS for styling.

## Features

- Service Oriented Architecture
- PostgreSQL database
- Tailwind CSS for styling

## Requirements

- Python 3.x
- PostgreSQL
- Node.js and npm (for Tailwind CSS)

## Installation

### Clone the Repository

```sh
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### Set Up Virtual Environment

```sh
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies

```sh
pip install -r requirements.txt
```
### Create Database

install PostgreSQL from [this link](https://www.postgresql.org/download/). After installing PostgreSQL, create a database called `mydatabase`, user `postgres`, password `admin` on port `5432`.

### Apply Migrations

```sh
python manage.py migrate
```

### Run the Server

```sh
python manage.py runserver
```



