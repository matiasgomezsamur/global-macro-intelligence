from pathlib import Path

import pandas as pd


def load_inflation_data():
    """
    Load raw U.S. headline and core CPI data.
    """

    project_root = Path(__file__).resolve().parents[2]

    input_file = (
        project_root
        / "data"
        / "raw"
        / "us_inflation.csv"
    )

    df = pd.read_csv(input_file)

    # Convert date column to datetime.
    df["date"] = pd.to_datetime(df["date"])

    # Ensure CPI columns are numeric.
    df["headline_cpi"] = pd.to_numeric(
        df["headline_cpi"],
        errors="coerce",
    )

    df["core_cpi"] = pd.to_numeric(
        df["core_cpi"],
        errors="coerce",
    )

    return df


def calculate_inflation_metrics(df):
    """
    Calculate headline and core CPI inflation metrics.

    Metrics:
    - Month-over-month inflation (MoM)
    - Year-over-year inflation (YoY)
    """

    df = df.copy()

    # ---------------------------------------------------------------
    # HEADLINE CPI
    # ---------------------------------------------------------------

    df["headline_lag_1m"] = (
        df["headline_cpi"].shift(1)
    )

    df["headline_lag_12m"] = (
        df["headline_cpi"].shift(12)
    )

    df["headline_mom"] = (
        (
            df["headline_cpi"]
            / df["headline_lag_1m"]
        )
        - 1
    ) * 100

    df["headline_yoy"] = (
        (
            df["headline_cpi"]
            / df["headline_lag_12m"]
        )
        - 1
    ) * 100

    # ---------------------------------------------------------------
    # CORE CPI
    # ---------------------------------------------------------------

    df["core_lag_1m"] = (
        df["core_cpi"].shift(1)
    )

    df["core_lag_12m"] = (
        df["core_cpi"].shift(12)
    )

    df["core_mom"] = (
        (
            df["core_cpi"]
            / df["core_lag_1m"]
        )
        - 1
    ) * 100

    df["core_yoy"] = (
        (
            df["core_cpi"]
            / df["core_lag_12m"]
        )
        - 1
    ) * 100

    return df


def display_inflation_monitor(df):
    """
    Display the latest available U.S. inflation metrics.
    """

    required_columns = [
        "headline_cpi",
        "headline_mom",
        "headline_yoy",
        "core_cpi",
        "core_mom",
        "core_yoy",
    ]

    valid_data = df.dropna(
        subset=required_columns
    )

    latest = valid_data.iloc[-1]

    print()
    print("U.S. INFLATION MONITOR")
    print("=" * 45)

    print()
    print(
        f"Latest observation: "
        f"{latest['date'].strftime('%B %Y')}"
    )

    print()
    print("HEADLINE CPI")
    print("-" * 45)

    print(
        f"CPI Index:                 "
        f"{latest['headline_cpi']:.3f}"
    )

    print(
        f"Month-over-Month:          "
        f"{latest['headline_mom']:.2f}%"
    )

    print(
        f"Year-over-Year:            "
        f"{latest['headline_yoy']:.2f}%"
    )

    print()
    print("CORE CPI")
    print("-" * 45)

    print(
        f"Core CPI Index:            "
        f"{latest['core_cpi']:.3f}"
    )

    print(
        f"Month-over-Month:          "
        f"{latest['core_mom']:.2f}%"
    )

    print(
        f"Year-over-Year:            "
        f"{latest['core_yoy']:.2f}%"
    )

    print()
    print("LATEST 12 OBSERVATIONS")
    print("-" * 45)

    output_columns = [
        "date",
        "headline_cpi",
        "headline_mom",
        "headline_yoy",
        "core_cpi",
        "core_mom",
        "core_yoy",
    ]

    print(
        df[output_columns].tail(12)
    )


if __name__ == "__main__":

    inflation_data = load_inflation_data()

    inflation_metrics = (
        calculate_inflation_metrics(
            inflation_data
        )
    )

    display_inflation_monitor(
        inflation_metrics
    )