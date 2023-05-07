# gcp-dataflow

demo of gcp dataflow pipeline with apache beam

## Local Setup

1. Check your Python version by entering the command `python -V`

* Install Python 3 if you do not have it or a later version. You can install multiple versions of Python. Windows users can simply type python3 in the terminal, and it will open an installer from the Windows store.

2. Setup your environment with `python3 -m venv venv`

* The second "venv" is the name of the folder you want to use for your Python environment. Common names are env or venv.
* Make sure to include this folder in your .gitignore file

3. Activate the virtual environment

* From a Powershell prompt: `.\venv\Scripts\Activate.ps1`

* From bash: /venv/Scripts/activate

4. Install dependencies

~~~
pip3 install apache-beam
pip3 install google-cloud-pubsub
pip3 install google-cloud-firestore
pip install fhir.resources
pip install 'apache-beam[gcp]'
~~~

5. Save dependencies to the project

* `pip freeze > requirements.txt`

* These can be installed with pip install -r requirements.txt by teammates

6. Configure VS Code debugger

* View -> Command Palette -> Python -> Select Interpreter

* Click the + Enter Interpreter path

* Browse to the {folder}\Scripts\python.exe and select

7. Configure VS Code launch settings

* Add your GCP project and Pub/Sub to the args

* `"args": ["--runner=DirectRunner", "--mode=local", "--myproject=YOUR_PROJECT_NAME", "--input_sub=YOUR_INPUT_SUBSCRIPTION"]`

## Run as Dataflow in GCP

Make sure Dataflow is enabled in your project.

~~~
python main.py \
--project YOUR_PROJECT_NAME \
--job_name YOUR_JOB_NAME \
--runner DataflowRunner \
--region us-east1 \ 
--temp_location YOUR_BUCKET_LOCATION \
--input_sub YOUR_INPUT_SUBSCRIPTION \
--setup_file .\setup.py \
--service_account_email=YOUR_SERVICE_ACCOUNT_IF_USING
~~~

Now you will see the job listed in the Jobs menu of Dataflow.
