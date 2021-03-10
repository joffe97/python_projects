from grafer.graf_naboliste import GrafNaboliste


def bygg_emnegraf():
    grafen = GrafNaboliste()
    ing100 = grafen.add_node("ING100")       # 0
    dat110 = grafen.add_node("DAT110")       # 1
    dat200 = grafen.add_node("DAT200")       # 2
    dat250 = grafen.add_node("DAT250")       # 3
    dat320 = grafen.add_node("DAT320")       # 4
    dat310 = grafen.add_node("DAT310")       # 5
    dat230 = grafen.add_node("DAT230")       # 6
    dat300 = grafen.add_node("DAT300")       # 7
    dat220 = grafen.add_node("DAT220")       # 8
    dat240 = grafen.add_node("DAT240")       # 9
    mat100 = grafen.add_node("MAT100")       # 10
    sta100 = grafen.add_node("STA100")       # 11
    mat200 = grafen.add_node("MAT200")       # 12
    fys100 = grafen.add_node("FYS100")       # 13
    grafen.add_edge(ing100, dat110, 1)
    grafen.add_edge(dat110, dat200, 1)
    grafen.add_edge(dat200, dat220, 1)
    grafen.add_edge(dat110, dat250, 1)
    grafen.add_edge(dat110, dat320, 1)
    grafen.add_edge(dat110, dat310, 1)
    grafen.add_edge(dat220, dat240, 1)
    grafen.add_edge(dat310, dat240, 1)
    grafen.add_edge(dat230, dat300, 1)
    grafen.add_edge(mat100, sta100, 1)
    grafen.add_edge(mat100, mat200, 1)
    return grafen
