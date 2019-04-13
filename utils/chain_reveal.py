from collections import deque


def chain_reveal(tiles, tile):
    """Reveal all "0" tiles directly touching this one. Uses BFS."""
    revealed = 0
    touching = ((0, 1), (1, 0), (0, -1), (-1, 0))
    S = deque()
    S.append(tile)
    discovered = set([(tile.x, tile.y)])
    tile.reveal()
    while len(S) > 0:
        v = S.popleft()
        if v.type != "0":
            continue
        v.reveal()
        revealed += 1
        for x, y in touching:
            if x + v.x < 0 or y + v.y < 0:
                continue
            try:
                tile = tiles[x + v.x][y + v.y]
            except IndexError:
                continue
            if (x + v.x, y + v.y) not in discovered:
                discovered.add((x + v.x, y + v.y))
                S.append(tile)
    return revealed or 1
