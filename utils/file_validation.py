import os


def validate_file_path(path: str) -> None:
    if not path:
        raise ValueError("El path no puede estar vacío")

    if not os.path.exists(path):
        raise FileNotFoundError(f"El archivo no existe: {path}")

    if not os.path.isfile(path):
        raise ValueError(f"El path no es un archivo: {path}")

    if not path.lower().endswith(".csv"):
        raise ValueError("El archivo debe ser un CSV")


REQUIRED_COLUMNS = {"id", "sentiment", "message "}


def normalize_columns(df):
    df.columns = df.columns.str.strip().str.lower()
    return df


def validate_csv_structure(df, required_columns: set):
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")