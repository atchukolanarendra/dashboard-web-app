# Dashboard Web Application

This is a Flask-based web application that serves as a dashboard for users to interact with various functionalities like scraping data from websites, generating AI-based prompts, and viewing past logs. The application uses Flask for the backend, SQLAlchemy for database management, and integrates with Google OAuth for user authentication. It also uses LangChain's OpenAI integration for generating responses to prompts.

## Features
- **User Authentication** via Google OAuth.
- **Data Scraping**: Scrape content from URLs and store metadata in the database.
- **Prompt Generation**: Use OpenAI's language models to generate responses based on user-provided prompts.
- **Dashboard**: View past scraped data and prompt logs in a user-friendly interface.

## Requirements

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-Dance
- OpenAI API (via LangChain)
- SQLite database (or configure a different database)

### Set Up Environment Variables
 Create a .env file in the root directory and add your environment variables:
 SECRET_KEY=your_secret_key
 DATABASE_URL=sqlite:///test.db  # You can use a different database like PostgreSQL
 GOOGLE_CLIENT_ID=your_google_client_id
 GOOGLE_CLIENT_SECRET=your_google_client_secret

###  Install Dependencies
 Create a virtual environment and install the dependencies:
 python3 -m venv venv
 source venv/bin/activate  # For Linux/MacOS
 venv\Scripts\activate  # For Windows
 pip install -r requirements.txt

### Initialize the Database
 Run the following commands to set up the database:

flask db init
flask db migrate
flask db upgrade

### Run the Application
Run the Flask application:
    
    run: app.py

#### Your application should now be running on http://127.0.0.1:5000.

### Access the Dashboard
Go to the home page (http://127.0.0.1:5000/) and log in with your Google account to start interacting with the dashboard.

## Output Images:
![WhatsApp Image 2024-11-20 at 4 53 57 PM](https://github.com/user-attachments/assets/bca15799-034f-421a-8361-7be4509fc24f)

![WhatsApp Image 2024-11-20 at 4 53 57 PM (1)](https://github.com/user-attachments/assets/e9544e47-3e9d-4367-b0d2-d05d22268c29)

The backend image:
![WhatsApp Image 2024-11-20 at 4 53 57 PM (2)](https://github.com/user-attachments/assets/4313d8b5-3256-4874-b3f4-3cadd0c995f7)

### **requirements.txt**

 1.Flask==2.2.3
 
 2.Flask-SQLAlchemy==2.5.1

 3.Flask-Dance==5.1.0
4.Flask-Migrate==3.1.0
5.requests==2.28.1
6.beautifulsoup4==4.11.1
7.python-dotenv==0.21.0
8.langchain==0.0.162
9.openai==0.27.0

#### Explanation of the requirements.txt file:
Flask - The web framework for Python used to build the web application.
Flask-SQLAlchemy - For integrating SQLAlchemy with Flask for database management.
Flask-Dance - Provides OAuth integration, specifically for Google login in this case.
Flask-Migrate - To handle database migrations.
requests - To handle HTTP requests for web scraping.
beautifulsoup4 - To parse HTML content and scrape data from web pages.
python-dotenv - For managing environment variables in the .env file.
langchain - The library to interface with OpenAI for generating prompts.
openai - The official OpenAI Python client, used here for calling the GPT model via LangChain.


