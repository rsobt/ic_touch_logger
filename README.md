# Touch logger
An application that records the time spent in Google Calendar by touching a student ID card (Felica) to the installed reader.

## Aim
Under the covid-19 situation, the laboratory decided to record entry and exit times as an independent measure. However, it is very tedious to memorize and manually input or handwrite the entry/exit time every day. With this application, students simply touch their student ID card to the card reader located next to the entrance to record their entry/exit times in Google calender, which can then be viewed in real time by other students who share the same calendar.
## Requirements
* Card reader

## How to use
0. If you are not Hokkaido university student.
    Dump and analyze the contents of the card and rewrite the program

1. Please fill "./ic_touch_logger/.env" file
    This program is developed with the intention of running on a raspberrypi. Please prepare various information of RDB on raspberry pi and API key to register information to Google calender.
    
2. Run main.py
## References
* [大学生協FeliCaの仕様](https://gist.github.com/oboenikui/ee9fb0cb07a6690c410b872f64345120)

## TODO
- [x] : Ability to post to Google calender
- [] : Ability to post to slack
- [] : Error handling
