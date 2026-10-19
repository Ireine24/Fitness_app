-- SQLite Schema: Opdelt i Træningspas og Løft/Sæt

BEGIN TRANSACTION;

-- 1. Træningspas (Sessions)
CREATE TABLE IF NOT EXISTS workout_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dato TEXT NOT NULL UNIQUE,
    noter TEXT DEFAULT ''
);

-- 2. Enkelte løft/sæt tilknyttet et specifikt træningspas
CREATE TABLE IF NOT EXISTS workout_sets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    ovelse TEXT NOT NULL,
    vaegt REAL NOT NULL,
    reps INTEGER NOT NULL,
    estimeret_1rm REAL NOT NULL,
    noter TEXT DEFAULT '',
    FOREIGN KEY (session_id) REFERENCES workout_sessions(id) ON DELETE CASCADE
);

-- 3. Kropsvægt
CREATE TABLE IF NOT EXISTS bodyweight_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dato TEXT NOT NULL,
    vaegt REAL NOT NULL
);

-- Data: Opret træningspas fra din log
INSERT INTO workout_sessions (id, dato, noter) VALUES (1, '2026-01-05', '');
INSERT INTO workout_sessions (id, dato, noter) VALUES (2, '2026-01-07', '');
INSERT INTO workout_sessions (id, dato, noter) VALUES (3, '2026-01-12', '');
INSERT INTO workout_sessions (id, dato, noter) VALUES (4, '2026-01-14', '');
INSERT INTO workout_sessions (id, dato, noter) VALUES (5, '2026-01-19', '');
INSERT INTO workout_sessions (id, dato, noter) VALUES (6, '2026-01-21', '');
INSERT INTO workout_sessions (id, dato, noter) VALUES (7, '2026-01-26', '');
INSERT INTO workout_sessions (id, dato, noter) VALUES (8, '2026-01-28', '');
INSERT INTO workout_sessions (id, dato, noter) VALUES (9, '2026-02-02', '');
INSERT INTO workout_sessions (id, dato, noter) VALUES (10, '2026-02-04', '');

-- Data: Sæt tilknyttet passene
INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (1, 'Bænkpres', 70.0, 8, 88.7, 'Første pas');
INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (1, 'Bænkpres', 72.5, 6, 87.0, 'God fart');
INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (1, 'Squat', 90.0, 6, 108.0, 'Dybde i orden');

INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (2, 'Dødløft', 110.0, 5, 128.3, 'Føles let');

INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (3, 'Bænkpres', 72.5, 8, 91.8, 'Stærkt');
INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (3, 'Squat', 95.0, 6, 114.0, 'God kontrol');

INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (4, 'Dødløft', 115.0, 5, 134.2, 'Grebet holdt fint');

INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (5, 'Bænkpres', 75.0, 6, 90.0, 'God teknik');
INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (5, 'Squat', 97.5, 5, 113.8, 'Lidt tung');

INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (6, 'Dødløft', 120.0, 5, 140.0, 'PR');

INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (7, 'Bænkpres', 75.0, 8, 95.0, 'Ny rep PR!');
INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (7, 'Squat', 100.0, 5, 116.7, 'Tre-cifret');

INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (8, 'Dødløft', 122.5, 5, 142.9, 'Fokus på spænd');

INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (9, 'Bænkpres', 77.5, 6, 93.0, 'Fint overskud');
INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (9, 'Squat', 105.0, 5, 122.5, 'Stærk form');

INSERT INTO workout_sets (session_id, ovelse, vaegt, reps, estimeret_1rm, noter) VALUES (10, 'Dødløft', 125.0, 5, 145.8, 'Kørte rent igennem');

-- Data: Kropsvægt
INSERT INTO bodyweight_log (dato, vaegt) VALUES ('2026-10-14', 85.0);
INSERT INTO bodyweight_log (dato, vaegt) VALUES ('2026-10-16', 90.0);

COMMIT;