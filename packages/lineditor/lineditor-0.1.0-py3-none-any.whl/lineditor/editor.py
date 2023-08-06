import os

class Editor:
    def __init__(self, path: str, create=True, auto_save=True, encoding="utf-8"):
        if not os.path.isfile(path):
            if create:
                with open(path, "w", encoding=encoding):
                    pass
            else:
                raise RuntimeError("File doesn't exists at '" + path + "'")
        self.auto_save = auto_save
        self.path = path
        self.encoding = encoding
        with open(path, "r", encoding=encoding) as f:
            self.cached = f.readlines()

    def save(self):
        self._save()

    def __getitem__(self, index):
        if not (0 < int(index) <= len(self.cached)):
            raise RuntimeError("Line number out of range")
        return self._read(index)

    def __setitem__(self, index, text):
        if not (0 < index <= len(self.cached)):
            raise RuntimeError("Line number out of range")
        self._write(index, text)

    def __len__(self):
        return len(self.cached)

    def _write(self, line, text):
        self.cached[line-1] = text + "\n"
        if self.auto_save:
            self._save()

    def _read(self, line):
        return self.cached[line-1]

    def _save(self):
        with open(self.path, "r+", encoding=self.encoding) as f:
            f.writelines(self.cached)



