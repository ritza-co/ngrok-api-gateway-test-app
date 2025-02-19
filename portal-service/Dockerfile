# Use an official lightweight Python image.
FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file and install dependencies.
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the application code and static files.
COPY . .

# Expose the port the app runs on.
EXPOSE 5002

# Run the application with Uvicorn.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5002"]