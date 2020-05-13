from bs4 import BeautifulSoup
from enum import IntEnum
from random import Random


DASH = "\u2013"
SOURCE_FILE = "data/source.html"


class Terrain(IntEnum):
    BEACH = 1
    JUNGLE_NO_UNDEAD = 2
    JUNGLE_LESSER_UNDEAD = 3
    JUNGLE_GREATER_UNDEAD = 4
    MOUNTAINS = 5
    RIVERS = 6
    RUINS = 7
    SWAMP = 8
    WASTELAND = 9


class EncounterFrequency(IntEnum):
    STANDARD = 16
    INFREQUENT = 18
    RARE = 20


class EncounterTime(IntEnum):
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3


class Model:
    def __init__(self, random=Random()):
        self.random = random
        self.encounter_frequency = EncounterFrequency.STANDARD
        self.terrain = Terrain.JUNGLE_NO_UNDEAD
        self.encounter_data = {}
        self.encounter_lookup_tables = {}
        self.encounters = {
            EncounterTime.MORNING: "",
            EncounterTime.AFTERNOON: "",
            EncounterTime.EVENING: "",
        }
        self.ingest_data()

    def encounter_occurs(self):
        roll = self.random.randrange(20) + 1
        return roll >= self.encounter_frequency

    def get_encounter(self):
        roll = self.random.randrange(100)
        encounter_table = self.encounter_lookup_tables[self.terrain]
        encounter_key = encounter_table[roll]
        return self.encounter_data[encounter_key]

    def generate_encounters(self):
        for time in self.encounters:
            if self.encounter_occurs():
                self.encounters[time] = self.get_encounter()
            else:
                self.encounters[time] = "No encounter"

    def ingest_data(self):
        class Encounter:
            def __init__(self, name, probability):
                self.name = name
                self.probability = probability

        def d100_to_int(n):
            return 100 if n == "00" else int(n)

        def probability_to_count(p):
            return d100_to_int(p[-2:]) - d100_to_int(p[0:2]) + 1 if DASH in p else 1

        def cell_contents(cell):
            if link := cell.find("a"):
                return link.get("href")
            else:
                return cell.text

        with open(SOURCE_FILE) as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")

        # The HTML source splits the encounter table into two, mimicking how it was printed in the hardcover.
        # Here we consolidate into a single logical table, by splitting off the header rows from each table
        # and merging the remaining rows.
        raw_encounter_table = [
            [cell_contents(cell) for cell in row.find_all("td")]
            for i in (1, 2)
            for row in tables[i].find_all("tr")[2:]
        ]

        for row in raw_encounter_table:
            key = row[0]
            tag_id = key.strip("#")
            if header := soup.find("h4", id=tag_id):
                siblings = []
                next_sibling = header.find_next_sibling("p")
                while next_sibling.name != "h4":
                    siblings.append(str(next_sibling))
                    next_sibling = next_sibling.next_sibling
                self.encounter_data[key] = str(header) + "".join(siblings)
            else:
                self.encounter_data[key] = str(soup.find("p", id=tag_id))

        # Build a dictionary mapping terrains to the encounter table for that terrain
        for terrain in Terrain:
            # Grab a column of encounters, filtering for only those encounters that can occur in that column's terrain.
            column = [
                Encounter(row[0], row[terrain])
                for row in raw_encounter_table
                if any(c.isdigit() for c in row[terrain])
            ]

            # Build the encounter list for the terrain, weighting instances of each encounter by its probability
            encounter_table = []
            for encounter in column:
                encounter_table += [encounter.name] * probability_to_count(
                    encounter.probability
                )

            self.encounter_lookup_tables[terrain] = encounter_table
