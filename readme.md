Python version:Python 3.12.0



python -m app.db.db_init =dbsetup
uvicorn app.main:app --reload
INSERT INTO users (id, email, first_name, last_name, date_of_birth, password, role)
VALUES
    (
        'a0b1c2d3-e4f5-6789-0a1b-2c3d4e5f6789', -- Mock UUID
        'admin@size.ba', -- Email
        'Hamza', -- First Name
        'Starcevic', -- Last Name
        '2002-01-03', -- Date of Birth (YYYY-MM-DD)
        'adminpass', -- Password (Hashed)
        'admin' -- Role
    );

Setting Up a Virtual Environment and Installing Packages
Install Python:

Ensure that Python is installed on your system. You can download it from python.org.
Open Terminal or Command Prompt:

On Windows, open Command Prompt.
On macOS or Linux, open Terminal.
Navigate to Your Project Folder:

Use the cd command to navigate to your project directory.
Example: cd path/to/your/project.
Create a Virtual Environment:

Run the following command to create a virtual environment:
Copy code
python -m venv venv
This creates a new folder named venv in your project directory containing the virtual environment.
Activate the Virtual Environment:

On Windows, run:
Copy code
.\venv\Scripts\activate
On macOS or Linux, run:
bash
Copy code
source venv/bin/activate
Your command prompt or terminal should now indicate that the virtual environment is activated.
Install Packages from requirements.txt:

Ensure requirements.txt is in your project folder.
Run the following command to install all packages listed in requirements.txt:
Copy code
pip install -r requirements.txt
Verify Installation:

You can verify that the packages are installed correctly by running:
Copy code
pip freeze
This should display all the installed packages and their versions.
Deactivate Virtual Environment:

When you're done working in the virtual environment, you can deactivate it by running:
Copy code
deactivate
Tips:
Always activate the virtual environment before working on your project.
If you add new packages to your project, update requirements.txt by running pip freeze > requirements.txt.
To ensure compatibility, it's a good practice to specify the Python version in your project documentation, especially if you are working in a team.
These instructions should help any user set up the project environment with ease.