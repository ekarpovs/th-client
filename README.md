# Theater client
Producer(Prompter) and consumer(Viewer) clients

## Project structure
``` bash
├── README.md
├── .gitignore
├── .github
│   └── workflows
│       └── publish.yaml
├── .pre-commit-config.yaml
├── src
│   ├── app.py
│   ├── config.py
│   ├── description.py
│   ├── loader.py
│   └── router.py
├── main.py
├── pytest.ini
├── requirements.txt
├── requirements_dev.txt
└── tests
    ├── __init__.py
    └── test_app.py
```

### Setup the project for the development
For this project will be installed:
* [aiofiles](https://pypi.org/project/aiofiles/) - for handling local disk files in asyncio applications   
* [fastapi](https://fastapi.tiangolo.com/) - popular framework for API's
* [flake8](https://flake8.pycqa.org/en/latest/) - for linting
* [pip](https://pypi.org/project/pip/) - for install packages
* [pipdeptree](https://pypi.org/project/pipdeptree/) - for sorting packages
* [pre-commit](https://pre-commit.com/) - Git hook scripts are useful for identifying simple issues before submission to code review   
* [pytest](https://docs.pytest.org/en/7.3.x/) - for unit tests  
* [python-dotenv](https://pypi.org/project/python-dotenv/) - for reading .env files  
* [uvicorn](https://www.uvicorn.org/) - an ASGI web server implementation for Python.  

### Create virtual environment
```bash
python3 -m venv .thcltvenv
```

### Install dependencies
    - development   
```bash
pip install -r requirements_dev.txt
```
    - production   
```bash
pip install -r requirements.txt
```

### Run (localy)
    - development   
```bash
python main.py <ext_url_value>
```
    - production   
```bash
EXTERNAL_URL=<ext_url_value>  python main.py
```

### Check from browser
```bash
1. http://127.0.0.1:8011/
```
Data broadcast service is live
```

### Linting
```bash
flake8 -v --max-line-length=79 --max-doc-length=72 --ignore=E203,W503 ./src
```

### Unit testing
```bash
pytest
```

### Build the docker file 
```bash
docker build . --tag ekarpovs/th-client-aarch64:1.0.0
docker build . --tag ekarpovs/th-client-x64:1.0.0
```

### Publish to the Docker registry
```bash
docker login -u <your-github-username>
docker push ekarpovs/th-client-aarch64:1.0.0
``` 

### Build and publish to the Docker registry the docker file for x64 architecture
```
from GitHub repository Actions run the publish action
```

