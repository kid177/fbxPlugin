import os, struct, sys

MAGIC = '\x65\x4e\xa1\x42' # binary section magic number

def pad(size, padding = 4):
    return ((padding-size)%padding)

def extract(fname, dirname):

    f = open(fname, 'rb')
    assert MAGIC == f.read(4)

    # read indeices size
    f.seek(-4, os.SEEK_END)
    index_size = struct.unpack('L', f.read(4))[0]
    assert((index_size % 4) == 0)
    f.seek(-4-index_size, os.SEEK_END)
    # read indices
    readsize = 0
    sec_list = [] # [(name, offset, size), ...]
    calc_size = 0 # calculate the size we get for verification
    calc_size += len(MAGIC) # magic
    while readsize < index_size:
        nums = struct.unpack('L'*6,f.read(4*6))
        readsize += 4*6
        sec_size = nums[0]
        secname_size = nums[5]
        # read secname
        secname = f.read(secname_size)
        readsize += secname_size
        pad_size = pad(secname_size)
        f.read(pad_size) # pad to 4bytes
        readsize += pad_size
        
        sec_list.append((secname, calc_size, sec_size)) #(name, offset, size)
        calc_size += sec_size + pad(sec_size) # sections are also pad to 4bytes

    # print sec_list

    calc_size += index_size
    calc_size += 4 # index_size dword
    # check file size correct
    f.seek(0, os.SEEK_END)
    fsize = f.tell()
    assert fsize == calc_size # check if size match

    # create target dirs
    os.makedirs(dirname)
    for name, offset, secsize in sec_list:
        # save each section
        #print 'writing: %s, offset %d, size %d' % (name, offset, secsize)
        f.seek(offset)
        content = f.read(secsize)
        open(dirname+'/'+name, 'wb').write(content)
    
    f.close()

def create(fname, dirname):
    f = open(fname, 'wb')
    f.write(MAGIC) # binsec magic
    
    secnames = []
    for secname in os.listdir(dirname):
        if os.path.isfile(dirname+'/'+secname):
            secnames.append(secname)
        else:
			pass
            #print 'skipping', secname
    
    sections = [] # [(name, offset, size),...]
    # writing each section contents
    for secname in secnames:
        content = open(dirname+'/'+secname,'rb').read()
        secsize = len(content)
        offset = f.tell()
        assert((offset % 4) == 0) # check padding
        #print 'packing %s, offset %d, size %d' % (secname, offset, secsize)
        f.write(content)
        # add padding
        padsize = pad(secsize)
        f.write('\x00'*padsize)
        
        sections.append((secname, offset, secsize))
        
    # generate index
    index = ''
    for secname, offset, secsize in sections:
        index += struct.pack('L'*6, secsize, 0,0,0,0, len(secname))
        index += secname
        index += '\x00' * pad(len(secname))

    index_size = len(index)
    f.write(index)
    f.write(struct.pack('L', index_size))
    f.close()
    
if __name__ == "__main__":
    if len(sys.argv) <> 4:
        #print 'usuage: %s [e|c] bin_filename target_dir' % sys.argv[0]
        exit()
        
    param, binfname, dirname = sys.argv[1:]
    
    if param.startswith('e'):
        #print 'extracting %s to %s' % (binfname, dirname)
        extract(binfname, dirname)
    elif param.startswith('c'):
        #print 'creating %s from %s' % (binfname, dirname)
        create(binfname, dirname)
    else:
		pass
        #print 'wrong param:', param
    
