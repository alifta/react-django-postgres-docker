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

# AI Prompt

I am working on the following project:

---

# Project Overview

## Name: Home In Block

## Short Summary: A blockchain-integrated web app combining Interior Design Project Management, Social Networking between homeowners and all the actors involved in home renovation, and NFT-based property tracking for interior designers, homeowners, and contractors.

## Core Idea:

-   Mint properties as NFTs to create immutable, timestamped records of design changes and smart contracts to maintain and manage main actions and transactions applicable to a property.
-   Secondarily, it enables social collaboration (follow, review, message) between designers and homeowners, mainly, and other agents.
-   Use AI to match designers with projects and crowdfund renovations via blockchain-secured transactions.

## Inspiration:

Combines Asana or Trello (project management), LinkedIn (social networking), OpenSea (NFTs), and Houzz (design inspiration).

# Key Objectives

-   Blockchain Integration
-   Mint properties as NFTs to track design history and ownership.
-   Reduce appraisal costs via transparent, auditable property records.
-   Social Collaboration
-   Allow designers and homeowners to follow, message, and review each other.
-   AI-Driven Matching
-   Suggest designers based on style, budget, and past NFT project data.
-   Crowdfunding & Payments
-   Securely fundraise for projects using NFT-backed milestones.
-   Transparency Dashboards
-   Real-time project tracking with blockchain-verified updates.

# Key Objectives Explanation

In this app, users are mainly homeowners and interior designers who get connected to each other in a social network format but with some extra benefits to both of these groups if they use our solution, such as connection (follow), message, booking, review, contract, and payments. Homeowners can list their property for re-design or renovation, and interdesigners can check out existing listings, propose to homeowners, and acquire the project. Users can sign up. The platform provides a project management tool for an interior designer who can create tasks, assign them to a team member, and give some extra visibility to homeowners. You can consider. Added on top is an AI system that trains interior designers' portfolios to match the best and compatible interior designers to homeowners for their project and provides the best match project to interior designers so that they know they are a great match and take on a new challenge, but at the end of the day it is homeowner and interior designer to agree on the project. Add comments to the code as much as possible for clarity and to help junior developers understand the code and concept better. In the future, I want to add LGTM stack to my project, Grafana Labs' opinionated observability stack, which includes Loki for logs, Grafana for dashboards and visualization, Tempo for traces, and Mimir for metrics.

# Target Audience

## Primary:

-   Interior designers seeking collaborative projects and reputation building.
-   Homeowners listing properties for renovation (tech-savvy, blockchain-curious).

## Secondary:

-   Contractors/architects bidding on NFT-linked tasks.
-   Real estate agents use NFT histories to make accurate property valuations.

# Core Features

-   Project Management
-   Assign tasks, track budgets, and share visible updates with stakeholders.
-   Homeowners view real-time spending, task progress, and change logs.
-   Social Network
-   Follow users, comment on listings/blog posts, and message collaborators.
-   Upload property details (photos, floor plans)
-   Track design changes (e.g., "2023 Kitchen Remodel").
-   Review designers/contractors post-project.
-   AI Matching Engine
-   Analyze homeowner preferences and history to recommend designers.
-   NFT Property Minting
-   Crowdfunding Module
-   Create campaigns tied to NFT properties; release funds via smart contracts.
-   Dashboard

# Technical Preferences

## Backend:

-   Django in Docker container

## Database:

PostgreSQL (relational data)

## Frontend:

-   Next.js/React.js (TypeScript)

## Blockchain:

-   Ethereum/Polygon for NFTs (low gas fees).
-   Solidity for smart contracts; IPFS for decentralized file storage.

## AI/ML:

-   Python/TensorFlow for recommendation models
-   DeepSeek for text analysis and other task automation.

Hosting:

-   AWS EC2 + S3

# Design Guidelines

## UI/UX:

-   Clean, minimalist and modern interface
-   Interactive timeline showing (blockchain-recorded) design changes and progress in the interior design project.
-   Dark/light mode toggle and WCAG 2.1 accessibility compliance.

Key Screens:

-   Social Feed (project updates, blog posts, etc.)
-   Property Gallery (maybe similar to OpenSea NFT)
-   AI Matching Wizard (sliders for budget/style preferences).

# User Stories/Use Cases

## As a Homeowner:

"I want to list my property for renovation/interior design project, crowdfund for renovation, and hire a designer matched by AI."
"I need to see a blockchain history of all design changes for insurance purposes."

## As a Designer:

"I want to showcase past projects on my profile and receive AI-matched clients."
"I need to assign tasks to contractors and release payments via smart contracts."

## As a Contractor:

"I want to bid on tasks and prove my work is completed via updates and notifications."

# Constraints

## Technical:

Blockchain gas fees could slow transaction speeds (mitigate with Polygon or a cheap and fast chain).
Training AI models require large datasets of historical projects. The project code is saved on the following repository URL:
https://github.com/alifta/react-django-postgres-docker
The project is dockerized using counter and docker-compose, where I have set up the backend using Django in one container and Postgres database (in a separate container) and for the frontend, I used Next.js (in a separate container), Redis (in a separate container) for caching and celery in another container.

## Regulatory:

Legal ambiguity around NFT property rights in some regions.

## Budget:

Smart contract audits and IPFS storage costs.

# Deliverables

Web app
Restful API Endpoints
REST/GraphQL for social features, AI matching, and blockchain interactions.
UI Prototypes
Smart Contracts
NFT minting, crowdfunding, and payment escrow logic.
Figma designs for NFT gallery, social feeds, and dashboards.
Architecture Diagrams
System flow showing blockchain integration with backend/services.

# Additional Context

## Competitors:

Houzz: Lacks blockchain transparency and AI matching.
Propy: Uses blockchain for real estate transactions but no design focus.

## Unique Value:

Combines NFT property tracking with interior design collaboration.
Crowdfunding tied to on-chain milestones reduces payment disputes.

## Inspiration:

Decentraland: Virtual land NFTs repurposed for physical properties.
Gitcoin: Community-funded projects adapted for design renovations.

## Concept Brainstorming

Property Workflow
Designer submits renovation proposals
Homeowner mints property NFT with metadata (location, size, photos).
After crowdfunding, smart contracts release payments at milestones (e.g., "Flooring Installed").
Final design is added to the NFT's history, accessible to future buyers/appraisers.
AI Matching Engine

## Data Inputs:

Homeowner's style preferences (e.g., "mid-century modern").
Designer's NFT project history and ratings.
Budget range and location.

## Output:

Ranked designer list with compatibility scores.

## Social Features

Designers post "Project Stories" to attract followers.
Homeowners share crowdfunding campaigns on social feeds (integrated with Twitter/Instagram).

# Output Format:

-   Present the directory structure as a tree view (in bash format).
-   For each file, output the complete content with the filename as a header. Example Format:
    Directory Tree View
    Complete code for {example}.py

# Fina thoughts:

I expect to complete the project in 6 months. Please help me with my start-up idea. My life's goals and success depend on it.

---

I will request your assistance with coding for this project in my upcoming prompts. Thank you!

In my Django project, I have a main app called core, which includes all the database models in the models.py file:

```python

```

can you make sure to add comments to the code as much as you can to help junior programmers on the team and make sure that fields has help text and verbose text and imrove each class as much as you can
