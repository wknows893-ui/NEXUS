# NEXUS

**NEXUS** is a production-oriented, multi-tenant real-time collaboration and project management platform designed to demonstrate how modern backend systems are built, scaled, and made reliable under concurrent workloads.

The platform allows organizations to manage users, projects, tasks, discussions, activity, notifications, and real-time collaboration from a single system.

The main goal of NEXUS is not simply to build CRUD APIs. It is designed as a progressively evolving backend system where PostgreSQL handles durable business data while Redis handles high-speed, temporary, distributed, and real-time workloads.

---

# What Does NEXUS Do?

NEXUS provides a centralized workspace where teams inside an organization can:

* Create and manage organizations
* Add users and manage memberships
* Create projects
* Create, assign, prioritize, and track tasks
* Add comments and discussions to tasks
* Track project and user activity
* Communicate through channels and messages
* See which users are currently online
* Receive real-time notifications
* Process background jobs and events
* Schedule time-sensitive operations
* Enforce authentication, authorization, and rate limits
* Handle concurrent operations safely
* Cache frequently accessed data
* Process real-time events at scale

The system is designed around a multi-tenant architecture, meaning multiple organizations can use the same platform while their data and permissions remain logically isolated.

---

# Core Architecture

                         CLIENTS
                            |
                            v
                     ┌─────────────┐
                     │   FastAPI   │
                     │ API Servers │
                     └──────┬──────┘
                            |
              ┌─────────────┴─────────────┐
              |                           |
              v                           v
       ┌──────────────┐           ┌──────────────┐
       │  PostgreSQL  │           │    Redis     │
       │              │           │              │
       │ Source of    │           │ Cache        │
       │ Truth        │           │ Sessions     │
       │              │           │ Presence     │
       │ Users        │           │ Rate Limits  │
       │ Projects     │           │ Queues       │
       │ Tasks        │           │ Events       │
       │ Comments     │           │ Pub/Sub      │
       └──────────────┘           └──────┬───────┘
                                         |
                                         v
                                  ┌──────────────┐
                                  │   Workers    │
                                  │              │
                                  │ Background   │
                                  │ Processing   │
                                  └──────────────┘
```

### Technology Responsibilities

| Technology    | Responsibility                                                                |
| ------------- | ----------------------------------------------------------------------------- |
| FastAPI       | HTTP APIs, validation, authentication, WebSockets                             |
| PostgreSQL    | Permanent business data and source of truth                                   |
| SQLAlchemy    | Database interaction and ORM                                                  |
| Alembic       | Database migrations                                                           |
| Redis         | Cache, temporary state, counters, queues, events and distributed coordination |
| Redis Streams | Durable event processing                                                      |
| Redis Pub/Sub | Real-time message distribution                                                |
| Pytest        | Testing                                                                       |
| Docker        | Containerization                                                              |
| Prometheus    | Metrics                                                                       |
| Grafana       | Monitoring and visualization                                                  |

---

# Core Data Model

NEXUS is organized around the following major entities:

```text
Organization
│
├── Users
│     │
│     └── Memberships
│
├── Projects
│     │
│     ├── Tasks
│     │     ├── Comments
│     │     └── Activity
│     │
│     └── Activity
│
└── Channels
      │
      ├── Members
      └── Messages
```

---

# 1. User

The **User** represents an individual account registered on NEXUS.

A user can belong to one or more organizations and can participate in projects, channels, tasks, and discussions.

### User contains

* `id`
* `name`
* `email`
* `password_hash`
* `avatar`
* `status`
* `created_at`
* `updated_at`
* `last_login_at`

### Responsibilities

The User model represents permanent identity and account information.

Authentication-related temporary information should not necessarily live directly in the User table.

For example:

```text
PostgreSQL
    ↓
User identity
    ↓
Redis
    ↓
