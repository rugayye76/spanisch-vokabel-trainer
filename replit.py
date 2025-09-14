replit.md
 Overview

This is a Spanish-German vocabulary learning application built with Flask. The app provides an interactive platform for users to learn Spanish vocabulary through two main methods: writing exercises (quiz mode) and flashcards. Users can register accounts, add their own vocabulary, and practice with sample vocabulary provided by the system. The application features a clean, responsive web interface with both light and dark themes.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
The application uses a traditional server-rendered web architecture with Flask's Jinja2 templating engine. The frontend is built with:
- **Bootstrap 5** for responsive design and UI components
- **Font Awesome** for icons and visual elements  
- **Custom CSS** for theme switching (light/dark mode)
- **Vanilla JavaScript** for interactive features like theme toggling and flashcard interactions

The template structure follows a base template pattern with `base.html` serving as the main layout, extended by specific page templates (login, register, quiz, flashcards, etc.).

## Backend Architecture
The backend is a Flask web application with a simple, monolithic structure:
- **Single Flask app** (`app.py`) handling all routes and business logic
- **Session-based authentication** using Flask's built-in session management
- **In-memory data storage** using Python dictionaries for user data and vocabulary
- **Password hashing** with Werkzeug's security utilities

The application follows a traditional MVC pattern where:
- Models are represented by in-memory dictionaries
- Views are Jinja2 templates
- Controllers are Flask route handlers

## Data Storage
Currently uses **in-memory storage** with Python dictionaries:
- `users_db`: Stores user credentials and IDs
- `vocabulary_db`: Stores user-specific vocabulary collections
- Sample vocabulary is provided as a constant list

The storage is temporary and resets when the application restarts. The architecture shows evidence of previous SQLite integration (seen in attached assets) but currently operates without persistent storage.

## Authentication and Authorization
- **Session-based authentication** using Flask sessions
- **Password hashing** with Werkzeug's `generate_password_hash` and `check_password_hash`
- **Session secret key** configurable via environment variable
- **User ID tracking** through session storage
- Simple authorization checks using session data

## Learning Features
The app implements two core learning modes:
- **Quiz Mode**: Users input German words and their Spanish translations for validation
- **Flashcard Mode**: Interactive cards showing German words with reveal functionality for Spanish translations

# External Dependencies

## Frontend Libraries
- **Bootstrap 5.3.0**: CSS framework for responsive design and UI components
- **Font Awesome 6.4.0**: Icon library for UI enhancement
- **CDN-hosted libraries**: Both Bootstrap and Font Awesome are loaded from external CDNs

## Backend Dependencies  
- **Flask**: Web framework for Python
- **Werkzeug**: WSGI toolkit (comes with Flask) used for password hashing utilities

## Environment Configuration
- **SESSION_SECRET**: Environment variable for Flask session security (falls back to development key)

## Notable Architecture Decisions
The application is designed for simplicity and educational purposes:
- Uses in-memory storage instead of a database for quick setup and demonstration
- Implements basic security practices with password hashing and session management
- Provides a disclaimer system acknowledging the educational nature and temporary data storage
- Includes sample vocabulary for immediate user engagement