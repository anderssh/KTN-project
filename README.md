# Kort beskrivelse av prosjektet

Prosjektet er delt inn i 7 moduler. Vi har en client.py-fil som er "dum". Den kan bare lese inn data fra brukern,
sende det til server, og printe respons. All annen funksjonalitet finner vi i server.py-filen. Denne inneholder 
historien, forbindelsene (en forbindelse TCP-forbindelse mellom bruker og server) og forbindelseshåndterer 
(som oppretter en forbindelse for hver client som blir kjørt). Historien er satt sammen av historieinnlegg, som er en
egen modul, struct i dettet tilfellet. Forbindelseobjektene inneholder brukerinnformasjon om sin respektive client, lagret
som et bruker-objekt. Den siste modulen i serveren er lagringsmodulen, denne inneholder historien, hjelp-dataen og listen over 
forbindelser. 

Det opprettes et forbindelsesobjekt for hver client-fil som kjøres så fremt denne oppnår kommunikasjon med serveren. Da står 
fritt til å be om historie og hjelp. Brukeren som tilhører denne forbindelsen er da foreløpig satt til "utlogget"/"inaktiv". 
Ved å logge inn med brukernavn får også brukeren tilang til å sende og motta meldinger fra andre aktive brukere. Hvis 
brukere forsøker å logge ut vil ikke forbindelsen slettes, men brukerinstansen vil settes til inaktiv igjen. Ved terminering
av client-filen vil TCP-forbindelsen ødelegges og om dette skjer, slettes gjeldende forbindelses-instans fra forbindelses-
listen.

Det er forbindelsesmodulen som foretar all kommunikasjon mellom ens egen bruker, lagringsmodulen og de andre brukerne. Hver 
av forbindelsene kjører, naturlig nok i en egen tråd. Ved meldingssending vil forbindelseslisten itereres over og meldingen 
sendes til alle aktive brukere. Historien blit naturlig nok også oppdatteres etter sendingen er gjort. 


