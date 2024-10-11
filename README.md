Overview
This project provides a RESTful API built with Django to analyze a patent dataset. It allows users to retrieve summary statistics and query the dataset based on various parameters.

Prerequisites
    Python 3.8 or higher
    Django 5.0 or higher
    Django REST framework
    Pandas
    PostgreSQL 16

You can install the necessary packages using pip:  pip install django djangorestframework pandas


**Running the API Locally**
  1 Clone the repository:
    git clone <repository-url>
    cd <repository-name>
  
  2 Set up the database:
      Make sure you have the CSV file with the patent data available in the project directory.
      Update the settings in settings.py to add postgresql as database
  
  3 Run migrations:
    python manage.py migrate
  
  4 Load the data: check the management command to load your CSV data into the database, run it:
    python manage.py load_patents
  
  5 Run the server:
    python manage.py runserver
    Access the API: Open your browser and navigate to [http://localhost:8000/.](http://0.0.0.0:8000/)


**Running the API with Docker-Compose**
  1 Ensure Docker and Docker-Compose are installed on your machine.
  
  2 Clone the repository (if you haven't already):
      git clone <repository-url>
      cd <repository-name>

  3 Build and start the services:
    docker-compose up --build
    Access the API: Open your browser and navigate to http://localhost:8000/.


**API Endpoints**
Summary Endpoint


![Screenshot 2024-10-12 at 01-50-13 Summary View – Django REST framework](https://github.com/user-attachments/assets/1800574a-057b-472a-a8bc-aebf0a9cb0f1)


  URL: /summary
    Method: GET
    Description: Retrieves summary statistics of the dataset.
    Response:
        json


Query Endpoint
    URL: /query
    Method: GET
    Query Parameters:
        id
        source
        date_published
        pages_min
        pages_max
        title
        inventer
        filing_date
        applicant_name
        patent_number
        relevancy_min
        relevancy_max
    Description: Filters the dataset based on provided parameters.

    
Example Request:![Screenshot 2024-10-12 at 01-54-18 Query View – Django REST framework](https://github.com/user-attachments/assets/0661afb3-b4c3-424b-a7c1-46ec45c66db3)
