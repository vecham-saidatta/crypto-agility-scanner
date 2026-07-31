# Step 1: Use an official Python image
FROM python:3.12-slim
# step 2: installs Git
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Step 3: Set the working directory
WORKDIR /app

# Step 4: Copy the dependency list
COPY requirements.txt .

# Step 5: Install all dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 6: Copy the project files
COPY . .

# Step 7: Start the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]