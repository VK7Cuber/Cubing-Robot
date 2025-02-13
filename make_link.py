def make_link(array):
    string_array = "_".join(list(map(str, array)))
    for i in range(len(string_array)):
        if string_array[i] == "'":
            string_array = string_array[:i] + "-" + string_array[i+1:]
    link = f"https://cubedb.net/?puzzle=3x3&alg={string_array}&type=alg"
    return link