FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/SSJIORI/Candletonia.git .

RUN pip3 install -r requirements.txt

EXPOSE 8501

# Define environment variables
ENV MYSQL_HOST=host.docker.internal
ENV MYSQL_DATABASE=dbCandletonia
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=Princessfranz02

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health 

ENTRYPOINT ["streamlit", "run", "CRUD.py", "--server.port=8501", "--server.address=0.0.0.0"]