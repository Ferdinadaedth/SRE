# level1

```python
class MyIterator:
    def __init__(self, items):
        self.items = items
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.items):
            raise StopIteration
        item = self.items[self.index]
        self.index += 1
        return item
iterator = MyIterator([1, 2, 3])
for item in iterator:
    print(item)
```



# level2

```python
import os
class FileFinder:
    def __init__(self, root_dir):
        self.root_dir = root_dir
    def find(self, name):
        for root, dirs, files in os.walk(self.root_dir):
            if name in dirs or name in files:
                yield os.path.join(root, name)
    def write_to_file(self, file_name):
        with open(file_name, "w") as file:
            for root, dirs, files in os.walk(self.root_dir):
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    dir_size = os.path.getsize(dir_path)
                    file.write(f"{dir}: {dir_size} bytes\n")
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)
                    file.write(f"{file}: {file_size} bytes\n")
finder = FileFinder("/path/to/root/dir")
for file in finder.find("my_file"):
    print(file)
finder.write_to_file("file_sizes.txt")

```

