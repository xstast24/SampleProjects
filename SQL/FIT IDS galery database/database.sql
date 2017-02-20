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

/*naplnit tabulku Zamestnanec*/
INSERT INTO Zamestnanec (IDZamestnance, jmeno, prijmeni, ulice, mesto, rodne_cislo, postaveni) VALUES ('1', 'Karel', 'Karlenko', 'Dlouh�', 'Brno', '8507012129', 'vedouc�');
INSERT INTO Zamestnanec (IDZamestnance, jmeno, prijmeni, ulice, mesto, rodne_cislo, postaveni) VALUES ('2', 'Ivan', 'Ivanovski', 'Kr�tk�', 'Brno', '8507012140', 'zam�stnanec');
INSERT INTO Zamestnanec (IDZamestnance, jmeno, prijmeni, ulice, mesto, rodne_cislo, postaveni) VALUES ('3', 'De�o', 'Demeter', 'Dlouh�', 'Praha', '8507012151', 'zam�stnanec');

/*naplnit tabulku Zakaznik*/
INSERT INTO Zakaznik (IDZakaznika, ulice, mesto, telefon, typ, jmeno, prijmeni, jmeno_firmy, ICO) VALUES ('1', 'St�edn�', 'Popovice', '777696969', 'FO', 'Boris', 'Zbo�il', '', '');
INSERT INTO Zakaznik (IDZakaznika, ulice, mesto, telefon, typ, jmeno, prijmeni, jmeno_firmy, ICO) VALUES ('2', 'Dlouh�', 'Brno', '777666666', 'FO', 'Boris', 'Zbo�il', '', '');
INSERT INTO Zakaznik (IDZakaznika, ulice, mesto, telefon, typ, jmeno, prijmeni, jmeno_firmy, ICO) VALUES ('3', 'St�edn� dlouh�', 'Rajhrad', '777999999', 'PO', '', '', 'Yolo, s.r.o.', '12345679');

/*naplnit tabulku Expozice*/
INSERT INTO Expozice (IDExpozice, IDZakaznika, IDZamestnance, typ_expozice, vystavena_od, vystavena_do) VALUES ('1', '1', '2', 'drah�', '20.03.1891', '23.02.2020');
INSERT INTO Expozice (IDExpozice, IDZakaznika, IDZamestnance, typ_expozice, vystavena_od, vystavena_do) VALUES ('2', '3', '3', 'levn�', '20.03.2012', '23.02.2018');

/*naplnit tabulku Dilo*/
INSERT INTO Dilo (nazev, IDExpozice, autor, typ_dila, cena, IDMista) VALUES ('Rann� obloha', '1', 'Milo� Heydrich', 'obraz', '105', '1'); 
INSERT INTO Dilo (nazev, IDExpozice, autor, typ_dila, cena, IDMista) VALUES ('Odpoledn� obloha', '1', 'Adolf Zeman', 'obraz', '1800', '2');
INSERT INTO Dilo (nazev, IDExpozice, autor, typ_dila, cena, IDMista) VALUES ('Ve�ern� obloha', '1', 'Reinhard Obama', 'obraz', '150000', '3');

INSERT INTO Dilo (nazev, IDExpozice, autor, typ_dila, cena, IDMista) VALUES ('Vol�n� divo�iny', '2', 'Miroslav Frosty', 'obraz', '15000', '4');
INSERT INTO Dilo (nazev, IDExpozice, autor, typ_dila, cena, IDMista) VALUES ('Pan tvr��k', '2', 'Rudolf Rud�', 'socha', '50000', '5');

/*naplnit tabulku Mistnost*/
INSERT INTO Mistnost (IDMistnosti, klimatizace, vlhkost_vzduchu, bezbarierovy_pristup, bezpecnostni_kamery) VALUES ('1', 'Ano', '30', 'Ano', 'Ano');
INSERT INTO Mistnost (IDMistnosti, klimatizace, vlhkost_vzduchu, bezbarierovy_pristup, bezpecnostni_kamery) VALUES ('2', 'Ne', '50', 'Ne', 'Ano');

