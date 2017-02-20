#include <stdio.h>
#include <string>
#include <time.h>
#include <unistd.h>
#include "simlib.h"
#include <vector>
#include <iostream>


using namespace std;


//casove jednotky
#define VTERINA 1
#define MINUTA 60*VTERINA
#define HODINA 60*MINUTA

#define START_SIMULACE 0
#define DOBA_TRVANI_SIMULACE 3*HODINA

#define INTERVAL_HISTOGRAMU 40*VTERINA
#define POCET_INTERVALU 10

//kapacitni limity restaurace
#define LIMIT_POKLADEN 5
#define LIMIT_KUCHARU 10
#define LIMIT_VYDEJCU 5

//limitni delky fronty
#define PRILIS_DLOUHA_FRONTA 6	//lide mohou zacit odchazet ihned po prichodu
#define PRILIS_DLOUHA_FRONTA_POKLADNY 8	//manager pujde pomoci pokladnam
#define PRILIS_DLOUHA_FRONTA_KUCHARI 20	//manager pujde pomoci do kuchyne
#define PRILIS_DLOUHA_FRONTA_VYDEJ 7	//manager pujde pomoci vydavat objednavky

// defaultni hodnoty pro obsluhu linky
#define DEFAULT_POKLADNY 2
#define DEFAULT_KUCHARI 5
#define DEFAULT_VYDEJCI 3

//define cekacich a generacnich parametru
#define EXP_DOBA_GENEROVANI_ZAKAZNIKA 15
#define EXP_DOBA_POZDRAVENI 5
#define DOBA_KLADENI_OTAZKY 10
#define UNIF_DOBA_PLACENI_MIN 3
#define UNIF_DOBA_PLACENI_MAX 23

//objednavky
#define PITI 0.20
#define HRANOLKY 0.42
#define MALY_BURGER 0.72
#define VELKY_BURGER 0.92
#define SALAT 1

//doba objednavky jidel
#define EXP_DOBA_OBJEDNANI_MALEHO_BURGERU 2
#define EXP_DOBA_OBJEDNANI_VELKEHO_BURGERU 4
#define EXP_DOBA_OBJEDNANI_HRANOLEK 3
#define EXP_DOBA_OBJEDNANI_PITI 4
#define EXP_DOBA_OBJEDNANI_SALATU 7

//predpripravene jidlo
#define PREDPRIPRAVENO_MALYCH_BURGERU 12
#define PREDPRIPRAVENO_VELKYCH_BURGERU 3
#define PREDPRIPRAVENO_HRANOLEK 15
#define PREDPRIPRAVENO_SALATU 4

//doba pripravy jidel v sekundach
#define DOBA_PRIPRAVY_VARKY_MALYCH_BURGERU 72	//pripravuji se po 1-8 kusech dle situace, behem obeda po 8
#define DOBA_PRIPRAVY_VELKEHO_BURGERU 27
#define DOBA_PRIPRAVY_VARKY_HRANOLEK 10	//kuchar da zmrazene hranolky smazit
#define DOBA_SMAZENI_HRANOLEK 180	//hranolky se smazi, neni potreba pritomnosti kuchare
#define DOBA_PRIPRAVY_VARKY_SALATU 110

//pocet kusu jidla v 1 varce
#define VARKA_MALYCH_BURGERU 8
#define VARKA_HRANOLEK 12
#define VARKA_SALATU 4

//doba baleni jidel v sekundach
#define EXP_DOBA_PRIPRAVY_A_DOKONCENI_BALENI 7
#define DOBA_BALENI_MALEHO_BURGERU 3
#define DOBA_BALENI_VELKEHO_BURGERU 5
#define DOBA_BALENI_SALATU 4
#define EXP_DOBA_BALENI_PITI 6
#define DOBA_TOCENI_PITI 7
#define UNIF_DOBA_BALENI_HRANOLEK_MIN 4
#define UNIF_DOBA_BALENI_HRANOLEK_MAX 12

//perioda uklidu kuchyne - utreni garnyru, vymena hader,...
#define PERIODA_UKLIDU_KUCHYNE HODINA
#define DELKA_UKLIDU_KUCHYNE 2*MINUTA


//enumerate jidel
enum jidla {malyBurger, velkyBurger, hranolky, piti, salat};

