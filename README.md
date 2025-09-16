# Employee Management API

A FastAPI-based REST API for managing employees with JWT authentication, built with MongoDB as the database.

## 📁 Project Structure
```text
project_root/
├── app/
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── models/
│   │   ├── employee.py
│   │   └── user.py
│   ├── auth/
│   │   ├── dependencies.py
│   │   ├── utils.py
│   │   └── routes.py
│   └── employees/
│       ├── routes.py
│       └── utils.py
└── requirements.txt
```

## 🚀 Features

- **JWT Authentication** - Secure user registration and login
- **Employee CRUD Operations** - Create, read, update, and delete employees
- **Advanced Search** - Search employees by skills with case-insensitive matching
- **Department Analytics** - Get average salary by department
- **Pagination** - Efficient data retrieval with pagination support
- **Data Validation** - Robust input validation using Pydantic models
- **MongoDB Integration** - Async MongoDB operations with Motor

## 🛠️ Technologies Used

- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB** - NoSQL database for data storage
- **Motor** - Async MongoDB driver
- **JWT** - JSON Web Tokens for authentication
- **Pydantic** - Data validation and settings management
- **Passlib** - Password hashing utilities
- **Bcrypt** - Secure password hashing

## 📋 Prerequisites

- Python 3.8+
- MongoDB 4.0+ (running locally or remote instance)
- pip (Python package installer)

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd employee-management-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB**
   - Ensure MongoDB is running locally on `mongodb://localhost:27017`
   - Or update the `MONGO_URI` in `app/config.py` for remote MongoDB

5. **Start the application**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Root endpoint: http://localhost:8000

## 🔐 Authentication

### Register a new user
```bash
POST /auth/signup
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### Login to get access token
```bash
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=your_username&password=your_password
```

### Using the token
Include the token in the Authorization header for protected endpoints:
```bash
Authorization: Bearer your_jwt_token_here
```

## 📚 API Endpoints

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/signup` | Register new user | No |
| POST | `/auth/token` | Login and get JWT token | No |
| POST | `/auth/logout` | Logout user | No |

### Employee Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/employees/` | List all employees (paginated) | No |
| POST | `/employees/` | Create new employee | Yes |
| GET | `/employees/{employee_id}` | Get employee by ID | No |
| PUT | `/employees/{employee_id}` | Update employee | Yes |
| DELETE | `/employees/{employee_id}` | Delete employee | Yes |
| GET | `/employees/search` | Search employees by skill | No |
| GET | `/employees/avg-salary` | Get average salary by department | No |

## 💡 Usage Examples

### Create an Employee
```bash
POST /employees/
Authorization: Bearer your_jwt_token
Content-Type: application/json

{
    "employee_id": "EMP001",
    "name": "John Doe",
    "department": "Engineering",
    "salary": 75000.0,
    "joining_date": "2024-01-15",
    "skills": ["Python", "FastAPI", "MongoDB"]
}
```

### Search Employees by Skill
```bash
GET /employees/search?skill=Python&page=1&size=10
```

### List Employees with Filters
```bash
GET /employees/?department=Engineering&page=1&size=5
```

### Get Average Salary by Department
```bash
GET /employees/avg-salary
```

## 📊 Data Models

### Employee Model
```json
{
    "employee_id": "string",
    "name": "string",
    "department": "string",
    "salary": "number",
    "joining_date": "date (YYYY-MM-DD)",
    "skills": ["array of strings"]
}
```

### User Model
```json
{
    "username": "string",
    "password": "string"
}
```

## 🔧 Configuration

Update `app/config.py` to customize:

```python
# Database Configuration
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "assessment_db"

# JWT Configuration
SECRET_KEY = "your_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Application Configuration
API_TITLE = "Employees API"
```
