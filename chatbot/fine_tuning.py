# ---
# 🔄 1. PRÉPARATION DES DONNÉES POUR LE FINE-TUNING (ex: avec FLAN-T5)
# Format recommandé : JSONL (une ligne = un exemple)
# Structure : chaque ligne doit avoir un 'instruction' (question RH) et 'output' (requête SELECT)

import json
from datasets import Dataset

# Exemple de données d'entraînement
train_data =[ 
  
  {
    "instruction": "Quel est mon nom complet ?",
    "output": "SELECT CONCAT(nom, ' ', prenom) FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon numéro de sécurité sociale ?",
    "output": "SELECT nss FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma nationalité ?",
    "output": "SELECT nationalite FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quand ai-je ete recrute ?",
    "output": "SELECT date_recrutement FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Combien d'enfants ai-je ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon email professionnel ?",
    "output": "SELECT email FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est mon adresse ?",
    "output": "SELECT adresse FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Est-ce que je bénéficie du transport ?",
    "output": "SELECT benification_transport FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Est-ce que je bénéficie du panier ?",
    "output": "SELECT retenu_panier FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Suis-je un manager ?",
    "output": "SELECT is_manager FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Mon email est-il public ?",
    "output": "SELECT email_public FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Mon numéro de téléphone est-il public ?",
    "output": "SELECT telephone_public FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Dans quel service travaille-je ?",
    "output": "SELECT service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon niveau hiérarchique ?",
    "output": "SELECT niveau FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est mon échelle salariale ?",
    "output": "SELECT echelle FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Dans quel département suis-je affecté ?",
    "output": "SELECT departement FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma direction ?",
    "output": "SELECT direction FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quel diplôme est requis pour mon poste ?",
    "output": "SELECT diplome_secteur FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle expérience est requise pour mon poste ?",
    "output": "SELECT experience_secteur FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes horaires d'aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quels étaient mes horaires hier ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = (CURRENT_DATE - INTERVAL '1 day')"
  },
  {
    "instruction": "Ai-je pointé ce matin ?",
    "output": "SELECT heure_arrive IS NOT NULL FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "À quelle heure suis-je arrivé hier ?",
    "output": "SELECT heure_arrive FROM pointage WHERE id_employe = 5 AND date = (CURRENT_DATE - INTERVAL '1 day')"
  },
  {
    "instruction": "À quelle heure suis-je parti vendredi dernier ?",
    "output": "SELECT heure_depart FROM pointage WHERE id_employe = 5 AND date = (CURRENT_DATE - (EXTRACT(DOW FROM CURRENT_DATE) + 2)::INTEGER % 7)"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quels congés ai-je pris ce mois-ci ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart >= DATE_TRUNC('month', CURRENT_DATE)"
  },
  {
    "instruction": "Quelle est la durée de mon prochain congé ?",
    "output": "SELECT (date_reprise - date_depart) AS duree FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE ORDER BY date_depart LIMIT 1"
  },
  {
    "instruction": "Quand commence mon prochain congé ?",
    "output": "SELECT date_depart FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE ORDER BY date_depart LIMIT 1"
  },
  {
    "instruction": "Quand se termine mon congé en cours ?",
    "output": "SELECT date_reprise FROM conge WHERE id_employe = 5 AND date_depart <= CURRENT_DATE AND date_reprise >= CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes droits à congé annuel ?",
    "output": "SELECT conge_annuelle FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé de récupération ?",
    "output": "SELECT conge_recup FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé sans solde ?",
    "output": "SELECT conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Combien de jours de congé me restent-ils ?",
    "output": "SELECT conge_annuelle - (SELECT COUNT(*) FROM conge WHERE id_employe = 5 AND designation = 'Congé annuel' AND date_depart >= DATE_TRUNC('year', CURRENT_DATE)) FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes missions actuelles ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 AND date_debut <= CURRENT_DATE AND date_fin >= CURRENT_DATE"
  },
  {
    "instruction": "Quelles missions ai-je effectuées l'année dernière ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 AND date_debut >= (CURRENT_DATE - INTERVAL '1 year') AND date_fin <= CURRENT_DATE"
  },
  {
    "instruction": "Quelle est ma prochaine mission ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 AND date_debut > CURRENT_DATE ORDER BY date_debut LIMIT 1"
  },
  {
    "instruction": "Où se déroule ma prochaine mission ?",
    "output": "SELECT lieu FROM mission WHERE id_employe = 5 AND date_debut > CURRENT_DATE ORDER BY date_debut LIMIT 1"
  },
  {
    "instruction": "Quel est l'itinéraire de ma prochaine mission ?",
    "output": "SELECT itineraire FROM mission WHERE id_employe = 5 AND date_debut > CURRENT_DATE ORDER BY date_debut LIMIT 1"
  },
  {
    "instruction": "Quelles sont mes formations prévues ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND date_debut > CURRENT_DATE"
  },
  {
    "instruction": "Quelles formations ai-je suivies cette année ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND date_debut >= DATE_TRUNC('year', CURRENT_DATE) AND date_fin <= CURRENT_DATE"
  },
  {
    "instruction": "Quelle était ma dernière formation ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 ORDER BY date_fin DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est la durée de ma prochaine formation ?",
    "output": "SELECT (date_fin - date_debut) AS duree FROM formation WHERE id_employe = 5 AND date_debut > CURRENT_DATE ORDER BY date_debut LIMIT 1"
  },
  {
    "instruction": "Quelles sont mes formations en interne ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type = 'Interne'"
  },
  {
    "instruction": "Quelles sont mes formations certifiantes ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type = 'Certifiante'"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT numero_contract, montant, date_depot FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quel est le montant total de mes prêts ?",
    "output": "SELECT SUM(montant) FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quand commence le remboursement de mon prêt ?",
    "output": "SELECT date_debut_remboursement FROM mes_prets WHERE id_employe = 5 AND rembourse = false ORDER BY date_depot DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est la durée de remboursement de mon prêt ?",
    "output": "SELECT duree FROM mes_prets WHERE id_employe = 5 AND rembourse = false ORDER BY date_depot DESC LIMIT 1"
  },
  {
    "instruction": "Quel est le motif de mon dernier prêt ?",
    "output": "SELECT motif_prets FROM mes_prets WHERE id_employe = 5 ORDER BY date_depot DESC LIMIT 1"
  },
  {
    "instruction": "Quels remboursements ai-je effectués ce mois-ci ?",
    "output": "SELECT montant, date_remboursement, type FROM remboursement WHERE id_employe = 5 AND date_remboursement >= DATE_TRUNC('month', CURRENT_DATE)"
  },
  {
    "instruction": "Quel est le montant total de mes remboursements MIP cette année ?",
    "output": "SELECT SUM(montant) FROM remboursement WHERE id_employe = 5 AND type = 'MIP' AND date_remboursement >= DATE_TRUNC('year', CURRENT_DATE)"
  },
  {
    "instruction": "Quelles sont mes réalisations professionnelles ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelles réalisations ai-je faites ce trimestre ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 AND date >= DATE_TRUNC('quarter', CURRENT_DATE)"
  },
  {
    "instruction": "Quelle était ma dernière réalisation ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC LIMIT 1"
  },
  {
    "instruction": "Quelles sont mes expériences professionnelles ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelles expériences ai-je eues dans le secteur ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 AND is_secteur = true"
  },
  {
    "instruction": "Combien d'années d'expérience ai-je ?",
    "output": "SELECT SUM(date_fin - date_debut) FROM experience WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes informations de carrière ?",
    "output": "SELECT duree, debut, structure, echelle, classification FROM carriere WHERE id_employe = 5 ORDER BY debut DESC"
  },
  {
    "instruction": "Quelle est ma classification actuelle ?",
    "output": "SELECT classification FROM carriere WHERE id_employe = 5 ORDER BY debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est mon échelle de carrière ?",
    "output": "SELECT echelle FROM carriere WHERE id_employe = 5 ORDER BY debut DESC LIMIT 1"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5 AND medailles IS NOT NULL"
  },
  {
    "instruction": "Quelle est la structure de ma dernière affectation ?",
    "output": "SELECT structure FROM carriere WHERE id_employe = 5 ORDER BY debut DESC LIMIT 1"
  },
  {
    "instruction": "Quand puis-je partir à la retraite ?",
    "output": "SELECT date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je demandé à poursuivre après la retraite ?",
    "output": "SELECT demande_poursuivre FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quand ai-je déposé mon dossier de retraite ?",
    "output": "SELECT date_depot FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Combien de temps avant ma retraite ?",
    "output": "SELECT (date_previsionnelle_retraite - CURRENT_DATE) FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes notifications non lues ?",
    "output": "SELECT titre, description FROM notification WHERE id_employe = 5 AND est_lue = false ORDER BY date DESC"
  },
  {
    "instruction": "Quelles notifications ai-je reçues cette semaine ?",
    "output": "SELECT titre, description FROM notification WHERE id_employe = 5 AND date >= (CURRENT_DATE - INTERVAL '7 days') ORDER BY date DESC"
  },
  {
    "instruction": "Quel document est associé à ma dernière notification ?",
    "output": "SELECT document FROM notification WHERE id_employe = 5 ORDER BY date DESC LIMIT 1"
  },
  {
    "instruction": "Qui m'a envoyé des messages non lus ?",
    "output": "SELECT DISTINCT expediteur_id FROM message WHERE destinataire_id = 5 AND lu = false"
  },
  {
    "instruction": "Quels sont mes derniers messages reçus ?",
    "output": "SELECT contenu, date_envoi FROM message WHERE destinataire_id = 5 ORDER BY date_envoi DESC LIMIT 5"
  },
  {
    "instruction": "Quand ai-je reçu mon dernier message ?",
    "output": "SELECT MAX(date_envoi) FROM message WHERE destinataire_id = 5"
  },
  {
    "instruction": "Ai-je des sanctions disciplinaires ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelle était ma dernière sanction ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC LIMIT 1"
  },
  {
    "instruction": "Ai-je des sanctions cette année ?",
    "output": "SELECT COUNT(*) FROM sanction_discipline WHERE id_employe = 5 AND date >= DATE_TRUNC('year', CURRENT_DATE)"
  },
  {
    "instruction": "Quel est le motif de ma dernière sanction ?",
    "output": "SELECT designation FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC LIMIT 1"
  },
  {
    "instruction": "Quels documents administratifs sont disponibles ?",
    "output": "SELECT titre FROM document"
  },
  {
    "instruction": "Où trouver mon contrat de travail ?",
    "output": "SELECT chemin FROM document WHERE titre ILIKE '%contrat travail%'"
  },
  {
    "instruction": "Comment obtenir mon attestation de salaire ?",
    "output": "SELECT chemin FROM document WHERE titre ILIKE '%attestation salaire%'"
  },
  {
    "instruction": "Où est stocké mon CV ?",
    "output": "SELECT chemin FROM document WHERE titre ILIKE '%cv%'"
  },
  {
    "instruction": "Quels sont les documents RH à jour ?",
    "output": "SELECT titre FROM document WHERE date_ajouter >= (CURRENT_DATE - INTERVAL '1 year')"
  },
  {
    "instruction": "Qui sont mes apprentis actuels ?",
    "output": "SELECT nom, specialite FROM apprentis WHERE id_employe = 5 AND CURRENT_DATE BETWEEN date_debut AND date_fin"
  },
  {
    "instruction": "Quel organisme forme mon apprenti ?",
    "output": "SELECT organisme FROM apprentis WHERE id_employe = 5 AND CURRENT_DATE BETWEEN date_debut AND date_fin LIMIT 1"
  },
  {
    "instruction": "Quand se termine la période d'apprentissage ?",
    "output": "SELECT date_fin FROM apprentis WHERE id_employe = 5 AND CURRENT_DATE BETWEEN date_debut AND date_fin LIMIT 1"
  },
  {
    "instruction": "Quelle est la spécialité de mon apprenti ?",
    "output": "SELECT specialite FROM apprentis WHERE id_employe = 5 AND CURRENT_DATE BETWEEN date_debut AND date_fin LIMIT 1"
  },
  {
    "instruction": "Quelles observations ont été faites sur mon apprenti ?",
    "output": "SELECT observation FROM apprentis WHERE id_employe = 5 AND CURRENT_DATE BETWEEN date_debut AND date_fin LIMIT 1"
  },
  {
    "instruction": "Quelles sont mes inscriptions sociales ?",
    "output": "SELECT sejour, type, date FROM inscription_social WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quand était mon dernier séjour social ?",
    "output": "SELECT MAX(date) FROM inscription_social WHERE id_employe = 5 AND type = 'Séjour'"
  },
  {
    "instruction": "Quels types d'inscriptions sociales ai-je utilisées ?",
    "output": "SELECT DISTINCT type FROM inscription_social WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je des inscriptions sociales à venir ?",
    "output": "SELECT sejour, date FROM inscription_social WHERE id_employe = 5 AND date > CURRENT_DATE"
  },
  {
    "instruction": "Quelle était la dernière activité sociale ?",
    "output": "SELECT sejour FROM inscription_social WHERE id_employe = 5 ORDER BY date DESC LIMIT 1"
  },
  {
    "instruction": "Qui sont mes collaborateurs si je suis manager ?",
    "output": "SELECT collaborateurs FROM manager WHERE id_employe = 5"
  },
  {
    "instruction": "Combien de collaborateurs ai-je ?",
    "output": "SELECT ARRAY_LENGTH(collaborateurs, 1) FROM manager WHERE id_employe = 5"
  },
  {
    "instruction": "Qui est mon manager direct ?",
    "output": "SELECT id_employe FROM manager WHERE 5 = ANY(collaborateurs) LIMIT 1"
  },
  {
    "instruction": "Quels sont les noms de mes collaborateurs ?",
    "output": "SELECT nom, prenom FROM employe WHERE id_employe IN (SELECT unnest(collaborateurs) FROM manager WHERE id_employe = 5)"
  },
  {
    "instruction": "Qui sont les membres de mon équipe ?",
    "output": "SELECT nom, prenom FROM employe WHERE id_employe IN (SELECT unnest(collaborateurs) FROM manager WHERE id_employe = 5)"
  },
  {
    "instruction": "Quelles sont les catégories qui me concernent ?",
    "output": "SELECT nom FROM categorie WHERE id_employe = 5"
  },
  {
    "instruction": "Quand ont été ajoutées mes catégories ?",
    "output": "SELECT nom, date_ajouter FROM categorie WHERE id_employe = 5"
  },
  {
    "instruction": "Combien de catégories m'ont été attribuées ?",
    "output": "SELECT COUNT(*) FROM categorie WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle était la dernière catégorie ajoutée ?",
    "output": "SELECT nom FROM categorie WHERE id_employe = 5 ORDER BY date_ajouter DESC LIMIT 1"
  },
  {
    "instruction": "Quelles catégories ont été ajoutées ce mois-ci ?",
    "output": "SELECT nom FROM categorie WHERE id_employe = 5 AND date_ajouter >= DATE_TRUNC('month', CURRENT_DATE)"
  },
   
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
  "instruction": "Quels sont mes congés à venir ?",
  "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },

  {
  "instruction": "Quelle est ma date de naissance ?",
  "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma date de naissance ?",
    "output": "SELECT date_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je reçu des médailles ?",
    "output": "SELECT medailles FROM carriere WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est la durée de mon dernier congé ?",
    "output": "SELECT date_reprise - date_depart AS duree FROM conge WHERE id_employe = 5 ORDER BY date_depart DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quelle est ma dernière expérience professionnelle ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quelles sont mes réalisations ?",
    "output": "SELECT description, date FROM realisation WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes droits à congé ?",
    "output": "SELECT conge_annuelle, conge_recup, conge_scev FROM droit_conge WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est le statut de ma retraite ?",
    "output": "SELECT date_depot, date_previsionnelle_retraite FROM retraite WHERE id_employe = 5"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes postes précédents ?",
    "output": "SELECT poste, employeur, date_debut, date_fin FROM experience WHERE id_employe = 5 ORDER BY date_debut ASC"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Ai-je reçu une sanction disciplinaire ?",
    "output": "SELECT designation, date FROM sanction_discipline WHERE id_employe = 5 ORDER BY date DESC"
  },
  {
    "instruction": "Quels sont mes prêts en cours ?",
    "output": "SELECT montant, date_depot, numero_contract FROM mes_prets WHERE id_employe = 5 AND rembourse = false"
  },
  {
    "instruction": "Quel est mon lieu de naissance ?",
    "output": "SELECT lieu_naissance FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quel est mon poste actuel ?",
    "output": "SELECT intitule, service FROM poste WHERE id_employe = 5"
  },
  {
    "instruction": "Quels sont mes pointages aujourd'hui ?",
    "output": "SELECT heure_arrive, heure_depart FROM pointage WHERE id_employe = 5 AND date = CURRENT_DATE"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon groupe sanguin ?",
    "output": "SELECT groupe_sanguin FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Combien ai-je d'enfants ?",
    "output": "SELECT nb_enfants FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Ai-je été en mission récemment ?",
    "output": "SELECT objet, lieu, date_debut, date_fin FROM mission WHERE id_employe = 5 ORDER BY date_debut DESC LIMIT 1"
  },
  {
    "instruction": "Quels sont mes congés à venir ?",
    "output": "SELECT designation, date_depart, date_reprise FROM conge WHERE id_employe = 5 AND date_depart > CURRENT_DATE"
  },
  {
    "instruction": "Quelles sont mes formations prévisionnelles ?",
    "output": "SELECT description, date_debut, date_fin FROM formation WHERE id_employe = 5 AND type ILIKE 'previsionnelle'"
  },
  {
    "instruction": "Quelle est ma situation familiale ?",
    "output": "SELECT situation_familiale FROM employe WHERE id_employe = 5"
  },
  {
    "instruction": "Quel est mon numéro de téléphone ?",
    "output": "SELECT numero_telephone FROM employe WHERE id_employe = 5"
  }
]

