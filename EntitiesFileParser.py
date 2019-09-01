import csv
import sys
import pandas as pd
from Entity import Entity


entities = dict()
values_per_property = dict()

def parse_entities_file():
    """
    This function parse the entities file and creates set of entities objects. The file must contain a column named id
    :return:
    """
    file_name = './entities.csv'
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        if 'id' not in csv_reader.fieldnames:
            sys.exit("Error! Start time can't be equal to end time! please change KLC code")
        for row in csv_reader:
            properties = dict()
            for prop in csv_reader.fieldnames:
                if prop == 'id':
                    entityId = row[prop].rstrip()
                else:
                    properties[prop] = row[prop].rstrip()
            entity = Entity(entityId=entityId, properties=properties)
            entities[entityId] = entity


def get_values_per_property():
    file_name = './entities.csv'
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        gapminder = pd.read_csv(file_name)
        for prop in csv_reader.fieldnames:
            values_per_property[prop] = gapminder[prop].unique()


parse_entities_file()
get_values_per_property()
