import json

from tqdm import tqdm
from pymarc import MARCReader, Record


AUTHORITY_FIELDS = ['100', '110', '111', '130', '148', '150', '151', '155']


def read_marc_from_file(file) -> Record:
    with open(file, 'rb') as fp:
        rdr = MARCReader(fp, to_unicode=True, force_utf8=True, utf8_handling='ignore', permissive=True)
        for rcd in rdr:
            yield rcd


def main_loop(input_file: str, output_file: str, limit: int = 0) -> None:
    dict_to_write = {}
    limit_counter = 0

    for rcd in tqdm(read_marc_from_file(input_file)):
        limit_counter += 1

        for fld in AUTHORITY_FIELDS:
            if fld in rcd:
                dict_to_write.setdefault(fld, []).append(rcd.get_fields(fld)[0].value())
                break

        if limit_counter > limit:
            break

    with open(output_file, 'w', encoding='utf-8') as fp:
        json.dump(dict_to_write, fp, ensure_ascii=False)


if __name__ == '__main__':

    auth_dump = 'authorities-all.marc'
    polona_mockup = 'polona_mockup_100000.json'

    main_loop(auth_dump, polona_mockup, limit=100000)
