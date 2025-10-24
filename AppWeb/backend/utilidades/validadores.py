import re
from datetime import datetime

def valida_fecha(date_str):
    """
    Valida que una fecha tenga formato dd/mm/yyyy o dd/mm/yyyy hh24:mi
    """
    # Patrón para dd/mm/yyyy
    date_patron = r'^(\d{2}/\d{2}/\d{4})$'
    # Patrón para dd/mm/yyyy hh24:mi
    datetime_patron = r'^(\d{2}/\d{2}/\d{4}) (\d{2}:\d{2})$'

    if re.match(date_patron, date_str):
        try:
            datetime.strptime(date_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    elif re.match(datetime_patron, date_str):
        try:
            datetime.strptime(date_str, "%d/%m/%Y %H:%M")
            return True
        except ValueError:
            return False
    return False

def valida_nit(nit_str):
    nit_patron = r'^(\d+-[A-Z0-9])$'
    return bool(re.match(nit_patron, nit_str))

def valida_numero_positivo(numero_str):
    """
    Valida que un string represente un número positivo
    """
    try:
        num = float(numero_str) 
        return num > 0
    except (ValueError, TypeError):
        return False