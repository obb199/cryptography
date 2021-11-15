from random import randint


def primes_generator(n):
    """
    Gera um conjunto de números primos com os n primeiros números inteiros.

    """
    primes = []

    for i in range(2, n):
        if i == 2:
            primes.append(2)

        if i % 2 == 0:
            continue

        divisor = False
        for prime in primes:
            if i % prime == 0:
                divisor = True
                break
            if prime > i ** (1 / 2):
                break

        if not divisor:
            primes.append(i)

    return primes


def keys(primes_list):
    p = 1
    q = 1
    length = len(primes_list)
    while p < 10:
        i = randint(0, length-1)
        p = primes_list[i]  # First prime number

    while q < 10 or p == q:
        i = randint(0, length-1)
        q = primes_list[i]  # First prime number

    n = p*q  # Product of p and q
    phi = (p - 1) * (q - 1)  # Numbers of divisors of p and q

    e = randint(2, phi)   # Random number from range 2 and phi

    while not mutual_primes(e, phi):  # 'phi' and 'e' need to be coprimes. (anyone mutual divisors)
        e = randint(2, phi)

    d = euclides_extends(e, phi)  # modular inverse

    print(f'Public Key: ({n},{e})\nPrivate Key: ({n},{d})')

    return p, q, n, phi, e, d


def mutual_primes(n1, n2):
    for i in range(2, n1):
        if n1 % i == 0 and n2 % i == 0:
            return False
    return True


def euclides_extends(e, phi):
    """
    Searching the modular inverse.
    """
    i = 1
    while i < phi:
        if (e*i) % phi == 1:
            return i
        else:
            i += 1


def encryption(n, e, word):
    encrypton = ''

    for letter in word:
        v = ord(letter)**e % n
        encrypton += str(v)
        encrypton += ' '

    return encrypton


def decryption(n, d, word):
    word = word.split(' ')

    descryption = ''

    for letter in range(len(word)):
        try:
            m = int(word[letter])
            m = m**d % n

            descryption += chr(m)

        except ValueError:
            pass

    return descryption


if __name__ == '__main__':
    print("DIGITE UMA MENSAGEM PARA SER CRIPTOGRAFADA: ")
    message = input()

    primes = primes_generator(100)

    p, q, n, phi, e, d = keys(primes)
    print(f"Números primos gerados: {p} e {q}")
    print(f"Produto dos números primos: {n}")
    print(f"Resultado da função totiente: {phi}")
    print(f"Número aleatório entre 2 e phi: {e}")
    print(f"Modular inverso de e no campo finito de phi: {d}")
    print()

    encrypted_message = encryption(n, e, message)
    print(f'ENCRYPTED MESSAGE: "{encrypted_message}"')

    original_message = decryption(n, d, str(encrypted_message))
    print(f'ORIGINAL MESSAGE: "{original_message}"')