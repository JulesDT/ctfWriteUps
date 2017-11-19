from Crypto.PublicKey import DSA
from Crypto.Hash import SHA


# Regular Modinv code

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

# nonce Generation code from the my_DSA.py file of the challenge
def nonce(msg, max_int):
    n = 0
    for i in msg:
        n += i % max_int
        n = 53 * n % max_int
    n = (n - len(msg)) % max_int
    return n


def solve():
    with open("public.pem", "rb") as public:
        public_dsa = DSA.importKey(public.read())
    with open('signed', 'rb') as f:
        signed_msg = f.read()
    with open('signature', 'rb') as f:
        r, s = eval(f.read())
    with open('sign_me', 'rb') as f:
        to_sign = f.read()

    k = nonce(signed_msg, public_dsa.q)
    hashed_message = int.from_bytes(SHA.new(signed_msg).digest(), byteorder='big')
    x = (((s * k) - hashed_message) * modinv(r, public_dsa.q)) % public_dsa.q
    if x:
        print('Found a potential private key !')
    else:
        raise Exception('Problem when calculating the private key')

    private_dsa = DSA.construct((public_dsa.y, public_dsa.g, public_dsa.p, public_dsa.q, x))
    # verify the private key is the right one:
    new_r, new_s = private_dsa.sign(hashed_message, k)
    if new_r != r or new_s != s:
        print("Error when getting the private key, the generated signature doesn't coincide with the known one")
        return
    else:
        print("The private key found is the right one")
    to_sign_hashed = SHA.new(to_sign).digest()
    solution = private_dsa.sign(to_sign_hashed, nonce(to_sign, public_dsa.q))
    print('Here is the signed message: {}'.format(solution))


if __name__ == '__main__':
    solve()
