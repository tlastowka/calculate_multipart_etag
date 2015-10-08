DESCRPTION:

	Given a file and a chunk size in megabytes, calculates what the Amazone S3 etag will be.



	Amazon uses a simple md5 sum for an etag on single part uploads, but on multipart uploads they use a scheme of md5ing the chunks, converting the md5s to binary, and then md5ing the binary of the chunks.

	This can make comparing files in s3 to local copies without downloading them a pain.

	The process to generate them is just convoluted enough that there's a lot of confused people out there on the forums.
	Lots of speculation, not much code examples other than some bash tools.

	It works from the command line, or import the function into your own code and use it there.

	Tested on python 3.4, but should work on 2.6+ unless I missed something obvious.

	Big thanks to antespi for his bash tool that does the same thing.
		 https://github.com/antespi/s3md5



USAGE:
	python calculate_multipart_etag.py source_path chunk_size [expected]

EXAMPLES:

	# just generate the etag

	$ python ./calculate_multipart_etag.py 100meg.file 50
	"67ff3c4020afd26957fe91c1891e362e-2"
	$


	# compare it with one you have already (success)

	$ python ./calculate_multipart_etag.py 100meg.file 50 "67ff3c4020afd26957fe91c1891e362e-2"
	"67ff3c4020afd26957fe91c1891e362e-2"

	# compare it with one you have already (failure)

	$ python ./calculate_multipart_etag.py 100meg.file 50 "1234567890abcdefghijklmnopqrstuv-42"
	Traceback (most recent call last):
	  File "./calculate_multipart_etag.py", line 81, in <module>
	    print(calculate_multipart_etag(source_path,chunk_size,expected))
	  File "./calculate_multipart_etag.py", line 56, in calculate_multipart_etag
	    raise ValueError('new etag %s does not match expected %s' % (new_etag,expected))
	ValueError: new etag "67ff3c4020afd26957fe91c1891e362e-2" does not match expected "1234567890abcdefghijklmnopqrstuv-42"
	$


