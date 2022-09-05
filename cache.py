def openFile(s):
	f = open(s, 'r')
	address = f.readlines()
	for i in range(len(address)):
        	s = address[i]
        	s = s[2:12]	#get hexadecimal address removing everything else
        	address[i] = s
	f.close()
	return address		

def getBinary(h):
	b = bin(int(h, 16))
	b = b[2:]	# remove '0b' in front
	result = ''
	l = len(b)
	i = 0
	while(i<32-len(b)):	# add required number of zeroes in
				# front to make the binary 32 bits
		result += '0'
		i += 1
	result += b
	return result		
		
def numHitMiss(address, cacheSize, blockSize):
	hit, miss = 0, 0
	cacheLines = int((cacheSize*1024)/blockSize)  
	temp = cacheLines
	numIndexBits = 0
	while(temp != 1):	# calculate number of index bits
		temp /= 2
		numIndexBits += 1
	temp = blockSize  
	numOffsetBits = 0
	while(temp != 1):	# calculate number of offset bits
                temp /= 2
                numOffsetBits += 1
	numTagBits = 32 - numIndexBits - numOffsetBits

	cache = []
	for i in range(cacheLines):	# add each row into cache
		cache.append([0, None, None])	# valid bit = 0,
                                                # tag and data = None
	
	valid = 0       # index values to access value of
	tag = 1         # valid bit and tag bit in each row

	for a in address:
		b = getBinary(a[2:])	# remove '0x' and get binary of hexadecimal address

		t = b[0 : numTagBits]			 # get tag value from binary address
		index = b[numTagBits : 32-numOffsetBits] # get index value from binary address
		index = int(index, 2)		
		if (cache[index][valid] == 0):		# check valid bit at given index
			cache[index][valid] = 1
			cache[index][tag] = t
			miss += 1
		else:
			if(cache[index][tag] == t):	# if valid bit == 1, check tag value
				hit += 1
			else:
				cache[index][tag] = t
				miss += 1
	return (hit, miss)	
		
	 
if __name__ == "__main__":
	cacheSize = int(input('Enter cache size : '))
	blockSize = int(input('Enter block size : '))
	file = ['twolf.trace', 'gcc.trace', 'swim.trace', 'gzip.trace', 'mcf.trace']
	for fl in file:
			
		address = openFile(fl)   # address is a list of
				        # hexadecimal address strings

		hit, miss = numHitMiss(address, cacheSize, blockSize)	
		#print("Number of hits = ", hit)
		#print("Number of misses = ", miss)
		#print("Total = ",miss+hit)
		print("Hit rate for " + fl + " = ", hit/(hit+miss))

