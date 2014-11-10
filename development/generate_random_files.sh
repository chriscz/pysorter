#!/bin/sh

touch photo1.jpg
touch photo2.png

touch anim.gif
touch movie.mp4
touch movie.api

touch writing.doc
touch writing.docx
touch writing.odt

touch sheet.xls
touch sheet.xlsx
touch sheet.ods

touch song1.mp3
touch song2.ogg
touch conflictsong.mp3

# Some nasty filenames
touch foolscreed.awesome.tpb.mp3
touch foolscreed.tpb.mp3.doc

# Some random unknown filetypes
touch aint_got_no_type
touch weirdType.typesareweird
touch whynotype
touch .hiddenfile

# Some directories
mkdir emptyDirectory
mkdir deepdir
cd deepdir
    touch asong.mp3
    touch conflictsong.mp3 # this should conflict
    touch meconflict.jpg # conflicting image
    mkdir deeperdir
    cd deeperdir
        touch meconflict.jpg # conflicting image
        touch adeepfile.doc
        cd ..
    mkdir Anotherempty
    mkdir deeperdir2
    cd deeperdir2
        touch moo.mp3
        touch adeepfile2.doc
        cd ..
    cd ..
