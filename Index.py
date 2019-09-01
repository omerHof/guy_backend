import ParseOutputFile
import json

TIRP_per_file = dict()


# def init_data_set(data_set_name, KL_outputfile, states_file, entities_file):
#     path = 'DataSets/' + data_set_name
#     if not os.path.exists(path):
#         os.mkdir(path)
#
#         shutil.copy2(path + '/'+KL_outputfile, path)
#         shutil.copy2(path + '/' + states_file, path)
#         shutil.copy2(path + '/' + entities_file, path)
#         #PreProccesing.create_index_files(KL_outputfile,)

def parse_main_index(path, states):
    TIRP_per_file.clear()
    root_elements = list()
    with open(path + '/main_Index.txt') as fp:
        line1 = fp.readline()
        while line1:
            line2 = fp.readline()
            file_name = fp.readline().rstrip()
            # ParseOutputFile.parse_states_file()
            TIRP = ParseOutputFile.parse_TIRP(line1, line2, states)
            # make the TIRP json serializable
            # s = json.dumps(TIRP)
            # s = json.dumps(TIRP.__dict__)
            s = json.dumps(TIRP, default=lambda x: x.__dict__)
            root_elements.append(s)
            # root_elements.append(TIRP)
            TIRP_name = TIRP.get_unique_name()
            TIRP_per_file[TIRP_name] = file_name
            line1 = fp.readline()
        return root_elements


def get_sub_tree(TIRP, states,path):
    TIRP_name = TIRP.get_unique_name()
    file_name = path + '/' + TIRP_per_file[TIRP_name]
    # ParseOutputFile.parse_states_file()
    TIRPs = ParseOutputFile.parse_output_file(file_name, 7, states)
    TIRP.set_childes(TIRPs)
    return TIRPs


# init_data_set('diabetes', 'C:/Users/GUY/Desktop/dataSets/KL/RawDataWithOffset.txt',
#               'C:/Users/GUY/Desktop/dataSets/States_KB_to_KLV.csv', 'C:/Users/GUY/Desktop/KLV/entities (1).csv')
# parse_main_index()
# for t in root_elements:
#     get_sub_tree(t)
