
Compare Urls
^^^^^^^^^^^^^^^^

A script that will compare the contents of two urls and return a similarity score between 0 and 1 indicating the approximate Jacquard similarity using simhash.

By default the script will tokenize the contents by words using 8 word rolling shingles.  Parameters can change the numbers of words in the shingle, as well as the switching to using characters instead of words.  The default is to use the builtin python hash function but the murmur hash can also be selected.


To install the dependencies run::

  ./setup.py install


To run the script::

  ./compare.py http://mysite.com/page1.html http://yoursite.com/page3.html

or to use murmur with 32 character shingles::

  ./compare.py -x murmur -l 32 -s '' http://mysite.com/page1.html http://yoursite.com/page3.html







  