/*naplnit tabulku Misto*/
INSERT INTO Misto (IDMista, IDMistnosti, IDExpozice, IDZamestnance, pronajato_od, pronajato_do, typ_mista, typ_osvetleni, alarm, velikost, cena_za_pronajem, stav_platby) VALUES ('1', '1', '1', '3', '01.01.1899', '10.10.2028', 'st�na', 'z��ivka', 'Ne', '4', '900', 'zaplaceno'); 
INSERT INTO Misto (IDMista, IDMistnosti, IDExpozice, IDZamestnance, pronajato_od, pronajato_do, typ_mista, typ_osvetleni, alarm, velikost, cena_za_pronajem, stav_platby) VALUES ('2', '1', '1', '3', '01.02.1893', '01.10.2025', 'st�na', 'LED', 'Ano', '8', '1500', 'zaplaceno');
INSERT INTO Misto (IDMista, IDMistnosti, IDExpozice, IDZamestnance, pronajato_od, pronajato_do, typ_mista, typ_osvetleni, alarm, velikost, cena_za_pronajem, stav_platby) VALUES ('3', '1', '1', '3', '01.01.1918', '25.10.2148', 'st�na', 'LED', 'Ano', '8', '1600', 'zaplaceno');

INSERT INTO Misto (IDMista, IDMistnosti, IDExpozice, IDZamestnance, pronajato_od, pronajato_do, typ_mista, typ_osvetleni, alarm, velikost, cena_za_pronajem, stav_platby) VALUES ('4', '2', '2', '2', '01.05.2012', '10.11.2025', 'st�na', 'LED', 'Ano', '6', '1500', 'zaplaceno');
INSERT INTO Misto (IDMista, IDMistnosti, IDExpozice, IDZamestnance, pronajato_od, pronajato_do, typ_mista, typ_osvetleni, alarm, velikost, cena_za_pronajem, stav_platby) VALUES ('5', '2', '2', '2', '10.12.2012', '10.11.2024', 'podstavec', 'z��ivka', 'Ano', '4', '800', 'zaplaceno');


/*SELECT 2x spojeni dvou tabulek*/
--vyp�e d�la, jejich� cena za pron�jem m�sta je v�t��, ne� 1000 K�
SELECT nazev, autor, cena_za_pronajem
FROM Dilo NATURAL JOIN Misto
WHERE cena_za_pronajem > 1000;
--vyp�e m�sta, o kter� se star� zam�stnanec Ivan Ivanovski
SELECT jmeno, prijmeni, IDMista stara_se_o_misto_ID
FROM Misto NATURAL JOIN Zamestnanec
WHERE IDZamestnance = 2;

/*SELECT 1x spojen� 3 tabulek*/
--vyp�e v�echna d�la a zam�stnance, kte�� se o n� staraj�
SELECT nazev, autor, IDZamestnance, jmeno, prijmeni
FROM Dilo NATURAL JOIN Misto NATURAL JOIN Zamestnanec;

/*SELECT 2x GROUP BY a agrega�n� funkce*/
--vyp�e kolik dohromady stoj� d�la v ka�d� m�stnosti
SELECT Mistnost.IDMistnosti, SUM(cena) cena_celkem
FROM Mistnost, Misto, Dilo
WHERE Mistnost.IDMistnosti = Misto.IDMistnosti AND Misto.IDMISTA = Dilo.IDMISTA
GROUP BY Mistnost.IDMISTNOSTI;

--vyp�e po�et d�l vystaven�ch v ka�d� m�stnosti
SELECT Mistnost.IDMistnosti, COUNT(*) pocet_del
FROM Mistnost, Misto, Dilo
WHERE Mistnost.IDMistnosti = Misto.IDMistnosti AND Misto.IDMISTA = Dilo.IDMISTA
GROUP BY Mistnost.IDMISTNOSTI;

/*SELECT 1x dotaz obsahuj�c� predik�t EXISTS*/
--vyp�e zam�stnance, kte�� se staraj� pouze o m�sta typu "st�na" (obrazy)
SELECT DISTINCT Zamestnanec.IDZamestnance, Zamestnanec.jmeno, Zamestnanec.prijmeni
FROM Zamestnanec, Misto
WHERE Zamestnanec.IDZamestnance = Misto.IDZamestnance AND Misto.typ_mista = 'st�na' AND 
     NOT EXISTS (SELECT *
                 FROM Misto
                 WHERE Zamestnanec.IDZamestnance = Misto.IDZamestnance AND Misto.typ_mista <> 'st�na');

/*SELECT 1x dotaz s predik�tem IN s vno�en�m selectem*/
--vyp�e zam�stnance, kte�� se staraj� o d�la s v�t�� hodnotou, ne� 100 000 K�
SELECT DISTINCT Zamestnanec.IDZamestnance, Zamestnanec.jmeno, Zamestnanec.prijmeni
FROM Zamestnanec
WHERE IDZamestnance IN
     (SELECT IDZamestnance
     FROM Misto
     WHERE IDmista IN
          (SELECT IDMista
          FROM Dilo
          WHERE cena > 100000));
          