# Use an official Debian image as a parent image
FROM debian:latest

# Update packages and install curl
RUN apt-get update && apt-get install -y curl

# Create a directory for the app
WORKDIR /app

# Add the script to the container
COPY send_heartbeat.sh /app/send_heartbeat.sh

# Make the script executable
RUN chmod +x /app/send_heartbeat.sh

# Command to run the script at runtime using Bash
CMD ["/bin/bash", "/app/send_heartbeat.sh"]
