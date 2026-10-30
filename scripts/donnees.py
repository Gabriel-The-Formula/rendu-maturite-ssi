"""Source unique des analyses MEDICA-SERVICES.

Toutes les notes, niveaux, scores et montants du rapport, du guide, de la
présentation CODIR et de la grille Excel proviennent de ce fichier. Modifier
une valeur ici puis lancer `python3 scripts/generer.py` met à jour l'ensemble.
"""

# ---------------------------------------------------------------------------
# G2 · Autodiagnostic DCSSI (Q01 à Q12)
# ---------------------------------------------------------------------------
# (id, intitulé de la grille, note 0-3, références, justification, confiance)
QUESTIONS = [
    ("Q01", "Adhérence du SI aux missions", 3, "P01, P03, P04",
     "MEDICA-SERVICES vend l'hébergement et l'exploitation d'applications pour 12 établissements de soins (P01). "
     "Sans SI il n'existe plus de prestation et les clients reviennent au papier (P04). Le SI est vital aux missions.",
     "Confirmé"),
    ("Q02", "Impacts internes", 2, "P01, P04",
     "La DG prévoit de fortes pertes contractuelles après une journée d'arrêt et le départ de certains clients si l'arrêt se prolonge (P04). "
     "Elle estime pouvoir poursuivre des prestations manuelles, ce qui écarte une conséquence fatale démontrée.",
     "Probable"),
    ("Q03", "Impacts externes", 3, "P04, P05",
     "Les établissements clients basculent sur papier (P04) et une altération non détectée peut provoquer des erreurs d'orientation et de prise en charge de patients (P05). "
     "La sécurité de personnes chez des tiers est en jeu. Note fondée sur des déclarations, sans étude d'impact chiffrée.",
     "Probable"),
    ("Q04", "Disponibilité", 2, "P01, P04, P05",
     "Une journée d'arrêt du portail est grave (pertes contractuelles, P04) et un arrêt prolongé affecte fortement la continuité des soins (P05). "
     "La DG décrit une activité dégradée et non un arrêt définitif, d'où 2 et non 3. Reprise contractuelle sous 8 h (P01).",
     "Probable"),
    ("Q05", "Intégrité", 2, "P05",
     "Les environnements contiennent des identifiants patients et des informations de santé. Une altération non détectée peut provoquer des erreurs d'orientation et de prise en charge (P05). "
     "L'impact est grave pour l'activité. Aucune pièce ne le décrit comme fatal pour l'entreprise, d'où 2 par cohérence avec Q02 et Q04.",
     "Probable"),
    ("Q06", "Confidentialité", 3, "P05, P07",
     "Identifiants patients et données de santé (P05). La DSI qualifie la divulgation de risque critique et les attaquants visés cherchent la revente de données et l'extorsion (P07).",
     "Probable"),
    ("Q07", "Fréquence des sinistres", 2, "P06",
     "Dix événements SSI enregistrés en 12 mois, soit environ 2,5 par trimestre (P06). Le registre n'étant ni exhaustif ni revu, la fréquence réelle peut être supérieure.",
     "Probable"),
    ("Q08", "Motivation des attaquants", 2, "P07",
     "Menaces ciblées jugées plausibles et potentiellement fortement motivées par la revente de données et l'extorsion (P07). Aucune pièce ne justifie le niveau très important.",
     "Probable"),
    ("Q09", "Moyens des attaquants", 2, "P07",
     "P07 écarte les moyens illimités. Une cybercriminalité d'extorsion dispose plausiblement de moyens importants. "
     "Hypothèse d'auditeur sans effet sur le maximum du groupe, déjà fixé à 2 par Q07 et Q08.",
     "Incertain"),
    ("Q10", "Hétérogénéité du SI", 2, "P08, T01",
     "Windows, Linux, hyperviseurs, réseau multi-constructeurs, SaaS et application propriétaire héritée. "
     "P08 qualifie l'architecture de fortement hétérogène mais non extrêmement hétérogène.",
     "Confirmé"),
    ("Q11", "Ouverture du SI", 2, "P03, P07, T01, T02",
     "Interconnexions clients encadrées par contrat (P07). Le portail est ouvert à des internautes non maîtrisés, mais par une publication unique filtrée (FW-01, FW-08) et un reverse proxy en DMZ (P03, T01, T02). Ouverture externe jugée sous contrôle. "
     "La note 3 serait défendable si l'on considère que l'accès public au portail échappe au contrôle de l'organisme. La somme passerait alors à 11 et la cible à 5.",
     "Probable"),
    ("Q12", "Variabilité du SI", 2, "P06, P08",
     "Changements applicatifs mensuels et d'infrastructure trimestriels (P08), deux indisponibilités dues à des changements (P06). "
     "Le SI change relativement souvent.",
     "Confirmé"),
]

AJUSTEMENT = 0  # B22, discuté dans le rapport (section G2)

GROUPES = [
    ("Conséquences", "Q01 à Q03", (0, 3)),
    ("Sensibilité", "Q04 à Q06", (3, 6)),
    ("Exposition aux menaces", "Q07 à Q09", (6, 9)),
    ("Importance des vulnérabilités", "Q10 à Q12", (9, 12)),
]


