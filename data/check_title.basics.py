import csv

INPUT = 'title.basics.tsv'
OUTPUT_GOOD = 'title.basics.cleaned.csv'
OUTPUT_BAD = 'title.basics.errors.csv'

EXPECTED_COLUMNS = [
    'tconst',
    'titletype',
    'primarytitle',
    'originaltitle',
    'isadult',
    'startyear',
    'endyear',
    'runtimeminutes',
    'genres'
]

EXPECTED_TYPES = {
    'tconst': str,
    'titletype': str,
    'primarytitle': str,
    'originaltitle': str,
    'isadult': bool,
    'startyear': float,
    'endyear': float,
    'runtimeminutes': int,
    'genres': str
}


def is_valid(value, expected_type):
    if value == '' or value == '\\N':
        return True
    try:
        if expected_type == bool:
            return value in ['0', '1', 'true', 'false', 'True', 'False']
        elif expected_type == int:
            return float(value).is_integer()
        elif expected_type == float:
            float(value)
            return True
        elif expected_type == str:
            return isinstance(value, str)
    except:
        return False
    return False


def clean_and_validate_row(row):
    if len(row) != len(EXPECTED_COLUMNS):
        return False, row

    row_dict = dict(zip(EXPECTED_COLUMNS, row))

    val = row_dict['runtimeminutes'].strip()
    if val not in ['', '\\N']:
        try:
            fval = float(val)
            if fval.is_integer():
                row_dict['runtimeminutes'] = str(int(fval))
        except ValueError:
            pass

    for col, val in row_dict.items():
        if not is_valid(val.strip(), EXPECTED_TYPES[col]):
            return False, row

    cleaned_row = [row_dict[col] for col in EXPECTED_COLUMNS]
    return True, cleaned_row


def split_safely(line): 
    parts = line.rstrip('\n').split('\t')

    if len(parts) == len(EXPECTED_COLUMNS):
        return parts

    if len(parts) > len(EXPECTED_COLUMNS):
        # tconst, titletype, ...
        first_two = parts[:2]
        last_six = parts[-6:]

        middle = parts[2:len(parts)-6]
        merged_title = ",".join(middle)
        fixed = first_two + [merged_title] + last_six
        if len(fixed) == len(EXPECTED_COLUMNS):
            return fixed

    return parts


# === MAIN ===
total, good, bad = 0, 0, 0

with open(INPUT, 'r', encoding='utf-8') as infile, \
     open(OUTPUT_GOOD, 'w', encoding='utf-8', newline='') as goodfile, \
     open(OUTPUT_BAD, 'w', encoding='utf-8') as badfile:

    writer = csv.writer(goodfile, quotechar='"', quoting=csv.QUOTE_ALL)

    header = infile.readline().strip().split('\t')
    header_lower = [h.strip().lower() for h in header]
    if header_lower != EXPECTED_COLUMNS:
        print("⚠️ Header does not match expected columns!")
        print(f"TSV header: {header_lower}")
        exit(1)
    writer.writerow(EXPECTED_COLUMNS)

    for idx, line in enumerate(infile, start=2):
        total += 1
        parts = split_safely(line)
        valid, cleaned = clean_and_validate_row(parts)

        if valid:
            writer.writerow(cleaned)
            good += 1
        else:
            badfile.write(f"Line {idx}: Napaka → {parts}\n")
            bad += 1

        if total % 500000 == 0:
            print(f"Processed {total:,} lines... ({good:,} OK, {bad:,} errors)")

print("\n✅ Finished!")
print(f"Total lines: {total:,}")
print(f"Valid: {good:,}")
print(f"Invalid: {bad:,}")
