BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "bodyweight_log" (
	"id"	INTEGER,
	"dato"	TEXT NOT NULL,
	"vaegt"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "exercises" (
	"id"	INTEGER,
	"dag"	TEXT NOT NULL,
	"oevelse_navn"	TEXT NOT NULL,
	"saet_reps"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "sets" (
	"id"	INTEGER,
	"dato"	TEXT NOT NULL,
	"ovelse"	TEXT NOT NULL,
	"vaegt"	REAL NOT NULL,
	"reps"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "workout_exercises" (
	"id"	INTEGER,
	"session_id"	INTEGER,
	"exercise_name"	TEXT NOT NULL,
	"weight"	REAL NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("session_id") REFERENCES "workout_sessions"("id")
);
CREATE TABLE IF NOT EXISTS "workout_sessions" (
	"id"	INTEGER,
	"dato"	TEXT NOT NULL UNIQUE,
	"noter"	TEXT DEFAULT '',
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "workout_sets" (
	"id"	INTEGER,
	"session_id"	INTEGER NOT NULL,
	"ovelse"	TEXT NOT NULL,
	"vaegt"	REAL NOT NULL,
	"reps"	INTEGER NOT NULL,
	"estimeret_1rm"	REAL NOT NULL,
	"noter"	TEXT DEFAULT '',
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("session_id") REFERENCES "workout_sessions"("id") ON DELETE CASCADE
);
INSERT INTO "exercises" VALUES (28,'Mandag','Incline chest press (+ Mavetræning)','3 × 6-8');
INSERT INTO "exercises" VALUES (29,'Mandag','Up-rope flyer','3 × 6-8');
INSERT INTO "exercises" VALUES (30,'Mandag','Fly machine','3 × 8-10');
INSERT INTO "exercises" VALUES (31,'Mandag','Triceps pushdown ropes','3 × 10-12');
INSERT INTO "exercises" VALUES (32,'Tirsdag','Lat-pulldown cable machine','3 × 8-10');
INSERT INTO "exercises" VALUES (33,'Tirsdag','Cable rows','3 × 6-8');
INSERT INTO "exercises" VALUES (34,'Tirsdag','Back fly cable tower','3 × 8-10');
INSERT INTO "exercises" VALUES (35,'Tirsdag','Seated lateral raises','3 × 10-12');
INSERT INTO "exercises" VALUES (36,'Tirsdag','Preacher curls','3 × 8-10');
INSERT INTO "exercises" VALUES (37,'Onsdag','Leg-press','3 × 8-10');
INSERT INTO "exercises" VALUES (38,'Onsdag','Split squat','3 × 6-8');
INSERT INTO "exercises" VALUES (39,'Onsdag','Leg Extension','3 × 8-10');
INSERT INTO "exercises" VALUES (40,'Onsdag','Leg curls','3 × 8-10');
INSERT INTO "exercises" VALUES (41,'Onsdag','Calf raises','3 × 8-10');
INSERT INTO "exercises" VALUES (42,'Torsdag','Bænkpres (+ Mavetræning)','3 × 6-8');
INSERT INTO "exercises" VALUES (43,'Torsdag','Shoulder Press dumbbell','3 × 8-10');
INSERT INTO "exercises" VALUES (44,'Torsdag','Incline dumbbell fly','3 × 8-10');
INSERT INTO "exercises" VALUES (45,'Torsdag','Triceps pushdown rod','3 × 10-12');
INSERT INTO "exercises" VALUES (46,'Fredag','Barbell rows','3 × 6-8');
INSERT INTO "exercises" VALUES (47,'Fredag','Bicep Lat-pulldown cable machine','3 × 8-10');
INSERT INTO "exercises" VALUES (48,'Fredag','Straight-arm cable pulldown','3 × 10-12');
INSERT INTO "exercises" VALUES (49,'Fredag','Seated incline bicep curl','3 × 8-10');
INSERT INTO "exercises" VALUES (50,'Søndag','Hack squad','3 × 6-8');
INSERT INTO "exercises" VALUES (51,'Søndag','Rumænsk Dødløft','3 × 8-10');
INSERT INTO "exercises" VALUES (52,'Søndag','Supersæt: Hip abductor and adductor machine','3 × 8-10');
INSERT INTO "exercises" VALUES (53,'Søndag','Leg Extension','3 × 8-10');
INSERT INTO "exercises" VALUES (54,'Søndag','Leg curl','3 × 8-10');
INSERT INTO "workout_sessions" VALUES (1,'2026-10-20','');
INSERT INTO "workout_sets" VALUES (1,1,'Back fly cable tower',80.0,5,93.3,'');
COMMIT;
