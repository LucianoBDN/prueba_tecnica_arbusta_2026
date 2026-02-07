import os


def validate_file_path(path: str) -> None:
    """_summary_
        Valida la ruta de un archivo CSV.

        Esta función realiza una serie de validaciones sobre el path proporcionado para asegurarse
        de que es un archivo CSV válido. Las validaciones incluyen comprobar si el path no está vacío,
        si el archivo existe, si es un archivo regular y si tiene la extensión ".csv".
        Args:
        path (str): Ruta del archivo a validar.

    Raises:
       ValueError: Si el path está vacío, no es un archivo CSV o no se puede verificar.
        FileNotFoundError: Si el archivo no existe en el path especificado.
    """
    if not path:
        raise ValueError("El path no puede estar vacío")

    if not os.path.exists(path):
        raise FileNotFoundError(f"El archivo no existe: {path}")

    if not os.path.isfile(path):
        raise ValueError(f"El path no es un archivo: {path}")

    if not path.lower().endswith(".csv"):
        raise ValueError("El archivo debe ser un CSV")





def normalize_columns(df):
    """
    Normaliza los nombres de las columnas del DataFrame.

    Esta función toma un DataFrame y realiza dos operaciones en sus nombres de columna:
    1. Elimina los espacios en blanco al principio y al final de los nombres de columna.
    2. Convierte todos los nombres de columna a minúsculas.
    
    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    df.columns = df.columns.str.strip().str.lower()
    return df


def validate_csv_structure(df, required_columns: set):
    """
    Valida que el DataFrame contenga todas las columnas requeridas.

    Compara las columnas presentes en el DataFrame con un conjunto de columnas requeridas.
    Si alguna de las columnas requeridas está ausente, lanza una excepción `ValueError` indicando 
    qué columnas faltan.

    Args:
        df (pandas.DataFrame): El DataFrame que se desea validar.
        required_columns (set): Un conjunto que contiene los nombres de las columnas requeridas.

    Raises:
        ValueError: Si faltan columnas requeridas en el DataFrame.
    """


    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")