Session / temporary authentication state
```

---

# 2. Organization

An **Organization** represents a company, team, startup, college group, or other independent workspace using NEXUS.

Organizations provide the primary boundary for multi-tenancy.

### Organization contains

* `id`
* `name`
* `slug`
* `description`
* `owner_id`
* `created_at`
* `updated_at`

### Example

```text
Organization: OpenTech

    Users
      ├── Alice
      ├── Bob
      └── Charlie

    Projects
      ├── NEXUS
      └── Mobile App

    Channels
      ├── general
      └── engineering
```

A user's access to an organization's resources is determined through membership and authorization rules.

---

# 3. Membership

A **Membership** connects a User to an Organization.

A user should not simply have an `organization_id` if NEXUS is intended to support users belonging to multiple organizations.

### Membership contains

* `id`
* `user_id`
* `organization_id`
* `role`
* `joined_at`

### Example

```text
Alice
 ├── Organization A → Admin
 └── Organization B → Member
```

This model is essential for multi-tenant authorization.

---

# 4. Project

A **Project** represents a major body of work inside an organization.

Projects contain tasks, discussions, activity, and potentially project-specific members.

### Project contains

* `id`
* `organization_id`
* `name`
* `description`
* `status`
* `owner_id`
* `created_at`
* `updated_at`
* `deadline`

### Example

```text
Organization
    |
    └── Project: NEXUS v1
           |
           ├── Authentication
           ├── Redis Integration
           ├── WebSockets
           └── Monitoring
```

Projects belong to organizations.

---

# 5. Task

A **Task** represents an individual unit of work inside a project.

Tasks are where much of the application's business logic will eventually live.

### Task contains

* `id`
* `project_id`
* `title`
* `description`
* `status`
* `priority`
* `assignee_id`
* `creator_id`
* `due_date`
* `created_at`
* `updated_at`
* `completed_at`

### Example

```text
Project: NEXUS

Tasks:

T1 → Implement authentication
     Priority: HIGH
     Status: IN_PROGRESS
     Assignee: Alice

T2 → Implement Redis caching
     Priority: MEDIUM
     Status: TODO
     Assignee: Bob
```

Tasks will eventually be useful for demonstrating:

* concurrency control
* optimistic locking
* caching
* activity tracking
* notifications
* background processing
* distributed events

---

# 6. Comment

A **Comment** represents a discussion attached to a task.

Users can use comments to communicate context, decisions, questions, or updates related to a task.

### Comment contains

* `id`
* `task_id`
* `author_id`
* `content`
* `created_at`
* `updated_at`

### Example

```text
Task:
"Implement Redis caching"

Comments:

Alice:
"Cache user profiles first."

Bob:
"Should we invalidate on profile updates?"

Alice:
"Yes, use cache-aside with invalidation."
```

---

# 7. Activity

The **Activity** model represents important events occurring inside NEXUS.

Instead of every action being treated as a normal CRUD operation, important actions can generate activity records.

### Activity contains

* `id`
* `organization_id`
* `actor_id`
* `entity_type`
* `entity_id`
* `action`
* `metadata`
* `created_at`

### Examples

```text
Alice created Project NEXUS

Bob created Task #42

Charlie changed Task #42 status

Alice assigned Task #42 to Bob
```

Activity becomes particularly useful when we introduce Redis Streams and event-driven processing.

---

# 8. Channel

A **Channel** represents a communication space inside an organization.

Channels allow users to communicate without attaching every message directly to a task.

### Channel contains

* `id`
* `organization_id`
* `name`
* `description`
* `created_by`
* `is_private`
* `created_at`

### Example

```text
Organization
    |
    ├── #general
    ├── #engineering
    ├── #random
    └── #project-nexus
```

---

# 9. Channel Member

A **Channel Member** connects users to channels.

### Channel Member contains

* `channel_id`
* `user_id`
* `joined_at`
* `last_read_message_id`

This allows NEXUS to track channel membership and eventually unread-message state.

---

# 10. Message

A **Message** represents a communication sent inside a channel.

### Message contains

* `id`
* `channel_id`
* `sender_id`
* `content`
* `created_at`
* `updated_at`
* `deleted_at`

Messages are stored durably in PostgreSQL, while Redis can later be used for real-time delivery, presence, caching, and event distribution.

---

# 11. Notification

A **Notification** represents an event that requires a user's attention.

Examples include:

```text
You were assigned a task.