//obsluha restaurace: objednani, priprava, baleni - defaultni hodnoty
int pocetPokladen = DEFAULT_POKLADNY;
int pocetKucharu = DEFAULT_KUCHARI;
int pocetVydejcu = DEFAULT_VYDEJCI;

//Predchystane zasoby
int nachystanoMalychBurgeru = PREDPRIPRAVENO_MALYCH_BURGERU;
int nachystanoVelkychBurgeru = PREDPRIPRAVENO_VELKYCH_BURGERU;
int nachystanoHranolek = PREDPRIPRAVENO_HRANOLEK;
int nachystanoSalatu = PREDPRIPRAVENO_SALATU;

//co bylo objednano/co se musi nachystat
int pripravMalyBurger = 0;
int pripravVelkyBurger = 0;
int pripravHranolky = 0;
int pripravPiti = 0;
int pripravSalat = 0;

//pocitani zakazniku do statistik
unsigned int pocetPrichozich = 0;
unsigned int pocetOdchozichKvuliFronte = 0;
unsigned int pocetObslouzenychUPokladny = 0;
unsigned int pocetJidelCelkem = 0;

//cas posledniho uklidu kuchyne - utreni garnyru, vymena hader,...
double casPoslednihoUkliduKuchyne = -600; //kuchyne se uklizi pred zacatkem obedove doby

//fronta objednanych jidel
vector<jidla> frontaJidel;

Store pokladny("pokladny", pocetPokladen); //store obsluznych linek ~ nekolik pokladen
Store vydejci("Vydejci", pocetVydejcu);
Store kuchari("Kuchari", pocetKucharu);
Stat dobaVeFronte("Doba cekani ve fronte u pokladny");
Stat dobaObjednavani("Doba objednavani u pokladny");
Stat dobaPripravyJidla("Doba pripravy jidla");
Stat dobaBaleniObjednavky("Doba baleni objednavky");
Stat dobaCekaniNaObjednavku("Celkova doba cekani na objednavku"); //cekani na pripravu jidla + baleni jidla
Stat dobaMeziUklidyKuchyne("Doba mezi uklidy kuchyne"); //kuchyne by se mela uklizet kazdou hodinu
Histogram dobaVRestauraci("Celkova doba stravena v restauraci (od vstoupeni do fronty)", 0, INTERVAL_HISTOGRAMU, POCET_INTERVALU); //histogram, zacina v par1, intervaly zaznamenava dlouhe par2, pocet intervalu je par3

//deklarace funkce pro zpracovani parametru
void zpracovaniParametru(int argc, char **argv);

//trida pro smazeni hranolek
class Hranolky : public Process {
public:
    void Behavior(){
        nachystanoHranolek += VARKA_HRANOLEK;
    }
};

//trida zakaznik
class Zakaznik : public Process {
public:
    double prichod, zacatekCekaniNaJidlo, dobaObjednani;
    int cisloZakaznika;
    vector<jidla> objednano;

    void Behavior(){
		bool objednavkaProbehla;
		bool odchazimKvuliFronte = false;

        prichod = Time; //ulozi cas prichodu do restaurace
		pocetPrichozich++; //pricte zakaznika do statistik
		cisloZakaznika = pocetPrichozich; //ulozi cislo zakaznika pro statistiku

		//zakaznik se rozhodne podle velikosti fronty, zda zustane, nebo nema cas a odejde
		if(pokladny.QueueLen() >= PRILIS_DLOUHA_FRONTA){
			if(Random()*160 < 3*pokladny.QueueLen()){ // % sance na okamzity odchod (zvysuje se s delkou fronty)
				odchazimKvuliFronte = true;
				pocetOdchozichKvuliFronte++;
				goto odchod;
			}
		}

        Enter(pokladny, 1); //prijde na pokladnu
        objednavkaProbehla = objednavani(); //zakaznik objednava
		pocetObslouzenychUPokladny++;
        Leave(pokladny, 1); //ma objednano, odchazi cekat na jidlo
		if(!objednavkaProbehla) goto odchod; //pokud si zakaznik nic neobjednal, odchazi z restaurace

		cekaniNaJidlo();	//TODO kdyz ceka moc dlouho, odejde? nebo jen naloguje?

		//bali se mu jidlo
		Enter(vydejci, 1);
		cekaniNaZabaleni();		//TODO kdyz ceka moc dlouho, odejde?
		Leave(vydejci, 1);

	odchod:
		if(!odchazimKvuliFronte){
			dobaVRestauraci(Time - prichod); //statistika doby stravene v restauraci od vstoupeni do fronty
		}
    }

