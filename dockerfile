# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN apt update -y && apt install awscli -y 
# Install any needed packages specified in requirements.txt
RUN apt-get update && pip install -r requirements.txt


# Run the application
CMD ["python3", "app.py"]