def niveau_adequat(somme):
    if somme <= 2:
        return 1
    if somme <= 5:
        return 2
    if somme <= 8:
        return 3
    if somme <= 10:
        return 4
    return 5


def calcul_cible():
    notes = [q[2] for q in QUESTIONS]
    maxima = [max(notes[a:b]) for _, _, (a, b) in GROUPES]
    somme = sum(maxima)
    niveau = niveau_adequat(somme)
    cible = max(1, min(5, niveau + AJUSTEMENT))
    return maxima, somme, niveau, cible


# ---------------------------------------------------------------------------
# G3 · Maturité effective des sept processus
# ---------------------------------------------------------------------------
# effectif : plus haut niveau entièrement démontré
# suivant : statut du niveau supérieur ("non atteint" ou "indéterminé")
PROCESSUS = [
    dict(nom="Définir la stratégie SSI", court="Stratégie", revendique="Non déclaré", effectif=1,
         preuves="P09, P02, P17",
         reserve="Niveau 1 étayé par la note d'orientation 2024 approuvée par la DG, des priorités annuelles et un référent (P09). "
                 "Niveau 2 indéterminé car aucune mesure qualitative n'est documentée et le compte rendu semestriel reste oral, sans trace écrite fournie. "
                 "Niveau 3 non atteint, faute de processus commun documenté (P09). Revue annuelle de la PSSI sans PV depuis deux ans (P17).",
         suivant="N2 indéterminé (mesures qualitatives et traces de compte rendu absentes)",
         progression="Tableau de bord qualitatif semestriel et comptes rendus écrits validés par la DG, intégrés au lot A01 (pilote RSSI). Preuve : deux PV de revue datés."),
    dict(nom="Gérer les risques SSI", court="Risques", revendique="Non déclaré", effectif=1,
         preuves="P10, P06",
         reserve="Risques recensés ponctuellement lors de projets récents, avec des mesures décidées (P10). "
                 "Niveau 2 non atteint : ni calendrier de revue, ni méthode réutilisable, ni registre consolidé approuvé. L'analyse du prestataire de 2025 reste isolée.",
         suivant="N2 non atteint (pas de planification ni de méthode)",
         progression="Méthode simple, registre consolidé et revue trimestrielle (A01). Preuve : registre approuvé par la DG et PV de revue."),
    dict(nom="Gérer les règles SSI", court="Règles", revendique="Non déclaré", effectif=2,
         preuves="P11, P17, T06",
         reserve="Niveau 2 étayé par une PSSI approuvée, des règles écrites, une application planifiée, des contrôles qualitatifs consignés et l'information des managers (P11). "
                 "Niveau 3 non atteint, les textes ne forment pas un processus commun. Fragilités : revue annuelle sans PV (P17) et aucune cible de délai de correctifs (T06).",
         suivant="N3 non atteint (pas de processus standardisé)",
         progression="PSSI révisée avec délais de correctifs par criticité, diffusée à tout le périmètre (A03). Preuve : PSSI v2 approuvée, PV de revue, taux de sensibilisation."),
    dict(nom="Superviser la SSI", court="Supervision", revendique="Non déclaré", effectif=1,
         preuves="P12, P06, T08",
         reserve="Outil de journalisation et alertes actifs, interventions à la demande (P12), d'où le niveau 1. "
                 "Niveau 2 non atteint : aucune campagne de contrôle planifiée, aucun reporting régulier ni procédure commune (P12). AL-1048 fermée automatiquement sans ticket (T08).",
         suivant="N2 non atteint (contrôles non planifiés, pas de reporting)",
         progression="Plan de contrôle annuel, procédure de traitement des alertes et reporting mensuel (A02). Preuve : échantillon de tickets d'alerte qualifiés et rapports mensuels."),
    dict(nom="Concevoir les mesures SSI", court="Conception", revendique="Non déclaré", effectif=2,
         preuves="P13, T02",
         reserve="Besoins identifiés sur certains projets, fiche type, responsable technique désigné, revues planifiées pour les projets majeurs avec compte rendu écrit remonté au responsable (P13). "
                 "Le compte rendu écrit des revues est retenu comme mesure qualitative. La compétence est retenue, comme pour les autres processus, sur la base d'un rôle désigné chargé de la sécurité, à confirmer en entretien. Niveau 3 non atteint, la démarche n'est pas globale. La règle provisoire FW-17 (T02) l'illustre sans le prouver.",
         suivant="N3 non atteint (démarche non uniformisée)",
         progression="Fiche de besoins SSI obligatoire pour tout projet ou changement significatif (préparée en régie, A04 différée). Preuve : fiches sur un échantillon de projets."),
    dict(nom="Réaliser les mesures SSI", court="Réalisation", revendique="Non déclaré", effectif=1,
         preuves="P14, T02",
         reserve="Niveau 1 étayé par des déploiements préparés par des techniciens compétents (P14). Comptes rendus d'installation et de validation, suivi régulier et information de la DSI couvrent quatre exigences du niveau 2. "
                 "Niveau 2 indéterminé car la planification n'est pas démontrée, P14 indiquant seulement que les déploiements sont « souvent préparés ». Règles FW-17 et FW-31 sans justification ni validation (T02).",
         suivant="N2 indéterminé (planification non démontrée)",
         progression="Plan de déploiement trimestriel des mesures et modèle commun de recette, en régie (pilote DSI). Preuve : plans datés et PV de recette sur trois déploiements."),
    dict(nom="Exploiter les mesures SSI", court="Exploitation", revendique="Non déclaré", effectif=2,
         preuves="P15, P17, T03, T04, T06, T09",
         reserve="Sauvegardes planifiées, comptes rendus hebdomadaires, astreinte, procédure de restauration connue et bilan qualitatif mensuel à la DSI (P15). "
                 "Niveau 3 non atteint. Fragilités : 2 PV de test sur 9 services (T09), MFA sur 6 comptes privilégiés sur 10 (T04), correctifs en retard sans exception (T06), déclarations de la DG non démontrées et de la DSI contredites (P17).",
         suivant="N3 non atteint (pas de processus commun standardisé)",
         progression="Standardiser restauration, correctifs et revue des comptes (A05, A08, A09). Preuve : PV de restauration avec RTO et RPO mesurés, export MFA, SLA de correctifs."),
]

