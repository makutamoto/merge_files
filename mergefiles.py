#!/usr/bin/env python3
import os
from hashlib import sha512
from optparse import OptionParser


def hash_file(filename):
    try:
        with open(filename, 'rb') as f:
            hash = sha512()
            while True:
                block = f.read(131072)
                if not block:
                    return hash.hexdigest()
                hash.update(block)
    except IOError:
        return None


if __name__ == '__main__':
    parser = OptionParser(usage="%prog [option] [files]")
    parser.add_option('-f', '--force', action='store_true', default=False, help="allow to merge files.")
    options, args = parser.parse_args()

    num_merge = 0
    num_merged = 0
    hashes = []
    if not options.force:
        print("Following merges are processed. (--force)")
    for filename in args:
        hash = hash_file(filename)
        if hash is None:
            print("Ignored: '%s' could not be read." % filename)
        else:
            merged = False
            for old_filename, old_hash in hashes:
                if hash == old_hash:
                    num_merge += 1
                    if options.force:
                        try:
                            os.remove(filename)
                            print("Merged: '%s' -> '%s' sha512: %s" % (filename, old_filename, hash))
                            num_merged += 1
                        except:
                            print("Error: '%s' couldn't be deleted." % filename)
                    else:
                        print("'%s' -> '%s' sha512: %s" % (filename, old_filename, hash))
                    marged = True
                    break
            if not merged:
                hashes.append([filename, hash])
    print("%d of %d files are merged." % (num_merged, num_merge))
