# Telegram Folder Monitoring Bot

A Python script that monitors a specified folder for file uploads, sends the files as photos to a Telegram chat, and deletes the files and their containing folders.

![img schema](https://media.springernature.com/lw685/springer-static/image/chp%3A10.1007%2F978-3-030-75836-3_24/MediaObjects/509999_1_En_24_Fig5_HTML.png)
## Features

- Monitors a folder for new file uploads.
- Sends the uploaded files as photos to a specified Telegram chat.
- Deletes the uploaded files and their containing folders.

## Prerequisites

- Python 3.9 or higher
- Required Python packages are listed in the `requirements.txt` file.

## Setup

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt

## Create a .env file in the project root and set the following environment variables:

```dotenv
API_TOKEN=your_telegram_bot_api_token
FOLDER_PATH=/path/to/your/upload/folder
CHAT_ID=your_telegram_chat_id
```


## Run the script:

``` bash
python main.py
```

## Configuration
* API_TOKEN: Your Telegram Bot API token.
* FOLDER_PATH: The path to the folder to monitor for file uploads.
* CHAT_ID: The Telegram chat ID where the photos will be sent.

## Usage
The script continuously monitors the specified folder. When a new file is detected, it sends the file as a photo to the specified Telegram chat and deletes the file and its containing folder.

Issues and Contributions
If you encounter any issues or have suggestions for improvement, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.