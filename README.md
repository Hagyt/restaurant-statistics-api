

# restaurant-statistics-api

**Description**:  
A simple REST API with CRUD operations and endpoint that returns a statistical data from a csv with some data imported into a sqlite database.


## How to start the project:  

**1. virtualenv**  
  
Inside the root folder of repository execute `virtualenv venv` to create a virtual enviroment the `venv` corresponds to enviroment name, so you can name it with another name if you want.  
  
Now you can activate it with `.\restaurant_env\Scripts\activate.bat` if you are on Windows or `. mientornovirtual/bin/activate` if you are on Linux, to desactivate it you can execute `deactivate`.

**2. requirements.txt**  
  
Now you have to install the requirements for the app, so execute `pip install -r requirements.txt` and that must work.

**3. FLASK_APP**  
  
Finally execute `export FLASK_APP=app.py` if you are on Linux or `set FLASK_APP=app.py` if you are on Windows and then execute `flask run` with that the app must start
