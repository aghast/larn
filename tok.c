/* tok.c		Larn is copyrighted 1986 by Noah Morgan. */
/*
   yylex()
   flushall()
   sethard()
   readopts()
*/
#ifdef VMS
#include <types.h>
#include <file.h>
#include <iodef.h>
#else VMS
#include <sys/types.h>
#ifdef SYSV
#include <fcntl.h>
# ifndef MSDOS
#   include <termio.h>
# endif
#else SYSV
# ifndef MSDOS
#   include <sys/ioctl.h>
# endif
#endif SYSV
#endif VMS
#include <ctype.h>
#include "header.h"

# define CHKPTINT	400

static char lastok=0;
int yrepcount=0,dayplay=0;
#ifndef FLUSHNO
#define FLUSHNO 5
#endif FLUSHNO
static int flushno=FLUSHNO;	/* input queue flushing threshold */
#define MAXUM 52	/* maximum number of user re-named monsters */
#define MAXMNAME 40	/* max length of a monster re-name */
static char usermonster[MAXUM][MAXMNAME]; /* the user named monster name goes here */
static char usermpoint=0;			/* the user monster pointer */
#ifdef DGK_MSDOS
 extern int rawio;
#endif

/*
	lexical analyzer for larn
 */
yylex()
	{
	char cc;
	int ic;
	if (hit2flag) { hit2flag=0;  yrepcount=0;  return(' '); }
	if (yrepcount>0)	{ --yrepcount;  return(lastok);	} else yrepcount=0;
	if (yrepcount==0) { bottomdo(); showplayer(); }	/*	show where the player is	*/
	lflush();  
	while (1)
		{
		c[BYTESIN]++;
		if (ckpflag)
		  if ((c[BYTESIN] % CHKPTINT) == 0)	/* check for periodic checkpointing */
			{
#ifndef DOCHECKPOINTS
#ifdef MSDOS
			cursors();
			lprcat("\nCheckpointing . . .");
			savegame(ckpfile);
			lprcat("\nDone\n");
			showplayer();
			lflush();
# ifdef OS2LARN
			flushallkbd();	/* Kill any stored key strokes */
# else
			flushall();	/* Kill any stored key strokes */
# endif
#else
#ifdef VMS
			savegame(ckpfile);
#else
			wait(0);	/* wait for other forks to finish */
			if (fork() == 0) { savegame(ckpfile); exit(); }
#endif
#endif
#else
#ifdef VMS
			savegame(ckpfile);
#else
			wait(0);	/* wait for other forks to finish */
			if (fork() == 0) { savegame(ckpfile); exit(); }
#endif
#endif

#ifdef TIMECHECK
			if (dayplay==0)
			  if (playable())
				{
				cursor(1,19);
				lprcat("\nSorry, but it is now time for work.  Your game has been saved.\n"); beep();
				lflush();
				savegame(savefilename);
				wizard=nomove=1;
				sleep(4);
				died(-257);
				}
#endif TIMECHECK

			}

# ifndef MSDOS
# ifdef VMS
		/* If keyboard input buffer is too big then flush some? RDE */
		/* Check this! but for now just ignore it... */
# else
		do /* if keyboard input buffer is too big, flush some of it */
			{
			ioctl(0,FIONREAD,&ic);
			if (ic>flushno)   read(0,&cc,1);
			}
		while (ic>flushno);
# endif VMS
# endif MSDOS

# ifdef MSDOS
		cc = ttgetch();
# else MSDOS
# ifdef VMS
		cc = ttgetch();
# else
		if (read(0,&cc,1) != 1) return(lastok = -1);
# endif VMS
# endif MSDOS
		if (cc == '!')		/* ! shell escape */
			{
			resetscroll();  /* scrolling region, home, clear, no attributes */
			clear();
# ifdef MSDOS
			doshell();
# else MSDOS
# ifdef VMS
			lflush();
			sncbr();
			oneliner("");
			scbr();
# else VMS
			if ((ic=fork())==0) /* child */
				{
				execl("/bin/csh",0);	exit();
				wait(0);
				}
			if (ic<0) /* error */
				{
				write(2,"Can't fork off a shell!\n",25); sleep(2);
				}
# endif VMS
# endif MSDOS
			setscroll();
			return(lastok = 'L'-64);	/* redisplay screen */
			}
		
		if ((cc <= '9') && (cc >= '0'))
			{ yrepcount = yrepcount*10 + cc - '0'; }
		else	{ if (yrepcount>0) --yrepcount;  return(lastok = cc); }
		}
	}

