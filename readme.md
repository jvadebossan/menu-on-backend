# Menu-On Backend

The **Menu-On** backend is built using **Python**, **FastAPI**, and **MongoDB**. The application provides a **digital menu** service with the option to place orders online, facilitating the management of orders and interaction between customers and the establishment.

## Technologies Used

- **Python** 3.9+
- **FastAPI**: Modern and fast framework for building APIs.
- **MongoDB**: NoSQL database to store orders, users, and menu data.
- **Swagger UI**: For interactive API documentation.
- **JWT (JSON Web Tokens)**: For user authentication.

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-user/menu-on-backend.git
cd menu-on-backend
```

### 2. Create and activate the virtual environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts activate     # For Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set environment variables
Create a `.env` file at the root of the project with the following variable:
```env
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority
MONGODB_DB_NAME="<dbname>"
SECRET_KEY="SECRET HERE"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="30"
ENVIRONMENT="development"
VERSION="1.0.0"
```

Replace the `<username>`, `<password>`, `<cluster-url>`, and `<dbname>` values with your MongoDB Atlas connection string.

### 5. Run the application
```bash
uvicorn app.main:app --reload
```

This will start the server locally at `http://127.0.0.1:8000`.

## How to Use

### API Documentation

The API documentation can be accessed directly via Swagger UI:

```
http://127.0.0.1:8000/docs
```

Swagger will provide an interactive interface to test the API routes directly.

### Main Routes

#### **Authentication**
- **POST /auth/register**: Register a new user.
- **POST /auth/login**: Log in and return an authentication JWT.

#### **Other routes under development**

### Example Usage (coming soon)

#### 1. Create an Order
Send a `POST` request to `/orders/new-order` with the following JSON body:
```json
{
  "establishment_id": "123",
  "table_number": 5,
  "customer_name": "João Silva",
  "customer_phone": "11999999999",
  "items": [
    {
      "name": "Hamburger",
      "quantity": 2,
      "price": 25.90
    },
    {
      "name": "Soda",
      "quantity": 1,
      "price": 5.50
    }
  ],
  "total_price": 57.30
}
```

#### 2. Check Order Status
Send a `GET` request to `/orders/status/{id}`.

#### 3. Update Order Status
Send a `PUT` request to `/orders/status/{id}` with the body:
```json
{
  "status": "delivered" // possible statuses: ["order_placed", "preparation", "finished", "delivered"]
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Menu-On** - Developed by João Vitor de Aguiar Debossan.