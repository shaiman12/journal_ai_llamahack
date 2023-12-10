import os
import re
import requests
from datetime import datetime, timezone
from notion_client import Client

NOTION_TOKEN = "secret_l6GiqeDCZ8YoMrGNJD2YH500UgCN7CskSgscriMtMHx"
DATABASE_ID = "a758658d1dce4fc1b10c193d729766a7"

notion = Client(auth=NOTION_TOKEN)

def parse_journal_to_notion_blocks(journal_text):
    blocks = []
    # Assuming each paragraph is separated by two newlines
    paragraphs = journal_text.split('\n\n')

    for paragraph in paragraphs:
        # If a paragraph starts with a number and period, it's a list item
        if re.match(r'\d+\.', paragraph):
            list_items = paragraph.strip().split('\n')
            for item in list_items:
                item_content = item[item.find(' ')+1:]
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content": item_content
                            }
                        }]
                    }
                })
        else:
            # Otherwise, it's a paragraph or heading
            if '**' in paragraph:
                # Extracting heading text
                heading_text = paragraph.split('**')[1]
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content": heading_text
                            }
                        }]
                    }
                })
                # Extracting the rest of the paragraph
                paragraph_text = '**'.join(paragraph.split('**')[2:])
                if paragraph_text:
                    blocks.append({
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{
                                "type": "text",
                                "text": {
                                    "content": paragraph_text
                                }
                            }]
                        }
                    })
            else:
                # Regular paragraph without bold text
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{
                            "type": "text",
                            "text": {
                                "content": paragraph
                            }
                        }]
                    }
                })
    return blocks



def upload_journal_to_notion(notion, database_id, journal_text, date):
    blocks = parse_journal_to_notion_blocks(journal_text)
    # Create a new page with the parsed blocks
    new_page = notion.pages.create(
        parent={"database_id": database_id},
        properties={
            'Name': {
                'title': [
                    {'text': {'content': date}}
                ]
            }
            # Remove 'Date' if it's not defined in your database
        },
        children=blocks
    )
    print(f"Page created with ID: {new_page['id']}")

# Replace 'your-database-id' and 'your-date' with the actual values
journal_date = '2023-12-10'

# This should be the path to the text file containing your journal entry
journal_file_path = 'journals/2023-12-10.txt'

with open(journal_file_path, 'r') as file:
    journal_content = file.read()
    upload_journal_to_notion(notion, DATABASE_ID, journal_content, journal_date)