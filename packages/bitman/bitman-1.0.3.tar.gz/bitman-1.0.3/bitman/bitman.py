class bitman:
    def __init__(self, size=0, init=0):
        '''
        Initializes the bitman class with 'size' bits initialized to init (either 0 or 1)
        '''
        
        assert init in [0,1], "Initialize the bits to 0 or 1"
        self.size = size
        if (init==0):
            self.bits=0
        elif (init==1):
            self.bits = 2**(size+1)-1

    def __repr__(self):
        #return bin(self.bits)[2:-1]
        ans = {True:'1', False:'0'}
        return ''.join([ ans[((self.bits & (1<<i))>0)] for i in range(self.size-1,-1,-1)])

    def get(self, n):
        '''
        Get the n-th bit.
        '''
        return (self.bits & (1<<n))>0

    def set(self, n, val):
        '''Set the n-th bit to val. 
        val is either 1 or 0.'''
        
        if (val == 1):
            self.bits = self.bits | 1<<n
        else:
            tmp = 2**(max( [self.size, n])) -1
            tmp = tmp - (1<<n)
            self.bits = (self.bits & tmp)
            if n>self.size:
                self.size=n
            

    def which(self, val):
        '''
        Returns a list of positions of bits with a value val (that is 0 or 1).
        '''
        ans = []
        for i in range(self.size):
                if self.get(i)==val:
                    ans.append(i)
        return ans


