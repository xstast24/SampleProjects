#!/bin/sh

#IOS, projekt 1
#xstast24

#kontrola utility realpath
realpath /etc > /dev/null
if [ $? -ne 0 ]
then
	echo "Utilita 'realpath' neni nainstalovana. Nainstalujte prosim utilitu realpath, a pote spustte wedi.sh znovu. // A 'realpath' utility is not installed. Please install the 'realpath' utility and run wedi.sh again." 1>&2;
	exit 1;
fi

#argumenty a globalni promenne
parM=0				#nejcasteji editovany soubor
parL=0				#seznam editovanych souboru
parB=0				#before
parA=0				#after
datum=""			#datum YYYY-MM-DD
soubor=""			#jmeno souboru
adresar=""			#jmeno slozky
aktualniAdresar=`realpath`
zadanyAdresar=""

#ziskani argumentu pomoci getopts
while getopts :m:l:b:a: opt
do
  case "$opt" in
    m)	#je zadan prepinac -m a adresar
		parM=1
		if [ -d $OPTARG ] 
		then
		adresar=$OPTARG
		else
			echo "Zadany adresar neexistuje." 1>&2;
			exit 1;
		fi ;;
    l)		#je zadan prepinac -l a adresar
		parL=1
		if [ -d $OPTARG ] 
		then
		adresar=$OPTARG
		else
			echo "Zadany adresar neexistuje." 1>&2;
			exit 1;
		fi ;;
	b)		#je zadan prepinac -b a datum
		parB=1
		datum="`echo $OPTARG | cut -d - -f1,2,3`" ;;
	a)		#je zadan prepinac -b a datum
		parA=1
		datum="`echo $OPTARG | cut -d - -f1,2,3`" ;;
	:)		
		if [ $OPTARG = "m" ]		#je zadan prepinac -m pro aktualni adresar
		then
			parM=1
		elif [ $OPTARG = "l" ]		#je zadan prepinac -l pro aktualni adresar
		then
			parL=1
		elif [ $OPTARG = "b" -o $OPTARG = "a" ]
		then
			echo "Chybne zadane parametry, chybi datum." 1>&2;
			exit 1;
		fi ;;
  esac
done

if [ -z $EDITOR -a -z $VISUAL ]
then
	echo "Neni zadana promenna EDITOR, ani VISUAL." 1>&2;
	exit 1;
fi

if [ -z $WEDI_RC ]
then
	echo "Format souboru neni specifikovan." 1>&2;
	exit 1;
fi

editovatSoubor()
{
	if [ -n $EDITOR ]
	then
		$EDITOR $1
		exC=$?
	else
		$VISUAL $1
		exC=$?
	fi
	cesta="`realpath $1`"
	aktualniDatum="`date +%Y-%m-%d`"
	echo "$cesta:$aktualniDatum" >> $WEDI_RC
	exit $exC
}

#zadane spatne prepinace
if [ \( $parM -eq 1 \) -a \( $parL -eq 1 \) ]
then
	echo "Je zadan i prepinac -l i prepinac -m, to neni povoleno." 1>&2;
	exit 1;
fi

#ziskani jmena adresare, kdyz je zadane -b/-a a datum
if [ "$1" = "-b" -o "$1" = "-a" ]
then
	adresar=$3
fi

