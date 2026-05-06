from Simu.interfaces.Router import Router
from Simu.interfaces.Node import Node


class ProphetImpl(Router):
    
    P_INIT = 0.75
    GAMMA = 0.98
    BETA = 0.25

    def __init__(self):
        self.proba = {}       # node_id -> {dest_id: prob}
        self.last_tick = {}   # node_id -> dernier tick

    def _init(self, node_id: int, tick: int):
        if node_id not in self.proba:
            self.proba[node_id] = {node_id: 1.0}
            self.last_tick[node_id] = tick

    def _age(self, node_id: int, tick: int):
        delta = tick - self.last_tick.get(node_id, tick)
        if delta <= 0:
            return

        factor = self.GAMMA ** delta
        for d in list(self.proba[node_id]):        # list() pour éviter erreur si modification
            if d != node_id:
                self.proba[node_id][d] *= factor

        self.last_tick[node_id] = tick

    def update_on_encounter(self, node_c: Node, node_n: Node, tick: int):
        """À appeler quand deux nœuds se rencontrent"""
        c, n = node_c.id, node_n.id
        
        self._init(c, tick)
        self._init(n, tick)
        self._age(c, tick)
        self._age(n, tick)

        # Mise à jour directe
        for src, dst in [(c, n), (n, c)]:
            p = self.proba[src].get(dst, 0.0)
            self.proba[src][dst] = min(p + (1 - p) * self.P_INIT, 0.99)

        # Mise à jour transitive
        for src, via in [(c, n), (n, c)]:
            p_src_via = self.proba[src][via]
            for dest, p_via_dest in list(self.proba[via].items()):
                if dest == src or dest == via:
                    continue
                p = self.proba[src].get(dest, 0.0)
                new_p = p + (1 - p) * p_src_via * p_via_dest * self.BETA
                self.proba[src][dest] = max(p, new_p)

    def routing_with_dest(self, nodeInRange: list[Node], destination: Node, 
                          current: Node, current_tick: int) -> list[Node]:
        
        c = current.id
        d = destination.id

        self._init(c, current_tick)
        self._age(c, current_tick)

        p_curr = self.proba[c].get(d, 0.0)

        return [
            n for n in nodeInRange
            if n.id == d or self.proba.get(n.id, {}).get(d, 0.0) > p_curr
        ]

    def routing(self, nodeInRange: list[Node]) -> list[Node]:
        return nodeInRange

    def __str__(self):
        return "Prophet"