from flask import Flask, jsonify, request
from sqlalchemy.exc import IntegrityError
from models import db, Book, Member
from schemas import BookSchema, MemberSchema
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
# Initialize Flask App
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "supersecretkey" 
jwt = JWTManager(app)
db.init_app(app)

# Initialize Schema
book_schema = BookSchema()
books_schema = BookSchema(many=True)

from datetime import datetime

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if email already exists
    if Member.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists!"}), 400

    # Hash the password
    hashed_password = generate_password_hash(data['password'])

    # Create a new member with an explicit join_date
    new_member = Member(
        name=data['name'],
        email=data['email'],
        password=hashed_password,
        join_date=datetime.now()  
    )

    # Add to database
    db.session.add(new_member)
    db.session.commit()

    return jsonify({"message": "Member registered successfully!"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Check if member exists
    member = Member.query.filter_by(email=email).first()
    if not member or not member.check_password(password):
        return jsonify({"message": "Invalid email or password"}), 401

    # Generate access token
    access_token = create_access_token(identity=member.id)  
    return jsonify({
        "access_token": access_token,
        "member_id": member.id,
        "name": member.name
    }), 200


# Route to Add a New Book
@app.route("/books", methods=["POST"])
@jwt_required()
def add_book():
    # Validate and parse the input data
    data = request.get_json()
    errors = book_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400  # Return validation errors

    # Check if ISBN already exists
    existing_book = Book.query.filter_by(isbn=data["isbn"]).first()
    if existing_book:
        return jsonify({"error": "A book with this ISBN already exists."}), 400

    # Try inserting the new book
    try:
        new_book = Book(
            title=data["title"],
            author=data["author"],
            published_year=data.get("published_year"),
            isbn=data["isbn"]
        )
        db.session.add(new_book)
        db.session.commit()

        # Serialize and return the response
        result = book_schema.dump(new_book)
        return jsonify(result), 201

    except IntegrityError:
        db.session.rollback()  # Rollback changes if there's an error
        return jsonify({"error": "Failed to add the book due to a database error."}), 500

# Route to Get All Books with Search and Pagination
@app.route("/books", methods=["GET"])
@jwt_required()
def get_books():
    # Get pagination parameters
    page = request.args.get("page", 1, type=int)  # Default page is 1
    per_page = request.args.get("per_page", 5, type=int)  # Default 5 records per page

    # Optional search filter
    search = request.args.get("search", None)
    query = Book.query  

    # Apply search filter if 'search' is provided
    if search:
        query = query.filter(
            (Book.title.ilike(f"%{search}%")) | (Book.author.ilike(f"%{search}%"))
        )

    # Apply pagination
    paginated_books = query.paginate(page=page, per_page=per_page, error_out=False)

    # Serialize the results
    books = books_schema.dump(paginated_books.items)

    # Build and return the response
    return jsonify({
        "total_books": paginated_books.total,
        "total_pages": paginated_books.pages,
        "current_page": page,
        "per_page": per_page,
        "books": books
    }), 200



# Route to Update a Book (PUT or PATCH)
@app.route("/books/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    # Update only the provided fields
    if "title" in data:
        book.title = data["title"]
    if "author" in data:
        book.author = data["author"]
    if "published_year" in data:
        book.published_year = data["published_year"]
    if "isbn" in data:
        book.isbn = data["isbn"]

    db.session.commit()

    result = book_schema.dump(book)
    return jsonify(result), 200

# Route to Delete a Book by ID
@app.route("/books/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_book(id):
    book = Book.query.get(id)  # Retrieve the book by ID
    if not book:
        return jsonify({"error": "Book not found"}), 404  # Return 404 if not found

    # Delete the book from the database
    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": f"Book with ID {id} has been deleted"}), 200

@app.route('/member', methods=['GET'])
@jwt_required()
def get_member():
    current_member_id = get_jwt_identity()  # Get the current logged-in member's ID

    # Find the member
    member = Member.query.get(current_member_id)
    if not member:
        return jsonify({"message": "Member not found!"}), 404

    # Return member information
    return jsonify({
        "id": member.id,
        "name": member.name,
        "email": member.email,
        "join_date": member.join_date
    }), 200

# Run the App
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
