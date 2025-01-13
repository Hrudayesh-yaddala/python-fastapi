# FastAPI Project with MySQL

This is a FastAPI project that demonstrates CRUD operations with a MySQL database.

## Prerequisites
- Python 3.8+
- MySQL installed and running

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/fastapi_project.git
   cd fastapi_project
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - On **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - On **Mac/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables**:
   - Create a `.env` file in the root directory and add:
     ```
      DATABASE=YOUR_DATABASE_NAME
      PASSWORD=YOUR_PASSWORD
     ```

6. **Run the FastAPI application**:
   ```bash
   uvicorn main:app --reload
   ```

7. **Access the application**:
   - Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.
   - Swagger UI is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Key Commands
- **Deactivate virtual environment**:
  ```bash
  deactivate
  ```
- **Reinstall dependencies from `requirements.txt`**:
  ```bash
  pip install -r requirements.txt
  ```
