# DictéePS — concurrence sur le Play Store

Étude du 14/11/2026, à revérifier avant publication.

| Appli | Prix / modèle | Comment ça marche | Ses manques |
|---|---|---|---|
| Gboard / clavier Samsung (dictée) | gratuit, intégré | micro du clavier, Google | pas Whisper, ponctuation moyenne, hors ligne inégal |
| Wispr Flow | gratuit limité, puis **≈ 15 $/mois** (abonnement) | bulle au-dessus du clavier, **dans le cloud** | abonnement, la voix part sur leurs serveurs |
| FUTO Voice Input | gratuit + achat facultatif (≈ 1500 ¥) | Whisper **hors ligne** | ne marche qu'avec les claviers compatibles (pas le micro de Gboard/Samsung), développement passé sur FUTO Keyboard |
| Dictate Keyboard | ≈ 3,49 $ + **clé OpenAI payée à l'usage** | clavier complet, bouton flottant (v4.2), cloud | faut une clé API, voix envoyée à OpenAI |
| Voxscribe | gratuit (F-Droid seulement) | clavier Whisper hors ligne | il faut fournir son modèle, pas sur le Play Store |
| Google AI Edge Eloquent | gratuit | dictée IA hors ligne | iPhone seulement pour l'instant (Android annoncé : à surveiller) |

**Ce qui nous démarque** : Whisper 100 % sur le téléphone, sans compte, sans clé, sans abonnement ;
bulle par-dessus **n'importe quel clavier** (on garde son clavier) ; texte écrit **en direct** dans le champ ;
longs messages (3 min) ; sans champ → presse-papiers. **Modèle visé : achat unique.**

**À ajouter / points faibles** : français seulement pour l'instant (`Moteur.transcribe(..., "fr", ...)`) →
choix de la langue ; modèle de 264 Mo à télécharger ; règle Google sur l'accessibilité (déclaration + vidéo,
risque de refus → plan B clavier) ; Yaps présente « bulle + accessibilité » comme un défaut → bien expliquer
pourquoi (garder son clavier) et que rien ne sort du téléphone.
