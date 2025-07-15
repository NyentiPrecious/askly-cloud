# Use official Python base image
FROM python:3.10

# Set work directory
WORKDIR /app

# Copy your code
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port (default for Django dev server)
EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]