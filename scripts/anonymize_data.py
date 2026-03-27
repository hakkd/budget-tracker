import hashlib
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Mapping, FrozenSet
import pandas as pd
import argparse

# Example usage:
# python3 scripts/anonymize_data.py --institution amex --statement-kind credit


class Institution(str, Enum):
    AMEX = "amex"


class StatementKind(str, Enum):
    CREDIT = "credit"


@dataclass(frozen=True)
class ScrubRule:
    excluded_columns: FrozenSet[str] = field(default_factory=frozenset)


SCRUB_RULES: Mapping[tuple[Institution, StatementKind], ScrubRule] = {
    (Institution.AMEX, StatementKind.CREDIT): ScrubRule(
        excluded_columns=frozenset({"Date", "Date Processed", "Amount"})
    )
}


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def scrub_data(
    filename: str | Path,
    institution: Institution,
    statement_kind: StatementKind,
) -> pd.DataFrame:
    """
    Read a statement CSV and hash sensitive columns.
    """
    # Read all columns as strings to avoid type inference changing their textual form.
    df = pd.read_csv(filename, dtype=str)

    rule = SCRUB_RULES.get((institution, statement_kind), ScrubRule())
    excluded_columns = rule.excluded_columns

    for column in df.columns:
        if column not in excluded_columns:
            series = df[column]
            mask = series.notna()
            df.loc[mask, column] = series[mask].apply(_sha256)

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input-dir",
        type=Path,
        help="Input directory",
        default=Path("test_data_confidential"),
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Output directory",
        default=Path("test_data_anonymized"),
    )
    parser.add_argument(
        "--institution",
        choices=[e.value for e in Institution],
        required=True,
    )
    parser.add_argument(
        "--statement-kind",
        choices=[e.value for e in StatementKind],
        required=True,
    )
    parser.add_argument("-p", "--pattern", help="File name pattern", default="*.csv")
    args = parser.parse_args()

    input_path = args.input_dir
    output_path = args.output_dir

    for in_file in input_path.glob(args.pattern):
        df = scrub_data(
            filename=in_file,
            institution=Institution(args.institution),
            statement_kind=StatementKind(args.statement_kind),
        )
        out_file = output_path / in_file.name
        df.to_csv(out_file, index=False)
