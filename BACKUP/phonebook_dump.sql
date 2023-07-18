BEGIN TRANSACTION;
CREATE TABLE "contacts" (
	"contact_id"	INTEGER,
	"first_name"	TEXT,
	"last_name"	TEXT,
	"email_address"	TEXT,
	"phone_number"	TEXT,
	PRIMARY KEY("contact_id" AUTOINCREMENT)
);
INSERT INTO "contacts" VALUES(27,'Larry','David','larryd@cye.com','+555-000001');
INSERT INTO "contacts" VALUES(28,'Jeff','Green','jeffg@cye.com','+555-000002');
INSERT INTO "contacts" VALUES(29,'Cherryl','David','cherryld@cye.com','+555-000003');
INSERT INTO "contacts" VALUES(30,'Susan','Green','suzzyg@cye.com','+555-000004');
INSERT INTO "contacts" VALUES(31,'Ted','Danson','teddyd@cye.com','+555-000005');
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('contacts',31);
COMMIT;
