from pathlib import Path

# def read_files_ext(ext):
#     '''
#     Reads all files with a given extension into a list
#     '''
#     file_contents = [
#     path.read_text()
#     for path in Path.cwd().rglob('*.' + ext)
# ]

def file_lines_into_list(path):
    '''
    Returns a list containing each line of given file
    '''

    file_contents = Path(path).read_text()

    return file_contents.split()

if __name__ == '__main__':
    pass