# Supprimer les doublons
unique_data = []
seen_instructions = set()
for item in train_data:
    if item["instruction"] not in seen_instructions:
        unique_data.append(item)
        seen_instructions.add(item["instruction"])

# Sauvegarder en JSONL
with open("train_data.jsonl", "w", encoding="utf-8") as f:
    for item in unique_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

# Charger le dataset
dataset = Dataset.from_json("train_data.jsonl")

# ⚡ 2. LORA + PEFT : Entraînement efficace (ex: Flan-T5 base)
from peft import LoraConfig, get_peft_model, TaskType
from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    Seq2SeqTrainingArguments,
    Seq2SeqTrainer,
    DataCollatorForSeq2Seq
)
import torch

# Configuration
MODEL_NAME = "google/flan-t5-base"
OUTPUT_DIR = r"C:\Users\WINDOWS 10\Desktop\Ma_Brique\try_1 - Copie (3)\chatbot\fichier_generer"


MAX_LENGTH = 256
BATCH_SIZE = 8
LEARNING_RATE = 3e-4
NUM_EPOCHS = 5

# Charger le modèle et le tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# Configuration LoRA
peft_config = LoraConfig(
    task_type=TaskType.SEQ_2_SEQ_LM,
    inference_mode=False,
    r=8,
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules=["q", "v"]
)

