# PedalPals

<p align='center'>
<img width="600" alt="image" src="https://github.com/crustyapples/PedalPals-Backend/assets/24990448/32bbe678-3cea-49a8-81a6-967c4e56680a">
</p>

<p align="center">
    <a href="https://github.com/crustyapples/PedalPals-Frontend">Frontend</a>
    |
    <a href="https://github.com/crustyapples/PedalPals-Backend">Backend</a>
    |
    <a href="https://youtu.be/yYxC69_shPs">Demo Video</a>
</p>

# PedalPals-Backend
This is the backend repository for PedalPals. Built on Flask, and MongoDB. Hosted on Railway

## Prerequisites

Before you begin, make sure you have the following installed on your system:

- Python (version 3.9.7)
- pip (Python package manager)

## Setting Up a Virtual Environment

It's a good practice to work in a virtual environment to keep project dependencies isolated. To set up a virtual environment, follow these steps:

1. In the root directory of the project, create a new virtual environment:

    ```bash
    python -m venv env
    ```

    This will create a new directory called `env

2. Activate the virtual environment:

    ```bash
    source env/bin/activate
    ```

    This will change your terminal prompt to indicate that you're working in the virtual environment.

3. Install the project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    This will install all the dependencies listed in the `requirements.txt` file.

4. Setup Config Files by creating a config.py at the given directories that contains the following:

    ```python
    # app/utils/config.py
    GOOGLE_MAPS_API = 'YOUR_API_KEY'
    EMAIL = 'EMAIL USED FOR ONEMAPS ACCOUNT'
    PASSWORD = 'YOUR_PASSWORD>'
    ```
    Note that you will need to register for the OneMap API

    ```python
    # app/config.py
    class Config:
        MONGO_URI = ''
        JWT_SECRET_KEY = '' 
    ```

5. Run tests by running the following command:

    ```bash
    pytest
    ```
