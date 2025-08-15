# About

This repo contains the FastAPI web application for Image Training Summary & Quiz Generator Project as a part of AI Education Innovation Bootcamp organized by [Chunjae Education](https://chunjae.co.kr)

# Running & Developing

## FYKI
We are using a [FastAPI](https://fastapi.tiangolo.com/) and [MongoDB](https://www.mongodb.com/) stack, utilizing [Jinja2](https://jinja.palletsprojects.com/en/stable/) templating engine. All CSS is hand-written currently, with no library shenanigans of Tailwind or Bootstrap *(likely to change in the near future)*. 
> Contributions are welcome **after** the Hackathon ends.

## Preliminary Setup of the Database -- MongoDB
### Installation Guide for `MongoDB Community Edition`
#### `Linux (Ubuntu 24.04.x)` guide 
```bash
sudo apt-get install gnupg curl

curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
   --dearmor

echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list

sudo apt-get update

sudo apt-get install -y mongodb-org

sudo systemctl start mongod # start the daemon
```

#### `Windows` guide
Follow this: [](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)

> अरु systemsको लागि आफै खोज लोल

## Repo setup using `uv` (recommended)
If `uv` isn't installed, install it using:
### Linux/macOS
In your favorite [terminal](https://sw.kovidgoyal.net/kitty/) run:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Windows
In `PowerShell` run:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### After `uv` is installed
Run (in MinGW or bash):

```bash
git clone https://github.com/suynep/ImageTrainingSummary-QuizGen
cd ImageTrainingSummary-QuizGen/
uv add -r requirements.txt
uv run fastapi run main.py
```

## Repo setup using `pip`
Run (in MinGW or bash):

```bash
git clone https://github.com/suynep/ImageTrainingSummary-QuizGen
cd ImageTrainingSummary-QuizGen/
python3 -m virtualenv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
fastapi run main.py
```

# Contributing
We **aren't currently accepting any external contributions** while the Hackathon/Bootcamp is running. However, post-event, you can always *Fork the repo, make changes to your fork, create a PR!*
