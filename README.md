# Continuum

# Freelancer Productivity Platform

A clean and unified platform designed for freelancers, contractors, and small dev teams to track work, log hours, manage tasks, share progress with clients, and automatically generate transparent invoices.

This system combines the practical structure of tools like Trello and ClickUp with an emphasis on accountability, documentation, and proof-of-work.

---

## Purpose

This platform exists to eliminate the administrative burden freelancers deal with daily. Instead of juggling multiple tools for tracking hours, managing tasks, writing updates, and creating invoices, everything is automated from real activity.

The goal is simple: structure the work, show the progress, and help freelancers get paid.

---

## Core Features

### Project and Task Management

* Create projects and break them into tasks.
* Assign tasks to team members.
* Each task contains a full timeline of activity: hours logged, commits linked, comments, attachments, and status changes.

### Work Sessions

* Start and end work sessions directly inside the task.
* Hours are captured automatically and tied to the correct task.
* Notes can be added to document what was accomplished.

### Git Integration

* Automatically link commits to tasks.
* Track contributions per member.
* Maintain a clean record of what was shipped and when.

### Project Health Indicators

* Clear signals when tasks fall behind.
* Alerts for inactive projects.
* Visual summaries showing overall progress.

### Milestones and Deliverables

* Group tasks under major deliverables.
* Track progress with honest, simple metrics.
* Provide clients with a clear view of what is being worked on and what is done.

### Client Portal

* Clients can view project progress, completed tasks, hours logged, and milestone updates.
* All activity is visible without requiring separate messages or manual reporting.

### AI Summaries

* Automatic generation of weekly summaries using the actual data from tasks, commits, and hours.
* Clean, factual summaries suitable for client updates or internal reviews.
* Optional invoice summaries describing the work performed during the billing period.

### Invoice Generation

* Users set their hourly rate and currency.
* One click generates a detailed PDF showing:

  * hours worked
  * tasks completed
  * commits linked
  * milestones reached
  * total amount owed
* All invoices are stored for future reference.

### Work Profiles

* Each team member has a profile showing their skills, contributions, and activity patterns.
* Helps clients understand who is working on what and how consistently.

### Weekly Digest

* Every week, the system generates a digest summarizing:

  * completed work
  * hours logged
  * commits made
  * milestone progress
  * any risks or delays

---

## Vision

This platform aims to become the single source of truth for freelancers and teams who want clear structure without overwhelming complexity. It focuses on transparency, accountability, and simplicity, ensuring that every project has a traceable history and every contributor has verifiable work.

The emphasis is on real work, real data, and clean reporting.

---

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/Continuum.git
cd Continuum

# Start the application
docker compose up --build
```

Access the application:
- **Frontend:** http://localhost:5173
- **API Docs:** http://localhost:8000/docs

📖 **For detailed setup instructions** (Windows, WSL, Linux), see the **[Docker Setup Guide](./DOCKER_SETUP.md)**.

---

## Project Structure

```
Continuum/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Config & security
│   │   ├── db/             # Database setup
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── Dockerfile
│   └── requirements.txt
├── continuum-frontend/      # React + Vite frontend
│   ├── src/
│   │   ├── api/            # API client
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── pages/          # Page components
│   │   └── store/          # State management
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml       # Docker orchestration
├── DOCKER_SETUP.md         # Complete setup guide
└── README.md
```

---

## Tech Stack

| Layer    | Technology                          |
|----------|-------------------------------------|
| Frontend | React, TypeScript, Vite, Tailwind   |
| Backend  | FastAPI, Python 3.12, SQLAlchemy    |
| Database | PostgreSQL                          |
| DevOps   | Docker, Docker Compose              |

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

---

## Status

This repository serves as the starting point for the system architecture, backend, frontend, and documentation. More sections will be added as the project evolves.

---

## License

MIT License
