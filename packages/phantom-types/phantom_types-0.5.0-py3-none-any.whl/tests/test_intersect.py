from phantom import Phantom
from phantom.predicates import boolean


class P:
    ...


class Q:
    ...


class R(P, Q):
    ...


class A(P, Phantom, predicate=boolean.true):
    ...


class B(Q, Phantom, predicate=boolean.true):
    ...


class C(A, B):
    ...


print(C.__predicate__)
print(C.__bound__)
