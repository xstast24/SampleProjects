DROP TABLE Dilo CASCADE CONSTRAINTS;
DROP TABLE Expozice CASCADE CONSTRAINTS;
DROP TABLE Zamestnanec CASCADE CONSTRAINTS;
DROP TABLE Zakaznik CASCADE CONSTRAINTS;
DROP TABLE Mistnost CASCADE CONSTRAINTS;
DROP TABLE Misto CASCADE CONSTRAINTS;


CREATE TABLE Dilo (
nazev                   varchar(50) PRIMARY KEY,
IDExpozice              integer NOT NULL,
autor                   varchar(50),
typ_dila                varchar(50),
cena                    integer,
IDMista				integer NOT NULL
);
CREATE INDEX dilo_typ_dila on Dilo(typ_dila);

CREATE TABLE Expozice (
IDExpozice              integer PRIMARY KEY,
IDZakaznika             integer NOT NULL,
IDZamestnance           integer NOT NULL,
typ_expozice            varchar(50),
vystavena_od            varchar(30),
vystavena_do            varchar(30)
);

CREATE TABLE Zamestnanec (
IDZamestnance           integer PRIMARY KEY,
jmeno                   varchar(20),
prijmeni                varchar(30),
ulice                   varchar(50),
mesto                   varchar(50),
rodne_cislo             integer,
postaveni               varchar(15)
);

CREATE TABLE Zakaznik (
IDZakaznika             integer PRIMARY KEY,
ulice                   varchar(50),
mesto                   varchar(50),
telefon                 integer,
typ                     varchar(10),
jmeno                   varchar(50),
prijmeni                varchar(50),
jmeno_firmy             varchar(100),
ICO                     integer
);

CREATE TABLE Mistnost (
IDMistnosti             integer PRIMARY KEY,
klimatizace             varchar (10),
vlhkost_vzduchu         integer,
bezbarierovy_pristup    varchar (10),
bezpecnostni_kamery     varchar (10)
);

CREATE TABLE Misto (
IDMista                 integer PRIMARY KEY,
IDMistnosti             integer NOT NULL,
IDExpozice              integer NOT NULL,
IDZamestnance            integer,
pronajato_od            varchar(30),
pronajato_do            varchar(30),
typ_mista               varchar(30),
typ_osvetleni           varchar(30),
alarm                   varchar(5),
velikost                integer NOT NULL,
cena_za_pronajem        integer NOT NULL,
stav_platby             varchar(20)
);


ALTER TABLE Dilo
ADD (CONSTRAINT FK_IDExpozice
FOREIGN KEY (IDExpozice)
REFERENCES Expozice,
CONSTRAINT CHECK_cena
CHECK (1 <= cena));

ALTER TABLE Expozice
ADD (CONSTRAINT FK_IDZakaznika
FOREIGN KEY (IDZakaznika)
REFERENCES Zakaznik,
CONSTRAINT FK_IDZamestnance
FOREIGN KEY (IDZamestnance)
REFERENCES Zamestnanec);

ALTER TABLE Misto
ADD (CONSTRAINT FK_IDMistnosti
FOREIGN KEY (IDMistnosti)
REFERENCES Mistnost,
CONSTRAINT FK_Misto_IDExpozice
FOREIGN KEY (IDExpozice)
REFERENCES Expozice,
CONSTRAINT CHECK_cena_za_pronajem
CHECK (1 <= cena_za_pronajem));

ALTER TABLE Zakaznik
ADD CONSTRAINT CHECK_Zakaznik_ICO
CHECK (LENGTH(TRIM(ICO))=8);

ALTER TABLE Zamestnanec
ADD CONSTRAINT CHECK_rodne_cislo
CHECK ((MOD(rodne_cislo,11)=0)AND(LENGTH(TRIM(rodne_cislo))=9 OR LENGTH(TRIM(rodne_cislo))=10));

--2x TRIGGER
--trigger na mazani zaznamu mistnost - misto, maze prikazem DELETE FROM Mistnost WHERE IDMistnosti=2;
CREATE OR REPLACE
TRIGGER DEMOLICE
BEFORE DELETE ON Mistnost
FOR EACH ROW DECLARE ID Mistnost.IDMistnosti%TYPE;
BEGIN
ID :=: OLD.IDMistnosti;
DELETE FROM Misto
WHERE IDMistnosti=ID;
END;
/

--triger na cislovani zaznamu ID v tabulce
DROP SEQUENCE seq_IDZamestnance;
CREATE SEQUENCE seq_IDZamestnance
INCREMENT BY 1
START WITH 1 ORDER;

