from Simu.interfaces.Router import Router
from Simu.interfaces.Node import Node

class EpidemicImp(Router):
    def __init__(self):
        # Ensemble des bundles (messages) que ce routeur/nœud possède
        # En Epidemic routing, chaque nœud maintient une copie des bundles qu'il a reçus
        self.bundles = set()  # Utilise un set pour éviter les doublons

    def routing(self, nodeInRange: list[Node]) -> list[Node]:
        # En Epidemic routing, on diffuse à tous les nœuds en portée
        # Car c'est une diffusion massive : chaque rencontre permet un échange potentiel
        return nodeInRange

    # def add_bundle(self, bundle_id: str):
    #     # Ajoute un bundle à ce nœud (simule la réception d'un message)
    #     self.bundles.add(bundle_id)

    # def get_bundles(self) -> set:
    #     # Retourne les bundles que ce nœud possède
    #     return self.bundles.copy()

    # def exchange_bundles(self, other_router: 'EpidemicImp'):
    #     # Simule l'échange Epidemic : on copie les bundles que l'autre n'a pas
    #     # C'est le cœur de l'algorithme : à chaque rencontre, échange des bundles non vus
    #     new_for_me = other_router.bundles - self.bundles
    #     new_for_other = self.bundles - other_router.bundles
        
    #     self.bundles.update(new_for_me)
    #     other_router.bundles.update(new_for_other)

    def __str__(self) -> str:
        return f"Epidemic Router with {len(self.bundles)} bundles"