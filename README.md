SMS-Viewer
==========

A GUI for "SMS to Text" (android) output (formated text file) 

## Text file format

        date    hour    in/out    num    msg

* Separator : `\t`
* Header : `FALSE`
* Date format : `YYYY-MM-DD`
* Hour format : `HH:MM:SS`
* in/out info : `in` or `out` depending on the direction of the message
* Message type : `string` with no `\n`