# ---------------------------------------------------------------------------
# T1 à T5 · Constats techniques (onglet 03)
# ---------------------------------------------------------------------------
CONSTATS = [
    dict(id="C01", pieces="T03/T04", processus="Exploiter les mesures SSI",
         titre="MFA sur 6 comptes privilégiés sur 10",
         observation="10 comptes privilégiés recensés, 6 enrôlés MFA (60 %). Sans MFA : svc-backup, admin-old (Domain Admin, dernière activité documentée 2025-02-14), admin-presta (VPN prestataire) et admin-db.",
         reserve="Fait documenté sur le périmètre de l'export (annuaire et administrateurs VPN). Exhaustivité SaaS non garantie, accès conditionnel et exceptions non fournis. Contredit la déclaration de la DSI (P17).",
         scenario="Prise de contrôle d'un compte privilégié sans second facteur puis modification non autorisée de l'AD (R01).",
         priorite="Élevée : privilèges étendus, accès VPN exposé, signaux T07 sur admin-old.",
         reco="DSI (IAM) : désactiver ou justifier admin-old, MFA pour admin-presta et admin-db, restriction de svc-backup (A08).",
         cloture="Export MFA exhaustif à 100 % ou exceptions approuvées, preuve de restriction de svc-backup, revue des groupes à privilèges.",
         risque="R01", action="A08", pilote="DSI (IAM)", niveau="Exploitation 2, fragile"),
    dict(id="C02", pieces="T02/T01", processus="Concevoir / Réaliser les mesures SSI",
         titre="FW-31 Any des postes vers les sauvegardes",
         observation="La règle FW-31 autorise tout service du VLAN 40 (postes) vers le VLAN 60 (BACKUP01). Règle héritée sans justification.",
         reserve="Configuration extraite sans journaux de trafic. Usage réel inconnu. Aucune exploitation constatée.",
         scenario="Un poste compromis par hameçonnage atteint BACKUP01 et chiffre ou supprime les copies, ce qui empêche la reprise (R02).",
         priorite="Élevée : les sauvegardes sont le dernier recours de reprise et l'hameçonnage est fréquent (P06).",
         reco="DSI réseau : restreindre FW-31 aux flux nécessaires après analyse des journaux, en régie sous un mois.",
         cloture="Règle supprimée ou justifiée et approuvée, journaux de trafic sur 30 jours, test de segmentation.",
         risque="R02", action="Régie (A10 différée)", pilote="DSI réseau", niveau="Conception 2, Réalisation 1"),
    dict(id="C03", pieces="T05/T06", processus="Exploiter les mesures SSI",
         titre="Correctif critique manquant sur APP01",
         observation="APP01 (criticité métier critique) sans correctif critique éditeur (CVSS communiqué 9,8, T05). L'hôte affiche 74 jours de retard de correctifs au 12/10/2026, exception non documentée (T06).",
         reserve="Non exposé directement à Internet et non exploité pendant l'audit. Date de publication du correctif critique, CVE, version et historique de déploiement absents. Retard déclaratif.",
         scenario="Rebond depuis WEB01 (flux WEB01 vers APP01) ou via RDP (FW-17) puis exploitation d'APP01, altération ou fuite de données patients (R03).",
         priorite="Élevée : actif critique joignable depuis la DMZ, aucune exception validée. Le score seul ne fixe pas la priorité.",
         reco="Responsable infrastructures : correctif sous 15 jours ou exception signée avec mesures compensatoires, traité en tête du lot A09.",
         cloture="Scan authentifié après correctif, ticket de changement, version installée.",
         risque="R03", action="A09", pilote="Resp. infrastructures", niveau="Exploitation 2, fragile"),
    dict(id="C04", pieces="T07/T08", processus="Superviser la SSI",
         titre="AL-1048 fermée sans ticket",
         observation="Le 09/10/2026, trois échecs puis un succès VPN pour admin-old depuis 198.51.100.44 (00:13), ajout au groupe Server-Admins (00:18), alerte AL-1048 de sévérité HIGH (00:22) fermée automatiquement après 24 h sans ticket.",
         reserve="Signaux compatibles avec un événement à investiguer, pas une compromission prouvée. Intégrité des journaux, trace MFA et contact du titulaire non fournis. Incohérence avec la dernière activité T03 (2025-02-14).",
         scenario="Usage frauduleux non détecté d'un compte à privilèges et persistance de droits (R01).",
         priorite="Très élevée : privilège Domain Admin, compte sans MFA, aucun examen de l'alerte tracé.",
         reco="RSSI : ouvrir un incident, mesures conservatoires (désactivation d'admin-old, revue de Server-Admins, préservation des journaux), investigation, fin de la fermeture automatique des alertes HIGH (A02).",
         cloture="Ticket d'incident qualifié, rapport d'investigation, membres de Server-Admins avant et après, paramétrage SIEM modifié.",
         risque="R01", action="A02", pilote="RSSI", niveau="Supervision 1"),
    dict(id="C05", pieces="T09", processus="Exploiter les mesures SSI",
         titre="PV de restauration pour 2 services sur 9",
         observation="9 services dans le périmètre, 2 PV de test (MEDI-PORTAL le 15/09, ticketing le 16/09/2026), 7 sans PV. RPO non fourni. Sauvegarde M365 alléguée chez un tiers.",
         reserve="L'absence de PV ne prouve pas l'absence de test. Le contenu des deux PV n'est pas communiqué, le respect du RTO de 8 h n'est donc pas démontré (P01, T09). Déclaration de la DG non démontrée (P17).",
         scenario="Restauration impossible ou trop lente après rançongiciel, dépassement du RTO contractuel (R02).",
         priorite="Élevée : engagement contractuel et continuité des soins (P01, P05).",
         reco="Responsable infrastructures : plan de tests trimestriel couvrant les 9 services (A05).",
         cloture="PV de restauration datés avec durée mesurée et RPO constaté pour chaque service.",
         risque="R02", action="A05", pilote="Resp. infrastructures", niveau="Exploitation 2, fragile"),
    dict(id="C06", pieces="T02/T01", processus="Réaliser les mesures SSI",
         titre="RDP direct FW-17 hors bastion",
         observation="FW-17 autorise RDP (3389/TCP) depuis VPN-ADMIN vers tout le VLAN 20, sans passer par BASTION01. Règle déclarée provisoire.",
         reserve="Durée, utilisateurs et journaux non fournis. Le contournement du bastion est déduit du schéma T01.",
         scenario="Un compte VPN sans MFA (admin-presta) atteint APP01 ou DB01 en RDP sans traçabilité du bastion (R01, R03).",
         priorite="Élevée : accès d'administration direct vers les serveurs critiques.",
         reco="DSI : retirer FW-17 ou lui fixer une date d'expiration, imposer le passage par le bastion.",
         cloture="Règle supprimée, connexions RDP tracées sur BASTION01.",
         risque="R01", action="Régie (A10 différée)", pilote="DSI", niveau="Réalisation 1"),
    dict(id="C07", pieces="T02/T05/T06", processus="Concevoir les mesures SSI",
         titre="SMB large et signature non obligatoire",
         observation="FW-19 ouvre SMB (445/TCP) de tout le VLAN 40 vers le VLAN 30. Signature SMB non obligatoire sur SRV-FICHIERS (CVSS 6,5). Correctifs en retard de 43 jours.",
         reserve="Constat de scanner non validé manuellement. Périmètre « large » sans liste des partages.",
         scenario="Relais d'authentification ou propagation latérale depuis un poste compromis, divulgation de données (R04).",
         priorite="Moyenne à élevée : exposition interne étendue et hameçonnage fréquent.",
         reco="Responsable infrastructures : signature SMB obligatoire, restriction de FW-19 aux groupes métiers (A09).",
         cloture="Stratégie de groupe appliquée, scan de contrôle, matrice des partages.",
         risque="R04", action="A09", pilote="Resp. infrastructures", niveau="Conception 2"),
    dict(id="C08", pieces="T02/T05", processus="Exploiter les mesures SSI",
         titre="WEB01 : port 80 et TLS 1.0 signalés",
         observation="Depuis le point de mesure DMZ, WEB01 répond sur 80/tcp et 443/tcp, 22/tcp filtré. Le scanner signale TLS 1.0 (CVSS 5,3). La redirection HTTP vers HTTPS est déclarée, non vérifiée.",
         reserve="Scan non authentifié depuis la DMZ, aucune vue depuis Internet. Validation manuelle absente. Un port ouvert ne prouve pas une faille exploitée.",
         scenario="Dégradation du chiffrement des sessions du portail public (R05).",
         priorite="Modérée : exposé à Internet mais impact limité si la redirection est effective.",
         reco="Responsable infrastructures : désactiver TLS 1.0 et 1.1, vérifier la redirection et activer HSTS, scan externe de contrôle (A09).",
         cloture="Rapport de test TLS et preuve de redirection permanente.",
         risque="R05", action="A09", pilote="Resp. infrastructures", niveau="Exploitation 2"),
    dict(id="C09", pieces="T06/P11/T05", processus="Gérer les règles SSI",
         titre="Aucun délai de correctifs par criticité",
         observation="La PSSI ne fixe aucun délai de correctifs par criticité. Retards de 12 j (WEB01), 43 j (SRV-FICHIERS) et 74 j (APP01) sans exception validée. AD01 à jour selon l'agent (inventaire du 25/09/2026).",
         reserve="Retards déclaratifs, historiques de déploiement absents. Inventaire AD01 ancien de 17 jours à la date de contrôle.",
         scenario="Fenêtre d'exposition prolongée sur des actifs critiques (R03).",
         priorite="Élevée : cause commune de C03, C07 et C08.",
         reco="RSSI : SLA par criticité et circuit d'exception (A03, A09).",
         cloture="SLA approuvés, tableau mensuel de conformité, exceptions signées.",
         risque="R03", action="A03, A09", pilote="RSSI", niveau="Règles 2"),
    dict(id="C10", pieces="P06/P12/T08", processus="Superviser la SSI",
         titre="Registre d'événements incomplet",
         observation="Registre de 10 événements non exhaustif et non revu en comité (P06). Alertes parfois conservées dans les tickets (P12), AL-1048 sans ticket (T08).",
         reserve="Pièces de gouvernance déclaratives, cohérentes avec T08.",
         scenario="Incidents non qualifiés et absence de retour d'expérience (R01).",
         priorite="Élevée : conditionne la détection.",
         reco="RSSI : registre unique alimenté par les alertes qualifiées et revue mensuelle (A02).",
         cloture="Registre consolidé, PV de revue, taux d'alertes HIGH qualifiées.",
         risque="R01", action="A02", pilote="RSSI", niveau="Supervision 1"),
    dict(id="C11", pieces="T03/T09", processus="Exploiter les mesures SSI",
         titre="svc-backup non restreint",
         observation="svc-backup, compte technique à droits élevés sans MFA, déclaré non interactif par la DSI sans preuve de restriction.",
         reserve="Déclaration non étayée. Lien avec BACKUP01 probable mais non documenté.",
         scenario="Détournement du compte de sauvegarde pour supprimer les copies (R02).",
         priorite="Élevée : touche la capacité de reprise.",
         reco="DSI (IAM) : interdire l'ouverture de session interactive, secret en coffre, rotation (A08).",
         cloture="Stratégie de refus d'ouverture de session appliquée, journal sans session interactive.",
         risque="R02", action="A08", pilote="DSI (IAM)", niveau="Exploitation 2, fragile"),
]

