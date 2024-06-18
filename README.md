# Flask Product API

This is a simple Flask application that provides a REST API for managing products in a PostgreSQL database. The application supports retrieving, updating, and deleting products.

## Prerequisites

- Python 3.x
- PostgreSQL
- `pip` package manager

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/flask-product-api.git
    cd flask-product-api
    ```

2. **Create and activate a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install flask psycopg2-binary configparser
    ```

4. **Set up PostgreSQL:**

    - Create the database:

        ```sql
        CREATE DATABASE products;
        ```

    - Create the table:

        ```sql
        CREATE TABLE product (
            product_ID SERIAL PRIMARY KEY,
            product_Name VARCHAR(100) NOT NULL,
            price FLOAT NOT NULL
        );
        ```

    - Insert some sample data:

        ```sql
        INSERT INTO products (product_Name, price) VALUES
        ('Product 1', 100.0),
        ('Product 2', 200.0),
        ('Product 3', 300.0);
        ```

5. **Create the configuration file:**

   Create a file named `config.ini` in the project root with the following content:

    ```ini
    [database]
    host = localhost
    dbname = yourdatabase
    user = username
    password = password
    ```

   Replace `yourdatabase`, `username`, and `password` with your actual database name, username, and password.

## Running the Application

1. **Start the Flask application:**

    ```sh
    python app.py
    ```

2. **Test the API:**

   You can test the API using tools like `curl`, Postman, or directly from your browser.

    - **Retrieve Products:**

      Open your browser and go to `http://127.0.0.1:5000/products`. You should see the list of products from the PostgreSQL database.

    - **Delete a Product:**

      Use `curl` or Postman to send a DELETE request to `http://127.0.0.1:5000/products/1` (replace `1` with the product ID you want to delete).

      Example `curl` command to delete a product:

        ```sh
        curl -X DELETE http://127.0.0.1:5000/products/1
        ```

    - **Update a Product Price:**

      Use `curl` or Postman to send a PUT request to `http://127.0.0.1:5000/products/1` (replace `1` with the product ID you want to update) with the new price in the request body.

      Example `curl` command to update a product price:

        ```sh
        curl -X PUT -H "Content-Type: application/json" -d '{"price": 150.0}' http://127.0.0.1:5000/products/1
        ```

## Error Handling

- **404 Not Found:**

  If a product with the specified ID does not exist, the API will return a 404 error.

    ```json
    {
        "error": "Not found"
    }
    ```

- **400 Bad Request:**

  If the request body does not contain the required fields, the API will return a 400 error.

    ```json
    {
        "error": "Bad request"
    }
    ```
