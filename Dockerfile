# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Update and install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository
RUN git clone https://github.com/SSJIORI/Candletonia.git .

# Set the working directory to the cloned repository
WORKDIR /app/Candletonia

# Copy requirements.txt separately to leverage Docker cache
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port where Streamlit runs
EXPOSE 8501

# Define environment variables
ENV MYSQL_HOST=host.docker.internal
ENV MYSQL_DATABASE=dbCandletonia
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=Princessfranz02

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Command to run your application
ENTRYPOINT ["streamlit", "run", "CRUD.py", "--server.port=8501", "--server.address=0.0.0.0"]