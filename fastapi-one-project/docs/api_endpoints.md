# API Endpoints Documentation

## Authentication Endpoints

### POST /token
- **Description**: Login endpoint to obtain access token
- **Request Body**: 
  - username: string
  - password: string
- **Response**: JWT access token
- **Notes**: Uses OAuth2 with Bearer token authentication

## User Management

### POST /users
- **Description**: Create a new user account
- **Request Body**: User registration details
- **Response**: Created user information
- **Authentication**: Not required

### GET /users/me
- **Description**: Get current authenticated user's details
- **Response**: User profile information
- **Authentication**: Required (Bearer token)

## Posts Management

### POST /posts
- **Description**: Create a new post
- **Request Body**: Post content and details
- **Response**: Created post information
- **Authentication**: Required (Bearer token)

### GET /posts
- **Description**: Get all posts
- **Response**: List of posts
- **Authentication**: Required (Bearer token)

### GET /posts/{post_id}
- **Description**: Get a specific post by ID
- **Parameters**: post_id (path parameter)
- **Response**: Post details
- **Authentication**: Required (Bearer token)

### PUT /posts/{post_id}
- **Description**: Update a specific post
- **Parameters**: post_id (path parameter)
- **Request Body**: Updated post content
- **Response**: Updated post information
- **Authentication**: Required (Bearer token)
- **Authorization**: Only post owner can update

### DELETE /posts/{post_id}
- **Description**: Delete a specific post
- **Parameters**: post_id (path parameter)
- **Response**: Success message
- **Authentication**: Required (Bearer token)
- **Authorization**: Only post owner can delete

## Authentication Details

All protected endpoints require a valid JWT token in the Authorization header: 