	/*
	 * Zakaznik objednava jidlo, kazdy pokrm ma jistou sanci na objednani, u pokladny stravi zakaznik nahodny cas umerny velikosti objednavky.
	 */
	bool objednavani(){
		dobaObjednani = Exponential(EXP_DOBA_POZDRAVENI);
		float pocetObjednani = Exponential(2.83);
		float objednavka;
		if(pocetObjednani < 0.004){
			dobaObjednani += DOBA_KLADENI_OTAZKY;	//obcas si nic neobjedna, napr. ho rozzlobi cena nebo nemaji oblibenou sezonni prichut
			Wait(dobaObjednani);
			dobaObjednavani(dobaObjednani);
			return false;
		}
		while(pocetObjednani > 0) {
			   pocetObjednani--;
			   objednavka = Random();
			   if (objednavka <= PITI) {    //chci piti
				   objednano.push_back(piti);
				   dobaObjednani += Exponential(EXP_DOBA_OBJEDNANI_PITI);
			   } else if ((objednavka > PITI) && (objednavka <= HRANOLKY)) {    //chci hranolky
				   frontaJidel.push_back(hranolky);
				   objednano.push_back(hranolky);
				   dobaObjednani += Exponential(EXP_DOBA_OBJEDNANI_HRANOLEK);
			   } else if ((objednavka > HRANOLKY) && (objednavka <= MALY_BURGER)) {    //chci maly burger
				   frontaJidel.push_back(malyBurger);
				   objednano.push_back(malyBurger);
				   dobaObjednani += Exponential(EXP_DOBA_OBJEDNANI_MALEHO_BURGERU);
			   } else if ((objednavka > MALY_BURGER) && (objednavka <= VELKY_BURGER)) {    //chci velky burger
				   frontaJidel.push_back(velkyBurger);
				   objednano.push_back(velkyBurger);
				   dobaObjednani += Exponential(EXP_DOBA_OBJEDNANI_VELKEHO_BURGERU);
			   } else if ((objednavka > VELKY_BURGER) && (objednavka <= SALAT)) {        //chci salat
				   frontaJidel.push_back(salat);
				   objednano.push_back(salat);
				   dobaObjednani += Exponential(EXP_DOBA_OBJEDNANI_SALATU);
			   }
		}

		dobaObjednani += Uniform(UNIF_DOBA_PLACENI_MIN, UNIF_DOBA_PLACENI_MAX);
		Wait(dobaObjednani);
		dobaObjednavani(dobaObjednani); //statistika doby stravene objednavanim
		return true;
	}

