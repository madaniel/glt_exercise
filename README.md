# Django service - Basic Matcher API
This API finds best match for candidate and job.

## Requirement
Python 3.10

## setup
### Install environment 
python -m venv venv
./venv/scripts/activate
### Install dependencies
pip install -r requirement.txt
### Init Django
cd basic_matcher_project
manage migrate
### Create admin user
createsuperuser
### Run Django server
manage runserver
## How to use
First, you'll need to create jobs and candidates.
The best way to do so is use the admin page in http://127.0.0.1:8000/admin

For each candidate you'll need to choose: name, title and skills (optional).
Also, for each job you'll need to choose: title and skills (optional)

After you completed to fill the DB, you can send a GET Request for match with the id of the job for example:
http://127.0.0.1:8000/match/3
You will get JSON in reply with the best match for job id:3 in DB.

## Using requests
- You may send GET requests to get all the candidates or jobs in DB.
  examples: 
    http://127.0.0.1:8000/jobs/
    http://127.0.0.1:8000/candidates/
    http://127.0.0.1:8000/skills/
  
or to get a specific job or candidate by id.
    example:
    http://127.0.0.1:8000/jobs/1
  
- If you want to add candidate or job, you'll need to use POST request with JSON with the required fields. 

## Assumptions
- Each skill is unique, but you may have the same skills set for different candidates.
- If the required job has not any skills, all candidates with title-match will be returned as a match.

## Known issues
- Trying to send POST or PUT request with skills-list in the JSON may fail due and issue in Serialization.





