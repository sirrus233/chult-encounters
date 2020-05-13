from bs4 import BeautifulSoup
from enum import IntEnum
from random import Random


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
        self.encounter_tables = ingest_data()
        self.encounters = {
            EncounterTime.MORNING: "",
            EncounterTime.AFTERNOON: "",
            EncounterTime.EVENING: "",
        }

    def encounter_occurs(self):
        roll = self.random.randrange(20) + 1
        return roll >= self.encounter_frequency

    def get_encounter(self):
        roll = self.random.randrange(100)
        return self.encounter_tables[self.terrain][roll]

    def generate_encounters(self):
        for time in self.encounters:
            if self.encounter_occurs():
                self.encounters[time] = self.get_encounter()
            else:
                self.encounters[time] = "No encounter."


def ingest_data():
    DASH = "\u2013"
    SOURCE_FILE = "data/source.html"

    class Encounter:
        def __init__(self, name, probability):
            self.name = name
            self.probability = probability

    def d100_to_int(n):
        return 100 if n == "00" else int(n)

    def probability_to_count(p):
        return d100_to_int(p[-2:]) - d100_to_int(p[0:2]) + 1 if DASH in p else 1

    with open(SOURCE_FILE) as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    tables = soup.find_all("table")

    # The HTML source splits the encounter table into two, mimicking how it was printed in the hardcover.
    # Here we consolidate into a single logical table, by splitting off the header rows from each table
    # and merging the remaining rows.
    raw_encounter_table = [
        [cell.text for cell in row.find_all("td")]
        for i in (1, 2)
        for row in tables[i].find_all("tr")[2:]
    ]

    # Build a dictionary mapping terrains to the encounter table for that terrain
    encounter_tables = {}

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

        encounter_tables[terrain] = encounter_table

    return encounter_tables
