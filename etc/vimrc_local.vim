" Project directory is ABOVE this one. ($PROJ/etc/vimrc_local.vim)
let proj_dir = expand('<sfile>:p:h:h')
setlocal path=.,larn

execute 'setlocal tags=./tags;'.fnameescape(proj_dir).',./TAGS;'.fnameescape(proj_dir)
