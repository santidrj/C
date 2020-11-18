from copy import copy

from Crypto.Util import number


def perfect_square(n):
    for value in range(9, 0, -1):
        if value ** 2 <= n:
            return value

    return 0


def next_digit(divisor, remainder):
    for value in range(9, 0, -1):
        product = (divisor * 10 + value) * value
        if product <= remainder:
            return value, product
    return 0, 0


def make_pairs(n):
    pairs = list()
    aux = n

    while aux > 0:
        pairs.insert(0, aux % 100)
        aux //= 100

    return pairs


def sqrt_long_division(n):
    if type(n) != int:
        raise ValueError(f'The number must be an integer: {n} is a {type(n)}')

    if n == 0:
        return 0
    if n < 0:
        raise ValueError(f'The number cannot be negative')

    pairs = make_pairs(n)
    result = perfect_square(pairs[0])
    divisor = copy(result)
    remainder = pairs[0] - divisor * divisor
    divisor *= 2

    for index in range(1, len(pairs)):
        remainder = remainder * 100 + pairs[index]
        digit, product = next_digit(divisor, remainder)
        result = result * 10 + digit
        divisor = divisor * 10 + digit * 2
        remainder -= product

    if remainder != 0:
        raise ValueError("The square root is not exact")

    return result


if __name__ == '__main__':
    x_sqr = 1522756
    x = sqrt_long_division(x_sqr)
    assert x ** 2 == x_sqr

    x_sqr = 163558521
    x = sqrt_long_division(x_sqr)
    assert x ** 2 == x_sqr

    x_sqr = 4
    x = sqrt_long_division(x_sqr)
    assert x ** 2 == x_sqr

    x_sqr = 0
    x = sqrt_long_division(x_sqr)
    assert x ** 2 == x_sqr

    x_sqr = 1522756
    x = sqrt_long_division(x_sqr)
    assert x ** 2 == x_sqr

    prime = number.getPrime(1024)
    x_sqr = prime * prime
    x = sqrt_long_division(x_sqr)
    assert x == prime

    x_sqr = 21456295454224840274800919448197726401783634894436945581822073662247181853262231931290502792597837766578009014102146097771919066828946252947733232109804901114348844766936001414294479408196377091784252787765313525558315558284702964019849163791893592212121569164574455714835491874342963969985365290824518130803452151059239955337116624452074580346902970934502747544491324033302052352458619938047020445739790228740775356023855903297351466164453246061599108454394116674778209239498227517687352295936184281679589697322925314830808440448027187667911001787040625129020193955182923696995753986854040516541661268164902293504
    x = sqrt_long_division(x_sqr)
    assert x ** 2 == x_sqr

    print(x)
