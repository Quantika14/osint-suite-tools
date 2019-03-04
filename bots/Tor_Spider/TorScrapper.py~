from multiprocessing import Pool
import os

with open("links.txt", "r") as websites:
    content = websites.read().splitlines()

def jaadu(url):
    BASE_URL = url
    execute = str('gnome-terminal -e \' python3 main.py ' + BASE_URL + '\'')
    os.system(execute)

if __name__ == '__main__':
    with Pool(processes=4) as pool:
        for website in range(0, len(content)):
            pool.apply(jaadu, args=(content[website],))