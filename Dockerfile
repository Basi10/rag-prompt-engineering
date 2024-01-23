# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Change to the frontend directory and install any frontend dependencies (assuming there is a package.json file)
WORKDIR /app/rag-frontend
RUN npm install
RUN npm run build

# Change back to the working directory
WORKDIR /app

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run your application
CMD ["python", "app.py"]  # Replace "your_flask_app.py" with the actual name of your Flask application file
