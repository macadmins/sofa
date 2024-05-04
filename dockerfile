# Use an Alpine Linux image with Python 3 installed
FROM python:3.12-alpine

# Copy the CA certificate into the container
#COPY apple_root_ca.pem /usr/local/share/ca-certificates/
#COPY Apple_Intermediate.crt /usr/local/share/ca-certificates/

# Update CA certificates store
#RUN update-ca-certificates

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and requirements.txt into the container
COPY build-sofa-feed.py /app/
COPY process_uma.py /app/
COPY process_ipsw.py /app/
COPY config.json /app/
COPY feed_structure_template_v1.yaml /app/
COPY forked_builds.json /app/
COPY sofa-time-series.py /app/
COPY requirements.txt /app/

# Check if the file exists before copying
RUN touch time-series.csv || true
COPY time-series.csv /app/

COPY model_identifier_*.json /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Accept an environment variable for the OS type at build time
ARG OS_TYPE
ENV OS_TYPE=${OS_TYPE}

# Use an entrypoint script to pass the environment variable as an argument to your Python script
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
