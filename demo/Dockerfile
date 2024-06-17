FROM python:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /app

# Command to run application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]