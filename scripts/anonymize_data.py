import argparse
import random
from enum import Enum
from datetime import date, timedelta
from datetime import datetime
from pathlib import Path

import pandas as pd


class Institution(str, Enum):
    AMEX = "amex"


INSTITUTION_HEADERS: dict[Institution, list[str]] = {
    Institution.AMEX: [
        "Date",
        "Date Processed",
        "Description",
        "Card Member",
        "Account #",
        "Amount",
    ]
}

CARD_MEMBERS = ["Alex Carter", "Jamie Lee", "Taylor Brooks", "Morgan Chen"]
ACCOUNT_BY_MEMBER = {
    "Alex Carter": "-91009",
    "Jamie Lee": "-92015",
    "Taylor Brooks": "-93022",
    "Morgan Chen": "-94031",
}
MERCHANTS = [
    "HARBOR MARKET",
    "NORTHLIGHT CINEMA",
    "CITYPUMP FUEL",
    "CEDAR BISTRO",
    "METRO TRANSIT RELOAD",
    "MAPLE PHARMACY",
    "SUNSET AIRLINES",
    "WESTSIDE BAKERY",
    "STREAMWAVE MEDIA",
    "HOMEFIX SERVICES",
]
CITIES = ["VANCOUVER", "BURNABY", "NORTH VANCOUVER", "TORONTO", "ONLINE"]


def _format_statement_date(day: date) -> str:
    return day.strftime("%d %b %Y")


def _random_purchase_amount(rng: random.Random) -> float:
    tier = rng.random()
    if tier < 0.70:
        return round(rng.uniform(4.0, 120.0), 2)
    if tier < 0.95:
        return round(rng.uniform(120.0, 700.0), 2)
    return round(rng.uniform(700.0, 3200.0), 2)


def _synthetic_description(rng: random.Random) -> str:
    merchant = rng.choice(MERCHANTS)
    city = rng.choice(CITIES)
    return f"{merchant} {city}"


def generate_statement_rows(
    institution: Institution,
    row_count: int,
    seed: int,
) -> pd.DataFrame:
    """Generate synthetic statement data with institution-specific headers."""
    rng = random.Random(seed)
    start_day = date.today() - timedelta(days=90)
    headers = INSTITUTION_HEADERS[institution]
    rows: list[dict[str, str]] = []

    for _ in range(row_count):
        statement_day = start_day + timedelta(days=rng.randint(0, 90))
        processed_day = statement_day + timedelta(days=rng.randint(0, 2))
        member = rng.choice(CARD_MEMBERS)

        if rng.random() < 0.08:
            description = "PAYMENT RECEIVED - THANK YOU"
            amount = round(-rng.uniform(500.0, 3200.0), 2)
        else:
            description = _synthetic_description(rng)
            amount = _random_purchase_amount(rng)

        rows.append(
            {
                "Date": _format_statement_date(statement_day),
                "Date Processed": _format_statement_date(processed_day),
                "Description": description,
                "Card Member": member,
                "Account #": ACCOUNT_BY_MEMBER[member],
                "Amount": f"{amount:.2f}",
            }
        )

    rows.sort(key=lambda row: datetime.strptime(row["Date"], "%d %b %Y"), reverse=True)
    return pd.DataFrame(rows, columns=headers)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate fully synthetic statement CSV data from code-defined institution headers."
    )
    parser.add_argument(
        "--institution",
        choices=[member.value for member in Institution],
        default=Institution.AMEX.value,
        help="Institution profile used to select the generated CSV headers.",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=Path,
        help="Output CSV file path.",
        default=Path("test_data_anonymized/activity.csv"),
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=50,
        help="Number of synthetic rows to generate.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Seed for deterministic output.",
    )
    args = parser.parse_args()

    institution = Institution(args.institution)
    output_file = args.output_file
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df = generate_statement_rows(
        institution=institution,
        row_count=max(1, args.rows),
        seed=args.seed,
    )
    df.to_csv(output_file, index=False)
