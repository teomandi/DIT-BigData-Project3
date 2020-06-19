import time

graph = {}
nodeset = list()
graph_file_path = "web-Google.txt"
print("Parsing the Graph file")
init_tm = time.time()
with open(graph_file_path) as fp:
    line = fp.readline()
    i = 0
    while line:
        if "#" in line:
            print("Found comment: ", line[:-1])
            line = fp.readline()  # in the end
            continue
        src, dest = [int(i) for i in line.split()]
        if i == 0:
            print(src, " ---> ", dest)
            i = 1
        if src not in nodeset:
            nodeset.append(src)
        if dest not in nodeset:
            nodeset.append(dest)
        line = fp.readline()  # in the end
# print("beforeee: ", nodeset[:20])
# nodeset = list(nodeset)
# print("afterr: ", nodeset[:20])

while True:
    try:
        index = input("Give index: ")
        intid = int(index)
    except:
        if intid == 'q':
            exit()
    print("Node ID: ", nodeset[intid])
