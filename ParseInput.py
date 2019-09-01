import fileinput

input_path = './RowData_time-intervals_knowledge-based_4bins_1paa_1max-gap2'
temp_path = './temp'
def pares(input_path):
    index=0
    file = open(input_path, "r+")
    t = open(temp_path, "w")
    line = file.readline()
    t.write(line)
    t.write(file.readline())
    line = file.readline()
    while line:
        line = line[0:line.index(';')]+','+str(index)+';0;10000\n'
        t.write(line)
        t.write(file.readline())
        line = file.readline()
        index= index + 1
    file.close()


pares(input_path)
