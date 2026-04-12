-- ============================================================
--  TranspoBot — Enrichissement de la base de données
--  Exécuter : mysql -u root -p transpobot < enrichissement.sql
-- ============================================================

USE transpobot;

-- ── Nouvelles lignes ─────────────────────────────────────────
INSERT INTO lignes (code, nom, origine, destination, distance_km, duree_minutes) VALUES
('L5', 'Ligne Dakar-Kaolack',    'Dakar',       'Kaolack',    194.0, 210),
('L6', 'Ligne Université',       'Liberté 6',   'UCAD',        8.0,  25),
('L7', 'Ligne Grand-Yoff',       'Grand-Yoff',  'Plateau',    12.0,  35),
('L8', 'Ligne Rufisque Express', 'Dakar',       'Rufisque',   25.0,  45);

-- ── Nouveaux tarifs ──────────────────────────────────────────
INSERT INTO tarifs (ligne_id, type_client, prix) VALUES
(5, 'normal', 4500), (5, 'etudiant', 2500), (5, 'senior', 3000),
(6, 'normal', 400),  (6, 'etudiant', 200),
(7, 'normal', 450),  (7, 'etudiant', 250),
(8, 'normal', 800),  (8, 'etudiant', 500),  (8, 'senior', 600);

-- ── Nouveaux véhicules ───────────────────────────────────────
INSERT INTO vehicules (immatriculation, type, capacite, statut, kilometrage, date_acquisition) VALUES
('DK-1111-KL', 'bus',     60, 'actif',         22000, '2023-01-15'),
('DK-2222-MN', 'minibus', 25, 'actif',         18000, '2023-04-10'),
('DK-3333-OP', 'bus',     60, 'hors_service',  95000, '2018-07-20'),
('DK-4444-QR', 'taxi',     5, 'actif',         45000, '2021-11-05'),
('DK-5555-ST', 'minibus', 25, 'maintenance',   61000, '2020-03-18'),
('DK-6666-UV', 'bus',     60, 'actif',          9000, '2024-02-01');

-- ── Nouveaux chauffeurs ──────────────────────────────────────
INSERT INTO chauffeurs (nom, prenom, telephone, numero_permis, categorie_permis, vehicule_id, date_embauche) VALUES
('MBAYE',   'Cheikh',   '+221776789012', 'P-2020-006', 'D', 6,    '2020-05-01'),
('DIOUF',   'Rokhaya',  '+221777890123', 'P-2021-007', 'B', 9,    '2021-08-15'),
('GAYE',    'Modou',    '+221778901234', 'P-2022-008', 'D', 7,    '2022-03-10'),
('SARR',    'Ndèye',    '+221779012345', 'P-2023-009', 'D', 8,    '2023-06-20'),
('THIAW',   'Pape',     '+221770123456', 'P-2023-010', 'D', 10,   '2023-11-01'),
('CISSE',   'Mariama',  '+221771234560', 'P-2024-011', 'D', NULL,  '2024-01-10');

-- ── Trajets supplémentaires (janvier à avril 2026) ───────────
INSERT INTO trajets (ligne_id, chauffeur_id, vehicule_id, date_heure_depart, date_heure_arrivee, statut, nb_passagers, recette) VALUES
-- Janvier 2026
(3, 6, 6,  '2026-01-05 06:30:00', '2026-01-05 07:15:00', 'termine', 58, 29000),
(4, 7, 9,  '2026-01-07 08:00:00', '2026-01-07 09:00:00', 'termine', 5,  25000),
(1, 8, 7,  '2026-01-10 06:00:00', '2026-01-10 07:30:00', 'termine', 52, 130000),
(2, 1, 1,  '2026-01-12 07:00:00', '2026-01-12 09:00:00', 'termine', 55, 165000),
(6, 9, 8,  '2026-01-15 07:30:00', '2026-01-15 07:55:00', 'termine', 23, 9200),
(7, 2, 2,  '2026-01-18 08:00:00', '2026-01-18 08:35:00', 'termine', 20, 9000),
(8, 3, 4,  '2026-01-20 09:00:00', '2026-01-20 09:45:00', 'termine', 4,  3200),
(1, 4, 5,  '2026-01-22 06:00:00', '2026-01-22 07:30:00', 'termine', 50, 125000),
(3, 5, 6,  '2026-01-25 07:00:00', '2026-01-25 07:45:00', 'termine', 55, 27500),
(5, 6, 6,  '2026-01-28 05:30:00', '2026-01-28 09:00:00', 'termine', 48, 216000),

