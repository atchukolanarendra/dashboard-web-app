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

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/dashboard-web-app.git
cd dashboard-web-app

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
![WhatsApp Image 2024-11-20 at 4 53 57 PM](https://github.com/user-attachments/assets/219422d4-6b53-42b6-a4b9-c725e21cc750)
![WhatsApp Image 2024-11-20 at 4 53 57 PM (1)](https://github.com/user-attachments/assets/5484b9df-af47-405b-9189-5197fcf788da)
The Backend Image:
![WhatsApp Image 2024-11-20 at 4 53 57 PM (2)](https://github.com/user-attachments/assets/4cd2da6f-8a0b-4868-a624-34f8ee1f67fe)


  
