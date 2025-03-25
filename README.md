# Portfolio App

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Setup and Installation](#setup-and-installation)
   - [Prerequisites](#prerequisites)
   - [Clone the Repository](#clone-the-repository)
   - [Set Up Environment Variables](#set-up-environment-variables)
   - [Run with Docker](#run-with-docker)
5. [Running the Application](#running-the-application)
   - [Access the Web App](#access-the-web-app)
   - [Viewing the User Map](#viewing-the-user-map)
6. [User Management](#user-management)
7. [API Endpoints](#api-endpoint)
8. [Testing](#testing)
9. [CI/CD and Deployment](#cicd-and-deployment)

## Project Overview
This is a Django-based portfolio application that allows users to create profiles, specify their locations, and visualize user distribution on an interactive map. The project is containerized using Docker and utilizes PostgreSQL with PostGIS for geospatial data.

## Features
- User authentication (signup/login/logout)
- User profile with extended details
- Interactive full-screen map displaying all users' locations
- Admin access control for viewing maps
- Logging user activities
- Test cases for core functionalities

## Tech Stack
- **Backend**: Django
- **Database**: PostgreSQL with PostGIS
- **Frontend**: HTML, Bootstrap, Leaflet.js (for maps)
- **Containerization**: Docker, Docker Compose
- **Testing**: Django Test Framework
- **CI/CD**: GitHub Actions, AWS EC2

---

## Setup and Installation
### Prerequisites
Ensure you have the following installed:
- Docker & Docker Compose
- Python 3.12+
- PostgreSQL with PostGIS (for local development)

### Clone the Repository
```sh
 git clone https://github.com/NitinV84/kartoza_portfolio.git
 cd portfolio
```

### Set Up Environment Variables
Create a `.env` file in the root directory and configure the database and email settings:
```ini
DATABASE_ENGINE=django.contrib.gis.db.backends.postgis
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=your_db_host # if use docker replace it with "db"
DATABASE_PORT=5432

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password
```

### Run with Docker
Build and start the containers:
```sh
docker compose up --build
```
Check running containers:
```sh
docker ps
```
Run migrations manually (Optional):
```sh
docker exec -it django_app python manage.py migrate
```
Create a superuser:
```sh
docker exec -it django_app python manage.py createsuperuser
```
Run tests:
```sh
docker exec -it django_app python manage.py test
```

---

## Running the Application
### Access the Web App
- Open your browser and go to: `http://localhost:8000/`
- Admin panel: `http://localhost:8000/admin/`

## User Management
- Only an admin can create a new user through the admin panel using the user's email and name. There is no separate API or UI for creating users.
- Log in as an admin, go to the "Users" model under the "USERS" section, and click the "Add User" button in the top-right corner.
- After adding the user, they will receive an email with their username details and a link to reset their password so they can set their own password.
- To show the map click on the "VIEW MAP" button in the top right corner.

---

## API Endpoint
| Method | Endpoint       | Description        |
|--------|--------------|-------------------|
| GET    | /users/profile/  | Get user profile |
| POST    | /users/profile/edit/{id}/ | Edit user profile  |
| POST   | /users/login/  | Authenticate user |
| POST   | /users/logout/  | Logout user |

### Viewing the User Map
- Only admin users can view the map.
- Log in as an admin and go to the User model under the Users section. Click the "View Map" button in the top right corner.

---

## Testing
Run tests inside the Docker container:
```sh
docker exec -it django_app python manage.py test
```
If running locally:
```sh
python manage.py test
```

---

## CI/CD and Deployment
This project is deployed using **GitHub Actions CI/CD pipeline** to an **AWS EC2 instance**.

### Deployment Process
1. On every push to the `master` branch, GitHub Actions:
   - Runs test cases in a Docker container.
   - If tests pass, it deploys the latest code to the AWS EC2 instance.
2. The deployment includes:
   - Pulling the latest code from the repository.
   - Restarting Docker containers with the latest changes.

### Accessing the Deployed App
The live application is hosted on **AWS EC2** and can be accessed at:
- **Web App**: [http://13.233.158.73:8000/](http://13.233.158.73:8000/)

- **Admin Panel**: [http://13.233.158.73:8000/admin/](http://13.233.158.73:8000/admin/)

### Admin Login Credentials
- **Username**: root
- **Password**: root


### User Login Credentials to the login page
- **Username**: user1
- **Password**: User1@321

- **Username**: user2
- **Password**: User2@321

---