	/*
	 * Zjistuje delku cekani na (ne)pripravene jidlo - zakaznik ceka, dokud neni hotove.
	 */
	void cekaniNaJidlo(){
		zacatekCekaniNaJidlo = Time;
		double nejdelsiPripravaJidla = 0;
		bool alreadyWaitedEnough = false;	//pokud cekal dost dlouho, nastavi 'true', nervozne preslapuje pred vydavacim pultem a vyznamne pokukuje na hodinky
		vector<jidla> cekamNaJidlo(objednano);

		while(cekamNaJidlo.size()>0){
			for(unsigned int i = 0; i < cekamNaJidlo.size(); i++){
				switch(cekamNaJidlo[i]){
					case malyBurger:
						if(nachystanoMalychBurgeru > 0){
							nachystanoMalychBurgeru--;
							cekamNaJidlo.erase(cekamNaJidlo.begin()+i);
							i--;
						}
						else{
							if(nejdelsiPripravaJidla < DOBA_PRIPRAVY_VARKY_MALYCH_BURGERU){
								nejdelsiPripravaJidla = DOBA_PRIPRAVY_VARKY_MALYCH_BURGERU;
							};
						}
						break;
					case velkyBurger:
						if(nachystanoVelkychBurgeru > 0){
							nachystanoVelkychBurgeru--;
							cekamNaJidlo.erase(cekamNaJidlo.begin()+i);
							i--;
						}
						else{
							if(nejdelsiPripravaJidla < DOBA_PRIPRAVY_VELKEHO_BURGERU){
								nejdelsiPripravaJidla = DOBA_PRIPRAVY_VELKEHO_BURGERU;
							};
						}
						break;
					case hranolky:
						if(nachystanoHranolek > 0){
							nachystanoHranolek--;
							cekamNaJidlo.erase(cekamNaJidlo.begin()+i);
							i--;
						}
						else{
							if(nejdelsiPripravaJidla < DOBA_PRIPRAVY_VARKY_HRANOLEK){
								nejdelsiPripravaJidla = DOBA_PRIPRAVY_VARKY_HRANOLEK;
							};
						}
						break;
					case piti:
						cekamNaJidlo.erase(cekamNaJidlo.begin()+i);
						i--;
						break;
					case salat:
						if(nachystanoSalatu > 0){
							nachystanoSalatu--;
							cekamNaJidlo.erase(cekamNaJidlo.begin()+i);
							i--;
						}
						else{
							if(nejdelsiPripravaJidla < DOBA_PRIPRAVY_VARKY_SALATU){
								nejdelsiPripravaJidla = DOBA_PRIPRAVY_VARKY_SALATU;
							};
						}
						break;
				}
			}

			//pokud jidlo neni pripravene, ceka
			if(alreadyWaitedEnough){
				Wait(1);	//nervozne preslapuje pred vydavacim pultem a vyznamne pokukuje na hodinky
			}
			else{	//napred ceka vyrobni dobu nejdelsiho jidla
				double zbyvajiciCas = nejdelsiPripravaJidla - dobaObjednani;

				alreadyWaitedEnough = true;
				if(zbyvajiciCas > 0){
					Wait(zbyvajiciCas);
				}
				else{
					Wait(nejdelsiPripravaJidla);
				}
			}
		}

		dobaPripravyJidla(Time - zacatekCekaniNaJidlo);
	}

	/*
	 * Pocita cas na celkove baleni objednavky, pote ceka na dokonceni.
	 */
	void cekaniNaZabaleni(){
		bool objednanePiti = false;
		double zacatekBaleni = Time;
		float dobaBaleni = Exponential(EXP_DOBA_PRIPRAVY_A_DOKONCENI_BALENI);
		for(unsigned int i = 0; i < objednano.size(); i++){
			switch(objednano[i]){
				case malyBurger:
					dobaBaleni += DOBA_BALENI_MALEHO_BURGERU;
					break;
				case velkyBurger:
					dobaBaleni += DOBA_BALENI_VELKEHO_BURGERU;
					break;
				case hranolky:
					dobaBaleni += Uniform(UNIF_DOBA_BALENI_HRANOLEK_MIN, UNIF_DOBA_BALENI_HRANOLEK_MAX);
					break;
				case piti:
					objednanePiti = true;
					dobaBaleni += Exponential(EXP_DOBA_BALENI_PITI);
					break;
				case salat:
					dobaBaleni += DOBA_BALENI_SALATU;
					break;
			}
		}

		if(objednanePiti && (dobaBaleni < DOBA_TOCENI_PITI)){
			dobaBaleni += DOBA_TOCENI_PITI;		//ma piti a nema dost jinych veci, ktere by se balily v prubehu toceni piti, proto musi pockat, nez se piti natoci
		}

		Wait(dobaBaleni);
		dobaBaleniObjednavky(Time - zacatekBaleni);
		dobaCekaniNaObjednavku(Time - zacatekCekaniNaJidlo);

	}
};

//trida pro cinnost v kuchyni, spusti kuchare, ktery bude pripravovat jidla a cistit kuchyni
class KuchynskaCinnost : public Process {
public:
	bool uklidKuchyne;
	jidla jidlo;

	KuchynskaCinnost(bool uklidKuchyne_ = false, jidla jidlo_ = malyBurger) : uklidKuchyne(uklidKuchyne_), jidlo(jidlo_){
	};

