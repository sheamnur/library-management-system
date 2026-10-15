# Library Management System

A Library Management System built with Python, Flask, and PostgreSQL. This project provides REST API endpoints for managing books and members, with database operations handled through Psycopg.

## Features

- **Book Management:** Add, view, search by ID, update, and delete books.
- **Book Availability:** View books that are currently available.
- **Member Management:** Register, view, search by ID, update, and delete members.
- **Category Management:** Organize books by category.
- **Database Integration:** Store and retrieve data using PostgreSQL.
- **Input Validation:** Validate incoming JSON data and handle invalid input.
- **Error Handling:** Handle database errors and return appropriate API responses.
- **Environment Configuration:** Load database credentials from a `.env` file.

## Technologies Used

- Python
- Flask
- PostgreSQL
- Psycopg
- python-dotenv

## Setup

1. Clone this repository:

   git clone https://github.com/sheamnur/library-management-system.git
   cd library-management-system


2. Create and activate a virtual environment (recommended):

   python -m venv .venv


3. Install the required packages:

   pip install Flask "psycopg[binary]" python-dotenv


4. Create a PostgreSQL database and execute the SQL commands to create the required tables.

5. Create a `.env` file in the project root and add your database password:

   DB_PASSWORD=your_database_password


6. Configure the database connection settings in `database.py` if needed.

7. Run the application:

   python app.py

## Note

This is an educational project that is actively being developed. Features and implementation may change as the project progresses.