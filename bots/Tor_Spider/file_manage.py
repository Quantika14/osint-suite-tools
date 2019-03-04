import os

def create_project_folder(dir):                 # Create seperate folder for each website
    if not os.path.exists(dir):
        print('Creating directory ' + dir)
        os.makedirs(dir)

def create_data_files(folder_name, start_link): # Append to queue and crawled list
    queue = os.path.join(folder_name , 'queue.txt')
    data_crawled = os.path.join(folder_name,"crawled.txt")
    if not os.path.isfile(queue):
        write_to_file(queue, start_link)
    if not os.path.isfile(data_crawled):
        write_to_file(data_crawled, '')

def write_to_file(path, url):                   # Create a new file for the task
    with open(path, 'w') as f:
        f.write(url)

def append_file(path, url):                     # Append new data to existing file
    with open(path, 'a') as file:
        file.write(url + '\n')

def empty_queue(path):                          # Delete contents of a file
    open(path, 'w').close()

def convert_to_set(file_name):                  # Read a file and convert each line to set items
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

def set_to_file(urls, file_name):               # Iterate through a set, each item will be a line in a file
    with open(file_name,"w") as f:
        for l in sorted(urls):
            f.write(l+"\n")
