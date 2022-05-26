from logging import getLogger, basicConfig, INFO
from pathlib import Path
from typing import Set

import requests as requests
from pandas import read_excel, DataFrame

_logger = getLogger(__name__)


class WordNotFoundError(LookupError):
    pass


class BrysbaertPrevalence:
    _file_path: Path = Path(Path(__file__).parent, "English_Word_Prevalences.xlsx")
    _file_url: str = "https://osf.io/nbu9e/download"

    @classmethod
    def _load_from_local_file(cls) -> DataFrame:
        with cls._file_path.open("rb") as f:
            return read_excel(f, sheet_name="Prevalence", header=0, index_col=None)

    @classmethod
    def download_data_file(cls) -> None:
        """Downloads the data file from the internet and saves it in the expected location."""
        _logger.info(f"Attempting to download data file from {cls._file_url}")
        excel_data: requests.Response = requests.get(cls._file_url, allow_redirects=True)
        if cls._file_path.exists():
            raise FileExistsError(cls._file_path)
        with cls._file_path.open("wb") as f:
            f.write(excel_data.content)

    def __init__(self):
        if not self._file_path.exists():
            _logger.info("Data file doesn't exist")
            try:
                self.download_data_file()
            except Exception as e:
                _logger.warning(f"File download failed: {e}")
        self.data: DataFrame = self._load_from_local_file()

        self.data["Word"] = self.data["Word"].str.lower()
        self.words: Set[str] = set(
            tup.Word
            for tup in self.data.itertuples(index=False)
        )

    def prevalence_for(self, word: str) -> float:
        try:
            return self.data[self.data["Word"] == word]["Prevalence"].values[0]
        except LookupError:
            raise WordNotFoundError(word)


if __name__ == '__main__':
    basicConfig(
        format='%(asctime)s | %(levelname)s | %(funcName)s @ %(module)s:%(lineno)d |➤ %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S",
        level=INFO)
    try:
        BrysbaertPrevalence.download_data_file()
    except Exception as e:
        logger.warning(f"Download failed: {e}")
