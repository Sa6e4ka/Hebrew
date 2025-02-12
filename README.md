# Hebrew Learning Bot

### This project is a Telegram bot designed to help Russian-speaking users learn Hebrew. The bot provides various features for learning new words, reviewing learned ones, participating in competitions, and managing the database.

## Installation and Setup

### Requirements:
Python 3.8 or higher
Virtual environment (recommended)
Installation

### Clone the repository:
```
git clone https://github.com/Sa6e4ka/Hebrew.git
```
### Navigate to the project directory:
```
cd Hebrew
```
### Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install dependencies:
```
pip install -r requirements.txt
```
### Create a .env file in the project's root directory and add the following variables:
```
TOKEN=<your_bot_token>
DATABASE_URL=<your_database_url>
```

### If running the bot on Linux Ubuntu 22.04, install the pkg-config and libmysqlclient-dev packages:
```
sudo apt-get update
sudo apt-get install pkg-config libmysqlclient-dev
```

## Running the Bot

### To start the bot, run the following command:
```
python main.py  
```
