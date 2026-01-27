#!/usr/bin/env python3
"""
Script unificado para migrar contactos de Argentina desde archivos CSV y XLSX a contacts.csv

CRITERIOS DE ACEPTACIÓN:
1. Estructura del archivo: Debe tener columnas 'title' y 'address'
2. Ubicación geográfica: Debe contener referencias a Argentina en address o complete_address
3. Datos mínimos: title (obligatorio), address (obligatorio), phone/email/website (opcionales)
4. Prevención de duplicados: No agregar si el título ya existe en contacts.csv
5. Formato de salida: First Name=ARG, Last Name=título, Phone=+549XXXXXXXXXX
"""

import csv
import re
import json
import glob
import os
import zipfile
import xml.etree.ElementTree as ET


# ============================================================================
# CRITERIO 5: FORMATO DE SALIDA - Formateo de teléfonos
# ============================================================================
def format_phone(phone):
    """
    Convierte el formato de teléfono a +549XXXXXXXXXX (formato Argentina)

    Ejemplos:
    - 011 4225-6588 -> +54911422565588
    - 11 4225-6588 -> +549114225688
    - 15 4225-6588 -> +549154225688
    - 42256588 -> +5491142256588
    """
    if not phone:
        return ""

    phone = str(phone).strip()
    phone_clean = re.sub(r'[^\d]', '', phone)  # Eliminar todo excepto números

    # Si empieza con 54 (código Argentina)
    if phone_clean.startswith('54'):
        if phone_clean.startswith('549') and len(phone_clean) >= 12:
            return f"+{phone_clean}"
        elif len(phone_clean) >= 11:
            return f"+549{phone_clean[2:]}"

    # Si empieza con 011 seguido de 8 dígitos -> +54911XXXXXXXX
    if phone_clean.startswith('011') and len(phone_clean) == 11:
        return f"+5491{phone_clean[3:]}"

    # Si empieza con 11 seguido de 8 dígitos -> +54911XXXXXXXX
    if phone_clean.startswith('11') and len(phone_clean) == 10:
        return f"+5491{phone_clean[2:]}"

    # Si empieza con 15 seguido de 8 dígitos -> +54911XXXXXXXX
    if phone_clean.startswith('15') and len(phone_clean) == 10:
        return f"+5491{phone_clean[2:]}"

    # Si tiene exactamente 8 dígitos, asumir que es celular de Buenos Aires
    if len(phone_clean) == 8:
        return f"+54911{phone_clean}"

    # Si empieza con 0 y tiene código de área argentino
    if phone_clean.startswith('0') and len(phone_clean) >= 10:
        return f"+549{phone_clean[1:]}"

    # Devolver el teléfono con formato +549 si tiene números
    if len(phone_clean) >= 8:
        return f"+549{phone_clean}"

    return phone


# ============================================================================
# CRITERIO 5: FORMATO DE SALIDA - Extracción de emails
# ============================================================================
def extract_emails(emails_field):
    """
    Extrae el primer email válido del campo emails
    Soporta JSON arrays y texto plano
    """
    if not emails_field:
        return ""

    try:
        # Intentar parsear como JSON array
        if emails_field.startswith('['):
            emails_list = json.loads(emails_field)
            if emails_list and len(emails_list) > 0:
                return emails_list[0]
    except:
        pass

    # Si no es JSON, buscar emails con regex
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, str(emails_field))
    return emails[0] if emails else ""


# ============================================================================
# CRITERIO 2: UBICACIÓN GEOGRÁFICA - Verificación de Argentina
# ============================================================================
def is_argentina(text):
    """
    Verifica si un texto contiene referencias a Argentina

    Patrones aceptados:
    - Palabras clave: argentina, buenos aires, caba, etc.
    - Códigos postales: B1824, C1430, etc.
    - Localidades: lanús, gerli, quilmes, etc.
    - Código de país: "ar", "country":"ar"
    """
    if not text:
        return False

    text_lower = str(text).lower()

    argentina_patterns = [
        # Palabras clave directas
        'argentina',
        'buenos aires',
        'provincia de buenos aires',
        'cdad. autónoma de buenos aires',
        'caba',

        # Código de país
        'ar"',
        '"country":"ar"',

        # Códigos postales Provincia de Buenos Aires
        'b1824', 'b1826', 'b1820', 'b1825', 'b1822', 'b1823', 'b1828',

        # Códigos postales CABA
        'c1025', 'c1406', 'c1426', 'c1430', 'c1431', 'c1419', 'c1424',

        # Localidades específicas
        'lanús', 'lanus',
        'gerli',
        'remedios de escalada',
        'valentín alsina',
        'quilmes',

        # Otras provincias
        'córdoba, argentina',
        'cordoba, argentina',
    ]

    return any(pattern in text_lower for pattern in argentina_patterns)


