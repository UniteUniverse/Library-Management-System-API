Library Management System
Overview
This project is a Library Management System built using Flask, SQLAlchemy, and JWT-based authentication. It allows users to perform CRUD operations on books and manage member information, all while ensuring secure access via token-based authentication.

Table of Contents
How to Run the Project
Design Choices
Assumptions and Limitations

How to Run the Project
Prerequisites
Before running the project, ensure you have the following installed:
Python 3.6+
pip (Python package installer)

Step-by-Step Guide
Clone the repository:
bash
git clone https://github.com/UniteUniverse/Library-Management-System-API.git
cd library-management-system
Create a virtual environment (optional, but recommended):

bash
python -m venv venv
source venv/bin/activate  # For Windows, use 'venv\Scripts\activate'

Install dependencies:
bash
pip install -r requirements.txt
Set up the database:

The project uses SQLite as the database, which is already set up in the project. However, you can easily switch to other databases by modifying the connection string in the app.py file.
Run the following command to initialize the database:
bash
flask db init
flask db migrate
flask db upgrade
Run the application:

bash
flask run
Access the API: The server will start at http://127.0.0.1:5000/. You can use tools like Postman or Curl to interact with the API.

Design Choices
Flask Framework:
Flask was chosen for its simplicity, scalability, and ease of use for building RESTful APIs. It's lightweight and allows us to focus on the core functionality without additional overhead.

JWT Authentication:
We used JWT (JSON Web Tokens) for secure authentication. It allows users to authenticate once, receive a token, and use that token to make authenticated requests to the API.
This approach ensures the system is stateless, where the server doesn't need to store session information, making it more scalable.

SQLAlchemy:
SQLAlchemy was chosen for ORM (Object-Relational Mapping) to interact with the SQLite database. This makes database operations like insertions, queries, and updates more intuitive and Pythonic.

Database:
The project uses SQLite as a lightweight, file-based relational database for simplicity. For production, the database can be replaced with MySQL, PostgreSQL, or any other relational database by changing the configuration in the SQLALCHEMY_DATABASE_URI.

Pagination and Search:
To enhance performance and usability, pagination is implemented for the GET /books endpoint, limiting the number of books returned per request (default 5).
Search functionality is added to allow users to filter books by title or author.

Model Design:
The database consists of two primary models:
Book: Stores information about books like title, author, published year, and ISBN.
Member: Stores member details like name, email, password (hashed), and join date.

Assumptions and Limitations
Assumptions:
The system assumes the use of Flask as the web framework and SQLAlchemy for database operations.
The JWT token is used for user authentication, and it must be included in the Authorization header for accessing secure routes.
Member data (such as name, email, and password) must be valid during registration, and email uniqueness is enforced.

Limitations:
Single Database (SQLite): The project uses SQLite as the database, which is suitable for development or small-scale applications. For larger production systems, a more robust database like MySQL or PostgreSQL should be considered.
No Admin Role: There is currently no distinction between user roles. All users can perform the same operations. An admin role could be added later for enhanced functionality (e.g., only admins can delete books).
Limited Error Handling: While basic error handling has been implemented, some edge cases or specific validation could be enhanced, such as better handling of duplicate ISBNs or email addresses.

Potential Enhancements:
Add admin roles to allow only admins to delete or update books.
Implement rate-limiting to prevent abuse of the API.
Add unit tests to ensure API functionality is working as expected.
Allow file uploads (e.g., book covers) to be associated with books.
Implement password reset functionality for members.

Conclusion
This Library Management System provides a simple, secure API for managing books and members. JWT-based authentication ensures secure access, and features like pagination and search enhance the usability of the system.


