10 'GOSUB1170:GOSUB1120
20 CLS:PRINT "INIT [        ]":
30 CLEAR5000
40 PRINT @6,".";
50 DIM L(511)
60 PRINT".";
70 DIM Y(542)
80 PRINT".";
90 DIM T(542)
100 PRINT".";
110 DIM K(255)
120 PRINT".";
130 DIM L$,B$
140 PRINT".";
150 DIM A,B,C,D,E,F,G,H,I,J,K,L,M
160 PRINT".";
170 DIM N,O,P,Q,R,S,T,U,V,W,X,Y,Z
180 PRINT".";
190 DIM AK,BC,N1,LV,SC
200 GOTO690
210 RETURN
220 FORU=I TO B:RESET(Y,K):K=K-I:ONPOINT(Y,K)GOTO250,250,250,230,230,230,230,460:SET(Y,K,I):NEXT:RESET(Y,K):RETURN
230 H=INT(K/W)*G+INT(Y/W):PRINT@H-I,CHR$(N2)CHR$(N2+RND(N7))CHR$(N2+RND(N7));:AK=AK+I:IFAK>N1 THENU=B:NEXT:L=E:RETURN
240 VP=VARPTR(L$):FORZ=-I TOI:POKE(PEEK(VP+W)*V)+PEEK(VP+R)+(H-L)+Z,N2:NEXT:SET(Y,K,I):U=B:K=O:NEXT:RETURN
250 RESET(Y,K):U=B:K=O:Y=O:NEXT:RESET(Y,K):RETURN
260 RESET(C,M):M=M+W:ONPOINT(C,M)GOTO430,340,340:SET(C,M,I):RETURN
270 T=R:NEXT:OND+I GOTO280,280:S=L:L=E:NEXT:D=I:F=O:E=N9:X=S1:GOTO290
280 S=L:L=E:NEXT:D=-I:F=N1:E=N1:X=R:MS=MS+W:PRINT@MS,M$;:IFMS>N8 THENPRINT@MS,LEFT$(B$,5);:MS=O
290 BC=BC+I:IFBC>(G-AK)/W AND S<N6 THENBC=O:PRINT@S,LEFT$(B$,L(S));:S=S+G
300 FORL=S TO E STEPD:PRINT@L,LEFT$(L$,L(L));:ONPOINT(P,N)GOSUB210,210,210,480,480,480,480:ONPOINT(P+W,N)GOSUB210,210,210,480,480,480,480
310 PRINT@Q,P$;:ON M GOSUB410,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,260,400,400,400
320 J=L+F:FORT=O TO T(J):ONPOINT(X,Y(J)+V(T))GOTO370,370,370,270,270,270,270:NEXT
330 ON1-((PEEK(343)ANDPEEK(344)ANDPEEK(345))=255)GOSUB380:ONK GOSUB220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220,220:NEXT:GOTO490
340 SET(C,M,I):GOSUB440:RETURN
350 ON(P>B)+I GOTO210:P=P-W:Q=Q-I:RETURN
360 ON(P<N4)+I GOTO210:P=P+W:Q=Q+I:RETURN
370 T=R:NEXT:GOTO330
380 ONK(PEEK(135))GOSUB350,360,390:RETURN
390 ON K GOTO210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210,210:K=N5:Y=P:RETURN
400 RESET(C,M):M=I
410 ONRND(R)GOTO210,210:FORZ=N3 TO R STEP-W:ONPOINT(P,Z)GOSUB210,210,210,420,420,420,420,420:NEXT:RETURN
420 M=Z:Z=R:C=P+I:RETURN
430 RESET(C,M):RESET(C,M-I):M=I:RETURN
440 SOUND1,3:NP=NP-I:POKE1535,48+NP:IFNP<I THENS=L:L=E:K=O:M=O:X=O:V(O)=Y(L+F)*-I:PRINT@Q+I,CHR$(160+RND(N7))CHR$(160+RND(N7));
450 RETURN
460 H=INT(K/W)*G+INT(Y/W):PRINT@H-I,CHR$(240+RND(14))CHR$(240+RND(14))CHR$(240+RND(14));
470 SOUND200,1:SOUND155,2:SOUND230,1:RESET(Y,K):U=B:K=O:NEXT:RESET(Y,K):PRINT@MS,LEFT$(B$,6);:MS=0:SC=SC+25:RETURN
480 NP=I:GOTO440
490 IFNP>O AND AK=32 THEN580
500 PRINT@MS,LEFT$(B$,6);:IFS<448 THEN FORL=S TO 479 STEP32:PRINT@L-N1,LEFT$(B$,L(L-N1));:PRINT@L,LEFT$(L$,L(L));:SOUND1,2:NEXT
510 PRINT@0, "YOU ARE DEAD.      ";:SC=SC+(AK*LV):PRINT"SCORE=";SC:IFSC>HS THEN HS=SC
520 PRINT@32,"PLAY AGAIN (Y/N)?  ";:PRINT"HIGH=";HS
530 IFAK<32 THEN PRINT@196,"THE ALIENS HAVE LANDED!";:SOUND100,15
540 I$=INKEY$:IFI$=""THEN540
550 IFI$="Y" THEN 990
560 IFI$="N"THENGOSUB1220:GOSUB1150:END
570 GOTO540
580 PRINT@0,"ANOTHER WAVE IS COMING!"
590 SOUND100,3:SOUND50,3:SOUND100,3:SOUND50,5:SOUND50,5:SOUND100,3:SOUND50,3
600 SC=SC+(32*LV):PRINT@266,"SCORE=";SC;:FORT=1TO2000:NEXT
610 IFNP=SS THEN PRINT@198,"+100 SURVIVAL BONUS";:FORT=1 TO 2:FORZ=1 TO 24:READAA,BB:SOUNDAA,BB:NEXT:RESTORE:NEXT:SC=SC+100
620 XM=XM+I:IFXM=2 THEN GOSUB640
630 GOSUB1010:GOTO300
640 XM=0:IFNP=3 THEN 680
650 PRINT@198,"*SHIELDS REPAIRED!*";
660 NP=NP+1
670 FORT=1 TO 10:POKE1535,48+NP+64:PRINT@Q,Q$;:FORZ=1 TO 200:NEXT:POKE1535,48+NP:PRINT@Q,P$;:FORZ=1 TO 200:NEXT:NEXT
680 RETURN
690 CLS:PRINT@231,"* SPACE INVADERS *";
700 PRINT@291,"FOR THE MC-10 BY JIM GERRIE";
710 PRINT@485,"PRESS ANY KEY TO BEGIN";
720 P$=INKEY$:R=RND(1000):IFP$="" THEN 720
730 CLS:PRINT"PLEASE WAIT [           ]";
740 FORT=1TO32:B$=B$+CHR$(128):NEXT
750 PRINT @13,".";
760 O=0:I=1:W=2:R=3:B=4:G=32:N=29:V=256:N1=31
770 K(65)=1:K(83)=2:K(32)=3:K(8)=1:K(9)=2:A=17023
780 PRINT".";
790 DIM N2,N3,N4,N5,N6,N7,N8,N9
800 PRINT".";
810 DIM MS,NS,XM,NP,SS,Q$,P$,I$,M$,V(3),VP,S1
820 P$=CHR$(128)+CHR$(135+32)+CHR$(139+32)+CHR$(128):Q$=CHR$(128)+CHR$(135+16)+CHR$(139+16)+CHR$(128)
830 N2=128:N3=27:N4=58:N5=28:N6=480:N7=14:N8=24:N9=479:S1=61:SH$=CHR$(135+32)+CHR$(139+32)
840 PRINT".";
850 FORT=0TO256:L(T)=224:NEXT:FORT=257TO479:L(T)=L(T-1)-1:NEXT
860 PRINT".";
870 FORT=0TO286:T(T)=3:Y(T)=INT((T/16)+.1):NEXT
880 PRINT".";
890 FORT=287TO350:T(T)=2:Y(T)=INT((T/16)+.1):NEXT
900 PRINT".";
910 FORT=351TO414:T(T)=1:Y(T)=INT((T/16)+.1):NEXT
920 PRINT".";
930 FORT=415TO478:T(T)=0:Y(T)=INT((T/16)+.1):NEXT
940 PRINT".";
950 FORT=479TO542:T(T)=0:Y(T)=28:NEXT
960 PRINT".";
970 FORT=0TO3:V(T)=B*T:NEXT:M$=CHR$(128)+CHR$(128)+CHR$(241)+CHR$(255)+CHR$(251)
980 PRINT".";
990 SC=0:LV=0:NS=0:NP=3:MS=0:XM=0:GOSUB1010
1000 GOTO300
1010 CLS0:D=1:E=479:X=61:V(0)=0:NS=NS+1:LV=LV+1:IFLV>4 THEN LV=4
1020 PRINT@480,NS;"    ";:FORT=1504TO1508:POKET,PEEK(T)-64:NEXT:FORT=1509TO1535:POKET,G:NEXT:POKE1535,48+NP
1030 FORT=1TO3:PRINT@348+(9*T),CHR$(135);CHR$(143);CHR$(139);:PRINT@348+(9*T)+32,CHR$(143);CHR$(143);CHR$(143);:NEXT
1040 P=31:Q=448+14:M=1:L=LV*32:S=L:AK=0:BC=0:F=0:H=0:K=0:U=0:Z=0
1050 L$="":C=32:FORY=1TO4:C=C+16:FORT=1TO8:L$=L$+CHR$(128+C)+CHR$(133+C)+CHR$(141+C):NEXT:IFY=4 THEN L$=L$+LEFT$(B$,W):GOTO1070
1060 L$=L$+B$+LEFT$(B$,8)
1070 NEXT:C=0:SS=NP:RETURN
1080 DATA 89,1,125,1,147,1,176,1,147,1,125,1
1090 DATA 89,1,125,1,147,1,89,1,147,1,125,1
1100 DATA 89,1,125,1,147,1,176,1,147,1,125,1
1110 DATA 89,1,125,1,147,1,89,1,147,1,125,1
1120 IF PEEK(65535)=27 THEN POKE65497,0:GOTO1140 :ELSE CLS:INPUT"CAN YOUR COMPUTER HANDLE DOUBLE SPEED (Y/N)";A$
1130 IF A$="Y" THEN POKE65495,0 :ELSE IF A$<>"N" THEN1120
1140 CLS:RETURN
1150 IF PEEK(65535)=27 THEN POKE65496,0 :ELSE POKE65494,0
1160 RETURN
1170 :' ENABLE DRAGON SPEEDKEY
1180 IF PEEK(65535)<>180 THEN 1200
1190 IF PEEK(269)+PEEK(270)<>1 THEN POKE65283,52:POKE256,116:POKE257,1:POKE258,81:POKE259,126:POKE260,PEEK(269):POKE 261,PEEK(270):POKE269,1:POKE270,0:POKE65283,53
1200 RETURN
1210 :' DISABLE DRAGON SPEEDKEY
1220 IF PEEK(65535)<>180 THEN 1240
1230 IF PEEK(269)+PEEK(270)=1 THEN POKE65283,52:POKE269,PEEK(260):POKE270,PEEK(261):POKE65283,53
1240 RETURN