import sys, struct

'''
    yuwu@ 
    Terrain format
    
	struct TerrainBlockHeader
	{
		uint32		version_;
		uint32		heightMapWidth_;
		uint32		heightMapHeight_;
		float		spacing_;
		uint32		nTextures_;
		uint32		textureNameSize_;
		uint32		detailWidth_;
		uint32		detailHeight_;
		uchar		uvRepeatTimes_[4];
		uchar		boxProjChannel_[4];
		uint32		padding_[64 - 8 - sizeof(uchar)*8/sizeof(uint32)];
	};
    
    0000: header(256B)
    0100: pics(128B*4)
    0300: height(4B*53*53)
    2ee4: unknown(?)
'''

def rotate(fname): # 90 degree
    #print 'rotating', fname
    f = open(fname, 'rb')
    
    header = f.read(256) # read headers
    version, w, h, spacing, ntex, texnamesize = struct.unpack('LLLfLL', header[:4*6])
    assert(w==h)
    assert(w>0)
    assert(ntex>0)
    assert(texnamesize==128)
    #print 'info'
    #print version, w, h, spacing, ntex, texnamesize
    
    texnames = []
    for i in range(ntex): # extract tex names
        texname = f.read(texnamesize)
        texname = texname.replace('\x00','')
        texnames.append(texname)
    #print texnames
    
    heights = struct.unpack('f'*w*h, f.read(4*w*h))
    #print heights
    
    f.close()
    
    # rotate heights
    newheights = []
    #print h, w
    for y in xrange(h):
        for x in xrange(w):
            # index in old heights (y,1-x)
            index = (w-x-1)*w + y 
            newheights.append(heights[index])           
    #print newheights
    assert(len(heights)==len(newheights))
    #print newheights
    #print len(newheights)
	
    return  (w, h, newheights)
    """
    f = open(fname, 'rb+') # open for modification
    f.seek(256+texnamesize*ntex)
    f.write(struct.pack('f'*w*h,*newheights))
    f.close()
    """
    
if __name__ == "__main__":
    if len(sys.argv) <> 2:
        #print 'usuage: %s height_map' % sys.argv[0]
        exit()
        
    fname = sys.argv[1]
    rotate(fname)
    
