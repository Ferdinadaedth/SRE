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
  def __init__(self, local_address):
    self.local_address = local_address

  def find_file(self, file_name):
    # Use os.walk() to search through the directory tree starting
    # at the given local address.
    for root, dirs, files in os.walk(self.local_address):
      # Check if the file we're looking for is in the current directory.
      if file_name in files:
        return os.path.join(root, file_name)
    return None
```