Alice mentioned you in a comment.

Task #42 is approaching its deadline.

You received a new message.
```

### Notification contains

* `id`
* `user_id`
* `type`
* `title`
* `message`
* `entity_type`
* `entity_id`
* `is_read`
* `created_at`

Redis can later help with real-time notification delivery and temporary unread counters.

---

# 12. Presence

Presence represents the temporary real-time state of a user.

Examples:

```text
ONLINE
OFFLINE
AWAY
BUSY
```

Unlike permanent user information, presence is inherently temporary.

Therefore, Redis is a natural place for this state.

Example:

```text
presence:user:42 → online
TTL → 30 seconds
```

A user's presence can expire automatically if their client stops sending heartbeats.

---

# Relationships

The major relationships are:

```text
User
 │
 ├──────────────< Membership >────────────── Organization
 │                                             │
 │                                             ├──< Project
 │                                             │      │
 │                                             │      └──< Task
 │                                             │             │
 │                                             │             └──< Comment
 │                                             │
 │                                             └──< Channel
 │                                                    │
 │                                                    └──< Message
 │
 └──< Notification
```

---

# Application Layer Architecture

Each major feature follows the same vertical structure:

```text
Feature
   ↓
Model
   ↓
Schema
   ↓
Repository
   ↓
Service
   ↓
Endpoint
```

For example:

```text
USER

User Model
    ↓
User Schema
    ↓
User Repository
    ↓
User Service
    ↓
User Endpoint
```

### Model

Defines how the data is represented in PostgreSQL.

### Schema

Defines what the API accepts and returns.

### Repository

Handles database operations.

### Service

Contains business rules and application logic.

### Endpoint

Exposes the functionality through FastAPI.

This separation keeps database access, business logic, validation, and HTTP concerns from becoming one enormous `main.py` file that eventually becomes an archaeological site.

---

# Redis Architecture

Redis is introduced only when NEXUS has a problem that Redis solves better than PostgreSQL.

Redis will eventually be used for:

```text
Strings
 ├── counters
 ├── flags
 └── temporary state

Hashes
 ├── cached objects
 └── sessions

Lists
 └── simple queues

Sets
 ├── online users
 └── membership/presence

Sorted Sets
 ├── task priorities
 ├── scheduling
 └── rankings

TTL
 ├── sessions
 ├── OTPs
 └── presence

Pub/Sub
 └── real-time notifications

Streams
 └── event processing

Lua
 └── atomic business operations

Transactions / WATCH
 └── concurrency control

Pipelines
 └── efficient batch operations

Locks
 └── distributed coordination
```

The project will not use Redis merely to demonstrate that Redis was installed.

---

# Data Ownership

NEXUS follows a clear ownership model:

```text
                 PostgreSQL
              Source of Truth
                    |
        ┌───────────┴───────────┐
        ↓                       ↓
   Permanent Data          Business State
        |
        ├── Users
        ├── Organizations
        ├── Projects
        ├── Tasks
        ├── Comments
        ├── Messages
        └── Notifications


                      Redis
                   Fast / Temporary
                        |
                        ├── Cache
                        ├── Sessions
                        ├── Presence
                        ├── Counters
                        ├── Rate Limits
                        ├── Events
                        └── Distributed Locks
```

Redis is not treated as a replacement for PostgreSQL.

If Redis disappears, NEXUS should be designed so that permanent business data remains safe in PostgreSQL and Redis-dependent state can be rebuilt where appropriate.

---

# Authentication & Authorization

NEXUS will implement:

* User registration
* Password hashing
* Login
* JWT authentication
* Refresh tokens
* Role-based access control
* Organization-level permissions
* Resource-level authorization
* Rate limiting
* Session management

Example:

```text
Request
   ↓
JWT
   ↓
Authentication
   ↓
User
   ↓
Organization Membership
   ↓
Role / Permission
   ↓
