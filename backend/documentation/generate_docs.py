import os
import re

import requests
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_URL = os.getenv("PUBLIC_SUPABASE_URL")
API_KEY = os.getenv("SUPABASE_KEY")

if BASE_URL is None or API_KEY is None:
    raise Exception("Make sure to set PUBLIC_SUPABASE_URL and SUPABASE_KEY")

req = requests.get(BASE_URL + "/rest/v1/", headers={"apikey": API_KEY})

if req.ok:
    schema = req.json()

else:
    raise Exception(f"Got HTTP code {req.status_code}: {req.reason}")


def generate_table(rows: list[list[str]]) -> str:
    """Generate a markdown table from rows."""

    rows.insert(0, ["Columns", "Type", "Description"])

    # Calculate size of each column
    columns = list(zip(*rows))
    column_lengths = [len(max(column, key=len)) for column in columns]

    # Generate heading
    table = ["|", "|"]

    for heading, length in zip(rows[0], column_lengths):
        table[0] += f" {heading:<{length}} |"

    # Add seperating line
    for length in column_lengths:
        table[1] += f" {'-'*length} |"

    # Add rest of the rows
    for row in rows[1::]:
        row_str = "|"

        for column, length in zip(row, column_lengths):
            row_str += f" {column:<{length}} |"

        table.append(row_str)

    return "\n".join(table)


output_md = ""

# Generate the table documentation
for table_name, table in schema["definitions"].items():
    table_md = f"### `{table_name}`\n"
    table_md += table.get("description", "") + "\n"

    # Generate rows for markdown table
    rows = []

    for column_name, column in table["properties"].items():
        description = column.get("description", "").replace("\n", " ")

        # Descriptions contain text saying that it's a key
        x = re.search(r"Note: This is a (Foreign|Primary) Key", description)
        if x:
            start = x.start()

            # Being specific to avoid accidentally triggering
            if re.search("This is a Foreign Key", description):
                key_to = re.search(r"`(.*?)`", description)

                description = (
                    description[:start] if start != 0 else ""
                ) + f" **FK({key_to.group()})**"  # type: ignore

            else:
                description = (description[:start] if start != 0 else "") + " **PK**"
                pass

        rows.append([column_name, column.get("format", ""), description.strip()])

    table_md += generate_table(rows) + "\n\n"
    output_md += table_md

# Finally, rewrite the database file
with open("database.md", "r") as f:
    database_docs = f.read()

database_docs = database_docs.split("## Tables")[0]

database_docs += f"## Tables\n\n{output_md}"

with open("database.md", "w") as f:
    f.write(database_docs)