# Lignes de la matrice T5 (au moins cinq corrélations)
CORRELATIONS = ["C04", "C01", "C05", "C03", "C02", "C09"]

# ---------------------------------------------------------------------------
# G4 · Registre des risques (onglet 04)
# ---------------------------------------------------------------------------
RISQUES = [
    dict(id="R01", court="Prise de contrôle d'un compte à privilèges",
         evenement="Prise de contrôle d'un compte à privilèges menant à une modification non autorisée de l'infrastructure (AD, serveurs)",
         actif="AD01, BASTION01 et VPN, groupe Server-Admins",
         menace="Attaquant externe à motivation cupide (P07) ou abus d'un accès prestataire",
         vuln="4 comptes privilégiés sur 10 non enrôlés MFA dont admin-old (dernière activité documentée en 2025, T03) et admin-presta, RDP direct FW-17, AL-1048 fermée sans examen tracé",
         mesures="MFA enrôlé sur 6 comptes sur 10, SIEM avec alertes, bastion pour une partie des accès",
         impact=4, vrais=3,
         decision="Réduire (A08, A02) et mesures conservatoires immédiates. Décision DG sur proposition du RSSI.",
         preuves="T03, T04, T07, T08, P17 · C01, C04, C06, C10"),
    dict(id="R02", court="Reprise impossible dans le RTO de 8 h",
         evenement="Indisponibilité de MEDI-PORTAL au-delà du RTO de 8 h faute de restauration fiable (rançongiciel ou panne)",
         actif="MEDI-PORTAL, base de données MEDI, BACKUP01",
         menace="Rançongiciel après hameçonnage ou erreur d'exploitation",
         vuln="2 tests documentés sur 9 services, RPO inconnu, FW-31 Any des postes vers les sauvegardes, svc-backup non restreint",
         mesures="Sauvegardes planifiées, comptes rendus hebdomadaires, site de secours, deux tests documentés",
         impact=4, vrais=3,
         decision="Réduire (A05, A08) et restriction de FW-31 en régie. Décision DG.",
         preuves="T09, T02, T03, P01, P15, P17 · C02, C05, C11"),
    dict(id="R03", court="Atteinte aux données via APP01 non corrigé",
         evenement="Altération ou divulgation de données patients via l'application métier non corrigée",
         actif="APP01, DB01",
         menace="Attaquant ayant pris pied en DMZ ou sur le VPN d'administration",
         vuln="Correctif critique manquant (T05), hôte en retard de 74 jours (T06), aucun SLA, flux WEB01 vers APP01, RDP FW-17",
         mesures="Absence d'exposition directe à Internet, cloisonnement DMZ et VLAN 20",
         impact=4, vrais=2,
         decision="Réduire (A09). Exception signée et mesures compensatoires si le correctif est reporté.",
         preuves="T05, T06, T02, P05 · C03, C06, C09"),
    dict(id="R04", court="Divulgation depuis les partages de fichiers",
         evenement="Divulgation de données internes depuis les partages de fichiers après compromission d'un poste, y compris des données de santé si les partages en contiennent (hypothèse)",
         actif="SRV-FICHIERS, AD01",
         menace="Hameçonnage (5 tentatives en 12 mois, P06)",
         vuln="SMB ouvert à tout le VLAN 40 (FW-19), signature non obligatoire, retard de correctifs de 43 jours",
         mesures="Blocage préventif de comptes, règles d'habilitation (P11)",
         impact=3, vrais=3,
         decision="Réduire partiellement (A09, A03). Segmentation complète A10 différée, risque résiduel accepté par la DG pour 12 mois.",
         preuves="T02, T05, T06, P06 · C07"),
    dict(id="R05", court="Dégradation des sessions du portail",
         evenement="Interception ou dégradation des sessions du portail public",
         actif="WEB01, MEDI-PORTAL",
         menace="Attaquant réseau opportuniste",
         vuln="TLS 1.0 signalé, port 80 ouvert, redirection non vérifiée",
         mesures="Publication limitée à 443 et 80 par FW-01 et FW-08, reverse proxy en DMZ",
         impact=2, vrais=2,
         decision="Réduire à faible coût dans A09. À défaut, acceptation temporaire par la DSI.",
         preuves="T02, T05 · C08"),
    dict(id="R06", court="Incident causé par un changement",
         evenement="Indisponibilité ou altération de service causée par un changement mal maîtrisé",
         actif="MEDI-PORTAL, infrastructure",
         menace="Erreur interne lors des changements mensuels et trimestriels",
         vuln="Conception et réalisation non standardisées (P13, P14), règle provisoire non retirée (FW-17)",
         mesures="Revues de conception des projets majeurs, comptes rendus d'installation",
         impact=3, vrais=3,
         decision="Accepter temporairement (A04 différée en année 2) avec revue de changement renforcée en régie. Risque résiduel porté par la DO.",
         preuves="P06, P08, P13, P14, T02 · C06"),
]

