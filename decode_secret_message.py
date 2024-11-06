from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
from typing import Optional


def download_from_gdocs(url: str) -> Optional[str]:
    """
    Downloads content from a published Google Doc URL.

    Args:
        url (str): The published Google Doc URL (must be a /pub URL)

    Returns:
        Optional[str]: HTML content of the document or None if download fails
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error downloading document: {e}")
        return None


def parse_html_table(html_content: str) -> pd.DataFrame:
    """
    Parses HTML content to extract coordinate data into a DataFrame.

    Args:
        html_content (str): HTML content containing the table

    Returns:
        pd.DataFrame: DataFrame with x-coordinate, y-coordinate, and Character columns

    Raises:
        ValueError: If the expected table is not found
    """
    soup = BeautifulSoup(html_content, "html.parser")
    expected_headers = {"x-coordinate", "Character", "y-coordinate"}

    # Find the target table
    for table in soup.find_all("table"):
        if first_row := table.find("tr"):
            headers = [cell.get_text().strip() for cell in first_row.find_all("td")]
            if set(headers) == expected_headers:
                # Extract data from rows
                data = [[cell.get_text().strip() for cell in row.find_all("td")] for row in table.find_all("tr")[1:]]  # Skip header row
                # Filter out incomplete rows
                data = [row for row in data if len(row) == 3]
                return pd.DataFrame(data, columns=headers)

    raise ValueError("Could not find table with expected headers")


def print_table(df: pd.DataFrame) -> None:
    """
    Prints a 2D grid representation of the coordinate data.

    Args:
        df (pd.DataFrame): DataFrame with x-coordinate, y-coordinate, and Character columns
    """
    # Convert coordinates to integers
    df = df.copy()  # Create copy to avoid modifying original
    df["x-coordinate"] = df["x-coordinate"].astype(int)
    df["y-coordinate"] = df["y-coordinate"].astype(int)

    # Create and fill grid
    max_x, max_y = df["x-coordinate"].max(), df["y-coordinate"].max()
    grid = np.full((max_y + 1, max_x + 1), " ", dtype=str)

    # Place characters
    for _, row in df.iterrows():
        grid[max_y - row["y-coordinate"], row["x-coordinate"]] = row["Character"]

    # Print grid
    for row in grid:
        print("".join(row))


def decode_secret_message(url: str) -> None:
    """
    Main function to decode and display the secret message from a Google Doc URL.

    Args:
        url (str): The published Google Doc URL containing the encoded message
    """
    # Download content
    if html_content := download_from_gdocs(url):
        try:
            # Parse table
            df = parse_html_table(html_content)
            # Print decoded message
            print_table(df)
        except ValueError as e:
            print(f"Error parsing table: {e}")
    else:
        print("Failed to download document")


if __name__ == "__main__":
    # Example usage
    decode_secret_message(
        "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
    )
    decode_secret_message(
        "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
    )
