Sure, here's a README guide for your Streamlit app:

---

# Candletonia Streamlit App

Welcome to the Candletonia Streamlit App! This guide will help you set up and run the app locally on your machine.

## Prerequisites

Ensure you have the following installed on your machine:
- Python 3.10
- Visual Studio Code
- MySQL (Workbench and MariaDB)

## Installation Steps

### Step 1: Clone the Repository

First, clone the repository to your local machine using Git:

```bash
git clone https://github.com/SSJIORI/Candletonia.git
cd Candletonia
```

### Step 2: Set Up the Virtual Environment

It's a good practice to use a virtual environment for your project. Run the following commands to create and activate a virtual environment:

```bash
python3.10 -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Required Packages

Install the necessary Python packages using pip:

```bash
pip install streamlit mysql-connector-python pandas
```

### Step 4: Set Up the Database

1. Open MySQL Workbench or your preferred MySQL client.
2. Create a new database (e.g., `candletonia_db`).
3. Import the provided SQL file to set up the database schema and entries:

```sql
source path/to/your/sql_file.sql;
```

Replace `path/to/your/sql_file.sql` with the actual path to your SQL file.

### Step 5: Configure Database Connection

Make sure the database connection details in your `CRUD.py` file match your local database configuration:

```python
import mysql.connector

db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'candletonia_db'
}

# Update the connection in CRUD.py accordingly
conn = mysql.connector.connect(**db_config)
```

### Step 6: Run the Streamlit App

To start the app, use the following command in the terminal:

```bash
streamlit run CRUD.py
```

This will open a new tab in your default web browser with the running Streamlit app.

## Usage

Once the app is running, you can interact with the Candletonia database through the Streamlit interface. The app provides functionality to create, read, update, and delete records in the database.

## Troubleshooting

- **Database Connection Issues**: Ensure your MySQL server is running and the connection details in `CRUD.py` are correct.
- **Package Installation Issues**: Ensure you are using Python 3.10 and have activated your virtual environment before installing packages.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

---

Happy coding with Candletonia! If you have any questions or encounter any issues, feel free to open an issue in the repository.
