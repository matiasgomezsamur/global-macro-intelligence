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

    df["date"] = pd.to_datetime(df["date"])

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
    Calculate U.S. inflation metrics.

    Metrics:
    - Month-over-month inflation
    - Year-over-year inflation
    - 3-month annualized inflation
    - 6-month annualized inflation
    """

    df = df.copy()

    # ===============================================================
    # HEADLINE CPI
    # ===============================================================

    df["headline_lag_1m"] = (
        df["headline_cpi"].shift(1)
    )

    df["headline_lag_3m"] = (
        df["headline_cpi"].shift(3)
    )

    df["headline_lag_6m"] = (
        df["headline_cpi"].shift(6)
    )

    df["headline_lag_12m"] = (
        df["headline_cpi"].shift(12)
    )

    # Month-over-month inflation
    df["headline_mom"] = (
        (
            df["headline_cpi"]
            / df["headline_lag_1m"]
        )
        - 1
    ) * 100

    # Year-over-year inflation
    df["headline_yoy"] = (
        (
            df["headline_cpi"]
            / df["headline_lag_12m"]
        )
        - 1
    ) * 100

    # 3-month annualized inflation
    df["headline_3m_ann"] = (
        (
            df["headline_cpi"]
            / df["headline_lag_3m"]
        ) ** 4
        - 1
    ) * 100

    # 6-month annualized inflation
    df["headline_6m_ann"] = (
        (
            df["headline_cpi"]
            / df["headline_lag_6m"]
        ) ** 2
        - 1
    ) * 100

    # ===============================================================
    # CORE CPI
    # ===============================================================

    df["core_lag_1m"] = (
        df["core_cpi"].shift(1)
    )

    df["core_lag_3m"] = (
        df["core_cpi"].shift(3)
    )

    df["core_lag_6m"] = (
        df["core_cpi"].shift(6)
    )

    df["core_lag_12m"] = (
        df["core_cpi"].shift(12)
    )

    # Month-over-month inflation
    df["core_mom"] = (
        (
            df["core_cpi"]
            / df["core_lag_1m"]
        )
        - 1
    ) * 100

    # Year-over-year inflation
    df["core_yoy"] = (
        (
            df["core_cpi"]
            / df["core_lag_12m"]
        )
        - 1
    ) * 100

    # 3-month annualized inflation
    df["core_3m_ann"] = (
        (
            df["core_cpi"]
            / df["core_lag_3m"]
        ) ** 4
        - 1
    ) * 100

    # 6-month annualized inflation
    df["core_6m_ann"] = (
        (
            df["core_cpi"]
            / df["core_lag_6m"]
        ) ** 2
        - 1
    ) * 100

    return df


def classify_momentum(short_term, medium_term):
    """
    Compare 3-month annualized inflation
    with 6-month annualized inflation.

    This is a directional indicator,
    not an economic forecast.
    """

    if pd.isna(short_term) or pd.isna(medium_term):
        return "Unavailable"

    if short_term > medium_term:
        return "Accelerating"

    if short_term < medium_term:
        return "Decelerating"

    return "Stable"


def save_processed_data(df):
    """
    Save calculated inflation metrics.
    """

    project_root = Path(__file__).resolve().parents[2]

    output_directory = (
        project_root
        / "data"
        / "processed"
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_file = (
        output_directory
        / "us_inflation_metrics.csv"
    )

    df.to_csv(
        output_file,
        index=False,
    )

    print()
    print(
        f"Processed data saved to: "
        f"{output_file}"
    )


def display_inflation_monitor(df):
    """
    Display latest U.S. inflation metrics.
    """

    required_columns = [
        "headline_cpi",
        "headline_mom",
        "headline_yoy",
        "headline_3m_ann",
        "headline_6m_ann",
        "core_cpi",
        "core_mom",
        "core_yoy",
        "core_3m_ann",
        "core_6m_ann",
    ]

    valid_data = df.dropna(
        subset=required_columns
    )

    latest = valid_data.iloc[-1]

    headline_momentum = classify_momentum(
        latest["headline_3m_ann"],
        latest["headline_6m_ann"],
    )

    core_momentum = classify_momentum(
        latest["core_3m_ann"],
        latest["core_6m_ann"],
    )

    print()
    print("U.S. INFLATION MONITOR")
    print("=" * 55)

    print()
    print(
        f"Latest observation: "
        f"{latest['date'].strftime('%B %Y')}"
    )

    # ===============================================================
    # HEADLINE CPI
    # ===============================================================

    print()
    print("HEADLINE CPI")
    print("-" * 55)

    print(
        f"CPI Index:                    "
        f"{latest['headline_cpi']:.3f}"
    )

    print(
        f"Month-over-Month:             "
        f"{latest['headline_mom']:.2f}%"
    )

    print(
        f"Year-over-Year:               "
        f"{latest['headline_yoy']:.2f}%"
    )

    print(
        f"3-Month Annualized:           "
        f"{latest['headline_3m_ann']:.2f}%"
    )

    print(
        f"6-Month Annualized:           "
        f"{latest['headline_6m_ann']:.2f}%"
    )

    print(
        f"Momentum:                     "
        f"{headline_momentum}"
    )

    # ===============================================================
    # CORE CPI
    # ===============================================================

    print()
    print("CORE CPI")
    print("-" * 55)

    print(
        f"Core CPI Index:               "
        f"{latest['core_cpi']:.3f}"
    )

    print(
        f"Month-over-Month:             "
        f"{latest['core_mom']:.2f}%"
    )

    print(
        f"Year-over-Year:               "
        f"{latest['core_yoy']:.2f}%"
    )

    print(
        f"3-Month Annualized:           "
        f"{latest['core_3m_ann']:.2f}%"
    )

    print(
        f"6-Month Annualized:           "
        f"{latest['core_6m_ann']:.2f}%"
    )

    print(
        f"Momentum:                     "
        f"{core_momentum}"
    )

    # ===============================================================
    # LATEST OBSERVATIONS
    # ===============================================================

    print()
    print("LATEST 12 OBSERVATIONS")
    print("-" * 55)

    output_columns = [
        "date",
        "headline_yoy",
        "headline_3m_ann",
        "headline_6m_ann",
        "core_yoy",
        "core_3m_ann",
        "core_6m_ann",
    ]

    latest_table = (
        df[output_columns]
        .tail(12)
        .copy()
    )

    # Round only numeric columns.
    numeric_columns = [
        "headline_yoy",
        "headline_3m_ann",
        "headline_6m_ann",
        "core_yoy",
        "core_3m_ann",
        "core_6m_ann",
    ]

    latest_table[numeric_columns] = (
        latest_table[numeric_columns]
        .round(3)
    )

    print(latest_table)


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

    save_processed_data(
        inflation_metrics
    )