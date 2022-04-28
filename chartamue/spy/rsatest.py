from cmath import e
import rsa
def generateKey():
    (pubkey, privkey) = rsa.newkeys(512)
    print(privkey.n)
    print(privkey.e)
    print(privkey.d)
    print(privkey.p)
    print(privkey.q)
    return privkey.n,privkey.e,privkey.d,privkey.p,privkey.q
generateKey()