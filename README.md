# Flask Project

Follow the next terminal commands:

```sh
# Create the venv
python -m venv venv

# Activate the venv
.\venv\Scripts\activate
pip3 install -r requirements.txt

# Run the App with uvicorn

uvicorn main:app --reload --port 8000 --host 0.0.0.0




# Navigate to:
http://127.0.0.1:8000/

- local:
http://192.168.1.5:8000/

#Documentation:

http://192.168.1.5:8000/docs
```