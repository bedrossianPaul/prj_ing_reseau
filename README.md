# Résilience d’un essaim de nano-satellites

## Sujet

La transmission des données dans un essaim de nano-satellites est fondée sur un **routage opportuniste**.  
Les protocoles proposés dans la littérature visent à optimiser le taux de délivrance de paquets et à minimiser le temps de latence.

Les traces de mobilité de l’essaim de nano-satellites sont disponibles sur **Moodle**.

---

## Hypothèses et problème posé

- Les nano-satellites peuvent adapter leur débit pour transmettre avec plusieurs niveaux de portée :
  - 20 km  
  - 40 km  
  - 60 km
- Les données générées par chaque satellite doivent être transmises à **tous les autres membres de l’essaim**.
- L’objectif du projet est d’étudier l’impact d’une **panne** :
  - prévisible (ex. décharge de batterie),
  - non prévisible,
  
  sur les **caractéristiques structurelles de l’essaim**, notamment :
  - le degré des nœuds,
  - la longueur des plus courts chemins (temporels).
- Le projet est structuré en deux phases :
  1. Étude des caractéristiques du réseau sur toute la durée d’observation (sans panne).
  2. Étude de l’impact de la suppression d’un ou plusieurs nœuds sur les performances de l’essaim.
- Le choix des algorithmes et des outils est libre.

---

## Étapes du projet

1. Mise en place d’un **algorithme de routage opportuniste** (algorithme de référence).
2. Parsing des traces de mobilité et **modélisation des déplacements** des nano-satellites.
3. **Test de validation** : vérification que les données de chaque nano-satellite sont présentes sur l’ensemble des nano-satellites.
4. Analyse des métriques du réseau.
5. Étude de l’évolution de ces métriques selon différents paramètres.
6. Conclusion et discussion sur la résilience de l’essaim.

---

## Métriques à analyser

### Métriques topologiques et temporelles
- Degré des nœuds.
- Stabilité des liens :
  - durée moyenne des contacts,
  - distribution des durées de contact,
  - fréquence des contacts par paire de satellites.
- Connexité du réseau.
- Densité du graphe.
- Longueur moyenne des plus courts chemins temporels.
- Distribution des longueurs des chemins temporels.
- Diamètre temporel du réseau.

### Métriques fonctionnelles
- Taux de réussite du test de validation (diffusion complète des données).
- Pourcentage moyen de batterie restante :
  - définition d’une règle d’usage de la batterie en fonction :
    - de la puissance d’émission,
    - du nombre de contacts.

---

## Paramètres d’analyse

Les métriques sont analysées en fonction :
- du temps,
- de la portée des communications,
- des pannes (prévisibles et non prévisibles).

---

## Modèle proposé

### Entrées
- (Optionnel) Trame de panne :  
  `(début, fin, nano-satellite concerné)`
- Traces de déplacements des nano-satellites (données Moodle).
- Distance maximale d’émission (par nano-satellite).

### Traitement
- Pour chaque pas de temps :
  - calcul des liens de communication,
  - application du routage opportuniste,
  - calcul de l’ensemble des métriques.

### Sortie
- Structure de type :
  ```text
  [temps → [métriques]]