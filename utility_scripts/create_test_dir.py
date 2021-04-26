"""
Fills a specified directory with n number of files containing garbage data
Used to create testing directories
"""

dr = "../testing_dirs/subdirs/4"
n = 10  # number of files
b = 100000  # number of ints per file

for i in range(n):
    with open(f"{dr}/{i}.sav", "w") as f:
        for k in range(b):
            f.write(str(k))
