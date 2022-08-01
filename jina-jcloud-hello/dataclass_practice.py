from jina import Document, DocumentArray
from docarray import dataclass
from docarray.typing import Image, Text, JSON
from typing import List, Optional


@dataclass
class Dialog:
    host: str
    utterance: str
    
@dataclass
class Episode:
    name: str
    number: int
    date: str
    title: str
    hosts: str
    show_tease: str
    description: str
    dialogs: Optional[List[Dialog]] = None

def get_episode(uri: str) -> Document:
    return Document(uri=uri)
    
uri = "https://www.grc.com/sn/sn-880.txt"

episode_details = []
for i in range(800, 802):
    print(f"[INFO] acquiring episode {i}...")
    d = get_episode(f"https://www.grc.com/sn/sn-{i}.txt")
    d.load_uri_to_text()
    
    dialog_list = [s.strip() for s in d.text.split("\n") if s.strip()]
    for idx, line in enumerate(dialog_list[:10]):
        colon_pos = line.find(":", 0)
        speaker = line[0:colon_pos].strip()
        utterance = line[colon_pos+1:].strip().replace("\t", "")
        print(idx, speaker, "--", utterance)
        episode_details.append([speaker, utterance])
        print("=========\n")

epi_dataclasses = []
for i in range(0, len(episode_details), 10):
    epi = Episode(
        name="Security Now!",
        number=episode_details[i:i+10][2][1],
        date=episode_details[i:i+10][3][1],
        title=episode_details[i:i+10][4][1],
        hosts=episode_details[i:i+10][5][1],
        show_tease=episode_details[i:i+10][8][1],
        description=episode_details[i:i+10][9][1],
    )
    print(epi)
    epi_dataclasses.append(epi)
    print("\n\n")

for e in epi_dataclasses:
    print(e.number)
    print(e.show_tease)
    print("====\n\n")


    
