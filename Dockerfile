# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run Gunicorn server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "3", "--timeout", "120", "app:app"]

