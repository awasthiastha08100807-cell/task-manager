# Task Manager 📝

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A **Task Manager** web app built with **React**, **Node.js/Express**, and **MySQL**. Fully **dockerized** for easy setup.

---

## Features

- ✅ Create, Read, Update, Delete tasks (CRUD)
- ✅ Responsive React frontend
- ✅ REST API backend with Express
- ✅ MySQL database
- ✅ Docker Compose ready for local deployment

---

## Quick Start 🚀

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/task-manager.git
cd task-manager

#####################
Make the wait script executable

chmod +x backend/wait-for-it.sh

#####################

Access the app

Frontend: http://localhost:3000

Backend API: http://localhost:5000/api

MySQL: localhost:3306 (user: root, password: root@12345)

####################

Stop & Cleanup

docker-compose down

####################

NOTES:

Ensure ports 3000, 5000, 3306 are free.

For HTTPS Git pushes, use a Personal Access Token instead of a password.
