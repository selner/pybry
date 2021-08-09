from sqlalchemy import BigInteger

class SLBigInteger(BigInteger):
    pass
from sqlalchemy.ext.compiler import compiles


@compiles(SLBigInteger, 'sqlite')
def bi_c(element, compiler, **kw):
    return "INTEGER"

@compiles(SLBigInteger)
def bi_c(element, compiler, **kw):
    return compiler.visit_BIGINT(element, **kw)

