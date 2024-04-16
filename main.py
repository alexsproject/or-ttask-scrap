import dotenv
import os
import csv
import requests
import json
import gspread
import argparse
from oauth2client.service_account import ServiceAccountCredentials
from bs4 import BeautifulSoup

from utils import validate_filename

dotenv.load_dotenv()
PATH_TO_CREDS = os.getenv("CREDS_PATH")
SHARING_EMAIL = os.getenv("SHARING_EMAIL")


class SpeakersScraper:
    def __init__(self, creds_path, base_url, sharing_email):
        self.creds_path = creds_path
        self.base_url = base_url
        self.sharing_email = sharing_email
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name(
            filename=self.creds_path, scopes=self.scope
        )
        self.speakers_data = []

    @staticmethod
    def get_speakers_data_from_site():
        try:
            # HTTP-request to the site
            response = requests.get("https://interaction24.ixda.org/", timeout=10)
            response.raise_for_status()
            # converts the response body into a BeautifulSoup object for HTML parsing
            soup = BeautifulSoup(response.text, "html.parser")
            # return all people
            return soup.select(
                "div.speakers-list_component div.speakers-list_list div.speakers-list_item"
            )
        except requests.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except Exception as err:
            print(f"An error occurred: {err}")

    def extract_speaker_data(self, speaker):
        # Collect all speakers' data into dictionaries
        speaker_data = {
            "Name": speaker.select_one("h3.speakers-list_item-heading").text,
            "Role": speaker.select_one(
                'div[class="margin-bottom margin-small"] > div:nth-of-type(2)'
            ).text,
            "ImageLink": speaker.select_one(
                "div.speakers-list_item-image-wrapper > img"
            )["src"].replace("..", self.base_url),
        }
        social_links_elements = speaker.select(
            'div[class="w-layout-grid speakers-list_social-list"] > a'
        )
        speaker_data["SocialLinks"] = [
            a["href"] for a in social_links_elements if a["href"] != "index.html#"
        ]
        return speaker_data

    def load_and_save_data(self, filename):
        people_list = self.get_speakers_data_from_site()
        self.speakers_data = [
            self.extract_speaker_data(speaker) for speaker in people_list
        ]

        writer = DataWriter(
            data=self.speakers_data, creds=self.creds, sharing_email=self.sharing_email
        )

        if filename.endswith(".json"):
            writer.write_to_json(filename)
        elif filename.endswith(".csv"):
            writer.write_to_csv(filename)
        elif filename.endswith(".gsheets"):
            writer.write_to_gsheets(filename)


class DataWriter:
    def __init__(self, data, creds, sharing_email):
        self.data = data
        self.creds = creds
        self.sharing_email = sharing_email

    def write_to_json(self, filename):
        try:
            with open(filename, "w") as json_file:
                json.dump(self.data, json_file, indent=4)
                print(f"Data successfully written to file: {filename}")
        except IOError as e:
            print(f"IOError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def write_to_csv(self, filename):
        try:
            with open(filename, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Name", "Role", "Image Link", "Social Links"])
                for item in self.data:
                    writer.writerow(
                        [
                            item["Name"],
                            item["Role"],
                            item["ImageLink"],
                            item["SocialLinks"],
                        ]
                    )
                print(f"Data successfully written to file: {filename}")
        except IOError as e:
            print(f"IOError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def write_to_gsheets(self, filename):
        try:
            client = gspread.authorize(self.creds)

            try:
                # Try to open the existing spreadsheet
                spreadsheet = client.open(filename)
            except gspread.SpreadsheetNotFound:
                # If not found, create a new one
                spreadsheet = client.create(filename)

            spreadsheet.share(self.sharing_email, perm_type="user", role="writer")
            sheet = spreadsheet.sheet1

            sheet.update(
                values=[["Name", "Role", "ImageLink", "SocialLinks"]],
                range_name="A1:D1",
            )

            for index, speaker in enumerate(self.data, start=2):
                row = [
                    speaker["Name"],
                    speaker["Role"],
                    speaker["ImageLink"],
                    ",".join(map(str, speaker["SocialLinks"])),
                ]
                sheet.insert_row(row, index)

            print(f"Data written to Google Spreadsheet successfully to file {filename}")
            print(spreadsheet.url)
        except gspread.exceptions.APIError as e:
            print(f"gspread APIError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Scrape data and save to different formats."
    )
    parser.add_argument(
        "-f",
        "--file",
        type=validate_filename,
        help="The filename to save. It could have one of these extensions: .json, .csv, .gsheets",
    )
    args = parser.parse_args()

    base_url = "https://interaction24.ixda.org"
    creds_path = PATH_TO_CREDS
    sharing_email = SHARING_EMAIL
    scraper = SpeakersScraper(creds_path, base_url, sharing_email)
    scraper.load_and_save_data(args.file)


if __name__ == "__main__":
    main()
