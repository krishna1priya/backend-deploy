# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

COPY ./patient-and-insurance-ma-53708-firebase-adminsdk-x24uk-6bca3490f1.json /app/

# Install system dependencies required for psycopg2
RUN apt-get update && apt-get install -y libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV DJANGO_SETTINGS_MODULE=phim_search_project.settings  

# Start Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "phim_search_project.wsgi:application"]
