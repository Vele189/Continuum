# Continuum Project - Docker Instructions

This document explains how to build and run the backend and frontend containers using Docker.

---

## Setup Steps

1. Make sure Docker is installed on your system.

2. Clone the repository:

git clone https://github.com/Vele189/Continuum.git
cd Continuum

3.  Build and Run Containers

docker build -t continuum-backend ./backend
docker run --rm -p 8000:8000 continuum-backend

4.  Troubleshooting

-If a container fails to start due to a port being in use:

sudo lsof -i :<PORT>
sudo kill -9 <PID>

-The dockerfile should handle permissions automatically

5.  Common Pitfalls

Port Conflicts:

Make sure no other processes or containers are using ports 8000 (backend) or 5173 (frontend).