# 1. Use Python 3.9 as the base
FROM python:3.9-slim

# 2. Set the working directory
WORKDIR /app

# 3. Copy all your GitHub files into the container
COPY . .

# 4. Install the libraries
RUN pip install --no-cache-dir -r requirements.txt

# 5. RUN THE INJECTION SCRIPT (Crucial Step!)
# This runs immediately after installation to fix the HTML
RUN python inject_meta.py

# 6. Expose the port
EXPOSE 8501

# 7. Start Streamlit
# We specifically bind to 0.0.0.0 for Railway compatibility
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
