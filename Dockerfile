# Base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy project files
COPY . .

# Expose port (e.g., 8000 for Django)
EXPOSE 8000

# Run Django development server
CMD python manage.py runserver 0.0.0.0:8000