#zadano prilis mnoho parametru
if [ $# -gt 3 ]
then
	echo "Spatne zadane parametry (prilis mnoho)." 1>&2;
	exit 1;
fi

#tail -1 vybere posledni radek, cut -d : -f1 vybere prvni sloupec s cestou
#1 neni zadan zadny argument, vybere soubor z aktualniho adresare
if [ $# -eq 0 ]
then
	pocetOtevrenych="`cat $WEDI_RC | grep "$aktualniAdresar/[^/]*$" | wc -l`"
	if [ $pocetOtevrenych -ge 1 ] #uz byl editovan soubor v aktualni slozce, vybere posledni otevreny
	then
		editovatSoubor "`cat $WEDI_RC | grep "$aktualniAdresar/[^/]*$" | tail -1 | cut -d : -f1`"
	else
		#v aktualnim adreesari nebyl jeste zadny soubor otevreny, chyba
		echo "V aktualnim adresari nebyl otevreny zadny soubor pomoci skriptu wedi.sh." 1>&2;
		exit 1;
	fi
	
#2  je zadan pouze soubor nebo adresar
elif [ \( $# -eq 1 \) -a \( $parM -eq 0 \) -a \( $parL -eq 0 \) ]
then
	if [ -d $1 ]
	then
		#je zadany adresar
		zadanyAdresar=`realpath "$1"`
		pocetOtevrenych="`cat $WEDI_RC | grep "$zadanyAdresar/[^/]*$" | wc -l`"
		if [ $pocetOtevrenych -ge 1 ] #uz byl editovan soubor v zadane slozce, vybere posledni otevreny
		then
		soubor="`cat $WEDI_RC | grep "$zadanyAdresar/[^/]*$" | tail -1 | cut -d : -f1`"
		editovatSoubor $soubor
		else
		#v zadanem adreesari nebyl jeste zadny soubor otevreny, chyba
		echo "V aktualnim adresari nebyl otevreny zadny soubor pomoci skriptu wedi.sh." 1>&2;
		exit 1;
		fi
	else
		#je zadany soubor
		editovatSoubor $1
	fi
	
#3 vybere nejcasteji editovany soubor z daneho nebo zvoleneho adresare
elif [ $parM -eq 1 ]
then
	if [ $# -eq 1 ]
	then
		#vybere z aktualniho adresare
		pocetOtevrenych="`cat $WEDI_RC | grep "$aktualniAdresar/[^/]*$" | wc -l`"
		if [ $pocetOtevrenych -ge 1 ]
		then
			soubor="`cat $WEDI_RC | grep "$aktualniAdresar/[^/]*$" | cut -d : -f1 | sort | uniq -c | sort -g | tail -1 | cut -d / -f2-500`" 		#bez prvniho lomitka, pridam na dalsim radku
			editovatSoubor "/$soubor"
		else
			echo "nebyl otevren zadny soubor v teto slozce." 1>&2;
		fi
		
	elif [ $# -eq 2 ]
	then
		#vybere ze zadaneho adresare
		zadanyAdresar=`realpath $2`
		pocetOtevrenych="`cat $WEDI_RC | grep "$zadanyAdresar/[^/]*$" | wc -l`"
		if [ $pocetOtevrenych -ge 1 ]
		then
			soubor="`cat $WEDI_RC | grep "$zadanyAdresar/[^/]*$" | cut -d : -f1 | sort | uniq -c | sort -g | tail -1 | cut -d / -f2-500`" 		#bez prvniho lomitka, pridam na dalsim radku
			editovatSoubor "/$soubor"
		else
			echo "nebyl otevren zadny soubor v teto slozce." 1>&2;
		fi
	else
		echo "Chybne zadane parametry nasledujici po -m." 1>&2;
		exit 1;
	fi

#4 seznam vsech souboru editovanych v danem adresari
elif [ $parL -eq 1 ]
then
	if [ $# -eq 2 ]
	then
		#vypise ze zadaneho adresare
		zadanyAdresar=`realpath $2`
		pocetOtevrenych="`cat $WEDI_RC | grep "$zadanyAdresar/[^/]*$" | wc -l`"
		if [ $pocetOtevrenych -ge 0 ]
		then
			cat $WEDI_RC | grep "$zadanyAdresar/[^/]*$" | cut -d : -f1 | sort -u | 
			{
			while read LINE
			do
				echo "`basename $LINE`"
			done
			}
		fi
		
	elif [ $# -eq 1 ]
	then
		#vypise z aktualniho adresare
		pocetOtevrenych="`cat $WEDI_RC | grep "$aktualniAdresar/[^/]*$" | wc -l`"
		if [ $pocetOtevrenych -ge 0 ]
		then
			cat $WEDI_RC | grep "$aktualniAdresar/[^/]*$" | cut -d : -f1 | sort -u | 
			{
			while read LINE
			do
				echo "`basename $LINE`"
			done
			}
		fi
	else
		echo "chybne zadane argumenty pro -l" 1>&2;
		exit 1;
	fi

#5 zobrazi pred nebo po datu
elif [ \( $parB -eq 1 \) -o \( $parA -eq 1 \) ]
then
	#z aktualniho adresare
	if [ $# -eq 2 ]	
	then
		if [ $parB -eq 1 ]
		then
			zadanycas="`echo $datum | tr -d "-"`"
			cat $WEDI_RC | grep "$aktualniAdresar/[^/]*$" | sort -u | 
			{
			while read LINE
			do
				cas="`echo "$LINE" | cut -d : -f2 | tr -d "-"`"
				if [ "$cas" -le "$zadanycas" ]
				then
				jmeno="`echo $LINE | cut -d : -f1`"
				echo "`basename $jmeno`"
				fi
			done
			}
		elif [ $parA -eq 1 ]
		then
			zadanycas="`echo $datum | tr -d "-"`"
			cat $WEDI_RC | grep "$aktualniAdresar/[^/]*$" | sort -u | 
			{
			while read LINE
			do
				cas="`echo "$LINE" | cut -d : -f2 | tr -d "-"`"
				if [ "$cas" -ge "$zadanycas" ]
				then
				jmeno="`echo $LINE | cut -d : -f1`"
				echo "`basename $jmeno`"
				fi
			done
			}
		fi
	#ze zadaneho adresare	
	elif [ \( $# -eq 3 \) -a \( -d $3 \) ]
	then
		if [ $parB -eq 1 ]
		then
			zadanyAdresar=`realpath $3`
			zadanycas="`echo $datum | tr -d "-"`"
			cat $WEDI_RC | grep "$zadanyAdresar/[^/]*$" | sort -u | 
			{
			while read LINE
			do
				cas="`echo "$LINE" | cut -d : -f2 | tr -d "-"`"
				if [ "$cas" -le "$zadanycas" ]
				then
				jmeno="`echo $LINE | cut -d : -f1`"
				echo "`basename $jmeno`"
				fi
			done
			}
		elif [ $parA -eq 1 ]
		then
			zadanyAdresar=`realpath $3`
			zadanycas="`echo $datum | tr -d "-"`"
			cat $WEDI_RC | grep "$zadanyAdresar/[^/]*$" | sort -u | 
			{
			while read LINE
			do
				cas="`echo "$LINE" | cut -d : -f2 | tr -d "-"`"
				if [ "$cas" -ge "$zadanycas" ]
				then
				jmeno="`echo $LINE | cut -d : -f1`"
				echo "`basename $jmeno`"
				fi
			done
			}
		fi
	else
		echo "Spatne zadane parametry pro -a/-b." 1>&2;
		exit 1;
	fi
fi