# Appliquer LoRA au modèle
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()

# Prétraitement des données
def preprocess_function(examples):
    inputs = [instruction for instruction in examples["instruction"]]
    targets = [output for output in examples["output"]]
    
    model_inputs = tokenizer(
        inputs,
        max_length=MAX_LENGTH,
        truncation=True,
        padding="max_length"
    )
    
    labels = tokenizer(
        targets,
        max_length=MAX_LENGTH,
        truncation=True,
        padding="max_length"
    )
    
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True)

# Collateur de données
data_collator = DataCollatorForSeq2Seq(
    tokenizer,
    model=model,
    label_pad_token_id=tokenizer.pad_token_id,
    pad_to_multiple_of=8
)

# Arguments d'entraînement
training_args = Seq2SeqTrainingArguments(
    output_dir=OUTPUT_DIR,
    overwrite_output_dir=True,
    per_device_train_batch_size=BATCH_SIZE,
    learning_rate=LEARNING_RATE,
    num_train_epochs=NUM_EPOCHS,
    logging_dir=f"{OUTPUT_DIR}/logs",
    logging_strategy="steps",
    logging_steps=50,
    save_strategy="epoch",
    save_total_limit=2,
    eval_strategy="no",
    predict_with_generate=True,
    fp16=torch.cuda.is_available(),
    report_to="none"
)

