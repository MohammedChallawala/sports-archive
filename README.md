# Sports Archive System

This repository contains a Python application and a MySQL database for managing a sports archive.

## Files in the Repository
- `SportsArchive.py`: Python code to interact with the database.
- `db/SpArDatabase.sql`: SQL dump file to recreate the database.

## How to Use
1. Clone this repository:
   ```bash
   git clone https://github.com/MohammedChallawala/sports-archive.git
   cd sports-archive

## Setting Up the Database Connection

Before running the application, open `DBMS_maincode.py` and update the following placeholders with your own database credentials:

```python
DB_HOST = "your_database_host"       # e.g., "localhost"
DB_USER = "your_database_user"       # e.g., "root"
DB_PASSWORD = "your_database_password"  # e.g., "password123"
DB_NAME = "your_database_name"       # e.g., "sports_archive"
DB_PORT = 3306                       # Change if not using default MySQL port
