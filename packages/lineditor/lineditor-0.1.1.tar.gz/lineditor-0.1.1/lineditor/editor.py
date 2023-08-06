import os

class Editor:
    def __init__(self, path: str, create=True, auto_save=True, read_only=False, encoding="utf-8"):

        self.auto_save: bool = auto_save
        self.path: str = path
        self.encoding: str = encoding
        self.read_only: bool = read_only
        self.cached = []

        if not os.path.isfile(path):
            if create:
                with open(path, "w", encoding=encoding):
                    pass
            else:
                raise RuntimeError("File doesn't exists at '" + path + "'")

        self._cache()

    def save(self) -> None:
        self._save()

    def reload(self) -> None:
        self._cache()

    def __getitem__(self, index: int) -> str:
        if not (0 < int(index) <= len(self.cached)):
            raise RuntimeError("Line number out of range")
        return self._read(index)

    def __setitem__(self, index: int, text: str) -> None:
        if not (0 < index <= len(self.cached)):
            raise RuntimeError("Line number out of range")
        elif self.read_only:
            raise RuntimeError("File loaded with read-only mode")
        self._write(index, text)

    def __len__(self) -> int:
        return len(self.cached)

    def _cache(self):
        with open(self.path, "r", encoding=self.encoding) as f:
            self.cached = f.readlines()

    def _write(self, line: int, text: str) -> None:
        self.cached[line-1] = text + "\n"
        if self.auto_save:
            self._save()

    def _read(self, line: int) -> str:
        return self.cached[line-1].rstrip("\n")

    def _save(self) -> None:
        with open(self.path, "w", encoding=self.encoding) as f:
            f.writelines(self.cached)



