/*
  newsphere(x,y,dir,lifetime)  Function to create a new sphere of annihilation
  rmsphere(x,y)      Function to delete a sphere of annihilation from list
  sphboom(x,y)       Function to perform the effects of a sphere detonation
  movsphere()        Function to look for and move spheres of annihilation
*/
#include "header.h"
#include "larndefs.h"
#include "monsters.h"
#include "objects.h"
#include "player.h"

#define min(x,y) (((x)>(y))?(y):(x))
#define max(x,y) (((x)>(y))?(x):(y))

/*
 *  newsphere(x,y,dir,lifetime)  Function to create a new sphere of annihilation
 *      int x,y,dir,lifetime;
 *
 *  Enter with the coordinates of the sphere in x,y
 *    the direction (0-8 diroffx format) in dir, and the lifespan of the
 *    sphere in lifetime (in turns)
 *  Returns the number of spheres currently in existence
 */
newsphere(x,y,dir,life)
    int x,y,dir,life;
    {
    int m;
    struct sphere *sp;
    if (((sp=(struct sphere *)malloc(sizeof(struct sphere)))) == 0)
        return(c[SPHCAST]); /* can't malloc, therefore failure */
    if (dir>=9) dir=0;  /* no movement if direction not found */
    if (level==0) vxy(&x,&y);   /* don't go out of bounds */
    else
        {
        if (x<1) x=1;  if (x>=MAXX-1) x=MAXX-2;
        if (y<1) y=1;  if (y>=MAXY-1) y=MAXY-2;
        }
    if ((m=mitem[x][y]) >= DEMONLORD+4) /* demons dispel spheres */
        {
        show1cell(x,y);     /* show the demon (ha ha) */
        cursors(); lprintf("\nThe %s dispels the sphere!",monster[m].name);
        beep(); rmsphere(x,y);  /* remove any spheres that are here */
        return(c[SPHCAST]);
        }
    if (m==DISENCHANTRESS) /* disenchantress cancels spheres */
        {
        cursors(); lprintf("\nThe %s causes cancellation of the sphere!",monster[m].name); beep();
boom:   sphboom(x,y);   /* blow up stuff around sphere */
        rmsphere(x,y);  /* remove any spheres that are here */
        return(c[SPHCAST]);
        }
    if (c[CANCELLATION]) /* cancellation cancels spheres */
        {
        cursors(); lprcat("\nAs the cancellation takes effect, you hear a great earth shaking blast!"); beep();
        goto boom;
        }
    if (item[x][y]==OANNIHILATION) /* collision of spheres detonates spheres */
        {
        cursors(); lprcat("\nTwo spheres of annihilation collide! You hear a great earth shaking blast!"); beep();
        rmsphere(x,y);
        goto boom;
        }
    if (playerx==x && playery==y) /* collision of sphere and player! */
        {
        cursors();
        lprcat("\nYou have been enveloped by the zone of nothingness!\n");
        beep(); rmsphere(x,y);  /* remove any spheres that are here */
        nap(4000);  died(258);
        }
    item[x][y]=OANNIHILATION;  mitem[x][y]=0;  know[x][y]=1;
    show1cell(x,y); /* show the new sphere */
    sp->x=x;  sp->y=y;  sp->lev=level;  sp->dir=dir;  sp->lifetime=life;  sp->p=0;
    if (spheres==0) spheres=sp; /* if first node in the sphere list */
    else    /* add sphere to beginning of linked list */
        {
        sp->p = spheres;    spheres = sp;
        }
    return(++c[SPHCAST]);   /* one more sphere in the world */
    }

/*
 *  rmsphere(x,y)       Function to delete a sphere of annihilation from list
 *      int x,y;
 *
 *  Enter with the coordinates of the sphere (on current level)
 *  Returns the number of spheres currently in existence
 */
rmsphere(x,y)
    int x,y;
    {
    register struct sphere *sp,*sp2=0;
    for (sp=spheres; sp; sp2=sp,sp=sp->p)
      if (level==sp->lev)   /* is sphere on this level? */
        if ((x==sp->x) && (y==sp->y))   /* locate sphere at this location */
            {
            item[x][y]=mitem[x][y]=0;  know[x][y]=1;
            show1cell(x,y); /* show the now missing sphere */
            --c[SPHCAST];   
            if (sp==spheres) { sp2=sp; spheres=sp->p; free((char*)sp2); }
            else
                { sp2->p = sp->p;  free((char*)sp); }
            break;
            }
    return(c[SPHCAST]); /* return number of spheres in the world */
    }

/*
 *  sphboom(x,y)    Function to perform the effects of a sphere detonation
 *      int x,y;
 *
 *  Enter with the coordinates of the blast, Returns no value
 */
static sphboom(x,y)
    int x,y;
    {
    register int i,j;
    if (c[HOLDMONST]) c[HOLDMONST]=1;
    if (c[CANCELLATION]) c[CANCELLATION]=1;
    for (j=max(1,x-2); j<min(x+3,MAXX-1); j++)
      for (i=max(1,y-2); i<min(y+3,MAXY-1); i++)
        {
        item[j][i]=mitem[j][i]=0;
        show1cell(j,i);
        if (playerx==j && playery==i)
            {
            cursors(); beep();
            lprcat("\nYou were too close to the sphere!");
            nap(3000);
            died(283); /* player killed in explosion */
            }
        }
    }

/*
 *  movsphere()     Function to look for and move spheres of annihilation
 *
 *  This function works on the sphere linked list, first duplicating the list
 *  (the act of moving changes the list), then processing each sphere in order
 *  to move it.  They eat anything in their way, including stairs, volcanic
 *  shafts, potions, etc, except for upper level demons, who can dispel
 *  spheres.
 *  No value is returned.
 */
#define SPHMAX 20   /* maximum number of spheres movsphere can handle */
movsphere()
    {
    register int x,y,dir,len;
    register struct sphere *sp,*sp2;
    struct sphere sph[SPHMAX];

    /* first duplicate sphere list */
    for (sp=0,x=0,sp2=spheres; sp2; sp2=sp2->p) /* look through sphere list */
      if (sp2->lev == level)    /* only if this level */
        {
        sph[x] = *sp2;  sph[x++].p = 0;  /* copy the struct */
        if (x>1)  sph[x-2].p = &sph[x-1]; /* link pointers */
        }
    if (x) sp= sph; /* if any spheres, point to them */
        else return;    /* no spheres */

    for (sp=sph; sp; sp=sp->p)  /* look through sphere list */
        {
        x = sp->x;    y = sp->y;
        if (item[x][y]!=OANNIHILATION) continue;    /* not really there */
        if (--(sp->lifetime) < 0)   /* has sphere run out of gas? */
            {
            rmsphere(x,y); /* delete sphere */
            continue;
            }
        switch(rnd((int)max(7,c[INTELLIGENCE]>>1))) /* time to move the sphere */
            {
            case 1:
            case 2:     /* change direction to a random one */
                        sp->dir = rnd(8);
            default:    /* move in normal direction */
                        dir = sp->dir;      len = sp->lifetime;
                        rmsphere(x,y);
                        newsphere(x+diroffx[dir],y+diroffy[dir],dir,len);
            };
        }
    }
