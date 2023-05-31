# Use the official Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the Python dependencies
RUN apt-get update \
    && apt-get install -y wget curl unzip gnupg2 apt-transport-https ca-certificates firefox-esr \
    && GECKO_DRIVER_VERSION=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest | grep tag_name | cut -d '"' -f 4) \
    && wget -q --continue -P /tmp "https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz" \
    && tar -xzf /tmp/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/geckodriver \
    && pip install --no-cache-dir -r requirements.txt

# Copy all the files to the container
COPY . /app

# Expose the port on which the Streamlit app will run (default is 8501)
EXPOSE 8501

# Run the Streamlit app when the container starts
CMD ["streamlit", "run", "app.py"]
