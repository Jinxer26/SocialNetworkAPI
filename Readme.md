# Social Networking API

This is an simple social networking API developed using Django Rest Framework.
This api has features such as signup,login,auth,send and receive friend requests etc..

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/Jinxer26/SocialNetworkAPI.git
   cd socialnetwork_backend
   ```

2. Build and run the application:

   ```bash
   docker-compose up --build
   ```

3. The application will be available at `http://localhost:8000`.

### API Endpoints

- `POST /api/users/signup/` - User signup
- `POST /api/users/login/` - User login
- `POST /api/users/auth/` - To get Authentication Token
- `GET /api/users/search/?keyword=<keyword>` - Search users by email
- `POST /api/users/friend-request/` - Send friend request
- `PATCH /api/users/friend-request/<int:pk>/` - Accept friend requests
- `GET /api/users/friends/` - Friend list view
- `GET /api/users/pending-requests/` - See pending friend requests

### POSTMAN Collections

1. This repository cotains the postman_collection files which I used to make Requests.
2. The API implements SessionAuthentication as well as Token Authentication.
3. When using POSTMAN, make sure to get the token from the API endpoint ('/api/users/auth')
4. Set Environment Variables like username, password, socket and token.
