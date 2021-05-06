1. dev setup (python 3)
```sh
python -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```

2. deploy to GCP
```sh
gcloud builds submit
```