# ---------------------------------------------------------------------------
# G4 · Plan d'action sous plafond (onglet 05)
# ---------------------------------------------------------------------------
PLAFOND = 120000
# id -> (pilote, échéance et livrable, retenu, justification, court)
ACTIONS = {
    "A01": ("RSSI", "T+4 mois : méthode, registre consolidé approuvé par la DG, revue trimestrielle, tableau de bord stratégique semestriel", 1,
            "Gérer les risques au niveau 1 (P10). Base de tous les arbitrages R01 à R06. Porte aussi l'étape stratégie (comptes rendus écrits).", "Registre et méthode des risques"),
    "A02": ("RSSI et exploitation", "T+3 mois : procédure de traitement des alertes, plan de contrôle, reporting mensuel", 1,
            "Superviser au niveau 1 (P12). AL-1048 fermée sans ticket (C04, C10). R01.", "Supervision et reporting"),
    "A03": ("RSSI et RH", "T+6 mois : PSSI révisée avec SLA de correctifs, PV de revue, campagne anti-hameçonnage", 1,
            "5 hameçonnages sur 10 événements (P06), revue PSSI sans PV (P17), aucun SLA (C09). R04.", "PSSI et sensibilisation"),
    "A04": ("DSI", "Différée en année 2", 0,
            "Conception et réalisation déjà au niveau 2. Fiche SSI obligatoire préparée en régie. Risque résiduel R06.", "Standardisation conception et réalisation"),
    "A05": ("Resp. infrastructures", "T+6 mois : PV de restauration pour 9 services sur 9, RTO et RPO mesurés, procédure d'incident", 1,
            "2 tests sur 9 (T09), RTO de 8 h (P01). R02. Même lot que T10 restauration, compté une seule fois.", "Restauration et incidents"),
    "A06": ("RSSI", "Différée en année 2", 0,
            "La mesure quantitative relève du niveau 4, prématurée avec des processus à 1 ou 2. Alternative à A11, non cumulée. Risque résiduel : pilotage sans indicateurs chiffrés.", "Outillage quantitatif"),
    "A07": ("DG et RH", "Différée en année 2", 0,
            "Utile mais moins urgente que R01 et R02. Risque résiduel : adhésion insuffisante aux nouvelles pratiques, suivie par la DG et les managers.", "Conduite du changement"),
    "A08": ("DSI (IAM)", "T+3 mois : 100 % des comptes privilégiés sous MFA ou exception approuvée, revue des privilèges, svc-backup restreint", 1,
            "C01, C04, C11. R01 et R02. Déclaration de la DSI contredite par T04.", "MFA et privilèges"),
    "A09": ("Resp. infrastructures", "APP01 sous 15 jours, puis T+4 mois : inventaire authentifié, SLA par criticité, TLS 1.0 retiré, signature SMB", 1,
            "C03, C07, C08, C09. R03, R04 et R05.", "Vulnérabilités et correctifs"),
    "A10": ("DSI réseau", "Différée en année 2, FW-31 et FW-17 restreintes en régie sous un mois", 0,
            "Plafond atteint. Risque résiduel R04 et part de R02 acceptés par la DG pour 12 mois.", "Segmentation réseau"),
    "A11": ("RSSI", "Différée en année 2", 0,
            "Recoupe A02 pour le workflow d'alerte. Outil à choisir après stabilisation au niveau 2. Alternative à A06. Risque résiduel : détection limitée sur R01, compensée en partie par A02.", "Détection et workflow SIEM"),
}
# Coûts préremplis dans la grille (vérifiés à la génération)
COUTS = {"A01": 18000, "A02": 16000, "A03": 14000, "A04": 24000, "A05": 22000, "A06": 35000,
         "A07": 14000, "A08": 28000, "A09": 18000, "A10": 30000, "A11": 35000}

