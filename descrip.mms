SOURCES = 	BILL.C, CONFIG.C, CREATE.C, DATA.C, DIAG.C, DISPLAY.C, -
		FORTUNE.C, GLOBAL.C, HELP.C, IO.C, MAIN.C, MONSTER.C, -
		MOREOBJ.C, MOVEM.C, NAP.C, OBJECT.C, REGEN.C, SAVELEV.C, -
		SCORES.C, SIGNAL.C, SPELLS.C, SPHERES.C, STORE.C, TOK.C, VMS.C, -
		ACTION.C, FGETLR.C, TGETENT.C, TGETSTR.C, TGOTO.C, TPUTS.C

OBJECTS =	BILL.OBJ, CONFIG.OBJ, CREATE.OBJ, DATA.OBJ, DIAG.OBJ, -
		DISPLAY.OBJ, FORTUNE.OBJ, GLOBAL.OBJ, HELP.OBJ, IO.OBJ, -
		MAIN.OBJ, MONSTER.OBJ, MOREOBJ.OBJ, MOVEM.OBJ, NAP.OBJ, -
		OBJECT.OBJ, REGEN.OBJ, SAVELEV.OBJ, SCORES.OBJ, SIGNAL.OBJ, -
		SPELLS.OBJ, SPHERES.OBJ, STORE.OBJ, TOK.OBJ, VMS.OBJ, -
		ACTION.OBJ, FGETLR.OBJ, TGETENT.OBJ, TGETSTR.OBJ, TGOTO.OBJ, -
		TPUTS.OBJ

DOBJECTS =	BILL.DBJ, CONFIG.DBJ, CREATE.DBJ, DATA.DBJ, DIAG.DBJ, -
		DISPLAY.DBJ, FORTUNE.DBJ, GLOBAL.DBJ, HELP.DBJ, IO.DBJ, -
		MAIN.DBJ, MONSTER.DBJ, MOREOBJ.DBJ, MOVEM.DBJ, NAP.DBJ, -
		OBJECT.DBJ, REGEN.DBJ, SAVELEV.DBJ, SCORES.DBJ, SIGNAL.DBJ, -
		SPELLS.DBJ, SPHERES.DBJ, STORE.DBJ, TOK.DBJ, VMS.DBJ, -
		ACTION.DBJ, FGETLR.DBJ, TGETENT.DBJ, TGETSTR.DBJ, TGOTO.DBJ, -
		TPUTS.DBJ

CDEFS =	/DEFINE=(LARNHOME="""larndir:""",DGK)

.SUFFIXES
.SUFFIXES .OBJ .DBJ .C

LARN.EXE : $(OBJECTS) vaxcrtl.opt
	LINK /NODEBUG/EXEC=LARN.EXE $(OBJECTS),vaxcrtl.opt/options

LARND.EXE : $(DOBJECTS)
	LINK /DEBUG/EXEC=LARND.EXE $(DOBJECTS), sys$library:vaxcrtl.olb/libr

LARNPCA.EXE : $(DOBJECTS), TERMCAP.OLB
        LINK /DEBUG=SYS$LIBRARY:PCA$OBJ.OBJ/EXEC=LARNPCA.EXE $(DOBJECTS),-
             SYS$LIBRARY:VAXCRTL.OLB/LIBR

vaxcrtl.opt :	    # ~ echo 'sys$share:vaxcrtl/shareable' >vaxcrtl.opt
  open/write f vaxcrtl.opt
  write f "sys$share:vaxcrtl/shareable"
  close f

$(OBJECTS),$(DOBJECTS) : HEADER.H

.C.OBJ
	CC $(CDEFS) /NODEB/OPTIM/OBJ=$*.OBJ $*.C

.C.DBJ
	CC $(CDEFS) /DEBUG/NOOPT/OBJ=$*.DBJ $*.C
