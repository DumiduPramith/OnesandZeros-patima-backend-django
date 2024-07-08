# Patima Backend Server

## Overview

The Patima backend server, which includes a Django application and Nginx server, is packaged for deployment using Docker containers. The deployment setup includes the following services:

- Admin Panel Nginx Server
- Django App
- MySQL Server
- Main Nginx Server

These services are all containerized using Docker.

## Features

- **Django Application**: Handles API calls, user-based authentication, and JWT token authentication.
- **MySQL Database**: Manages the application's data.
- **Nginx Servers**: Acts as reverse proxies and serves static files.

## Technologies Used

- **Django**: A high-level Python web framework.
- **Django REST Framework (DRF)**: A powerful and flexible toolkit for building Web APIs.
- **MySQL**: A widely used open-source relational database management system.
- **Nginx**: A high-performance HTTP server and reverse proxy.
- **Docker**: A platform for developing, shipping, and running applications in containers.

## Installation

### Prerequisites

- Docker
- Docker Compose