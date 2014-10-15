import unicodedata
from base64 import b16encode
from hashlib import md5

from clld.scripts.util import parsed_args
from clld.lib.dsv import reader


def main(args):
    mapping = {}
    for row in reader(args.data_file('phoible-phonemes.tsv'), namedtuples=True):
        if row.GlyphID not in mapping:
            unicode_desc = [(c, unicodedata.name(c)) for c in row.Phoneme]
            description = ' - '.join([t[1] for t in unicode_desc])
            mapping[int(row.GlyphID)] = b16encode(md5(description).digest())

    with open(args.data_file('segment_id_mapping.txt'), 'w') as fp:
        for gid in sorted(mapping.keys()):
            fp.write('    ("%s", "%s"),\n' % (gid, mapping[gid]))


if __name__ == '__main__':
    main(parsed_args())