	void Behavior(){
		Enter(kuchari,1);
		if(uklidKuchyne){	//uklid kuchyni - utrit garnyry, ciste hadry,...
			Wait(DELKA_UKLIDU_KUCHYNE);
		}
		else{	//priprav jidlo
			switch(jidlo) {
				case malyBurger:
					Wait(DOBA_PRIPRAVY_VARKY_MALYCH_BURGERU);
					nachystanoMalychBurgeru += VARKA_MALYCH_BURGERU;
					break;
				case velkyBurger:
					Wait(DOBA_PRIPRAVY_VELKEHO_BURGERU);
					nachystanoVelkychBurgeru++;
					break;
				case hranolky:
					Wait(DOBA_PRIPRAVY_VARKY_HRANOLEK);
					(new Hranolky)->Activate(Time + DOBA_SMAZENI_HRANOLEK);
					break;
				case salat:
					Wait(DOBA_PRIPRAVY_VARKY_SALATU);
					nachystanoSalatu += VARKA_SALATU;
					break;
				default:
					break;
			}
		}

		Leave(kuchari, 1);
	}
};


//trida kuchyne, ktera ridi cinnost kucharu a uklidu kuchyne
class Kuchyne : public Process {
public:
    jidla objednaneJidlo;

    void Behavior(){
		unsigned int odeberouMalychBurgeru = 0;
		unsigned int odeberouHranolek = 0;
		unsigned int odeberouSalatu = 0;
        while(1){
            if(frontaJidel.size() > 0){
                objednaneJidlo = frontaJidel.front();
				frontaJidel.erase(frontaJidel.begin());
				pocetJidelCelkem++;
				switch(objednaneJidlo){
                	case malyBurger:
						(odeberouMalychBurgeru >= VARKA_MALYCH_BURGERU) ? (odeberouMalychBurgeru = 0) : odeberouMalychBurgeru++;	//citac pro info kdy se ma dat delat dalsi varka burgeru
						if(odeberouMalychBurgeru >= VARKA_MALYCH_BURGERU/2){	//pokud je objednanych vic nez pulka jedne varky burgeru, da se delat jedna cela nova
							(new KuchynskaCinnost(false, malyBurger))->Activate();
						}
                	    break;
                	case velkyBurger:
						(new KuchynskaCinnost(false, velkyBurger))->Activate();
                	    break;
                	case hranolky:
						(odeberouHranolek >= VARKA_HRANOLEK) ? (odeberouHranolek = 0) : odeberouHranolek++;	//citac pro info kdy se ma dat delat dalsi varka hranolek
						if(odeberouHranolek >= VARKA_HRANOLEK/2){
							(new KuchynskaCinnost(false, hranolky))->Activate();
						}
                	    break;
                	case salat:
						(odeberouSalatu >= VARKA_SALATU) ? (odeberouSalatu = 0) : odeberouSalatu++;	//citac pro info kdy se ma dat delat dalsi varka salatu
						if(odeberouSalatu >= VARKA_SALATU/2){
							(new KuchynskaCinnost(false, salat))->Activate();
						}
                	    break;
                	default:
                	    break;
                }
            }
            else{
				if((Time - casPoslednihoUkliduKuchyne) >= PERIODA_UKLIDU_KUCHYNE){	//pokud je potreba, uklid kuchyni - utrit garnyr, ciste hadry,...
					(new KuchynskaCinnost(true))->Activate();

					dobaMeziUklidyKuchyne(Time - casPoslednihoUkliduKuchyne);
					casPoslednihoUkliduKuchyne = Time;
				}
				else {	//jinak cekej nez prijde objednavka

					WaitUntil(frontaJidel.size() > 0);
				}
            }
        }
    }
};


//generator zakazniku
class GeneratorZakazniku : public Event {
    void Behavior(){
		double koeficientNovePrichozich = Uniform(0, 3);

		//pro simulaci skupin zakaznici mohou prijit po jednom nebo po dvou zaroven
		if((koeficientNovePrichozich >= 1) && (koeficientNovePrichozich < 2)){ //generuj jednoho zakaznika
			(new Zakaznik)->Activate(); //vytvori noveho zakaznika
		}
		else if((koeficientNovePrichozich >= 2) && (koeficientNovePrichozich < 3)){ //generuj dva zakazniky
			(new Zakaznik)->Activate();
			(new Zakaznik)->Activate();
		}
		//else if koeficientNovePrichozich < 1 negeneruje zakaznika
        Activate(Time + Exponential(EXP_DOBA_GENEROVANI_ZAKAZNIKA)); //prida udalost znovuaktivace do casu "aktualni cas + exp cas", tzn. "exp cas" cas od teto chvile
    }
};


