1. dev setup
```sh
# (python3)
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
python -m pip install pytest
```

2. test
```sh
# (optional) tests will run without authentication
# gcloud auth revoke
pytest -v
```

2. deploy to GCP
```sh
gcloud auth login
gcloud builds submit
```
