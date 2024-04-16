# SpeakersScraper & DataWriter
This project is intended to scrape speaker data from a webpage and save it into various formats including JSON, CSV, and Google Sheets.

## Prerequisites
Before running this script, you will need a JSON file which contains the Google API keys. To download this JSON file:

1. Go to the [Google API Console](https://console.developers.google.com/)
2. Create or select a project.
3. Navigate to 'Credentials' on the sidebar.
4. Click 'Create Credentials' and choose 'Service account'.
5. Follow the prompts and download the JSON file.

Make sure to copy the downloaded JSON file in the project directory.
## Installation
Clone the repository:
```bash
git clone https://github.com/alexsproject/or-ttask-scrap.git
```

Run virtual environment:
```bash
poetry shell
```

Install dependencies:
```bash
poetry install
```
## Configuration

Configuration settings such as the path to Google service account credentials for Google Spreadsheet saving (`CREDS_PATH`), sharing email for Google Spreadsheet (`SHARING_EMAIL`) should be stored in a `.env` file which should be located in the same directory as your script. You simply need to replace the placeholder text in the `.env.example` file with your actual details and rename this file to `.env`.

Here is an example of what the contents of the `.env` should look like:
```env
CREDS_PATH=/path/to/creds.json 
SHARING_EMAIL=user@example.com
```
## Usage

The script is executed via command line with the valid file name passed as an argument using -f or --file. 
A sample command looks like this:
```bash
poetry run python3 main.py -f output.json
```
Replace `output.json` with your preferred filename and extension. The extension can be `.json`, `.csv` or `.gsheets`, depending on your preferred output format.


## Conclusion

This script provides a solid foundation for a variety of use-cases, since it separates the concerns of data scraping and data writing. Feel free to adjust or build on this template to suit your needs. Enjoy scraping!

## Disclaimer

This code is for educational purposes and should be used responsibly complying with legal and ethical guidelines. Always respect and protect privacy. Don’t use it to scrape confidential or sensitive data without proper permissions.