Resource Access
```

---

# Real-Time Architecture

NEXUS will eventually support real-time communication using WebSockets.

Example:

```text
User A
   |
   | WebSocket
   ↓
FastAPI Server
   |
   ↓
Redis Pub/Sub
   |
   ├──────────────→ FastAPI Server B
   |
   └──────────────→ FastAPI Server C
                         |
                         ↓
                       User B
```

This allows multiple FastAPI instances to coordinate real-time events.

---

# Event-Driven Architecture

Important application events can eventually flow through Redis Streams.

```text
Task Updated
     ↓
Application
     ↓
Redis Stream
     ↓
Workers
     ├── Notification
     ├── Activity Log
     ├── Analytics
     └── Other Side Effects
```

This separates the main API request from slower background operations.

---

# Production Engineering Goals

NEXUS is intended to evolve from a simple backend into a distributed production-style system.

The project will progressively explore:

* Database indexing
* Transactions
* Concurrency
* Optimistic locking
* Caching
* Cache invalidation
* Rate limiting
* Background jobs
* Event-driven architecture
* WebSockets
* Redis Streams
* Distributed locks
* Observability
* Metrics
* Logging
* Docker
* Load testing
* Horizontal scaling
* Redis replication
* Sentinel
* Redis Cluster
* Failure recovery

---

# Development Philosophy

NEXUS is built incrementally.

Every technology is introduced because it solves a concrete engineering problem.

```text
Problem
   ↓
Understand why it exists
   ↓
Design solution
   ↓
Implement
   ↓
Test
   ↓
Break it intentionally
   ↓
Understand the failure
   ↓
Fix it
   ↓
Move to the next problem
```

The objective is not to memorize frameworks or Redis commands.

The objective is to understand **how a real backend system works under normal conditions, concurrent workloads, failures, and scale.**

---

# Current Project Status

NEXUS is being developed incrementally.

### Foundation

* [x] Project structure
* [x] Python virtual environment
* [x] FastAPI setup
* [x] PostgreSQL database
* [x] SQLAlchemy connection
* [x] Database session foundation
* [ ] User model
* [ ] User schemas
* [ ] User repository
* [ ] User service
* [ ] User endpoints

### Core Platform

* [ ] Organizations
* [ ] Memberships
* [ ] Projects
* [ ] Tasks
* [ ] Comments
* [ ] Activity
* [ ] Channels
* [ ] Messages
* [ ] Notifications

### Redis

* [ ] Redis integration
* [ ] Caching
* [ ] Sessions
* [ ] Presence
* [ ] Rate limiting
* [ ] Transactions
* [ ] Pipelines
* [ ] Pub/Sub
* [ ] Redis Streams
* [ ] Lua scripting
* [ ] Distributed locks

### Production

* [ ] Docker
* [ ] Testing
* [ ] WebSockets
* [ ] Background workers
* [ ] Monitoring
* [ ] Prometheus
* [ ] Grafana
* [ ] Load testing
* [ ] Redis replication
* [ ] Sentinel
* [ ] Redis Cluster

---

# Final Architecture

The long-term architecture of NEXUS is intended to look approximately like:

```text
                         CLIENTS
                            |
                            ↓
                    ┌──────────────┐
                    │ Load Balancer│
                    └───────┬──────┘
                            |
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
          FastAPI #1    FastAPI #2    FastAPI #3
              |             |             |
              └─────────────┼─────────────┘
                            |
              ┌─────────────┴─────────────┐
              ↓                           ↓
        PostgreSQL                    Redis
       Source of Truth          Distributed State
              |                           |
              |                    ┌──────┼──────┐
              |                    ↓      ↓      ↓
              |                  Cache  Pub/Sub Streams
              |                                  |
              |                                  ↓
              |                              Workers
              |
              ↓
       Permanent Business Data

                            +
                       Observability
                       ├── Prometheus
                       ├── Grafana
                       └── Logging
```

NEXUS is therefore both a **real application** and a practical environment for understanding production backend engineering, distributed systems, concurrency, caching, real-time communication, and scalable architecture.
