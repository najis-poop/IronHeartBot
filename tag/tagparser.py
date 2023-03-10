import enum
from lark import Lark, Transformer, Token

tagparser = Lark(open("tag/grammar.lark"))

def _parseout(text: str):
    print(tagparser.parse(text).pretty())

class TagNode(enum.Enum):
    LITERAL = 0
    BINOP = 1
    UNARY = 2
    REFVAR = 3
    DECLVAR = 4
    ASSIGN = 5
    FNCALL = 6
    
    DOSTMT = 7
    IFSTMT = 8
    RETSTMT = 9
    FORLOOP = 10

class TagAST(Transformer):
    
    def NAME(self, t: Token):
        return str(t)
    
    def start(self, t: list[dict]):
        return t[0]
    
    def integer(self, t: tuple[Token]):
        (v,) = t
        return {
            "type": TagNode.LITERAL,
            "value": int(v)
        }
    
    def real(self, t: list[Token]):
        (v,) = t
        return {
            "type": TagNode.LITERAL,
            "value": float(v)
        }
    
    def string(self, t: list[Token]):
        v = t[0][1:-1]
        
        nv = ''
        i = 0
        while True:
            if i >= len(v):
                break
            c = v[i]
            if c == '\\':
                i += 1
                c = v[i]
                match c:
                    case 'n':
                        nv += '\n'
                    case 't':
                        nv += '\t'
                    case 'r':
                        nv += '\r'
                    case _:
                        nv += c
                i += 1
                continue
            nv += c
            i += 1
        
        return {
            "type": TagNode.LITERAL,
            "value": nv
        }
    
    def binop(self, t: tuple[dict, Token, dict | str]):
        l, o, r = t
        return {
            "type": TagNode.BINOP,
            "left": l,
            "right": r,
            "op": str(o)
        }
    
    def unary(self, t: tuple[Token, dict]):
        o, l = t
        return {
            "type": TagNode.UNARY,
            "op": str(o),
            "value": l
        }
    
    def refvar(self, t: tuple[Token]):
        (n,) = t
        return {
            "type": TagNode.REFVAR,
            "name": n
        }
    
    def declvar(self, t: list[Token]):
        return {
            "type": TagNode.DECLVAR,
            "names": t
        }
    
    def assign(self, t: tuple[dict, dict]):
        (n, v) = t
        return {
            "type": TagNode.ASSIGN,
            "target": n,
            "value": v
        }
    
    def fncall(self, t: list[dict]):
        c, *a = t
        if None in a:
            a = []
        return {
            "type": TagNode.FNCALL,
            "caller": c,
            "args": a
        }
    
    def dostmt(self, t: list[dict]):
        return {
            "type": TagNode.DOSTMT,
            "block": t
        }
    
    def ifstmt(self, t: tuple[dict, dict, dict | None]):
        c, b, e = t
        return {
            "type": TagNode.IFSTMT,
            "condition": c,
            "body": b,
            "else": e
        }
    
    def retstmt(self, t: tuple[dict | None]):
        return {
            "type": TagNode.RETSTMT,
            "value": t[0]
        }
    
    def forloop(self, t: tuple[str, dict, dict]):
        return {
            "type": TagNode.FORLOOP,
            "name": t[0],
            "value": t[1],
            "body": t[2]
        }

tagtransformer = TagAST()

def tagparse(text: str):
    return tagtransformer.transform(tagparser.parse(text))