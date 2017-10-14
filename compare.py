#!/bin/env python

from simhash import fingerprint, hamming_distance
from httplib import HTTPConnection, HTTPSConnection
from urlparse import urlparse
from argparse import ArgumentParser
from collections import deque
import zlib, re, sys

def options():
    options = ArgumentParser()
    options.add_argument('url1', action='store',  help='First Url')
    options.add_argument('url2', action='store',  help='Second Url')
    options.add_argument('-l', '--length', dest='length', action='store', type=int, default=8, help='Length of each shingle')
    options.add_argument('-s', '--separator', dest='separator', action='store', default=' ', help='Token separator \'\' (empty string) for characters instead of words')
    options.add_argument('-x', '--hash', dest='hash', action='store', help='hash|murmur')
    return options.parse_args()

def main():
    args = options()
    print "Comparing: "
    print args.url1
    print args.url2

    hash_func = hash
    if args.hash == 'murmur':
        import mmh3
        hash_func = lambda x: mmh3.hash64(x)[0]
        
    print "Similarity: %0.3f"%url_similarity(args.url1,args.url2,args.length,args.separator,hash_func)
    

def inflate(data):
    #http://bytes.com/topic/python/answers/836692-deflate-urllib2
    output = None
    #Try gzip
    try:
        return zlib.decompress(data, zlib.MAX_WBITS + 16)
    except zlib.error:
        pass
    #Try deflate
    try:
        return zlib.decompress(data)
    except zlib.error:
        pass
    #Try raw-deflate
    return zlib.decompress(data, -zlib.MAX_WBITS)

def fetch(url):
    urlo = urlparse(url)
    if url.lower().startswith('https'):
        HTTPClass = HTTPSConnection
    else:
        HTTPClass = HTTPConnection

    connection = HTTPClass(urlo.netloc)
    connection.request('GET',url)
    response = connection.getresponse()
    data = None
    try:
        if response.status != 200:
            raise Exception("Failed to retrieve: %s"%url)
        encoding = response.getheader('Content-Encoding')
        data = response.read()
        if encoding:
            data = inflate(data)
    finally:
        connection.close()
    return data

def canonize(data):
    data = data.lower()
    #Remove everythign between these tags
    data = re.sub(r'<(script|style|svg|video|audio|picture|menu|map|head|canvas).*?</?\1>',' ',data,flags=re.M|re.S)
    #Remove all comments
    data = re.sub(r'<!--.*?-->',' ',data,flags=re.M|re.S)
    data = re.sub(r'<!doctype[^>]*>',' ',data,flags=re.M|re.S)
    #Remove all tags
    data = re.sub(r'<[^>]*/?>',' ',data,flags=re.M|re.S)
    #remove xml entitites
    data = re.sub(r'&\w+;',' ',data)
    #Replace anything not a char, number, hyphen or whitespace, with a space
    data = re.sub(r'[^ a-zA-Z0-9-]',' ',data)
    #Replace all blocks of white space with a single space 
    data = re.sub(r'\s+',' ',data)
    return data

def tokenize(text,separator=' '):
    pos = endpos = 0
    text_len = len(text)
    while True:
        endpos = text.find(separator,pos)
        if endpos < 0 or endpos >= text_len: break
        if pos == endpos:
            yield text[pos]
        else:
            yield text[pos:endpos]
        pos = endpos + 1

def shingle(iterable,length=8,separator=' '):
    count = 0;
    shingle = deque([], length)
    for token in iterable:
        shingle.append(token)
        if len(shingle) >= length:
            result = separator.join(shingle)
            print result
            yield result
    
def hash_list(iterable, hash_func = hash):
    return [ hash_func(val) for val in iterable ]

def simhash(data,length=8,separator=' ',hash_func=hash):
    text       = canonize(data)
    tokenizer  = tokenize(text,separator)
    shingler   = shingle(tokenizer,length,separator)
    hashs      = hash_list(shingler,hash_func)
    return fingerprint(hashs)


def hash_url(url,length=8,separator=' ',hash_func=hash):
    data = fetch(url)
    return simhash(data,length,separator,hash_func)

def compare_fingerprints(hash1,hash2):
    return hamming_distance(hash1,hash2)

def url_similarity(url1,url2,length=8,separator=' ',hash_func=hash):
    hash1 = hash_url(url1,length,separator,hash_func)
    hash2 = hash_url(url2,length,separator,hash_func)
    return hash_similarity(hash1,hash2)

def hash_similarity(hash1,hash2):
    return 1 - compare_fingerprints(hash1,hash2)/64.0


if __name__ == '__main__': main()
# vi:sw=4:ts=4:et
