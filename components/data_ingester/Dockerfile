# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the script into the container
COPY data_ingenstion.py ./

# Install dependencies
RUN pip install pandas google-cloud-storage

# Set the command to run the script
ENTRYPOINT ["python", "data_ingenstion.py"]