CREATE OR REPLACE
TRIGGER CISLOVANI
BEFORE INSERT ON ZAMESTNANEC
FOR EACH ROW
BEGIN
  SELECT seq_IDZamestnance.NEXTVAL
  INTO :new.IDZamestnance
  FROM dual;
END;
/

/*naplnit tabulku Zamestnanec*/
INSERT INTO Zamestnanec (IDZamestnance, jmeno, prijmeni, ulice, mesto, rodne_cislo, postaveni) VALUES ('1', 'Karel', 'Karlenko', 'Dlouhá', 'Brno', '8507012129', 'vedoucí');
INSERT INTO Zamestnanec (IDZamestnance, jmeno, prijmeni, ulice, mesto, rodne_cislo, postaveni) VALUES ('2', 'Ivan', 'Ivanovski', 'Krátká', 'Brno', '8507012140', 'zamìstnanec');
INSERT INTO Zamestnanec (IDZamestnance, jmeno, prijmeni, ulice, mesto, rodne_cislo, postaveni) VALUES ('', 'Dežo', 'Demeter', 'Dlouhá', 'Praha', '8507012151', 'zamìstnanec');

/*naplnit tabulku Zakaznik*/
INSERT INTO Zakaznik (IDZakaznika, ulice, mesto, telefon, typ, jmeno, prijmeni, jmeno_firmy, ICO) VALUES ('1', 'Støední', 'Popovice', '777696969', 'FO', 'Boris', 'Zboøil', '', '');
INSERT INTO Zakaznik (IDZakaznika, ulice, mesto, telefon, typ, jmeno, prijmeni, jmeno_firmy, ICO) VALUES ('2', 'Dlouhá', 'Brno', '777666666', 'FO', 'Boris', 'Zboøil', '', '');
INSERT INTO Zakaznik (IDZakaznika, ulice, mesto, telefon, typ, jmeno, prijmeni, jmeno_firmy, ICO) VALUES ('3', 'Støednì dlouhá', 'Rajhrad', '777999999', 'PO', '', '', 'Yolo, s.r.o.', '12345679');

/*naplnit tabulku Expozice*/
INSERT INTO Expozice (IDExpozice, IDZakaznika, IDZamestnance, typ_expozice, vystavena_od, vystavena_do) VALUES ('1', '1', '2', 'drahá', '20.03.1891', '23.02.2020');
INSERT INTO Expozice (IDExpozice, IDZakaznika, IDZamestnance, typ_expozice, vystavena_od, vystavena_do) VALUES ('2', '3', '3', 'levná', '20.03.2012', '23.02.2018');

/*naplnit tabulku Dilo*/
INSERT INTO Dilo (nazev, IDExpozice, autor, typ_dila, cena, IDMista) VALUES ('Ranní obloha', '1', 'Miloš Heydrich', 'obraz', '105', '1'); 
INSERT INTO Dilo (nazev, IDExpozice, autor, typ_dila, cena, IDMista) VALUES ('Odpolední obloha', '1', 'Adolf Zeman', 'obraz', '1800', '2');
INSERT INTO Dilo (nazev, IDExpozice, autor, typ_dila, cena, IDMista) VALUES ('Veèerní obloha', '1', 'Reinhard Obama', 'obraz', '150000', '3');

INSERT INTO Dilo (nazev, IDExpozice, autor, typ_dila, cena, IDMista) VALUES ('Volání divoèiny', '2', 'Miroslav Frosty', 'obraz', '15000', '4');
INSERT INTO Dilo (nazev, IDExpozice, autor, typ_dila, cena, IDMista) VALUES ('Pan tvrïák', '2', 'Rudolf Rudý', 'socha', '50000', '5');

/*naplnit tabulku Mistnost*/
INSERT INTO Mistnost (IDMistnosti, klimatizace, vlhkost_vzduchu, bezbarierovy_pristup, bezpecnostni_kamery) VALUES ('1', 'Ano', '30', 'Ano', 'Ano');
INSERT INTO Mistnost (IDMistnosti, klimatizace, vlhkost_vzduchu, bezbarierovy_pristup, bezpecnostni_kamery) VALUES ('2', 'Ne', '50', 'Ne', 'Ano');

