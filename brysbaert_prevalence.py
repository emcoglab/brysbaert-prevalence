from pathlib import Path
from typing import Set

from pandas import read_excel, DataFrame


class WordNotFoundError(LookupError):
    pass


class BrysbaertPrevalence:
    _file_path: Path = Path(Path(__file__).parent, "English_Word_Prevalences.xlsx")

    def __init__(self):
        with self._file_path.open("rb") as f:
            self.data: DataFrame = read_excel(f, sheet_name="Prevalence", header=0, index_col=None)
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
    b = BrysbaertPrevalence()
    p = b.prevalence_for("abbey")
    print(p)
