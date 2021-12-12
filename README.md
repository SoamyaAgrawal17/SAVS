# SAVS Project
COMS 4156
ASE Team Project

### Team Members
Asmita Kumar (ak4581)

Shikha Asrani (sa3864)

Soamya Agrawal (sa3881)

Vani Jain (vj2245)

First Iteration Report: <br>
  Link: https://github.com/SoamyaAgrawal17/SAVS/blob/main/documentation/Assignment%20T3_First%20Iteration.pdf <br>
  
Seond Iteration Report: <br>
  Link: https://docs.google.com/document/d/1BTBdACvA5GKgEZiXol5g-6VtmcsekXndxYVzewYmy0E/edit?usp=sharing <br>


Documented API: <br>
  Link: https://app.swaggerhub.com/apis/savs2/SAVS/1.0.0 <br>

System Tests Corresponding to API: <br>
  Link: https://documenter.getpostman.com/view/14290543/UVC9gkKY <br>
  We used Postman test suite to run the integration tests. The API entry points are implemented in ClubsController, EventsController, StudentsController. <br>
  Postman collection json: https://github.com/SoamyaAgrawal17/SAVS/blob/main/SAVS.postman_collection.json <br>
  Postman run result : https://github.com/SoamyaAgrawal17/SAVS/blob/main/SAVS.postman_test_run.json <br>

Unit Tests: <br>
Command to run unit test: coverage run -m unittest discover test <br>
We have covered all the methods implemented in ClubService, EventService, and StudentService. <br>
For Controller methods, we have used the above System Tests. Unit tests for Controllers is planned to be implemented as part of the next iteration. <br>

Style-compliant: <br>
We used the command flake8 application>bugs.txt and flake8 test>bugs1.txt. We have fixed all the major bugs as part of this iteration. <br>


Build, run, test instructions: <br>
We have deployed the code on Heroku. And below are the configurations for the same.  <br>
Configuration: <br>
Endpoint: https://savs-project-final.herokuapp.com/ <br>
Production Database: postgresql://xbasblmhnpkibi:8a1264b9c4b71b4c8abac23f12fc7a991e3fe81671b1169a0d09c6692f7606f4@ec2-18-207-72-235.compute-1.amazonaws.com:5432/d1qeu6i6agoejb <br>
Test Database: postgresql://ganjvezplkwnyf:c2ab9de3ce2ca931f13aa6e62667607ac5f19929425b7ef16a237fe61c664d97@ec2-34-198-189-252.compute-1.amazonaws.com:5432/dbjeqssrqgcj15 <br> <br>

To build, run and test on localhost or Heroku, follow the following steps:
1. git clone https://github.com/SoamyaAgrawal17/SAVS
2. Create a virtual environment and activate it. Command: python3 -m virtualenv venv > source venv/bin/activate 
4. pip3 install -r requirements.txt
5. python3 freeze> requirements.txt
6. python3 app.py
7. The application would run on port 5000
8. To deploy the code on Heroku, follow the instructions in the following reference link: https://medium.com/analytics-vidhya/heroku-deploy-your-flask-app-with-a-database-online-d19274a7a749 <br> 
9.  To run the code on local, postgres db has to be setup in local, and replace the
10.  To connect to your local database, replace app.config['SQLALCHEMY_DATABASE_URI'] in app.py with 'postgresql://<username>:<password>@localhost:5432/<db-name>'


- Manual Testing can be done by using the above Endpoint. <br>
- Unit Testing could be done by running the command coverage run -m unittest discover test or using push button to run all the unit tests. <br>
- For integration testing clear the database and run the collection SAVS on Postman(The collection json is shared and IA is added to the postman workspace). <br>

To build client: <br>
  
  1. Install node: https://nodejs.org/en/download/
  2. Alternative through Homebrew: brew install node
  3. Check if node is installed: node -v
  4. Add your Google Client ID in index2.html
  5. Go to SAVS/client and run: node app.js
  6. Open Chrome in Guest mode or any other browser after logging out from google accounts and go to http://localhost:8080
  
CI/CD reports: <br>
  ![alt text](https://github.com/SoamyaAgrawal17/SAVS/blob/main/CircleCI_reports_instructions.png?raw=true)
  Unit Test Cases and Coverage: [ENTER THE LINK AFTER THE LAST COMMIT] <br>
  Integration Test Cases: [ENTER THE LINK HERE AFTER THE LAST COMMIT] <br>
  Bug Finder using SonarCloud: [ENTER THE LINK HERE AFTER THE LAST COMMIT] <br>
  Style Checker using Flake: [ENTER THE LINK HERE AFTER THE LAST COMMIT] <br>
  
