# Use an Alpine Linux image with Python 3 installed
FROM python:3.9-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the Python script and requirements.txt into the container
COPY muf-script.py /app/
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set an environment variable for the macOS versions
ENV MACOS_VERSIONS="Sonoma 14, Monterey 12, Ventura 13"

# Use an entrypoint script to pass the environment variable as an argument to your Python script
ENTRYPOINT ["sh", "-c", "python muf-script.py --versions \"$MACOS_VERSIONS\""]