-- Février 2026
(1, 1, 1,  '2026-02-02 06:00:00', '2026-02-02 07:30:00', 'termine', 60, 150000),
(2, 2, 2,  '2026-02-04 07:00:00', '2026-02-04 09:00:00', 'termine', 22, 66000),
(3, 8, 7,  '2026-02-06 07:30:00', '2026-02-06 08:15:00', 'termine', 50, 25000),
(4, 9, 8,  '2026-02-08 09:00:00', '2026-02-08 10:00:00', 'termine', 18, 90000),
(6, 3, 4,  '2026-02-10 07:30:00', '2026-02-10 07:55:00', 'termine', 25, 10000),
(7, 4, 5,  '2026-02-12 08:00:00', '2026-02-12 08:35:00', 'termine', 24, 10800),
(8, 5, 6,  '2026-02-14 09:00:00', '2026-02-14 09:45:00', 'termine', 5,  4000),
(1, 6, 6,  '2026-02-16 06:00:00', '2026-02-16 07:30:00', 'termine', 57, 142500),
(5, 7, 9,  '2026-02-18 05:30:00', '2026-02-18 09:00:00', 'termine', 4,  18000),
(2, 8, 7,  '2026-02-20 07:00:00', '2026-02-20 09:00:00', 'termine', 20, 60000),
(3, 9, 8,  '2026-02-22 07:30:00', '2026-02-22 08:15:00', 'termine', 60, 30000),
(1, 1, 1,  '2026-02-25 06:00:00', '2026-02-25 07:30:00', 'termine', 55, 137500),
(4, 2, 2,  '2026-02-27 09:00:00', '2026-02-27 10:00:00', 'termine', 20, 100000),

-- Mars 2026 (déjà quelques données, on complète)
(6, 3, 4,  '2026-03-03 07:30:00', '2026-03-03 07:55:00', 'termine', 22, 8800),
(7, 4, 5,  '2026-03-06 08:00:00', '2026-03-06 08:35:00', 'termine', 25, 11250),
(8, 5, 6,  '2026-03-08 09:00:00', '2026-03-08 09:45:00', 'termine', 4,  3200),
(5, 6, 6,  '2026-03-15 05:30:00', '2026-03-15 09:00:00', 'termine', 50, 225000),
(2, 7, 9,  '2026-03-17 07:00:00', '2026-03-17 09:00:00', 'termine', 23, 69000),
(3, 8, 7,  '2026-03-19 07:30:00', '2026-03-19 08:15:00', 'termine', 58, 29000),
(4, 9, 8,  '2026-03-22 09:00:00', '2026-03-22 10:00:00', 'termine', 17, 85000),
(1, 1, 1,  '2026-03-25 06:00:00', '2026-03-25 07:30:00', 'termine', 59, 147500),
(6, 2, 2,  '2026-03-27 07:30:00', '2026-03-27 07:55:00', 'termine', 24, 9600),
(7, 3, 4,  '2026-03-28 08:00:00', '2026-03-28 08:35:00', 'termine', 23, 10350),
(8, 4, 5,  '2026-03-30 09:00:00', '2026-03-30 09:45:00', 'termine', 5,  4000),

-- Avril 2026 (en cours et planifiés)
(1, 5, 6,  '2026-04-01 06:00:00', '2026-04-01 07:30:00', 'termine', 54, 135000),
(2, 6, 7,  '2026-04-02 07:00:00', '2026-04-02 09:00:00', 'termine', 21, 63000),
(3, 7, 8,  '2026-04-03 07:30:00', '2026-04-03 08:15:00', 'termine', 57, 28500),
(4, 8, 9,  '2026-04-04 09:00:00', '2026-04-04 10:00:00', 'termine', 19, 95000),
(6, 9, 10, '2026-04-05 07:30:00', '2026-04-05 07:55:00', 'termine', 24, 9600),
(1, 1, 1,  '2026-04-07 06:00:00', NULL,                  'en_cours', 42, 105000),
(3, 2, 2,  '2026-04-07 07:30:00', NULL,                  'en_cours', 20, 10000),
(5, 3, 6,  '2026-04-08 05:30:00', NULL,                  'planifie',  0,  0),
(7, 4, 7,  '2026-04-08 08:00:00', NULL,                  'planifie',  0,  0);

-- ── Nouveaux incidents ───────────────────────────────────────
INSERT INTO incidents (trajet_id, type, description, gravite, date_incident, resolu) VALUES
(9,  'retard',   'Travaux sur la route de Rufisque',            'faible', '2026-01-20 09:20:00', TRUE),
(11, 'panne',    'Problème de batterie, véhicule immobilisé',   'moyen',  '2026-01-28 07:00:00', TRUE),
(13, 'retard',   'Embouteillage à la sortie de Dakar',          'faible', '2026-02-02 06:45:00', TRUE),
(19, 'accident', 'Collision légère avec un deux-roues',         'grave',  '2026-02-18 06:30:00', FALSE),
(25, 'panne',    'Surchauffe moteur, arrêt forcé',              'moyen',  '2026-03-03 07:40:00', TRUE),
(28, 'retard',   'Contrôle de police sur la nationale',         'faible', '2026-03-15 06:15:00', TRUE),
(33, 'autre',    'Passager malaise, arrêt médical',             'moyen',  '2026-03-25 06:50:00', TRUE),
(38, 'panne',    'Crevaison pneu arrière gauche',               'faible', '2026-04-02 07:30:00', FALSE),
(40, 'retard',   'Manifestation bloquant le Plateau',           'moyen',  '2026-04-05 07:45:00', FALSE);

-- ── Vérification ─────────────────────────────────────────────
SELECT 'vehicules'  as table_name, COUNT(*) as total FROM vehicules  UNION ALL
SELECT 'chauffeurs',                COUNT(*)           FROM chauffeurs UNION ALL
SELECT 'lignes',                    COUNT(*)           FROM lignes     UNION ALL
SELECT 'trajets',                   COUNT(*)           FROM trajets    UNION ALL
SELECT 'incidents',                 COUNT(*)           FROM incidents;