//manager, ktery chodi kolem a kdyz je potreba, prilozi ruku k praci
class Manager : public Process {
public:
	void Behavior(){
		while(1){
			Wait(10*VTERINA);	//manager dojde a overi mista, aby tam pripadne pomohl
			if(kuchari.QueueLen() >= PRILIS_DLOUHA_FRONTA_KUCHARI){
			    kuchari.SetCapacity(kuchari.Capacity()+1);
			    Wait(MINUTA);   //minimalne minutu pomaha s akutnimi problemy
			    while((kuchari.QueueLen() >= PRILIS_DLOUHA_FRONTA_KUCHARI/2) && ((pokladny.QueueLen()<=PRILIS_DLOUHA_FRONTA_POKLADNY) && (vydejci.QueueLen()<=PRILIS_DLOUHA_FRONTA_VYDEJ))){
			       Wait(30*VTERINA);   //vzdy chvili pomaha, po intervalech se rozhlizi, zda neni potreba pomoc nekde jinde
			    }
			    WaitUntil(kuchari.Free() >= 1);
			    kuchari.SetCapacity(kuchari.Capacity()-1);
			    }
			else if(pokladny.QueueLen() >= PRILIS_DLOUHA_FRONTA_POKLADNY){
				pokladny.SetCapacity(pokladny.Capacity()+1);
				Wait(MINUTA);	//minimalne minutu pomaha s akutnimi problemy
				while((pokladny.QueueLen() >= PRILIS_DLOUHA_FRONTA_POKLADNY/2) && ((kuchari.QueueLen()<=PRILIS_DLOUHA_FRONTA_KUCHARI) && (vydejci.QueueLen()<=PRILIS_DLOUHA_FRONTA_VYDEJ))){
					Wait(30*VTERINA);	//vzdy chvili pomaha, po intervalech se rozhlizi, zda neni potreba pomoc nekde jinde
				}
				WaitUntil(pokladny.Free() >= 1);	//jeho pomoc neni potreba, nebo je ptoreba jinde, proto pocka, az dokonci svoji cinnost (nebo to nekdo jiny prebere za nej) a odchazi
				pokladny.SetCapacity(pokladny.Capacity()-1);
			}
			else if(vydejci.QueueLen() >= PRILIS_DLOUHA_FRONTA_VYDEJ){
				vydejci.SetCapacity(vydejci.Capacity()+1);
				Wait(MINUTA);	//minimalne minutu pomaha s akutnimi problemy
				while((vydejci.QueueLen() >= PRILIS_DLOUHA_FRONTA_VYDEJ/2) && ((kuchari.QueueLen()<=PRILIS_DLOUHA_FRONTA_KUCHARI) && (pokladny.QueueLen()<=PRILIS_DLOUHA_FRONTA_POKLADNY))){
					Wait(30*VTERINA);	//vzdy chvili pomaha, po intervalech se rozhlizi, zda neni potreba pomoc nekde jinde
				}
				WaitUntil(vydejci.Free() >= 1);
				vydejci.SetCapacity(vydejci.Capacity()-1);
			}
			else{
				Wait(MINUTA);	//nikde neni treba pomoct, venuje se pocitani zbozi, organizaci, kontrole a udrzbe cistoty,...
			}
		}
	}
};



