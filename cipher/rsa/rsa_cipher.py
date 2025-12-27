from random import randrange,getrandbits
from itertools import repeat
from functools import reduce
from math import log10
from time import perf_counter
import ast
import os
class RSACipher:
    def __init__(self):
        pass
    
    def getPrime(self,n):
        def isProablePrime(n,t=7):
            def isComposite(a):
                if pow(a,d,n) == 1:
                    return False
                for i in range(s):
                    if pow(a, 2 ** i * d,n) == n - 1:
                        return False
                return True
            assert n > 0
            if n < 3:
                return[False,False,True][n]
            elif not n & 1:
                return False
            else:
                s,d=0,n-1
                while not d & 1:
                    s+=1
                    d>>=1
            for _ in repeat(None,t):
                if isComposite(randrange(2,n)):
                    return False
            return True
        p=getrandbits(n)
        while not isProablePrime(p):
            p=getrandbits(n)
        return p
    def inv(self,p,q):
        def xgcd(x,y):
            s1,s0=0,1
            t1,t0=1,0
            while y:
                q= x // y
                x,y= y,x % y
                s1,s0= s0 - q * s1,s1
                t1,t0= t0 - q * t1,t1
            return x, s0, t0
        s,t= xgcd(p,q)[0:2]
        assert s==1
        if t < 0:
            t+=q
        return t
    
    def genRSA(self,p,q):
        n= p * q
        phi= (p-1)*(q-1)
        if n <65537:
            e=3
            d=self.inv(e,phi)
        else:
            e=65537
            d=self.inv(e,phi)
        return (e,d,n)
    
    def generate_keys(self):
        p=self.getPrime(1024)
        q=self.getPrime(1024)
        e,d,n=self.genRSA(p,q)
        return((e,n),(d,n),p,q)
    
    def load_keys(self,directory_path:str):
        private_key = None
        public_key = None
        p=None
        q=None
        # Loop through all files in the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                with open(file_path, "r") as f:
                    data = f.read()
                    key = ast.literal_eval(data)
                # Check filename pattern
                if filename.endswith('_private.txt'):
                    private_key = key
                elif filename.endswith('_public.txt'):
                    public_key = key
                elif filename.endswith("_p.txt"):
                    p=key
                elif filename.endswith("_q.txt"):
                    q=key

        return public_key, private_key,p,q
    
        
    
    def encrypt(self, message: str, key):
        e, n = key
        plain_bytes = message.encode()

        cipher_nums = [pow(b, e, n) for b in plain_bytes]

        cipher_bytes = b".".join(str(x).encode() for x in cipher_nums)

        return cipher_bytes

        
    
    def decrypt(self, cipher_bytes: bytes, key):
        d, n = key

        # Tách thành list số
        nums = cipher_bytes.decode().split(".")
        nums = [int(x) for x in nums]

        plain_bytes = bytes([pow(x, d, n) for x in nums])

        return plain_bytes.decode()


    
    def sign(self, message: str, private_key):
        d, n = private_key
        h = sum(message.encode())  # simple hash
        sig = pow(h, d, n)
        return str(sig).encode()

    # ---------------------------
    # VERIFY signature(bytes)
    # ---------------------------
    def verify(self, message: str, signature_bytes: bytes, public_key):
        e, n = public_key
        sig = int(signature_bytes.decode())

        h_real = sum(message.encode())
        h_dec = pow(sig, e, n)

        return h_real == h_dec
    
    

    def printHexList(self,intList):
        for index, elem in enumerate(intList):
            if index % 32 == 0:
                print(),
                print("{0:02x}".format(elem))
            print()
        
            
            
        
            
        
        
        
        
                
    