/*
 *	flushall()	Function to flush all type-ahead in the input buffer
 */
#ifdef OS2LARN
flushall()
#else
flushall()
#endif
	{
# ifdef MSDOS
	while (kbhit())
		getch();
# else MSDOS
# ifdef VMS
	/* Flush all type-ahead -- RDE */
	extern int	iochan;		/* defined in IO.C	*/
	int		c;

	SYS$QIOW(0,iochan,IO$_READLBLK|IO$M_TIMED|IO$M_PURGE,0,0,0,&c,1,0,0,0,0);

# else VMS
	char cc;
	int ic;
	for (;;) {		/* if keyboard input buffer is too big, flush some of it */
		ioctl(0,FIONREAD,&ic);
		if (ic<=0)
			return;
		while (ic>0) {
			read(0,&cc,1);
			--ic;
		} /* gobble up the byte */
	}
# endif VMS
# endif MSDOS
}

/*
	function to set the desired hardness 
	enter with hard= -1 for default hardness, else any desired hardness
 */
sethard(hard)
int hard;
{
	register int	j,k;
	long		i;
	struct monst	*mp;

	j=c[HARDGAME]; hashewon(); 
	if (restorflag==0)	/* don't set c[HARDGAME] if restoring game */
		{
		if (hard >= 0) c[HARDGAME]= hard;
		}
	else c[HARDGAME]=j; /* set c[HARDGAME] to proper value if restoring game */

	if (k=c[HARDGAME])
	  for (j=0; j<=MAXMONST+8; j++) {
	  	mp = &monster[j];
		i = ((6+k) * mp->hitpoints + 1)/6;
		mp->hitpoints = (i<0) ? 32767 : i;
		i = ((6+k) * mp->damage + 1) / 5;
		mp->damage = (i>127) ? 127 : i;
		i = (10 * mp->gold)/(10+k);
		mp->gold = (i>32767) ? 32767 : i;
		i = mp->armorclass - k;
		mp->armorclass = (i< -127) ? -127 : i;
		i = (7*mp->experience)/(7+k) + 1;
		mp->experience = (i<=0) ? 1 : i;
	}
}


/*
	function to read and process the larn options file
 */
