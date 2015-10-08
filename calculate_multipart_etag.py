# calculate_multipart_etag  Copyright (C) 2015
#      Tony Lastowka <tlastowka at gmail dot com>
#      https://github.com/tlastowka	
#
#
# calculate_multipart_etag is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# calculate_multipart_etag is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with calculate_multipart_etag.  If not, see <http://www.gnu.org/licenses/>.


def calculate_multipart_etag(source_path, chunk_size, expected=None):

    """
    calculates a multipart upload etag for amazon s3

    Arguments:

    source_path -- The file to calculate the etage for
    chunk_size -- The chunk size to calculate for.

    Keyword Arguments:

    expected -- If passed a string, the string will be compared to the resulting etag and raise an exception if they don't match


    """

    import hashlib
    md5s = []

    with open(source_path,'rb') as fp:
        while True:

            data = fp.read(chunk_size)

            if not data:
                break
            md5s.append(hashlib.md5(data))

    digests = b"".join(m.digest() for m in md5s)

    new_md5 = hashlib.md5(digests)
    new_etag = '"%s-%s"' % (new_md5.hexdigest(),len(md5s))
    if expected:
        if not expected==new_etag:
            raise ValueError('new etag %s does not match expected %s' % (new_etag,expected))

    return new_etag

if __name__ == '__main__':

	import sys


	if  len(sys.argv) < 3 or len(sys.argv) > 4:

		print("python %s source_path chunk_size [expected]" % (sys.argv[0]))
		exit()

	source_path = sys.argv[1]
	chunk_size = sys.argv[2]
	chunk_size = int(chunk_size) * 1024 * 1024


	try:
		expected = '"%s"' % (sys.argv[3])
	except Exception as e:
		expected = None


	print(calculate_multipart_etag(source_path,chunk_size,expected))

