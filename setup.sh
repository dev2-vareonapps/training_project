sudo apt update
sudo apt install -y git python3-venv gh
cd backend 
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic
echo "Setup completed.activate venv and run uvicorn"
