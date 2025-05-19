# CollabW - Project Management Tool

CollabW is a lightweight web project management tool designed to facilitate collaboration among teams. It features a modern front-end built with Vue 3 and a robust back-end powered by FastAPI. This README provides an overview of the project, its features, and how to get started.

## Features

- **User Authentication**: Secure login and registration for users.
- **Project Management**: Create, update, and delete projects.
- **Task Management**: Add, update, and manage tasks within projects.
- **Real-time Collaboration**: Collaborate with team members in real-time.
- **Responsive Design**: Works seamlessly on both desktop and mobile devices.

## Project Structure

The project is organized into two main directories: `backend` and `frontend`.

### Backend

- **app**: Contains the main application code.
  - **api**: Defines the API endpoints and dependencies.
  - **core**: Contains core functionalities and configurations.
  - **db**: Manages database interactions.
  - **models**: Defines the data models.
  - **schemas**: Contains Pydantic schemas for data validation.
- **main.py**: Entry point for the FastAPI application.
- **requirements.txt**: Lists the required Python packages.

### Frontend

- **public**: Contains static files for the main HTML file.
- **src**: Contains the Vue application source code.
  - **components**: Reusable Vue components.
  - **views**: Different views for the application.
  - **stores**: Vuex stores for state management.
  - **router**: Vue Router configuration.
- **package.json**: Lists the required npm packages and scripts.
- **vite.config.ts**: Configuration for Vite.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd collabw
   ```

2. Set up the backend:
   - Navigate to the `backend` directory:
     ```
     cd backend
     ```
   - Install the required Python packages:
     ```
     pip install -r requirements.txt
     ```

3. Set up the frontend:
   - Navigate to the `frontend` directory:
     ```
     cd frontend
     ```
   - Install the required npm packages:
     ```
     npm install
     ```

### Running the Application

1. Start the backend server:
   ```
   cd backend
   uvicorn main:app --reload
   ```

2. Start the frontend development server:
   ```
   cd frontend
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:3000` to access the application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.