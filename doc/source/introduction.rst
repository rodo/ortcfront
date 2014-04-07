============
Introduction
============

Éléments
--------

On retrouve les notions suivantes dans osmrtcheck

- utilisateur
- alerte
- domaine
- événements
- notifications
- validation
- zone de couverture
- règles de conformités


.. graphviz::

   digraph foo {
   "rules 1" -> "domaine";
   "rules 2" -> "domaine";
   "geo zone" -> "domaine";

   "domaine" -> "alerte";
   "utilisateur" -> "validation" -> "alerte";
   "alerte" -> "utilisateur" [color="blue"];
   }


Événements
----------

Un événement peut être de trois types différents, ``création``,
``modification`` et ``suppression``.

Alerte
------

Une alerte se déclenche suite à un ``événement`` qui se produit dans
une zone donnée, elle provoque l'envoi de message sur le Une alerte
est associée à un utilisateur, pour un évènement donné sur une zone de
couverture donnée.

Zone de couverture
------------------

Une zone de couverture est un objet géométrique de type 

Domaine
-------

Un domaine décrit un ensemble d'object OpenStreetMap répondant à des
règles de sélection. Une règle peut-être du type ``key=*``,
``key=value`` ou répondre à une expression régulière du type
``^value$`` et s'appliquer aux clés présentes sur un object. Chacune
des règles peut être affinée par le type d'object sur lequel elle
s'applique, ``node``, ``way``, ``relation``.

Utilisateur
-----------

Un utilisateur se définit par un identifiant, un mot de passe et une
adresse email. Optionnellement un utilisateur peut indiquer son
identifiant OpenStreetMap.

Validation
----------

Une validation est effectuée par un utilisateur sur un évènement.
