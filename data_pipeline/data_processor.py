import logging
import pandas as pd

logger = logging.getLogger(__name__)

def remove_duplicates(df):
    """Remove duplicate rows."""
    before = df.copy()
    df = df.drop_duplicates()
    logger.debug(f"remove_duplicates: {len(before)} -> {len(df)} rows")
    return df


def handle_missing(df, axis="rows"):
    """Drops rows or columns containing missing values."""
    if axis == "rows":
        before = len(df)
        df = df.dropna()
        logger.debug(f"handle_missing: {before} -> {len(df)} rows")
    elif axis == "columns":
        before = df.shape[1]
        df = df.dropna(axis=1)
        logger.debug(f"handle_missing: {before} -> {df.shape[1]} columns")
    else:
        logger.error(f"Unsupported axis {axis}")
        raise ValueError(f"Unsupported axis {axis}")

    return df


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric column."""
    if method not in ("iqr", "zscore"):
        logger.error(f"Unsupported outlier method: {method}")
        raise ValueError(f"Unsupported outlier method: {method}")

    for col in columns:
        if col not in df.columns:
            logger.warning(f"Column not found: {col}")
            continue
        if not pd.api.types.is_numeric_dtype(df[col]):
            logger.warning(f"Column isn't numeric: {col}")
            continue

        before = len(df)
        if method == "iqr":
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr
            df = df[(df[col] >= lower) & (df[col] <= upper)]
        else:
            z_scores = (df[col] - df[col].mean()) / df[col].std()
            df = df[z_scores.abs() <= threshold]

        removed = before - len(df)
        logger.debug(f"method: {method}, threshold: {threshold}, rows removed: {removed}")

    return df


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    dct = config["processing"]
    if dct["remove_duplicates"] is True:
        df = remove_duplicates(df)

    if dct["missing"]["enabled"] is True:
        df = handle_missing(df, axis=dct["missing"]["axis"])

    if dct["outliers"]["enabled"] is True:
        df = remove_outliers(
            df,
            dct["outliers"]["columns"],
            dct["outliers"]["method"],
            dct["outliers"]["threshold"]
        )

    return df


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    dct = {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": df_before.shape[1],
        "columns_after": df_after.shape[1],
        "columns_removed": df_before.shape[1] - df_after.shape[1]
    }

    return dct