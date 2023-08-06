from .boss import package_boss as pb, boss as b

def main(q):
    _b = b(q)
    _b.listen()

def boss():
    return pb(main)

__all__ = [boss]