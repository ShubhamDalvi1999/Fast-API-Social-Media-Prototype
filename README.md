# FastAPI Social Network

A social network application built with FastAPI, featuring user authentication, posts, likes, retweets, and following functionality.

## Features

- User Authentication
  - Register with username, email, and password
  - Login with username and password
  - JWT token-based authentication

- Posts Management
  - Create new posts
  - View all posts with likes and retweets count
  - Delete own posts
  - Edit posts within 10 minutes of creation

- Social Interactions
  - Like/Unlike posts
  - Retweet/Unretweet posts
  - Follow/Unfollow other users

## Tech Stack

- FastAPI - Modern Python web framework
- SQLAlchemy - SQL toolkit and ORM
- Pydantic - Data validation using Python type annotations
- SQLite - Lightweight database
- JWT - JSON Web Tokens for authentication
- Uvicorn - Lightning-fast ASGI server

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python -m uvicorn app.main:app --reload
```

The application will be available at http://127.0.0.1:8000

## Project Structure

```
fastapi-one-project/
├── app/
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── app.js
│   ├── templates/
│   │   └── index.html
│   ├── routes/
│   │   ├── auth.py
│   │   ├── posts.py
│   │   └── users.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   ├── exceptions.py
│   └── main.py
├── requirements.txt
└── README.md
```

## API Documentation

- Interactive API documentation (Swagger UI): http://127.0.0.1:8000/docs
- Alternative API documentation (ReDoc): http://127.0.0.1:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/token` - Login and get access token

### Users
- `POST /users/` - Register new user
- `GET /users/me` - Get current user info
- `POST /users/{user_id}/follow` - Follow a user
- `POST /users/{user_id}/unfollow` - Unfollow a user

### Posts
- `GET /posts/` - Get all posts
- `POST /posts/` - Create new post
- `DELETE /posts/{post_id}` - Delete a post
- `PUT /posts/{post_id}` - Update a post
- `GET /posts/with_counts/` - Get posts with likes and retweets count
- `POST /posts/{post_id}/like` - Like a post
- `POST /posts/{post_id}/unlike` - Unlike a post
- `POST /posts/{post_id}/retweet` - Retweet a post
- `POST /posts/{post_id}/unretweet` - Unretweet a post

## Security Features

- Password hashing using bcrypt
- JWT token authentication
- Protected routes requiring authentication
- User ownership verification for post operations

## Frontend Features

- Modern, responsive UI
- Real-time post updates
- Interactive like and retweet buttons
- User-friendly forms for login and registration
- Success/Error notifications
- Loading states for better UX

## Development

The project uses SQLite for development. For production, consider using a more robust database like PostgreSQL.

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request 