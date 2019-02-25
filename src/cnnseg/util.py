# -*- coding: utf-8 -*-


def Traverse(nd, row, col):
    append_rc = []
    while nd.traversed[row, col] == 0:
        append_rc.append([row, col])
        nd.traversed[row, col] = 2
        idx = nd.center_node[:, row, col]
        row = idx[0]
        col = idx[1]
    if nd.traversed[row, col] == 2:
        for uc in append_rc[::-1]:
            if uc[0] != row or uc[1] != col:
                nd.is_center[uc[0], uc[1]] = True
        nd.is_center[row, col] = True
    for qq in append_rc:
        nd.traversed[qq[0], qq[1]] = 1
        nd.parent[0, qq[0], qq[1]] = row
        nd.parent[1, qq[0], qq[1]] = col


def SetUnion(nd, row, col, row2, col2):
    r1, c1 = SetFind(nd, row, col)
    r2, c2 = SetFind(nd, row2, col2)
    if r1 == r2 and c1 == c2:
        return
    if nd.node_rank[r1, c1] < nd.node_rank[r2, c2]:
        nd.parent[0, r1, c1] = r2
        nd.parent[1, r1, c1] = c2
    elif nd.node_rank[r1, c1] > nd.node_rank[r2, c2]:
        nd.parent[0, r2, c2] = r1
        nd.parent[1, r2, c2] = c1
    else:
        nd.parent[0, r2, c2] = r1
        nd.parent[1, r2, c2] = c1
        nd.node_rank[r1, c1] += 1


def SetFind(nd, row, col):
    row2 = nd.parent[0, row, col]
    col2 = nd.parent[1, row, col]
    if (row2 == row and col == col2) or \
            (row2 == nd.parent[0, row2, col2] and col2 == nd.parent[1, row2, col2]):
        return row2, col2
    r_row, r_col = SetFindRecursive(nd, nd.parent[0, row2, col2], nd.parent[1, row2, col2])
    nd.parent[0, row, col] = r_row
    nd.parent[1, row, col] = r_col
    nd.parent[0, row2, col2] = r_row
    nd.parent[1, row2, col2] = r_col
    return r_row, r_col


def SetFindRecursive(nd, row, col):
    if nd.parent[0, row, col] != row or nd.parent[1, row, col] != col:
        nd.parent[0, row, col], nd.parent[1, row, col] \
            = SetFindRecursive(nd, nd.parent[0, row, col], nd.parent[1, row, col])
    return nd.parent[0, row, col], nd.parent[1, row, col]
