# Home In Block

## Key Considerations

-   Authentication: Use JWT or OAuth2 for token-based authentication.
-   Permissions: Restrict endpoints based on user roles (e.g., only designers can create portfolios, only admins can delete users).
-   Rate Limiting: Protect critical endpoints like authentication and messaging.
-   Filters and Pagination: Apply filters (e.g., location, budget) and paginate results for endpoints with large datasets.

## API Endpoints

Here’s a list of main API endpoints for your interior design social network platform that oversees the entire interior design project. These endpoints cover user management, project workflows, collaborations, marketplace, and communication.

### 1. User Management Endpoints

These endpoints handle user registration, authentication, and profile management.

#### Authentication

-   POST /api/auth/register/
-   Register new users (e.g., designers, homeowners).
-   Payload: { "username": "johndoe", "email": "john@example.com", "password": "securepass", "role": "designer" }
-   Response: { "message": "User registered successfully" }
-   POST /api/auth/login/
-   Log in users and return JWT tokens.
-   Response: { "access_token": "abc123", "refresh_token": "xyz456" }
-   POST /api/auth/logout/
-   Log out users by blacklisting tokens.
-   POST /api/auth/refresh/
-   Refresh JWT tokens.

#### User Profiles

-   GET /api/users/me/
-   Retrieve the authenticated user’s profile.
-   PATCH /api/users/me/
-   Update the authenticated user’s profile.
-   GET /api/users/{user_id}/
-   View another user’s public profile (e.g., portfolio, reviews).

#### User Connections

-   POST /api/users/connect/
-   Send connection requests between users.
-   GET /api/users/connections/
-   List all connections for a user.

### 2. Project Management Endpoints

Facilitate the creation, management, and tracking of interior design projects.

#### Project CRUD

-   POST /api/projects/
-   Create a new project.
-   Payload: { "title": "Living Room Redesign", "description": "Modern style", "budget": 5000, "timeline": "2024-05-30", "location": "New York" }
-   GET /api/projects/
-   List all projects (filterable by user role, status, budget, etc.).
-   GET /api/projects/{project_id}/
-   Retrieve details of a specific project.
-   PATCH /api/projects/{project_id}/
-   Update a project (e.g., adjust budget or timeline).
-   DELETE /api/projects/{project_id}/
-   Delete a project (admin or project owner only).

#### Task Management

-   POST /api/projects/{project_id}/tasks/
-   Add tasks to a project.
-   GET /api/projects/{project_id}/tasks/
-   View all tasks within a project.
-   PATCH /api/projects/{project_id}/tasks/{task_id}/
-   Update task status (e.g., “completed”).

#### Assigning Professionals

-   POST /api/projects/{project_id}/assign/
-   Assign professionals (designers, contractors, etc.) to a project.
-   Payload: { "user_id": 42, "role": "designer" }

### 3. Collaboration and Communication Endpoints

Enable seamless collaboration between stakeholders.

#### Messaging

-   POST /api/messages/
-   Send a message to another user.
-   Payload: { "receiver_id": 5, "message": "Can we schedule a meeting?" }
-   GET /api/messages/
-   List all messages for the authenticated user.
-   GET /api/messages/{conversation_id}/
-   Retrieve a specific conversation.

#### File Sharing

-   POST /api/projects/{project_id}/files/
-   Upload project files (e.g., design mockups, contracts).
-   GET /api/projects/{project_id}/files/
-   List all files for a project.

### 4. Reviews and Ratings Endpoints

#### Facilitate feedback and trust-building on the platform.

-   POST /api/reviews/
-   Add a review for a professional or homeowner.
-   Payload: { "reviewee_id": 12, "rating": 4, "comment": "Great work!" }
-   GET /api/reviews/{user_id}/
-   Retrieve all reviews for a specific user.

### 5. Marketplace Endpoints

Support the sale and purchase of interior design materials or services.

-   POST /api/marketplace/items/
-   Add a new item for sale (e.g., furniture, decor).
-   Payload: { "name": "Sofa", "price": 1200, "category": "Furniture", "stock": 10 }
-   GET /api/marketplace/items/
-   List all marketplace items (filterable by category, price range, etc.).
-   GET /api/marketplace/items/{item_id}/
-   View details of a specific item.
-   PATCH /api/marketplace/items/{item_id}/
-   Update item details.
-   DELETE /api/marketplace/items/{item_id}/
-   Remove an item from the marketplace.
-   POST /api/marketplace/purchase/
-   Purchase an item.
-   Payload: { "item_id": 7, "quantity": 2 }

### 6. Analytics and Insights Endpoints

Provide actionable data for users to track progress and make decisions.

-   GET /api/analytics/projects/
-   Summary of projects (e.g., completed, in progress).
-   GET /api/analytics/users/
-   User activity and engagement stats (admin only).
-   GET /api/analytics/marketplace/
-   Sales and inventory insights for marketplace sellers.

### 7. Admin Endpoints

Allow platform admins to monitor and manage the system.

-   GET /api/admin/users/
-   List all users.
-   PATCH /api/admin/users/{user_id}/
-   Update user roles or statuses.
-   DELETE /api/admin/users/{user_id}/
-   Delete a user.
-   GET /api/admin/projects/
-   Monitor all projects.
-   DELETE /api/admin/projects/{project_id}/
-   Remove a project if necessary.