# Entraîneur
trainer = Seq2SeqTrainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator,
    tokenizer=tokenizer,
)

# Entraînement
print("Début de l'entraînement...")
trainer.train()
trainer.save_model(OUTPUT_DIR)


print("Entraînement terminé!")


# 🚀 3. UTILISER LE MODÈLE AFFINÉ POUR GÉNÉRER DES REQUÊTES
import re
from transformers import pipeline
import unicodedata
import re

def nettoyer_instruction(instruction: str) -> str:
    # Supprimer les accents
    texte = unicodedata.normalize('NFKD', instruction)
    texte = ''.join([c for c in texte if not unicodedata.combining(c)])
    
    # Convertir en minuscules
    texte = texte.lower()
    
    # Enlever les caractères spéciaux (facultatif)
    texte = re.sub(r"[^\w\s]", "", texte)

    # Tentative simple de suppression de pluriels (très basique)
    mots = texte.split()
    mots_singuliers = []
    for mot in mots:
        if mot.endswith("s") and len(mot) > 3:
            mots_singuliers.append(mot[:-1])
        else:
            mots_singuliers.append(mot)
    
    texte_singulier = ' '.join(mots_singuliers)

    return texte_singulier.strip()

def generate_sql_query(question, model_path=OUTPUT_DIR, max_attempts=3):
    # Charger le modèle fine-tuné
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    # Créer un pipeline
    sql_pipeline = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1
    )
    
    for attempt in range(max_attempts):
        try:
            # Générer la réponse
            outputs = sql_pipeline(
                question,
                max_length=MAX_LENGTH,
                num_beams=5,
                early_stopping=True,
                temperature=0.7
            )
            
            raw_output = outputs[0]["generated_text"].strip()
            
            # Extraire la requête SQL
            sql_match = re.search(r'(SELECT\s.+?(?:;|$))', raw_output, re.IGNORECASE | re.DOTALL)
            if sql_match:
                sql = sql_match.group(1).strip().rstrip(';')
                return sql
                
        except Exception as e:
            print(f"Erreur lors de la tentative {attempt + 1}: {str(e)}")
    
    return "Désolé, je n'ai pas pu générer de requête SQL valide."


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "train":
        print("Début de l'entraînement...")
        trainer.train()
        trainer.save_model(OUTPUT_DIR)
        print("Entraînement terminé!")
    
    else:
        # 🔹 Test automatique sur les données d'entraînement
        print("🧪 Test sur les questions de l'entraînement :\n")
        for example in unique_data:
            original_question = example["instruction"]
            question_cleaned = nettoyer_instruction(original_question)
            expected_sql = example["output"]
            generated_sql = generate_sql_query(question_cleaned)
            print(f"❓ Question originale : {original_question}")
            print(f"🧼 Nettoyée           : {question_cleaned}")
            print(f"✅ SQL attendu        : {expected_sql}")
            print(f"🤖 SQL généré         : {generated_sql}")
            print("-" * 80)

        # 🔹 Mode interactif manuel
        print("\n💬 Mode interactif : posez d'autres questions (ou tapez 'exit' pour quitter)")
        while True:
            question = input("Votre question : ")
            if question.lower() == "exit":
                break
            question_cleaned = nettoyer_instruction(question)
            generated_sql = generate_sql_query(question_cleaned)
            print(f"🧠 Question nettoyée        : {question_cleaned}")
            print(f"🧠 Requête SQL générée : {generated_sql}\n")

