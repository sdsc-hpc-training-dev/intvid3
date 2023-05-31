# Imports
import requests
import json
import argparse
import xml.etree.ElementTree as ET

from util import *
from youtube_transcript_api import YouTubeTranscriptApi


def sync_events(full_refresh = False):
    """
    Syncs Events from `https://sdsc.edu/education_and_training/training_hpc.xml`
    to local. Supports two modes: Incremental and Full Syncs. Incremental will
    append the new events to the pre-existing data while Full will overwrite 
    previous completely. 
    """
    # Load current events data
    event_data = {}
    with open("events.json", "r") as fh:
        event_data = json.load(fh)

    # Fetch data
    res = requests.get("https://sdsc.edu/education_and_training/training_hpc.xml")
    resText = res.content
    root = ET.fromstring(resText)

    # Parse res for new events
    page_nodes = root.findall("system-page")
    events = {}
    for page_node in page_nodes:

        page_id = page_node.get("id")

        # Checking if the event is new
        if not full_refresh and page_id in event_data:
            continue

        # General information parsing
        name = page_node.find("name").text
        title = page_node.find("title").text
        item_node = page_node.find("system-data-structure")
        start = item_node.find("start_date")
        start_ts = int(start.text) // 1000 if start is not None else None
        end = item_node.find("end_date")
        end_ts = int(end.text) // 1000 if end is not None else None
        desc_long_node = item_node.find("description_long/p")
        long = ET.tostring(desc_long_node, encoding="unicode", method="html") if desc_long_node else None
        short = item_node.find("description_short").text
        instr_node = item_node.find("instructor")
        instr_label = instr_node.find("link_chooser/link_label").text
        instr_title = instr_node.find("instructor_title").text
        instr_bio = instr_node.find("instructor_bio").text
        external_links = page_node.findall(".//external_link")
        intvid_link = None
        for link_node in external_links:
            link = link_node.text
            if link is None:
                continue
            if link.startswith("https://education.sdsc.edu/training/interactive/"):
                intvid_link = link.replace("https://education.sdsc.edu/training/interactive/", "")

        # Build event
        events[name] = {
            "name": name,
            "title": title,
            "start": start_ts,
            "end": end_ts,
            "desc" : {
                "long": long,
                "short": short
            },
            "instr": {
                "label": instr_label,
                "title": instr_title,
                "bio": instr_bio
            },
            "vid_link": intvid_link
        }

    # Saving the data
    if full_refresh:
        json.dump(events, open("events.json", "w"), indent=4)
        print(f"Full Refresh Sync with {len(events)} events")
    else:
        event_data.update(events)
        json.dump(event_data, open("events.json", "w"), indent=4)
        print(f"Incremental Sync with {len(events)} new events")

def generate_transcript(youtube_id, event_id):
    """
    Generates a transcript and saves it given the Youtube ID and the 
    SDSC Event ID. The Event ID corresponds to the same one matching 
    inside the `events.json`.
    """
    folder_name = f"./transcripts/{event_id}.json"

    transcript = YouTubeTranscriptApi.get_transcript(youtube_id)
    with open(folder_name, 'w') as fh:
        json.dump(transcript, fh)
    chmod_774(folder_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Optional arguments
    parser.add_argument("--fullrefresh", help="Refreshes all of the events without using increments", action="store_true")
    args = parser.parse_args()
    
    # Call
    sync_events(args.fullrefresh)