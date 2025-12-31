# Overview

This is a Music Playlist Manager called CloudMeowsic using Python and Firestore (Firebase). The application allows users to create, edit, delete, and view playlists. Each playlist contains a list of songs, and each song has attributes such as title, artist, and genre. The system supports multiple playlists per user and allows basic searching and filtering. It uses a NoSQL structure with Firestore and implements a basic CLI (command-line interface) to interact with the data. It implements user authentication so users can securely manage their playlists.

CloudMeowsic integrates with Firestore, a cloud-hosted NoSQL database, to store user information, playlists, and songs. User credentials are securely saved, and each user's playlists are organized under their own Firestore document collections. The Python program interacts with Firestore through the Firebase Admin SDK, allowing real-time database operations such as creating, reading, updating, and deleting playlists and songs.

To use the program, run the Python script `CloudMeowsic.py`. You will first be prompted to either log in or register as a new user. After authentication, you can create playlists, add songs, update or delete playlists, and search for songs within your playlists—all through simple text-based menu options.

The purpose of writing this software was to build a practical, user-friendly music playlist manager that demonstrates cloud database integration with Python. It also serves as a learning project for working with Firestore and practicing secure user authentication and CRUD operations.

[Software Demo Video](https://youtu.be/r7VDe9yDNu8)

# Cloud Database

The cloud database used is **Google Firestore**, a flexible, scalable NoSQL database from Firebase. Firestore provides real-time synchronization, offline support, and robust querying capabilities, which make it well suited for managing hierarchical data like users, playlists, and songs.

The database structure is as follows:

- `users` collection: Each document corresponds to a user, keyed by their username.
  - Fields: `password` (stored as plaintext currently, to be improved), `created` (timestamp).
  - Each user document has a subcollection `playlists`.
- `playlists` subcollection under each user document: Each playlist is a document with a numeric string ID.
  - Fields: `name` (playlist name), `description` (text), `songs` (an array of song objects).
- Each song in `songs` array has fields: `title`, `artist`, and `genre`.

This structure isolates each user’s data and allows efficient querying and management of their playlists.

# Development Environment

This project was developed using:

- **Programming Language:** Python 3.9+
- **Libraries:**
  - `firebase-admin` for Firestore database operations and authentication.
- **Tools:**
  - Firebase Console for managing Firestore database and service account credentials.
  - Code editor: VS Code (recommended) or any Python IDE.
- **Operating System:** Development was done on Windows 11, but the program is cross-platform as long as Python and required libraries are installed.

# Useful Websites

- [Database Options in the Cloud](https://www.oreilly.com/library/view/an-introduction-to/9781492044857/ch01.html)
- [Firestore Documentation](https://firebase.google.com/docs/firestore)
- [Firebase Admin SDK for Python](https://firebase.google.com/docs/admin/setup)
- [Google Cloud Authentication](https://cloud.google.com/docs/authentication/client-libraries)
- [Python Official Documentation](https://docs.python.org/3/)

# Future Work

- Upgrade security by implementing cryptographic hashing (e.g., bcrypt) to securely store passwords instead of plaintext.
- Add functionality for user password reset and recovery.
- Improve user interface with a GUI or web-based frontend for better usability.
- Add support for song metadata such as duration, album, and release year.
- Implement user session management and token-based authentication for enhanced security (MAYBE).