# Feuille de route SSI sur 12 mois (hypothèse : décision CODIR mi-novembre 2026, T0 = décembre 2026)
FEUILLE_ROUTE = [
    ("Suites de l'investigation", 0, 1, "Clôture de l'incident AL-1048"),
    ("A08 MFA et privilèges", 0, 3, "100 % MFA ou exception"),
    ("A02 Supervision et reporting", 0, 3, "Alertes tracées"),
    ("A01 Registre des risques", 1, 4, "Registre approuvé"),
    ("A09 Vulnérabilités", 0, 4, "APP01 en M1, SLA en M4"),
    ("A05 Restauration", 2, 6, "9 PV sur 9"),
    ("A03 PSSI et sensibilisation", 3, 6, "PSSI v2 approuvée"),
    ("Stabilisation et mesures", 6, 11, "Indicateurs trimestriels"),
    ("Bilan de maturité et année 2", 11, 12, "Arbitrage A04, A10, A06 ou A11"),
]
# Trajectoire cumulative visée (niveau démontrable à M6 et M12)
TRAJECTOIRE = {"Stratégie": (2, 2), "Risques": (2, 2), "Règles": (2, 2), "Supervision": (2, 2),
               "Conception": (2, 2), "Réalisation": (2, 2), "Exploitation": (2, 2)}

