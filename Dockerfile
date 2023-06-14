# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
RUN apt-get update && apt-get install -y gcc

WORKDIR /app

# Copy the contents of the local repository to the container's working directory
COPY . /app

# Install project dependencies
RUN pip install -r requirements.txt
RUN cd pmeter/
RUN pip install -e . && echo 'export PATH="$PATH:/app"' >> /etc/profile

# Set the entrypoint command to run the pmeter CLI
ENTRYPOINT ["pmeter"]
# Set the default command to display the help message
CMD ["--help"]
