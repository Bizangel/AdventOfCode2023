
def read_file_line_splitted(fname: str):
    with open(fname,'r') as fhandle:
        contents = fhandle.read()

    return contents.split('\n')


