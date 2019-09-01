import re
# output_path = 'C:/Users/GUY/Desktop/dataSets/KL/RawData.txt'


def create_index_files(output_file, path):
    main = open(path + "/main_Index.txt", "w")
    with open(output_file) as fp:
        line = fp.readline()
        while line:
            vals = re.split('[ ,-]', line)
            if vals[0] == '1':
                file_name = vals[1]
                f = open(file_name + ".txt", "w")
                f.close()
                #tirp = vals[1] + ' - ' + vals[4] + ' ' + vals[5]
                main.write(line)
                line = fp.readline()
                main.write(line)
                main.write(file_name + ".txt\n")
                f.close()
            else:
                fp.readline()
            line = fp.readline()
    main.close()
    insert_tirps_to_files(output_file, path)


def insert_tirps_to_files(output_file, path):
    with open(output_file) as fp:
        line = fp.readline()
        while line:
            vals = re.split('[ ,-]', line)
            if vals[0] != '1':
                file_name = vals[1]
                f = open(path + '/' + file_name + ".txt", "a")
                f.write(line)
                line = fp.readline()
                f.write(line)
                f.close()
            else:
                fp.readline()
            line = fp.readline()
    fp.close()


# create_index_files('RawDataWithOffset.txt')
# insert_tirps_to_files('RawDataWithOffset.txt')