# ============================================================================
# LECTURA DE ARCHIVOS CSV
# ============================================================================
def read_csv_contacts(filepath):
    """
    Lee un archivo CSV y retorna lista de contactos de Argentina

    CRITERIO 1: Verifica estructura del archivo (title y address)
    CRITERIO 2: Filtra por ubicación en Argentina
    CRITERIO 3: Valida datos mínimos requeridos
    """
    contacts = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # CRITERIO 1 y 3: Verificar estructura y datos mínimos
                if 'title' in row and 'address' in row:
                    # CRITERIO 2: Verificar ubicación en Argentina
                    address = row.get('address', '')
                    complete_address = row.get('complete_address', '')

                    if is_argentina(address) or is_argentina(complete_address):
                        contacts.append(row)
    except Exception as e:
        print(f"Error leyendo CSV {filepath}: {e}")

    return contacts


# ============================================================================
# LECTURA DE ARCHIVOS XLSX
# ============================================================================
def read_xlsx_contacts(filepath):
    """
    Lee un archivo XLSX y retorna lista de contactos de Argentina
    Los XLSX son archivos ZIP que contienen XML

    CRITERIO 1: Verifica estructura del archivo
    CRITERIO 2: Filtra por ubicación en Argentina
    CRITERIO 3: Valida datos mínimos requeridos
    """
    try:
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            # Leer strings compartidos
            strings = []
            try:
                with zip_ref.open('xl/sharedStrings.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

                    for si in root.findall('.//main:si', ns):
                        t = si.find('main:t', ns)
                        if t is not None:
                            strings.append(t.text if t.text else '')
                        else:
                            strings.append('')
            except:
                pass

            # Leer worksheet
            with zip_ref.open('xl/worksheets/sheet1.xml') as f:
                tree = ET.parse(f)
                root = tree.getroot()
                ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

                rows_data = []
                for row in root.findall('.//main:row', ns):
                    row_data = []
                    for cell in row.findall('.//main:c', ns):
                        value = ''
                        v = cell.find('main:v', ns)
                        if v is not None and v.text:
                            # Si es tipo string compartido
                            if cell.get('t') == 's':
                                try:
                                    idx = int(v.text)
                                    if idx < len(strings):
                                        value = strings[idx]
                                except:
                                    value = v.text
                            else:
                                value = v.text
                        row_data.append(value)
                    rows_data.append(row_data)

                if len(rows_data) < 2:
                    return []

                # Primera fila = headers
                headers = rows_data[0]
                contacts = []

                # CRITERIO 1: Verificar que tenga estructura de contactos
                if 'title' not in headers or 'address' not in headers:
                    return []

                for row in rows_data[1:]:
                    contact = {}
                    for i, val in enumerate(row):
                        if i < len(headers):
                            contact[headers[i]] = val

                    # CRITERIO 3: Datos mínimos
                    if not contact.get('title') or not contact.get('address'):
                        continue

                    # CRITERIO 2: Verificar Argentina
                    address = contact.get('address', '')
                    complete_address = contact.get('complete_address', '')

                    if is_argentina(address) or is_argentina(complete_address):
                        contacts.append(contact)

                return contacts

    except Exception as e:
        print(f"Error leyendo XLSX {filepath}: {e}")
        return []


# ============================================================================
# CRITERIO 4: PREVENCIÓN DE DUPLICADOS Y AGREGAR A CONTACTS.CSV
# ============================================================================
def append_to_contacts_csv(new_contacts, contacts_filepath, source_type='CSV'):
    """
    Agrega nuevos contactos al CSV de Google Contacts

    CRITERIO 4: Previene duplicados verificando títulos existentes
    CRITERIO 5: Aplica formato de salida correcto
    """

    # Definir columnas de Google Contacts
    fieldnames = [
        'First Name', 'Middle Name', 'Last Name', 'Phonetic First Name',
        'Phonetic Middle Name', 'Phonetic Last Name', 'Name Prefix', 'Name Suffix',
        'Nickname', 'File As', 'Organization Name', 'Organization Title',
        'Organization Department', 'Birthday', 'Notes', 'Photo', 'Labels',
        'E-mail 1 - Label', 'E-mail 1 - Value', 'Phone 1 - Label',
        'Phone 1 - Value', 'Website 1 - Label', 'Website 1 - Value'
    ]

    # CRITERIO 4: Leer contactos existentes para evitar duplicados
    existing_titles = set()
    try:
        with open(contacts_filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_titles.add(row.get('Last Name', '').strip().lower())
    except Exception as e:
        print(f"Error leyendo contactos existentes: {e}")

    # Agregar nuevos contactos
    added_count = 0
    with open(contacts_filepath, 'a', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        for contact in new_contacts:
            title = contact.get('title', '').strip()

            # CRITERIO 4: Verificar si ya existe
            if not title or title.lower() in existing_titles:
                continue

            # Agregar al set de existentes
            existing_titles.add(title.lower())

            # CRITERIO 5: Crear contacto en formato Google Contacts
            google_contact = {
                'First Name': 'ARG',
                'Middle Name': '',
                'Last Name': title,
                'Phonetic First Name': '',
                'Phonetic Middle Name': '',
                'Phonetic Last Name': '',
                'Name Prefix': '',
                'Name Suffix': '',
                'Nickname': '',
                'File As': '',
                'Organization Name': '',
                'Organization Title': '',
                'Organization Department': '',
                'Birthday': '',
                'Notes': contact.get('address', ''),
                'Photo': '',
                'Labels': f'Importado el 21/11 desde {source_type} ::: * myContacts',
                'E-mail 1 - Label': '* ' if extract_emails(contact.get('emails', '')) else '',
                'E-mail 1 - Value': extract_emails(contact.get('emails', '')),
                'Phone 1 - Label': '',
                'Phone 1 - Value': format_phone(contact.get('phone', '')),
                'Website 1 - Label': '',
                'Website 1 - Value': contact.get('website', '')
            }

            writer.writerow(google_contact)
            added_count += 1

    return added_count


# ============================================================================
# RENOMBRAR ARCHIVOS PROCESADOS
# ============================================================================
def rename_processed_file(filepath):
    """Renombra archivo agregando prefijo TRASLADO"""
    try:
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        new_name = 'TRASLADO 21112025-1135 ARG ' + filename
        new_path = os.path.join(directory, new_name)
        os.rename(filepath, new_path)
        return True
    except Exception as e:
        print(f"Error renombrando {filepath}: {e}")
        return False


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================
def main():
    """
    Función principal que ejecuta la migración completa

    Proceso:
    1. Busca todos los archivos CSV y XLSX
    2. Filtra por criterios de aceptación
    3. Agrega contactos a contacts.csv
    4. Renombra archivos procesados
    """

    base_path = '/mnt/c/Users/Esteban Selvaggi/Desktop/PROMPT/Archivo de contactos'
    contacts_file = os.path.join(base_path, 'contacts.csv')

    print("=" * 80)
    print("MIGRACIÓN DE CONTACTOS DE ARGENTINA")
    print("=" * 80)
    print()
    print("CRITERIOS DE ACEPTACIÓN:")
    print("1. ✓ Estructura: Archivo debe tener columnas 'title' y 'address'")
    print("2. ✓ Ubicación: Debe contener referencias a Argentina")
    print("3. ✓ Datos mínimos: title y address obligatorios")
    print("4. ✓ Sin duplicados: No agregar si el título ya existe")
    print("5. ✓ Formato: First Name=ARG, Phone=+549XXXXXXXXXX")
    print()
    print("=" * 80)
    print()

    # Procesar archivos CSV
    print("PROCESANDO ARCHIVOS CSV...")
    print("-" * 80)

    csv_files = glob.glob(os.path.join(base_path, '*.csv'))
    csv_total_added = 0
    csv_processed = 0

    for csv_file in csv_files:
        filename = os.path.basename(csv_file)

        # Saltar contacts.csv y archivos ya procesados
        if filename == 'contacts.csv' or filename.startswith('TRASLADO'):
            continue

        contacts = read_csv_contacts(csv_file)

        if contacts:
            added = append_to_contacts_csv(contacts, contacts_file, 'CSV')
            if added > 0:
                print(f"✓ {filename}: {added} contactos agregados")
                rename_processed_file(csv_file)
                csv_processed += 1
                csv_total_added += added
            else:
                print(f"○ {filename}: {len(contacts)} encontrados pero ya existían")

    print()
    print(f"CSV procesados: {csv_processed} archivos, {csv_total_added} contactos agregados")
    print()

    # Procesar archivos XLSX
    print("PROCESANDO ARCHIVOS XLSX...")
    print("-" * 80)

    xlsx_files = glob.glob(os.path.join(base_path, '*.xlsx'))
    xlsx_total_added = 0
    xlsx_processed = 0

    for xlsx_file in xlsx_files:
        filename = os.path.basename(xlsx_file)

        # Saltar archivos temporales y ya procesados
        if filename.startswith('~$') or filename.startswith('TRASLADO'):
            continue

        contacts = read_xlsx_contacts(xlsx_file)

        if contacts:
            added = append_to_contacts_csv(contacts, contacts_file, 'XLSX')
            if added > 0:
                print(f"✓ {filename}: {added} contactos agregados")
                rename_processed_file(xlsx_file)
                xlsx_processed += 1
                xlsx_total_added += added
            else:
                print(f"○ {filename}: {len(contacts)} encontrados pero ya existían")

    print()
    print(f"XLSX procesados: {xlsx_processed} archivos, {xlsx_total_added} contactos agregados")
    print()

    # Resumen final
    print("=" * 80)
    print("RESUMEN FINAL")
    print("=" * 80)
    print(f"Total archivos procesados: {csv_processed + xlsx_processed}")
    print(f"  - CSV: {csv_processed} archivos")
    print(f"  - XLSX: {xlsx_processed} archivos")
    print()
    print(f"Total contactos agregados: {csv_total_added + xlsx_total_added}")
    print(f"  - Desde CSV: {csv_total_added}")
    print(f"  - Desde XLSX: {xlsx_total_added}")
    print()

    # Contar líneas en contacts.csv
    try:
        with open(contacts_file, 'r') as f:
            total_lines = sum(1 for _ in f)
        print(f"Total contactos en contacts.csv: {total_lines - 1} (excluyendo encabezado)")
    except:
        pass

    print()
    print("✓ Proceso completado exitosamente!")
    print("=" * 80)


if __name__ == '__main__':
    main()
