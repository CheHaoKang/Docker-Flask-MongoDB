`Masky` Code Challenge
----

Thank you for your interest in joining the Pluvio team. This coding challenge will test your ability to self learn and build practical applications. All resources on internet are available to you, but you must work independently to complete the assignment.

Instructions
----
1. Create a Flask Command Line Interface application, named `Masky` <http://flask.pocoo.org/docs/1.0/cli/> using python 3
    1. Use `.env` to set any necessary environment variables
    2. Use docker or virtualenv/virtualenvwrapper to isolate your python environment
    3. Create a `requirements.txt` file to hold all python dependencies
    4. Use `git` <https://git-scm.com/> for version control and create a `.gitignore` file
2. Implement `MongoDB` and `pymongo` as the database for the web application <https://api.mongodb.com/python/current/>
3. Create a flask cli command, named `load` that saves the `fruits.csv` file from a local directory path to MongoDB, with an additional date time field for when the csv file was saved
4. Create a flask cli command, named `alter` to manipulates the original csv and saves the altered csv file in a new mongo document. The csv should be manipulated as follows:
    1. All characters in columns with string type should be capitalized.
    2. All columns with floats/integers should be incremented by 1
5. Using pytest <https://docs.pytest.org/en/latest/> , provide test coverage to prove that your program works

Bonus
----
* Using PEP 8 standards 
* Documentation, docstrings, and comments.
* Using pandas <https://pandas.pydata.org/> to perform tasks in Step 4
* Using docker-compose <https://docs.docker.com/compose/> to setup python and mongo containers.