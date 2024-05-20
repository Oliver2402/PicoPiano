from machine import Pin, PWM
import time

Button1 = Pin(3, Pin.IN, Pin.PULL_UP)
Button2 = Pin(6, Pin.IN, Pin.PULL_UP)
Button3 = Pin(10, Pin.IN, Pin.PULL_UP)
Button4 = Pin(13, Pin.IN, Pin.PULL_UP)
Button5 = Pin(17, Pin.IN, Pin.PULL_UP)
Button6 = Pin(19, Pin.IN, Pin.PULL_UP)
led = Pin(25, Pin.OUT)
buzzer = PWM(Pin(18))
BCL=0
Input=0
OnBoot=True
Level=1
Default_Level=1
InputLevel=0
InputLevelOctave=0

#Default volume at 25%
Volume=16384

#Stored Notes
#Naturals Octave 5
C5=523
D5=587
E5=659
F5=698
G5=783
A5=880
B5=987
#Naturals Octave 4
C4=261
D4=293
E4=329
F4=349
G4=391
A4=440
B4=493
#Naturals Octave 3
C3=130
D3=146
E3=164
F3=174
G3=195
A3=220
B3=246
#Sharps Octave 4
CS4=277
DS4=311
FS4=369
GS4=415
AS4=466

while BCL==0:
    if Level!=Default_Level:
        led.value(1)
    if Level==Default_Level:
        led.value(0)
    if Level==1:
        Note1=C4
        Note2=D4
        Note3=E4
        Note4=F4
        Note5=G4
        Note6=A4
        Note7=B4
    elif Level==2:
        Note1=CS4
        Note2=DS4
        Note3=FS4
        Note4=GS4
        Note5=AS4
    elif Level==3:
        Note1=C3
        Note2=D3
        Note3=E3
        Note4=F3
        Note5=G3
        Note6=A3
        Note7=B3
    elif Level==4:
        Note1=C5
        Note2=D5
        Note3=E5
        Note4=F5
        Note5=G5
        Note6=A5
        Note7=B5
    #Input Checking
    if Button6.value() == 0:
        #Switch from Sharps and Flats to Natural and vice verca
        #Remove and InputLevelOctave==0 if you want it to give sharps and octave changes if this comment is still here this is depricated and doesn't work
        if Default_Level==1 and InputLevelOctave==0:
            Level=2
        if Default_Level==2 and InputLevelOctave==0:
            Level=1
        #Switch Octaves Down
        if InputLevelOctave==4:
            Level=3
        #Switches Octave Up
        if InputLevelOctave==5:
            Level=4
        Input=6
        InputLevel=6
    else:
        Level=Default_Level
        InputLevel=0
        
    if Button1.value() == 0:
        buzzer.freq(Note1)
        Input=1

    if Button2.value() == 0:
        buzzer.freq(Note2)
        Input=2
    
    if Button3.value() == 0:
        buzzer.freq(Note3)
        Input=3
    
    if Button4.value() == 0:
        buzzer.freq(Note4)
        if Input==3 and Level!=2:
            buzzer.freq(Note6)
        if not OnBoot:
            Input=4
        if OnBoot:
            InputLevelOctave=4
    
    if Button5.value() == 0:
        buzzer.freq(Note5)
        if Input==4 and Level!=2:
            buzzer.freq(Note7)
        if not OnBoot:
            Input=5
        if OnBoot:
            InputLevelOctave=5
        
    #Volume and Octave Controls (Hold it down as you plug it in)
    if OnBoot:
        if Input==0:
            #No buttons held down
            Volume=16384
        if Input==1:
            #Volume at 50%
            Volume=32768
        if Input==2:
            #Volume at 0.75%
            Volume=491
        if InputLevel==6:
            #Switch to sharps
            Default_Level=2
            Level=2
        if InputLevelOctave==4 or InputLevelOctave==5 and Input==0:
            time.sleep(1)
        #If volume was changed don't play sounds for a Button2
        if Volume!=16384 or Level>1:
            time.sleep(1)
        #Turns off OnBoot after the First loop
        OnBoot=False
            
    #Sound Playing
    if Input>0 and Input<6:
        buzzer.duty_u16(Volume)
        time.sleep(0.01)
        buzzer.duty_u16(0)
        Input=0