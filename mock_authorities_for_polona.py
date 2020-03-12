import json

from tqdm import tqdm
from pymarc import MARCReader, Record


AUTHORITY_FIELDS = ['100', '110', '111', '130', '148', '150', '151', '155']

def read_marc_from_file(file) -> Record:
    with open(file, 'rb') as fp:
        rdr = MARCReader(fp, to_unicode=True, force_utf8=True, utf8_handling='ignore', permissive=True)
        for rcd in rdr:
            yield rcd


def main_loop(input_file: str, output_file: str, limit=) -> None:
    dict_to_write = {}

    for rcd in tqdm(read_marc_from_file(input_file)):
        for fld in AUTHORITY_FIELDS:
            if fld in rcd:
                dict_to_write.setdefault(fld, []).append(rcd.get_fields(fld)[0].value())




if __name__ == '__main__':

    auth_dump = 'authorities-all.marc'
    polona_mockup = 'polona_mockup.json'

    main_loop(auth_dump, polona_mockup)
