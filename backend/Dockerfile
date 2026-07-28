# Step 1: Use an official Python image
FROM python:3.12-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy the dependency list
COPY requirements.txt .

# Step 4: Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the project files
COPY . .

# Step 6: Start the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]