/*naplnit tabulku Misto*/
INSERT INTO Misto (IDMista, IDMistnosti, IDExpozice, IDZamestnance, pronajato_od, pronajato_do, typ_mista, typ_osvetleni, alarm, velikost, cena_za_pronajem, stav_platby) VALUES ('1', '1', '1', '3', '01.01.1899', '10.10.2028', 'stìna', 'záøivka', 'Ne', '4', '900', 'zaplaceno'); 
INSERT INTO Misto (IDMista, IDMistnosti, IDExpozice, IDZamestnance, pronajato_od, pronajato_do, typ_mista, typ_osvetleni, alarm, velikost, cena_za_pronajem, stav_platby) VALUES ('2', '1', '1', '3', '01.02.1893', '01.10.2025', 'stìna', 'LED', 'Ano', '8', '1500', 'zaplaceno');
INSERT INTO Misto (IDMista, IDMistnosti, IDExpozice, IDZamestnance, pronajato_od, pronajato_do, typ_mista, typ_osvetleni, alarm, velikost, cena_za_pronajem, stav_platby) VALUES ('3', '1', '1', '3', '01.01.1918', '25.10.2148', 'stìna', 'LED', 'Ano', '8', '1600', 'zaplaceno');

INSERT INTO Misto (IDMista, IDMistnosti, IDExpozice, IDZamestnance, pronajato_od, pronajato_do, typ_mista, typ_osvetleni, alarm, velikost, cena_za_pronajem, stav_platby) VALUES ('4', '2', '2', '2', '01.05.2012', '10.11.2025', 'stìna', 'LED', 'Ano', '6', '1500', 'zaplaceno');
INSERT INTO Misto (IDMista, IDMistnosti, IDExpozice, IDZamestnance, pronajato_od, pronajato_do, typ_mista, typ_osvetleni, alarm, velikost, cena_za_pronajem, stav_platby) VALUES ('5', '2', '2', '2', '10.12.2012', '10.11.2024', 'podstavec', 'záøivka', 'Ano', '4', '800', 'zaplaceno');

--INDEX EXPLAIN PLAN
--vypíše nároènost a postup operace pro výpis všech dìl urèitého typu a informací, kde se nachází
EXPLAIN PLAN FOR
SELECT /*+ INDEX(Dilo, dilo_typ_dila) */ *
FROM Dilo NATURAL JOIN Misto
WHERE typ_dila = 'socha';

SELECT plan_table_output
FROM table(dbms_xplan.display('plan_table'));

--EXPLAIN PLAN
--vypíše nároènost a postup operace pro výpis poètu dìl vystavených v každé místnosti
--index pro urychleni pouzity u dilo.typ_dila (obraz, socha, ...)
EXPLAIN PLAN FOR
SELECT IDMistnosti, COUNT(*) pocet_del
FROM Mistnost NATURAL JOIN Misto NATURAL JOIN Dilo
WHERE typ_dila = 'obraz'
GROUP BY IDMISTNOSTI;

SELECT plan_table_output
FROM table(dbms_xplan.display('plan_table'));

--MATERIALIZED VIEW, vypise dila jedne expozice
DROP MATERIALIZED VIEW dila_expozice;
create materialized view dila_expozice
nologging 
cache 
build immediate
enable query rewrite 
as
SELECT xstast24.Expozice.IDExpozice, xstast24.Dilo.nazev, xstast24.Dilo.autor
FROM xstast24.Dilo, xstast24.Expozice
WHERE xstast24.Dilo.IDExpozice = xstast24.Expozice.IDExpozice AND xstast24.Dilo.IDExpozice = '1';

--MATERIALIZED VIEW EXPLAIN PLAN
EXPLAIN PLAN FOR SELECT * FROM xstast24.dila_expozice;
SELECT plan_table_output
FROM table(dbms_xplan.display());

--udeleni prav
GRANT ALL ON Dilo TO xjochl00;
GRANT ALL ON Expozice TO xjochl00;
GRANT ALL ON Misto TO xjochl00;
GRANT ALL ON Zamestnanec TO xjochl00;
GRANT ALL ON Zakaznik TO xjochl00;
GRANT ALL ON Mistnost TO xjochl00;
GRANT ALL ON seq_IDZamestnance TO xjochl00;
GRANT ALL ON dila_expozice TO xjochl00;

--KURZOR
/*
DECLARE CURSOR kurzor IS
FOR
SELECT Dilo.nazev, Dilo.typ_dila
FROM Dilo, Expozice
WHERE Dilo.IDExpozice = Expozice.IDExpozice AND Dilo.typ_dila = 'obraz';
*/

--procedura
/*
CREATE OR REPLACE
PROCEDURE remove_dilo (typ_dila VARCHAR) AS
BEGIN
     DELETE FROM Dilo
     WHERE Dilo.typ_dila = remove_dilo.typ_dila;
END;
/
*/



