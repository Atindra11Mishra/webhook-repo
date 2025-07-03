# Dev Assessment - Webhook Receiver

Please use this repository for constructing the Flask webhook receiver.

*******************

## Setup

* Create a new virtual environment

```bash
pip install virtualenv
```

* Create the virtual env

```bash
virtualenv venv
```

* Activate the virtual env

```bash
source venv/bin/activate
```

* Install requirements

```bash
pip install -r requirements.txt
```

* Run the flask application (In production, please use Gunicorn)

```bash
python run.py
```

* The endpoint is at:

```bash
POST http://127.0.0.1:5000/webhook/receiver
```

You need to use this as the base and setup the flask app. Integrate this with MongoDB (commented at `app/extensions.py`)

✅ GitHub Webhook Endpoint

Set this endpoint in your GitHub repository webhook settings:
POST http://<your-domain-or-ngrok-url>/webhook/receiver


✅ Dashboard (UI)
You can view the stored events in a browser at:
GET http://127.0.0.1:5000/webhook/


*******************