readopts()
	{
	register char *i;
	register int j,k;
	char original_objects = FALSE ;
	int flag = 1;		/* set to 0 if a name is specified */

# ifdef DGK_MSDOS
	if (plopen(optsfile) < 0)
# else
	if (lopen(optsfile) < 0)
# endif
		{
		strcpy(logname,loginname);
		lprintf("Can't open options file \"%s\"\n", optsfile);
		lflush();
		sleep(2);
		original_objects = FALSE;
		goto set_objects;
		}
	i = " ";
	while (*i)
	  {
	  if ((i=(char *)lgetw()) == 0) break; /* check for EOF */
	  while (*i && ((*i==' ') || (*i=='\t'))) i++; /* eat leading whitespace */
		if (strcmp(i,"bold-objects") == 0)
		    boldon=1;
		else if (strcmp(i,"enable-checkpointing") == 0)
		    ckpflag=1;
		else if (strcmp(i,"inverse-objects") == 0)
		    boldon=0;
		else if (strcmp(i,"prompt-on-objects") == 0 )
		    prompt_mode = TRUE ;
		else if (strcmp(i,"auto-pickup") == 0 )
		    auto_pickup = TRUE ;
		else if (strcmp(i,"highlight-objects") == 0 )
		    boldobjects = TRUE ;
		else if (strcmp(i,"original-objects") == 0 )
		    original_objects = TRUE ;
		else if (strcmp(i,"female") == 0)
		    sex=0; /* male or female */
# ifdef DGK_MSDOS
		else if (strcmp(i, "graphics:") == 0)
		    {
		    wallc = atoi(lgetw());
		    floorc = atoi(lgetw());
		    }
		else if (strcmp(i, "larndir:") == 0) {
			if ((i=lgetw())==0)
				break;
			strncpy(larndir, i, DIRLEN);
			larndir[DIRLEN - 1] = 0;
		}
		else if (strcmp(i, "rawio") == 0)
			rawio = 1;
		else if (strcmp(i, "swapfile:") == 0) {
			if ((i = lgetw()) == 0)
				break;
			strncpy(swapfile, i, PATHLEN);
			swapfile[PATHLEN - 1] = 0;
		}
		else if (strcmp(i, "ramlevels:") == 0)
			ramlevels = atoi(lgetw());
		else if (strcmp(i, "cursor:") == 0) {
			cursorset = 1;
			cursorstart = (unsigned char) atoi(lgetw());
			cursorend = (unsigned char) atoi(lgetw());
		}
		else if (strcmp(i, "keypad") == 0)
			keypad = 1;
		else if (strcmp(i, "DECRainbow") == 0)
			DECRainbow = 1;
# endif
		else if (strcmp(i,"monster:")== 0)   /* name favorite monster */
			{
			if ((i=lgetw())==0) break;
			if (strlen(i)>=MAXMNAME) i[MAXMNAME-1]=0;
			strcpy(usermonster[usermpoint],i); 
			if (usermpoint >= MAXUM) break; /* defined all of em */
			if (isalpha(j=usermonster[usermpoint][0]))
				{
				for (k=1; k<MAXMONST+8; k++) /* find monster */
				  if (monstnamelist[k] == j)
					{
					monster[k].name = &usermonster[usermpoint++][0];
					break;
					}
				}
			}
		else if (strcmp(i,"male") == 0)	sex=1;
		else if (strcmp(i,"name:") == 0) /* defining players name */
			{
			if ((i=lgetw())==0) break;
			if (strlen(i)>=LOGNAMESIZE) i[LOGNAMESIZE-1]=0;
			strcpy(logname,i); flag=0;
# ifdef MSDOS
			strcpy(loginname,i);
# endif
			}
		else if (strcmp(i,"no-introduction") == 0) nowelcome=1;
		else if (strcmp(i,"no-beep") == 0) nobeep=1;
# ifndef MSDOS
		else if (strcmp(i,"process-name:")== 0) 
			{
			if ((i=lgetw())==0) break;
			if (strlen(i)>=PSNAMESIZE) i[PSNAMESIZE-1]=0;
			strcpy(psname,i);
			}
		else if (strcmp(i,"play-day-play") == 0)  dayplay=1;
# endif
		else if (strcmp(i,"savefile:") == 0) /* defining savefilename */
			{
			if ((i=lgetw())==0) break;
			if (strlen(i)>=SAVEFILENAMESIZE) /* avoid overflow */
				i[SAVEFILENAMESIZE-1]=0;
			strcpy(savefilename,i); flag=0;
			}
		else {
			lprintf("Unknown option \"%s\"\n", i);
			lflush();
			sleep(1);
		}
	  }
 set_objects:
	if (flag)
	    strcpy(logname,loginname);

	/* original objects require object highlighting to be ON (in order
	   to distinguish between objects and monsters.  set up object list
	   properly.
	*/
	if (original_objects)
	    {
	    boldobjects = TRUE ;
	    strncpy( objnamelist, original_objnamelist, MAXOBJECT );
	    }
	else
	    strncpy( objnamelist, hacklike_objnamelist, MAXOBJECT );
	objnamelist[MAXOBJECT] = '\0' ;

	/* now set all the invisible objects and monsters to have the
	   same appearance as the floor (as defined by the user)
	*/
	objnamelist[OWALL] = wallc;

	objnamelist[0]		  =
	objnamelist[OIVTELETRAP]  =
	objnamelist[OTRAPARROWIV] =
	objnamelist[OIVDARTRAP]	  =
	objnamelist[OIVTRAPDOOR]  = floorc;
	monstnamelist[0] =
	monstnamelist[INVISIBLESTALKER] = floorc;
	for (j=DEMONLORD; j<=DEMONPRINCE; j++)
		monstnamelist[j] = floorc;

	}
