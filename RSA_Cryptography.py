from random import sample, randint


def primes_generator(n):
    """Function to find all prime number until 'n'"""
    primes = []

    for i in range(2, n):
        if i % 2 == 0 and len(primes) > 0:
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
    p = sample(primes_list, 1)  # First prime number
    q = sample(primes_list, 1)  # Second prime number

    while p == q:  # It's to have sure that p is not equals to q
        q = sample(primes_list, 1)

    p = p[0]  # Random.sample() return a list, we only need the value from the list, so we do that
    q = q[0]

    n = p*q  # Product of p and q
    phi = (p - 1) * (q - 1)  # Numbers of divisors of p and q

    e = randint(2, phi)   # Random number from range 2 and phi

    while not mutual_primes(e, phi):  # phi and 'e' need to be coprimes. (anyone mutual divisors)
        e = randint(2, phi)

    d = euclides_extends(e, phi)  # modular inverse

    print(f'Public Key ({n},{e})\nPrivate Key: ({p},{q},{d})')

    return p, q, n, phi, e, d


def mutual_primes(n1, n2):
    """
    Function to discover if n1 and n2 is coprimes.

    :return: True if they are coprimes, False if not.
    """
    if n2 < n1:
        n1, n2 = n2, n1

    divisors_n1 = []

    for i in range(2, n1):
        if n1 % i == 0:
            divisors_n1.append(i)

    for i in range(2, n2):
        if n2 % i == 0:
            if i in divisors_n1:
                return False

    return True


def euclides_extends(e, phi):
    """
    Searching the modular inverse.
    """
    i = 1
    while True:
        if e*i % phi == 1:
            return i
        else:
            i += 1


def encryption(n, e, word):
    """
    Using the key to encrypt a message
    :param n: product of the prime numbers
    :param e: a random number
    :param word: the message
    :return: encrypted message
    """
    letters = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10,
               'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19,
               'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26, '1': 27, '2': 28,
               '3': 29, '4': 30, '5': 31, '6': 32, '7': 33, '8': 34, '9:': 35, '0': 36, '!': 37,
               '@': 38, '#': 39, '$': 40, '%': 41, '¨': 42, '&': 43, '*': 44, '(': 45, ')': 46,
               '[': 47, ']': 48, '|': 49, '+': 50, '-': 51, '/': 52, '\\': 53, '_': 54, ':': 55,
               '=': 56}

    encrypton = ''
    word = word.upper()

    for letter in word:
        v = letters[letter]**e % n
        encrypton += str(v)
        encrypton += ' '

    return encrypton


def decryption(n, d, word):
    """
    receives a encrypted message and return the message.
    :param n: product of the prime numbers
    :param d: inverse modular number
    :param word: encrypted message
    :return: original message
    """
    descryption = ''

    letters = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I', 10: 'J',
               11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P', 17: 'Q', 18: 'R', 19: 'S',
               20: 'T', 21: 'U', 22: 'V', 23: 'W', 24: 'X', 25: 'Y', 26: 'Z', 27: '1', 28: '2',
               29: '3', 30: '4', 31: '5', 32: '6', 33: '7', 34: '8', 35: '9', 36: '0', 37: '!',
               38: '@', 39: '#', 40: '$', 41: '%', 42: '¨', 43: '&', 44: '*', 45: '(', 46: ')',
               47: '[', 48: ']', 49: '|', 50: '+', 51: '-', 52: '/', 53: '\\', 54: '_', 55: ':',
               56: '='}

    word = str(word).split(' ')
    word.pop()

    for letter in word:
        m = int(letter)**d % n
        descryption += letters[m]

    return descryption


if __name__ == '__main__':
    primes = primes_generator(500)

    p, q, n, phi, e, d = keys(primes)

    print()
    encrypted_message = encryption(n, e, '1J5A@#$I412JR_+=QAWIE')
    print(f'ENCRYPTED MESSAGE: "{encrypted_message}"')

    original_message = decryption(n, d, str(encrypted_message))
    print(f'ORIGINAL MESSAGE: "{original_message}"')
