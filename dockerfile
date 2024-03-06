# Use an Alpine Linux image with Python 3 installed
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and requirements.txt into the container
COPY muf-script.py /app/
COPY muf-time-series.py /app/
COPY requirements.txt /app/

# Check if the file exists before copying
RUN touch time-series.csv || true
COPY time-series.csv /app/

COPY model_identifier_*.json /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set an environment variable for the macOS versions
ENV MACOS_VERSIONS="Sonoma 14, Monterey 12, Ventura 13"

# Use an entrypoint script to pass the environment variable as an argument to your Python script

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