# ---------------------------------------------------------------------------
# Organisation du projet étudiant (calendrier de production, 20/10 au 10/11/2026)
# ---------------------------------------------------------------------------
EQUIPE = ["Team", "Marc", "Matteo", "Bernard"]
# Couleur par responsable (Gantt et Kanban)
COULEURS = {"Team": "1D5C7A", "Marc": "3B7A57", "Matteo": "B7791F", "Bernard": "6B4C9A", "Tous": "5F6B7A"}

# Planning cible. Dépendances de type fin-début : une tâche démarre quand celles dont elle dépend sont finies.
# Les fenêtres sont des périodes de réalisation, pas un travail à plein temps.
# (id, libellé, responsable, début, fin, dépendances, phase)
TACHES = [
    ("E1", "Lecture du sujet et des pièces", "Tous", "2026-10-20", "2026-10-21", [], "Cadrage"),
    ("E2", "Collecte des preuves P/T", "Team", "2026-10-21", "2026-10-23", ["E1"], "Cadrage"),
    ("E3", "G1 Périmètre et limites", "Team", "2026-10-24", "2026-10-26", ["E2"], "Analyses"),
    ("E4", "G2 Autodiagnostic Q01 à Q12", "Marc", "2026-10-24", "2026-10-27", ["E2"], "Analyses"),
    ("E5", "T1 Architecture et flux", "Matteo", "2026-10-24", "2026-10-26", ["E2"], "Analyses"),
    ("E6", "T2 Identités et MFA", "Matteo", "2026-10-26", "2026-10-28", ["E2"], "Analyses"),
    ("E7", "T3 Vulnérabilités", "Bernard", "2026-10-24", "2026-10-26", ["E2"], "Analyses"),
    ("E8", "T4 Journaux et sauvegardes", "Bernard", "2026-10-26", "2026-10-28", ["E2"], "Analyses"),
    ("E9", "Atelier de consolidation", "Tous", "2026-10-29", "2026-10-29", ["E3", "E4", "E5", "E6", "E7", "E8"], "Consolidation"),
    ("E10", "G3 Sept processus", "Marc", "2026-10-30", "2026-11-01", ["E9"], "Consolidation"),
    ("E11", "T5 Corrélation", "Matteo", "2026-10-30", "2026-11-01", ["E9"], "Consolidation"),
    ("E12", "G4 Risques, budget, feuille de route", "Team", "2026-11-02", "2026-11-03", ["E10", "E11"], "Consolidation"),
    ("E13", "Remplissage progressif de l'Excel", "Bernard", "2026-10-24", "2026-11-03", ["E2"], "Consolidation"),
    ("E14", "Rédaction du rapport", "Team", "2026-11-04", "2026-11-06", ["E12", "E13"], "Rédaction et restitution"),
    ("E15", "Relectures croisées", "Tous", "2026-11-07", "2026-11-07", ["E14"], "Rédaction et restitution"),
    ("E16", "Corrections", "Marc", "2026-11-08", "2026-11-08", ["E15"], "Rédaction et restitution"),
    ("E17", "Compilation et contrôle du PDF", "Team", "2026-11-09", "2026-11-09", ["E16"], "Rédaction et restitution"),
    ("E18", "Présentation CODIR et répétition", "Matteo", "2026-11-04", "2026-11-09", ["E12"], "Rédaction et restitution"),
]
PHASES = ["Cadrage", "Analyses", "Consolidation", "Rédaction et restitution"]
JALONS = [
    ("J1", "Cadrage figé", "2026-10-23"),
    ("J2", "Analyses figées", "2026-11-03"),
    ("J3", "Livrables finalisés", "2026-11-09"),
    ("J4", "Dépôt et soutenance", "2026-11-10"),
]
# Liens dessinés sur le Gantt (chaîne critique et convergences), la liste complète figure en annexe
LIENS_GANTT = [("E1", "E2"), ("E9", "E10"), ("E9", "E11"), ("E10", "E12"), ("E11", "E12"),
               ("E12", "E14"), ("E14", "E15"), ("E15", "E16"), ("E16", "E17"), ("E12", "E18")]

