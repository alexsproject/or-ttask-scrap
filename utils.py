import argparse
import os


def validate_filename(filename):
    valid_extensions = [".json", ".csv", ".gsheets"]
    _, ext = os.path.splitext(filename)  # split filename and extension
    if ext not in valid_extensions:
        raise argparse.ArgumentTypeError(
            f"Invalid file extension, choices are {valid_extensions}"
        )
    return filename
