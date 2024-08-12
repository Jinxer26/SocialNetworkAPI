# Social Networking API

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Build and run the application:

   ```bash
   docker-compose up --build
   ```

3. The application will be available at `http://localhost:8000`.

### API Endpoints

- `POST /api/users/signup/` - User signup
- `POST /api/users/login/` - User login
- `GET /api/users/search/?keyword=<keyword>` - Search users by email
