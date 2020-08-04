import xarray as xr
import pint_xarray
from ruamel.yaml import YAML 
from loguru import logger


class Ingestor:
    def __init__(self, path: str):
        self._path = path
        self._data = None
        self.writer = None

    def read(self, manual: str):
        raise NotImplementedError

    def write(self) -> None:
        if not self.writer:
            outpath = 'test.nc'
            self.writer = Writer(outpath)

        if self._data:
            self.writer.write()



class LPJIngestor(Ingestor):
    def __init__(self, path: str):
        super().__init__(path)
    
    def read(self, manual: str) -> None:
        print("parsing LPJ output")
        print(f"using lpj manual {manual}")


class DNDCIngestor(Ingestor):
    def __init__(self, path: str):
        super().__init__(path)
    
    def read(self, manual: str) -> None:
        print("parsing DNDC output")
        print(f"using dndc manual {manual}")
        print(f"writing to {self.writer.destination if self.writer else '<NOTSET>'}")



class Writer:
    def __init__(self, outpath: str):
        self._path = outpath
    
    @property
    def destination(self):
        return self._path

    def write(self) -> None:
        pass


if __name__ == "__main__":
    yaml = YAML()
    
    logger.debug("Test logging (with emojis): 🤷‍♂️")

    ingestor = DNDCIngestor(".")
    ingestor.read("parser.txt")

    ingestor.write()

