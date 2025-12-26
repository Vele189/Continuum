# Continuum Docker Setup Guide

Complete guide for setting up the Continuum development environment using Docker on **Windows**, **WSL (Windows Subsystem for Linux)**, and **Linux**.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Docker Installation](#docker-installation)
  - [Windows](#windows)
  - [WSL (Windows Subsystem for Linux)](#wsl-windows-subsystem-for-linux)
  - [Linux (Ubuntu/Debian)](#linux-ubuntudebian)
  - [Linux (Fedora/RHEL)](#linux-fedorarhel)
  - [Linux (Arch)](#linux-arch)
- [Project Setup](#project-setup)
- [Running the Application](#running-the-application)
  - [Easiest Way (Linux/WSL/macOS)](#-easiest-way-linuxwslmacos)
  - [Quick Start (All Platforms)](#quick-start-all-platforms)
  - [Windows (PowerShell)](#windows-powershell-1)
  - [Manual Docker Commands](#manual-docker-commands)
- [Accessing the Application](#accessing-the-application)
- [Development Workflow](#development-workflow)
- [Useful Commands](#useful-commands)
- [Troubleshooting](#troubleshooting)
- [Port Reference](#port-reference)

---

## Prerequisites

Before you begin, ensure you have:

- **Git** installed and configured
- **Docker** and **Docker Compose** installed (instructions below)
- At least **4GB of free RAM** for Docker
- At least **10GB of free disk space**

---

## Docker Installation

### Windows

#### Option 1: Docker Desktop (Recommended)

1. **Download Docker Desktop** from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)

2. **Run the installer** and follow the prompts

3. **Enable WSL 2 backend** (recommended) when prompted during installation

4. **Restart your computer** after installation

5. **Verify installation** by opening PowerShell or Command Prompt:
   ```powershell
   docker --version
   docker compose version
   ```

6. **Start Docker Desktop** from the Start menu if it doesn't auto-start

> ⚠️ **Note:** Docker Desktop requires Windows 10/11 Pro, Enterprise, or Education for Hyper-V, or Windows 10/11 Home with WSL 2.

---

### WSL (Windows Subsystem for Linux)

WSL is the **recommended approach for Windows users** as it provides a native Linux environment.

#### Step 1: Install WSL 2

Open PowerShell as Administrator and run:

```powershell
wsl --install
```

This installs WSL 2 with Ubuntu by default. Restart your computer when prompted.

#### Step 2: Set Up Ubuntu

After restart, Ubuntu will launch automatically. Create your username and password.

#### Step 3: Install Docker in WSL

**Option A: Use Docker Desktop with WSL 2 Backend (Easier)**

1. Install Docker Desktop on Windows (see Windows section above)
2. Open Docker Desktop → Settings → Resources → WSL Integration
3. Enable integration with your WSL distro (e.g., Ubuntu)
4. Docker commands will now work in your WSL terminal

**Option B: Install Docker Engine directly in WSL (No Docker Desktop)**

```bash
# Update packages
sudo apt update && sudo apt upgrade -y

# Install prerequisites
sudo apt install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to the docker group (to run without sudo)
sudo usermod -aG docker $USER

# Start Docker service
sudo service docker start

# Log out and back in, or run:
newgrp docker
```

#### Step 4: Verify Installation

```bash
docker --version
docker compose version
docker run hello-world
```

> 💡 **Tip:** Store your project files inside WSL (e.g., `~/projects/`) for better performance, not on `/mnt/c/`.

---

### Linux (Ubuntu/Debian)

```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up the repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker Engine and Compose
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add your user to the docker group
sudo usermod -aG docker $USER

# Apply group changes (or log out and back in)
newgrp docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Verify installation
docker --version
docker compose version
```

---

### Linux (Fedora/RHEL)

```bash
# Remove old versions
sudo dnf remove docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

# Set up the repository
sudo dnf -y install dnf-plugins-core
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# Install Docker Engine
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to the docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

---

### Linux (Arch)

```bash
# Install Docker
sudo pacman -S docker docker-compose

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add your user to the docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

---

## Project Setup

---

## Running the Application

### 🚀 Easiest Way (Linux/WSL/macOS)

We provide simple start scripts that handle everything for you:

```bash
# From the project root directory

# Option 1: Start the frontend (automatically starts backend too)
./continuum-frontend/start.sh

# Option 2: Start only the backend
./backend/start.sh
```

That's it! The script will:
- Build the Docker containers
- Start the services
- Show you the logs (press `Ctrl+C` to exit logs - containers keep running)

> 💡 **Tip:** Most developers just need to run `./continuum-frontend/start.sh` - it starts both frontend AND backend.

---

### Quick Start (All Platforms)

From the project root directory, run both services:

```bash
docker compose up --build
```

Add `-d` to run in detached (background) mode:

```bash
docker compose up -d --build
```

---

### Windows (PowerShell)

Windows users without bash can run these commands directly:

```powershell
# Start everything
docker compose up --build

# Or start services individually:

# Backend only
docker compose up -d --build backend
docker compose logs -f backend

# Frontend only (starts backend as dependency)
docker compose up -d --build frontend
docker compose logs -f frontend
```

---

### Manual Docker Commands

```bash
# Build and start all services
docker compose up --build

# Start in background
docker compose up -d --build

# Start specific service
docker compose up -d backend
docker compose up -d frontend

# View logs
docker compose logs -f              # All services
docker compose logs -f backend      # Backend only
docker compose logs -f frontend     # Frontend only

# Stop all services
docker compose down

# Stop and remove volumes (fresh start)
docker compose down -v
```

---

## Accessing the Application

Once running, access the application at:

| Service  | URL                                    | Description              |
|----------|----------------------------------------|--------------------------|
| Frontend | [http://localhost:5173](http://localhost:5173) | React/Vite application   |
| Backend  | [http://localhost:8000](http://localhost:8000) | FastAPI server           |
| API Docs | [http://localhost:8000/docs](http://localhost:8000/docs) | Swagger UI documentation |
| Health   | [http://localhost:8000/health](http://localhost:8000/health) | Health check endpoint    |

> 📝 **Note:** The backend port (8000) is only exposed within the Docker network by default. The frontend communicates with the backend internally. If you need direct backend access, uncomment the ports in `docker-compose.yml`.

---

## Development Workflow

### Hot Reloading

Both services support hot reloading for development:

- **Frontend:** Changes to files in `continuum-frontend/src/` automatically trigger a rebuild
- **Backend:** Changes to files in `backend/app/` automatically restart the server

### Making Changes

1. Edit files in your local editor
2. Changes are automatically synced to containers via volume mounts
3. The application reloads automatically

### Installing New Dependencies

**Frontend (npm packages):**

```bash
# Run npm install inside the container
docker compose exec frontend npm install <package-name>

# Or rebuild the container
docker compose up -d --build frontend
```

**Backend (Python packages):**

```bash
# Add to requirements.txt, then rebuild
echo "new-package==1.0.0" >> backend/requirements.txt
docker compose up -d --build backend
```

### Running Commands Inside Containers

```bash
# Access frontend shell
docker compose exec frontend sh

# Access backend shell
docker compose exec backend bash

# Run a one-off command
docker compose exec backend python -c "print('Hello')"
docker compose exec frontend npm run lint
```

---

## Useful Commands

```bash
# Check running containers
docker compose ps

# View resource usage
docker stats

# Rebuild a specific service
docker compose build backend
docker compose build frontend

# Restart a service
docker compose restart backend
docker compose restart frontend

# View container logs (last 100 lines)
docker compose logs --tail=100 backend

# Remove all stopped containers and unused images
docker system prune

# Remove all unused data (use with caution)
docker system prune -a --volumes
```

---

## Troubleshooting

### Port Already in Use

**Error:** `Bind for 0.0.0.0:5173 failed: port is already allocated`

**Solution:**

```bash
# Find what's using the port
# Linux/WSL
sudo lsof -i :5173
# or
sudo netstat -tlnp | grep 5173

# Windows PowerShell
netstat -ano | findstr :5173

# Kill the process or stop the other container
docker ps  # Find conflicting container
docker stop <container_name>
```

Or change the port in `docker-compose.yml`:

```yaml
ports:
  - "5174:5173"  # Use 5174 instead
```

---

### Permission Denied (Linux/WSL)

**Error:** `permission denied while trying to connect to the Docker daemon socket`

**Solution:**

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes
newgrp docker
# or log out and back in
```

---

### Docker Daemon Not Running

**Error:** `Cannot connect to the Docker daemon`

**Solution:**

```bash
# Linux
sudo systemctl start docker

# WSL (without Docker Desktop)
sudo service docker start

# Windows
# Start Docker Desktop from the Start menu
```

---

### Slow Performance on Windows/WSL

**Solution:**

1. Store project files inside WSL, not on Windows drives (`/mnt/c/`)
2. Use WSL 2 (not WSL 1)
3. Allocate more resources to WSL in `.wslconfig`:

   Create/edit `C:\Users\<YourUsername>\.wslconfig`:
   ```ini
   [wsl2]
   memory=8GB
   processors=4
   ```

4. Restart WSL: `wsl --shutdown`

---

### Container Keeps Restarting

**Solution:**

```bash
# Check logs for errors
docker compose logs backend
docker compose logs frontend

# Check container status
docker compose ps

# Try rebuilding
docker compose down
docker compose up --build
```

---

### Module Not Found / Import Errors

**Solution:**

```bash
# Rebuild containers to reinstall dependencies
docker compose down
docker compose build --no-cache
docker compose up
```

---

### Database Issues

```bash
# Reset the database (removes all data)
rm backend/continuum.db
docker compose restart backend
```

---

### Clear Everything and Start Fresh

```bash
# Stop all containers
docker compose down

# Remove all project containers, networks, and volumes
docker compose down -v --rmi local

# Remove all Docker data (use with caution - affects all projects)
docker system prune -a --volumes

# Rebuild from scratch
docker compose up --build
```

---

## Port Reference

| Port | Service           | Description                    |
|------|-------------------|--------------------------------|
| 5173 | Frontend (Vite)   | React development server       |
| 8000 | Backend (FastAPI) | API server (internal by default) |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Docker Network                          │
│                                                             │
│  ┌─────────────────┐         ┌─────────────────────────┐   │
│  │    Frontend     │         │        Backend          │   │
│  │   (continuum-   │  ────►  │    (continuum-backend)  │   │
│  │    frontend)    │  HTTP   │                         │   │
│  │                 │         │  ┌───────────────────┐  │   │
│  │  Port: 5173     │         │  │  PostgreSQL DB    │  │   │
│  │  Vite + React   │         │  │   (postgres:16)   │  │   │
│  └────────┬────────┘         │  └───────────────────┘  │   │
│           │                  │                         │   │
│           │                  │  Port: 8000 (internal)  │   │
│           │                  │  FastAPI + Uvicorn      │   │
│           │                  └─────────────────────────┘   │
│           │                                                 │
└───────────┼─────────────────────────────────────────────────┘
            │
            ▼
    localhost:5173
    (Your Browser)
```

---

## Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/your-org/Continuum/issues)
2. Search existing issues for similar problems
3. Create a new issue with:
   - Your OS and version
   - Docker version (`docker --version`)
   - Full error message
   - Steps to reproduce

---

## Next Steps

After setup is complete:

1. Access the frontend at [http://localhost:5173](http://localhost:5173)
2. Create an account or log in
3. Start exploring the platform!

Happy coding!
