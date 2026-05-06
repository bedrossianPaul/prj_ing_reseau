from Simu.interfaces.Router import Router
from Simu.interfaces.Node import Node

class SprayAndWaitImp(Router):
    def __init__(self, L: int = 6):
        self.L = L
        self.bundles = {}  # bundle_id -> copies restantes

    def routing(self, nodeInRange: list[Node]) -> list[Node]:
        """
        Implémentation simplifiée de Spray and Wait directement dans routing.

        - Phase Spray : si un bundle a encore plus d'une copie, on peut diffuser à tous les nœuds en portée.
        - Phase Wait : si tous les bundles sont à leur dernière copie, on n'envoie pas aux nœuds non destinataires.
        """
        if self.L > 1:
            self.L -= 1  # Réduire le nombre de copies restantes pour chaque bundle
            return nodeInRange
        return []

    def __str__(self) -> str:
        bundle_count = len(self.bundles)
        return (
            f"SprayAndWaitImp(router_type='SprayAndWait', "
            f"bundles={bundle_count}, L={self.L})"
        )
    def routing_with_dest(self, nodeInRange: list[Node], dest: Node) -> list[Node]:
        """
        Version de routing qui prend en compte la destination.
        - Phase Spray : si un bundle a encore plus d'une copie, on peut diffuser à tous les nœuds en portée.
        - Phase Wait : si tous les bundles sont à leur dernière copie, on n'envoie pas aux nœuds non destinataires.
        """
        if self.L > 1:
            self.L -= 1  # Réduire le nombre de copies restantes pour chaque bundle
            return nodeInRange
        else:
            self.L -= 1  # il ne restera plus de copies comme on a déjà croisé le destinataire
            return [node for node in nodeInRange if node.get_id() == dest.get_id()]