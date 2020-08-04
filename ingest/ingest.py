import pint_xarray
import xarray as xr
from loguru import logger
from ruamel.yaml import YAML

logger.add("ingest.log", rotation="1 week")  # Once the file is too old rotate


class Ingestor:
    model = None

    def __init__(self, path: str):
        self._path = path
        self._data = xr.Dataset()
        self.writer = None
        logger.debug(f"{type(self).__name__} instance created")

    @property
    def model(cls):
        return cls.model

    def read(self, manual: str) -> None:
        raise NotImplementedError

    def write(self, outpath: str = "test.nc") -> None:
        if not self.writer:
            self.writer = Writer(outpath)

        if len(self._data.data_vars) > 0:
            self.writer.write()


class LPJIngestor(Ingestor):
    model = "LPJ"

    def __init__(self, path: str):
        super().__init__(path)

    def read(self, manual: str) -> None:
        logger.info("parsing LPJ output")
        logger.info(f"using lpj manual {manual}")


class DNDCIngestor(Ingestor):
    model = "DNDC"

    def __init__(self, path: str):
        super().__init__(path)

    def read(self, manual: str) -> None:
        logger.info(f"Parsing {self.model} using '{manual}'")
        logger.info(f"Write to {self.writer.destination if self.writer else '<UNSET>'}")


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

    logger.info("Starting up ... 🏎")

    ingestor = DNDCIngestor(".")
    ingestor.read("dndc_parser.yaml")

    ingestor.write()