# Kanban : état attesté au 30 octobre 2026, date de production de la version 1 des livrables.
# Une tâche dont le livrable existe en version 1 est « À relire » (relecture croisée de l'équipe à venir).
# Une tâche sans trace de réalisation reste « À faire », avec la mention « non attesté » si sa fenêtre est passée.
DATE_KANBAN = "2026-10-30"
KANBAN = {
    "E1": ("À faire", "non attesté"), "E9": ("À faire", "non attesté"),
    "E2": ("À relire", ""), "E3": ("À relire", ""), "E4": ("À relire", ""), "E5": ("À relire", ""),
    "E6": ("À relire", ""), "E7": ("À relire", ""), "E8": ("À relire", ""), "E10": ("À relire", ""),
    "E11": ("À relire", ""), "E12": ("À relire", ""), "E13": ("À relire", ""), "E14": ("À relire", ""),
    "E18": ("En cours", "diapositives prêtes, répétition à faire"),
    "E15": ("À faire", ""), "E16": ("À faire", ""), "E17": ("À faire", ""),
}

# ---------------------------------------------------------------------------
# Données des graphiques
# ---------------------------------------------------------------------------
# Grille des exigences DCSSI par processus : O démontré, N non établi, I indéterminé, D déduit (à confirmer)
PROC_COURTS = ["Stratégie", "Risques", "Règles", "Supervision", "Conception", "Réalisation", "Exploitation"]
EXIGENCES = [
    (1, "Pratiques de base", "OOOOOOO"),
    (2, "Actions planifiées", "ONONOIO"),
    (2, "Acteurs compétents en SSI", "OOOODOO"),
    (2, "Pratiques en partie formalisées", "ONONOOO"),
    (2, "Mesures qualitatives", "INONOOO"),
    (2, "Autorités informées", "OIONOOO"),
    (3, "Processus défini et standardisé", "NNNNNNN"),
    (3, "Compétences appropriées", "IIIIIII"),
    (3, "Soutien de l'organisme", "IIIIIII"),
]
# T03 et T04 : comptes privilégiés
COMPTES = [("admin-jdupont", 1), ("admin-mmartin", 1), ("admin-astreinte1", 1), ("admin-astreinte2", 1),
           ("admin-cloud1", 1), ("admin-net1", 1), ("svc-backup", 0), ("admin-old", 0), ("admin-presta", 0), ("admin-db", 0)]
# T09 : services et dernier test documenté
SAUVEGARDES = [("MEDI-PORTAL", "15/09"), ("Ticketing", "16/09"), ("ERP", ""), ("Active Directory", ""),
               ("Fichiers partagés", ""), ("Messagerie M365", ""), ("Base MEDI", ""), ("VPN et bastion", ""), ("Supervision", "")]
# T05 et T06 : (actif, CVSS, retard en jours, exposition, priorité retenue)
VULNS = [("APP01", 9.8, 74, "DMZ et FW-17", 1), ("SRV-FICHIERS", 6.5, 43, "VLAN 40", 2), ("WEB01", 5.3, 12, "Internet", 3)]

# Décision résumée par risque (tableau du corps du rapport)
DECISION_COURTE = {"R01": "Réduire (A08, A02)", "R02": "Réduire (A05, A08, régie)", "R03": "Réduire (A09)",
                   "R04": "Réduire en partie, résiduel accepté", "R05": "Réduire (A09)", "R06": "Accepter 12 mois (A04 différée)"}
