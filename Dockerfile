# CRITICAL: Using 'latest' tag (Triggers IaC Scanner)
FROM python:latest

# CRITICAL: Missing USER directive (Running as Root)
# No user creation means container runs as root, offering easy escape path

# CRITICAL: Hardcoded Secret in ENV (Triggers IaC and Secret Scanner)
ENV DB_PASSWORD="production_db_password_root"
ENV API_TOKEN="sk-live-0987654321abcdef"

WORKDIR /app

# Copy files
COPY . /app

# Install dependencies (running pip as root)
RUN pip install -r requirements.txt

# CRITICAL: Installing unnecessary packages
RUN apt-get update && apt-get install -y vim curl wget

# CRITICAL: Exposing SSH port (Triggers IaC Scanner)
EXPOSE 22
EXPOSE 5000

# CRITICAL: Using shell form CMD (signals not passed correctly)
CMD python app.py
