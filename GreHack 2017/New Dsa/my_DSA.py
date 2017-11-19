from Crypto.PublicKey import DSA
from Crypto.Hash import SHA

with open("private.pem", "rb") as priv:
    priv_dsa = DSA.importKey(priv.read())
with open("public.pem", "rb") as public:
    public_dsa = DSA.importKey(public.read())

def nonce(msg, max_int):
    n = 0
    for i in msg:
        n += i % max_int
        n = 53*n % max_int
    n = (n - len(msg)) % max_int 
    return n

def new_sign(msg):
    n = nonce(msg, public_dsa.q)
    h = SHA.new(msg).digest()
    sig = priv_dsa.sign(h, n)
    return sig

def new_verify(msg, s):
    h = SHA.new(msg).digest()
    return public_dsa.verify(h,s)

with open('signed', 'rb') as f:
    s = new_sign(f.read())

with open('signature', 'wb') as f:
    f.write(str(s).encode())
