# Usage

#### Run PostgreSQL in Docker  
``` shell  
 docker run -d \
--name myPostgresDb \
-p 5432:5432 \
-e POSTGRES_USER=root \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_DB=suppliers \
-e POSTGRES_HOST=localhost \
postgres
```

## Docker-compose

#### Build the image  
``` shell  
docker build --tag api_automation .  
```
#### Run image  
``` shell  
 docker run \
    -d \
    -v ${PWD}/allure-results/default/results:/pytest_template/allure-results \
    api_automation
```
#### Run docker-compose for generating and displaying Allure reports  
``` shell  
docker-compose up -d  
``` 

## Docker

#### Run Allure service  
``` shell 
docker run -d \
    -p 5050:5050 \
    -e CHECK_RESULTS_EVERY_SECONDS=3 \
    -e KEEP_HISTORY=25 \
    -v ${PWD}/allure-results:/app/allure-results \
    -v ${PWD}/allure-reports:/app/allure-reports \
    frankescobar/allure-docker-service  
```
#### Run Allure UI  
``` shell 
docker run -d \
    -p 5252:5252 \
    -e ALLURE_DOCKER_PUBLIC_API_URL=http://localhost:5050 \
    frankescobar/allure-docker-service-ui  
```
#### Run tests  
``` shell 
docker run \
    -d \
    -v ${PWD}/allure-results/default/results:/pytest_template/allure-results \
    api_automation  
```

# Useful info

#### Virtual environment (Mac OS)
``` shell
python3 -m venv venv
source venv/bin/activate
```

#### Run Jenkins  
``` shell
jenkins-lts
```
#### Saving and installing packages

``` shell
# Create file requirements.txt and save all packages here
pip freeze > requirements.txt 

# Install all packages from file
pip install -r requirements.txt
```
#### Allure reporting
1. Install **allure-pytest** modul (create report in JSON format)
2. Converting JSON filed to HTML report  
-- Install Java 8+  
-- Install node.js  
-- Install allure command line tool
``` shell
npm install -g allure-commandline --save-dev
```
3. Create dir to save reports (in JSON format) 
4. Run the command
``` shell
pytest --alluredir allure-results Test_dir
```  
5. Run the command (to convert JSON files in HTML)  
``` shell
allure serve AllureReports  
```
#### Pytest report
**pytest-html-reporter==0.2.9** lib
#### Allure configuration in Jenkins
1. Manage Jenkins -> Manage Plugins -> Install "Allure" plugin
2. Manage pipeline -> Global Tool Configuration -> Allure Commandline-> set allure settings
#### Dockerfile  
[Dockerfile usage](https://docs.docker.com/engine/reference/builder/)