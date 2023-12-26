##  Reference for nextpy/__init__.pyi

# Nextpy Documentation

Welcome to the official documentation for Nextpy, a powerful library for building full-stack Python applications. Nextpy enables developers to seamlessly create dynamic, responsive web applications using Python.

The documentation is structured to help you understand and utilize Nextpy's components, APIs, and best practices effectively. 

---

## Table of Contents

- Introduction
- Getting Started
- Backend
  - Admin
  - Events
  - Middleware
  - Route
  - State
  - Vars
- Frontend
  - Components
  - Page
  - Style
- Data
  - Model
  - Session
- Build
  - Compiler
  - Config
  - Testing
- Utils
- Configurations and Constants

---

## Introduction

Nextpy brings a modern twist to Python web development by integrating backend and frontend components into a single cohesive framework. It draws inspiration from projects like Streamlit and is designed to offer a developer experience similar to that of FastAPI, SQLModel, or Next.js, prioritizing documentation quality and user-friendly interfaces.

---

## Getting Started

Before diving into the comprehensive features of Nextpy, ensure you have the latest version installed. You can install Nextpy using pip:

```shell
pip install nextpy
```

To create a new Nextpy application, run:

```shell
nextpy create my-app
cd my-app
nextpy run
```

---

## Backend

### Admin

- **AdminDash**: The dashboard for administrative tasks.

### Events

- **EventChain**: Manages the sequence of backend events triggered by user actions.
- **background**: Execute tasks in the background.
- **call_script**: Run external scripts.
- **download**: Facilitate file downloads.
- **upload_files**: Handle file uploads.

### Middleware

- **Middleware**: Intercepts and processes requests and responses.

### Route

Define URL routes for your application's pages.

### State

- **State**: Represents the state of a component or the application.
- **Cookie**: Manipulate browser cookies.
- **LocalStorage**: Interact with the browser's local storage.

### Vars

- **Var**: A reactive variable that updates the UI upon changes.
- **cached_var**: A variable with a cached value for optimized performance.

---

## Frontend

### Components

- **Accordion**: Display collapsible content panels.
- **Button**: Interactive buttons for user actions.
- **DataTable**: Present data in a tabular format.
- **Form**: Collect user inputs through various form elements.
- **Modal**: Display content in a dialog overlay.
- **Tabs**: Organize content across different panes.

Each component comes with sub-components to control appearance and behavior, such as `AccordionItem`, `ModalBody`, `TabPanel`, etc.

### Page

Manage the layout and lifecycle of a web page.

### Style

- **color_mode**: Manage light and dark UI themes.
- **toggle_color_mode**: Switch between color modes.

---

## Data

### Model

- **Model**: Define data models for the application's database.

### Session

Handle database session operations for transactions and queries.

---

## Build

### Compiler

Compile and build the application for deployment.

### Config

- **Config**: Application configuration settings.
- **DBConfig**: Database configuration settings.

### Testing

Framework to write and run unit and integration tests.

---

## Utils

Utility functions for common tasks and operations.

---

## Configurations and Constants

- **Env**: Environment variables for application configuration.

---

Remember, this outline is just the starting point. Each section will be expanded with detailed explanations, code samples, property tables, and best practices. The goal is to empower developers to build robust full-stack applications with Nextpy.