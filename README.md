# Idealista Bot

A bot designed to monitor real estate listings on Idealista. It fetches and analyzes property data daily, and sends email notifications for possible new investment opportunities.

## Features

* Featches real estate data from Idealista API
* Analyzes and cleans data to ensure relevance
* Sends email notifications with detailed info
* Executes daily to keep the data up to date

## Instalation

To run this project locally or on a Raspberry Pi, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/vitor29narciso/idealista-bot.git
cd idealista-bot
```

### 2. Set Up the Environment
#### Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

#### Environment Variables
Create a `.env` file in the root directory with the following content:
```python
API_KEY="your_api_key_here"

SENDER_EMAIL="sender_email@example.com"
SENDER_APP_PASSWORD="sender_password_here"

RECIPIENT_EMAIL_ONE="recipient_one_email@example.com"
RECIPIENT_EMAIL_TWO="recipient_two_email@example.com"
RECIPIENT_EMAIL_THREE="recipient_three_email@example.com"
```
**Note:** Replace the placeholders with your actual credentials. You can use the `.env.example` as a template.

## File Structure

This project consists of the following Python files:
* `main.py`: Coordinates all functionality.
* `fetch_listings.py`: Fetches initial and daily property data from Idealista.
* `process_listings.py`: Cleans and processes the initial and the daily data.
* `notify.py`: Sends email notifications with the new property details.
* `config.py`: Contains all the configuration constants.

```bash
Idealista-Bot/
├── data/
│    ├── default_image.webp
│    └── region_listings.csv
├── idealista_bot/
│    ├── __init__.py
│    ├── config.py
│    ├── fetch_listings.py
│    ├── notify.py
│    └── process_listings.py
├── .env
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

## Notification Scheduling

To schedule notifications from the bot, use `cron` to run the bot at a certain time of the day. Add the following line to your `crontab`:
```bash
0 HH * * * /usr/bin/python3 /path/to/idealista-bot/main.py >> /path/to/idealista-bot/log.txt 2>&1
```
**Note:**
* Replace `HH` with the hour you want to send your daily notification.
* Replace `/path/to/idealista-bot/` with the actual directory path where the project is stored.
* `log.txt` file will store output logs for debugging purposes.

## Author

**Vítor Narciso**

Data Analyst @ Airbus | Teaching Assistant @ ISCTE-IUL \
PGCert Business Intelligence | MSc Aerospace Engineering

* Location: Lisbon, PT
* Phone: [+351 965465625](tel:+351965465625)
* E-mail: [vitor.narciso@tecnico.ulisboa.pt](mailto:vitor.narciso@tecnico.ulisboa.pt)
* GitHub: [@Vitor29Narciso](https://github.com/Vitor29Narciso)
* LinkedIn: [vitor29narciso](https://www.linkedin.com/in/vitor29narciso/)