int main(int argc, char **argv) {
	//zpracovani parametru
    zpracovaniParametru(argc, argv);


	//nastaveni a beh simulace
    RandomSeed(time(NULL)); //nastaveni seedu pro RNG
    Init(0, DOBA_TRVANI_SIMULACE); //nastaveni delky simulovane doby (pocatek, konec)

	pokladny.SetCapacity(pocetPokladen);
	kuchari.SetCapacity(pocetKucharu);
	vydejci.SetCapacity(pocetVydejcu);

	(new Kuchyne)->Activate();
	(new Manager)->Activate();
    (new GeneratorZakazniku)->Activate(); //vytvori generator zakazniku

    Run(); //spusti simulaci


    /************** VYPIS STATISTIK**********/
    //vypis statistik a informaci
    //cout << "Personal v kuchyni formou Kucahri:Pokladny:Vydejci  " << pocetKucharu << ":" << pocetPokladen << ":" << pocetVydejcu << endl;
    //printf("Celkem prislo %d zakazniku.\n", pocetPrichozich);
	//printf("Celkem %d zakazniku odeslo okamzite kvuli dlouhe fronte\n", pocetOdchozichKvuliFronte);
    pokladny.Output();
	dobaObjednavani.Output();
	dobaPripravyJidla.Output();
	dobaBaleniObjednavky.Output();
	dobaCekaniNaObjednavku.Output();
	dobaVRestauraci.Output();
	dobaMeziUklidyKuchyne.Output();
	kuchari.Output();
	//cout << "Zakazniku za minutu prumerne " << ((float)pocetPrichozich / ((float)DOBA_TRVANI_SIMULACE/60.0)) << endl;
	//cout << "pocet jidel celkem: " << pocetJidelCelkem << "\npocet jidel na jednoho cloveka: " << ((float)pocetJidelCelkem / pocetObslouzenychUPokladny) << endl;

    /*int celkemZamestnancu = pocetPokladen + pocetKucharu + pocetVydejcu;
	float procentLidiOdeslo;
	if(pocetOdchozichKvuliFronte == 0){
	    procentLidiOdeslo = 0;
	}
	else{
	    procentLidiOdeslo = ((float) pocetOdchozichKvuliFronte / (float) pocetPrichozich) * 100;
	}*/

	//celkemzamestnancu(pokladna:kuchyn:vydej),pocet lidi kolik odeslo v procentech, prumerna cekaci doba na jidlo po obednani
	//cout <<  celkemZamestnancu << "(" << pocetPokladen << ":" << pocetKucharu << ":" << pocetVydejcu << ")" << "," << procentLidiOdeslo << "," << dobaCekaniNaObjednavku.MeanValue() << endl;

    return 0;
}


/*
 * Zpracuje parametry, ulozi potrebne hodnoty pro simulaci.
 * -p <int> - pocet lidi u pokladen
 * -k <int> - pocet kucharu v kuchyni
 * -v <int> - pocet lidi u vydavani objednavek
 */
void zpracovaniParametru(int argc, char **argv){
    char zpracovavanyParametr;

    while((zpracovavanyParametr = getopt(argc, argv, "p:k:v:")) != -1){		// p - pocet pokladen, k - pocet kucharu, v - pocet vydejcu
        switch(zpracovavanyParametr){
            case 'p':
                pocetPokladen = atoi(optarg);
                if(!pocetPokladen){
                    fprintf(stderr, "Neplatna hodnota pro pocet pokladen... Nastafuji defaultni hodnotu *%i*.\n", DEFAULT_POKLADNY);
                    pocetPokladen = DEFAULT_POKLADNY;
                }
                else if(pocetPokladen > LIMIT_POKLADEN){
                    fprintf(stderr, "Prekrocen limit pokladen... Nastavuji maximalni hodnotu *%i*\n", LIMIT_POKLADEN);
                    pocetPokladen = LIMIT_POKLADEN;
                }
                break;
            case 'k':
                pocetKucharu = atoi(optarg);
                if(!pocetKucharu){
                    fprintf(stderr, "Neplatna hodnota pro pocet kucharu... Nastafuji defaultni hodnotu *%i*.\n", DEFAULT_KUCHARI);
                    pocetPokladen = DEFAULT_KUCHARI;
                }
                else if(pocetKucharu > LIMIT_KUCHARU){
                    fprintf(stderr, "Prekrocen limit kucharu... Nastavuji maximalni hodnotu *%i*\n", LIMIT_KUCHARU);
                    pocetPokladen = LIMIT_KUCHARU;
                }
                break;
            case 'v':
                pocetVydejcu = atoi(optarg);
                if(!pocetVydejcu){
                    fprintf(stderr, "Neplatna hodnota pro pocet vydejcu... Nastafuji defaultni hodnotu *%i*.\n", DEFAULT_VYDEJCI);
                    pocetVydejcu = DEFAULT_VYDEJCI;
                }
                else if(pocetVydejcu > LIMIT_VYDEJCU){
                    fprintf(stderr, "Prekrocen limit vydejcu... Nastavuji maximalni hodnotu *%i*\n", LIMIT_VYDEJCU);
                    pocetVydejcu = LIMIT_VYDEJCU;
                }
                break;
        }
    }
}
