# lineditor
Simple library to edit or read text of specific line.

## Install
`git clone https://github.com/mafusuke/lineditor.git && cd lineditor && pip install -e .`

## Sample Usage
```python
import lineditor

# load the target file
file = lineditor.Editor("./hoge.txt")

# print the string on the 10th line
print(file[10])
# modify the string on the 21th line into "new text"
file[21] = "new text"
# total lines count of the file
print(len(file)) 
```