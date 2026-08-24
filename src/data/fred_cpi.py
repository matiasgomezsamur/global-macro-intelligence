from pathlib import Path

import pandas as pd


# -------------------------------------------------------------------
# FRED SERIES
# -------------------------------------------------------------------

# CPIAUCSL:
# Consumer Price Index for All Urban Consumers:
# All Items in U.S. City Average
HEADLINE_CPI_SERIES = "CPIAUCSL"

# CPILFESL:
# Consumer Price Index for All Urban Consumers:
# All Items Less Food and Energy
CORE_CPI_SERIES = "CPILFESL"


def download_fred_series(series_id, column_name):
    """
    Download a monthly economic series from FRED.

    Parameters
    ----------
    series_id : str
        FRED series identifier.

    column_name : str
        Name that will be assigned to the data column.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing date and series values.
    """

    url = (
        f"https://fred.stlouisfed.org/graph/"
        f"fredgraph.csv?id={series_id}"
    )

    print(f"Downloading {series_id} from FRED...")

    df = pd.read_csv(url)

    # FRED's first column contains the observation date.
    date_column = df.columns[0]

    df = df.rename(
        columns={
            date_column: "date",
            series_id: column_name,
        }
    )

    # Convert data types.
    df["date"] = pd.to_datetime(df["date"])

    df[column_name] = pd.to_numeric(
        df[column_name],
        errors="coerce",
    )

    # Ensure that every calendar month exists.
    # Missing observations remain as NaN.
    df = (
        df.set_index("date")
        .asfreq("MS")
        .reset_index()
    )

    return df


def download_inflation_data():
    """
    Download headline and core CPI data from FRED
    and combine them into one dataset.
    """

    headline = download_fred_series(
        HEADLINE_CPI_SERIES,
        "headline_cpi",
    )

    core = download_fred_series(
        CORE_CPI_SERIES,
        "core_cpi",
    )

    # Combine both series using the date column.
    df = pd.merge(
        headline,
        core,
        on="date",
        how="outer",
    )

    # Sort chronologically.
    df = df.sort_values("date")

    return df


def save_data(df):
    """Save the raw inflation dataset."""

    project_root = Path(__file__).resolve().parents[2]

    output_directory = (
        project_root
        / "data"
        / "raw"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_directory
        / "us_inflation.csv"
    )

    df.to_csv(
        output_file,
        index=False,
    )

    print()
    print(f"Data saved to: {output_file}")


if __name__ == "__main__":

    inflation_data = download_inflation_data()

    print()
    print("Latest observations:")
    print(
        inflation_data.tail(12)
    )

    print()
    print(
        f"Total observations: "
        f"{len(inflation_data)}"
    )

    save_data(inflation_data)