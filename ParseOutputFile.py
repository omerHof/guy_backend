import os.path
import sys
import json
import re
import csv
from TIRP import TIRP
from SymbolicTimeInterval import SymbolicTimeInterval
from SupportingInstance import SupportingInstance
rel_allen_seven = 7



def get_supporting_instances(entities, instances, line_vector, symbols, index, next_line):
    next_line_parsed = re.split('[ \[ , \]]', next_line)
    line = line_vector[index+8:]
    for word in range(0, len(line) - 4, 5):
        entity_id = line[word]
        instance_vec = []
        symbolic_list = []
        tis = list(filter(None, line[word + 1].split(']')))
        for t in range(0, len(tis)):
            times = tis[t].split('-')
            start_time = int(times[0].replace("[", ""))
            end_time = int(times[1])
            if start_time == end_time:
                sys.exit("Error! Start time can't be equal to end time! please change KLC code")
            symbolic = SymbolicTimeInterval(start_time=start_time, end_time=end_time, symbol=symbols[t])#, duration=tis[t+1], offset_from_start=tis[t+2], offset_from_end=tis[t+3])
            symbolic_list.append(symbolic)
        instance_vec.append(symbolic_list)
        if entity_id in entities:
            instances[len(instances) - 1].add_list_to_intervals(instance_vec)
        else:
            for i in range(0, len(next_line_parsed)-9, 11):
                if entity_id == next_line_parsed[i]:
                    mean_duration = next_line_parsed[i+7]
                    mean_offset_from_start = next_line_parsed[i+8]
                    mean_offset_from_end = next_line_parsed[i+9]
                    break
            support_instance = SupportingInstance(entityId=int(entity_id), symbolic_intervals=instance_vec,
                                                      mean_duration=mean_duration, mean_offset_from_start=mean_offset_from_start,mean_offset_from_end=mean_offset_from_end)
            instances.append(support_instance)
            entities.append(entity_id)
    instance_vec.clear()
    # for instance in instances:
    #     for i in range(0, symbols+1):
    #         mean_of_each_interval[i] += instance[0][i]
    # for i in range(0, len(mean_of_each_interval)):
    #         mean_of_each_interval[i] = mean_of_each_interval[i] / len(entities)
    # support_instance.set___mean_of_each_interval(mean_of_each_interval)


def input_validation(filename):
    if not os.path.isfile(filename):
        print("Wrong file path to parse, please fix the path and try again")
        return False
    return True


def parse_output_file(filename, rel_number,states):
    """
    This function create TIRP list from KarmaLego output file.
    Output file structure: [0]TIRP_size [1]symbolNumber-symbolNumber-sym...- [2]rel.rel.rel... [3]mean_duration
    [4]mean_offset_from_start [5]mean_offset_from_end  [6]vertical_support
    [7]mean_horizontal_support [8]entity_id [9][start_time-end_time][10] duration [11]offset_from_start [12]offset_from_end
    :param filename:
    :param rel_number:
    :return: TIRPs list
    """
    if not input_validation(filename):
        return

    if rel_allen_seven is rel_number:
        relations_dict = {"<": 0, "m": 1, "o": 2, "f": 3, "c": 4, "=": 5, "s": 6, "-": 7}
    else:
        print("Wrong number of relations")
        return

    TIRP_list = []
    lines = [line.rstrip('\n') for line in open(filename)]
    for i in range(0, len(lines)-1):
        if i % 2 == 1:
            continue
        line_vector = lines[i].split()
        next_line = lines[i+1]
        instances = []
        entities = list()
        TIRP_size = int(line_vector[0])
        symbols = list(filter(None, line_vector[1].split('-')))
        for i in range(0, len(symbols)):
            symbol = states[symbols[i]]
            symbols[i] = symbol
        if TIRP_size >1:
            index = 0;
            relations = list(filter(None, line_vector[index+2].split('.')))
            for r in range(0, len(relations)):
                relations[r] = relations_dict[relations[r]]
        else:
            relations = list()
            index = -1;
        mean_duration = float(line_vector[index+3])
        mean_offset_from_start = float(line_vector[index+4])
        mean_offset_from_end = float(line_vector[index+5])
        vertical_support = int(line_vector[index+6])
        mean_horizontal_support = float(line_vector[index+7])
        get_supporting_instances(entities, instances, line_vector, symbols,index=index, next_line=next_line)
        TIRP_obj = TIRP(tirp_size=TIRP_size, symbols=symbols, relation=relations, supporting_instances= instances,
                        supporting_entities=entities, vertical_support=vertical_support,
                        mean_horizontal_support=mean_horizontal_support,mean_duration= mean_duration,
                        mean_offset_from_start=mean_offset_from_start, mean_offset_from_end=mean_offset_from_end)
        TIRP_list.append(TIRP_obj)
    return TIRP_list


def parse_TIRP(line1, line2, states):
    relations_dict = {"<": 0, "m": 1, "o": 2, "f": 3, "c": 4, "=": 5, "s": 6, "-": 7}
    line_vector = line1.split()
    instances = []
    entities = list()
    TIRP_size = int(line_vector[0])
    symbols = list(filter(None, line_vector[1].split('-')))
    for i in range(0, len(symbols)):
        symbol = states[symbols[i]]
        symbols[i] = symbol
    if TIRP_size >1:
        index = 0;
        relations = list(filter(None, line_vector[index+2].split('.')))
        for r in range(0, len(relations)):
            relations[r] = relations_dict[relations[r]]
    else:
        relations = list()
        index = -1;
    mean_duration = float(line_vector[index+3])
    mean_offset_from_start = float(line_vector[index+4])
    mean_offset_from_end = float(line_vector[index+5])
    vertical_support = int(line_vector[index+6])
    mean_horizontal_support = float(line_vector[index+7])
    get_supporting_instances(entities=entities, instances=instances, line_vector=line_vector, symbols=symbols,
                             index=index, next_line=line2)
    TIRP_obj = TIRP(tirp_size=TIRP_size, symbols=symbols, relation=relations, supporting_instances= instances,
                    supporting_entities=entities, vertical_support=vertical_support,
                    mean_horizontal_support=mean_horizontal_support,mean_duration=mean_duration,
                    mean_offset_from_start=mean_offset_from_start, mean_offset_from_end=mean_offset_from_end)
    return TIRP_obj


def parse_states_file(path):
    """
    This function parses the state file and init the states dictionary. The file must contain the columns - StateID, TemporalPropertyName, BinLabel
    :return:
    """
    states = dict()
    with open(path, 'r') as fs:
        states_from_file = json.load(fs)
    for state in states_from_file:
        state_id = state['StateID']
        state_name = state['TemporalPropertyName'].rstrip() + '.' + state['BinLabel'].rstrip()
        states[state_id] = state_name
    return states

    # file_name = './states.csv'
    # with open(file_name, mode='r') as csv_file:
    #     csv_reader = csv.DictReader(csv_file)
    #     for row in csv_reader:
    #         state_id = row[csv_reader.fieldnames[0].rstrip()]
    #         state_name = row['TemporalPropertyName'].rstrip() + '.' + row['BinLabel'].rstrip()
    #         states[state_id] = state_name
    return states


# parse_states_file()
# parse_output_file('./RawDataWithOffset.txt', 7)


