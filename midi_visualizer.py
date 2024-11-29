import pygame
import pygame.midi

pygame.init()
pygame.midi.init()

print('MIDI Devices:')
for i in range(pygame.midi.get_count()):
    print('%s - %s' % (i, pygame.midi.get_device_info(i)))

print('\nChoose MIDI Device (0-%s):' % pygame.midi.get_count())
dev_id = input()

if not dev_id or int(dev_id) >= pygame.midi.get_count():
    dev_id = pygame.midi.get_default_input_id()
else:
    dev_id = int(dev_id)
    
midi_in = pygame.midi.Input(dev_id)

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'

CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

BRIGHT_COLORS = [CRED2, CGREEN2, CYELLOW2, CBLUE2, CVIOLET2, CBEIGE2, CWHITE2]
DARK_COLORS = [CRED, CGREEN, CYELLOW, CBLUE, CVIOLET, CBEIGE, CWHITE]

CBLACKBG  = '\33[40m'
CREDBG    = '\33[41m'
CGREENBG  = '\33[42m'
CYELLOWBG = '\33[43m'
CBLUEBG   = '\33[44m'
CVIOLETBG = '\33[45m'
CBEIGEBG  = '\33[46m'
CWHITEBG  = '\33[47m'

BG_COLORS = [CREDBG, CGREENBG, CYELLOWBG, CBLUEBG, CVIOLETBG, CBEIGEBG, CWHITEBG]

CGREYBG    = '\33[100m'
CREDBG2    = '\33[101m'
CGREENBG2  = '\33[102m'
CYELLOWBG2 = '\33[103m'
CBLUEBG2   = '\33[104m'
CVIOLETBG2 = '\33[105m'
CBEIGEBG2  = '\33[106m'
CWHITEBG2  = '\33[107m'

BRIGHT_BG_COLORS = [CREDBG2, CGREENBG2, CYELLOWBG2, CBLUEBG2, CVIOLETBG2, CBEIGEBG2, CWHITEBG2]

running = True


holds = [False] * 16

while running:
    notes = [' --- '] * 16
    tick = 0
    
    while tick < 6:
        if midi_in.poll():
            data = midi_in.read(1)    
            timing = 0
            
            for event in data:
                msg = event[0]
                timestamp = event[1]
                
                status = msg[0]
                channel = status & 0x0F
                msgtype = status >>4
                
                if msgtype == 0xF: # system realtime
                    if status == 0xF8: # timing clock
                        tick += 1
                
                elif msgtype == 0x9: # note on
                    note = msg[1]
                    velocity = msg[2]
                    
                    if velocity:
                        notestr = pygame.midi.midi_to_ansi_note(note)
                        if not '#' in notestr:
                            notestr = '%s-%s' % (notestr[0], notestr[1])
                            
                        color = BRIGHT_COLORS[channel % (len(BRIGHT_COLORS)-1) + 1]
                        bgcolor = BRIGHT_BG_COLORS[channel % (len(BG_COLORS)-1) + 1]
                        #bgcolor = CGREYBG
                        color = CBLACK
                        
                        notes[channel] = bgcolor + color + (' %3s ' % notestr) + CBLACKBG
                        holds[channel] = True
                        
                    else: # same as note off
                        holds[channel] = False
                        
                elif msgtype == 0x8: # note off
                    holds[channel] = False
                    
            for channel in range(16):
                if holds[channel] and '---' in notes[channel]:
                    bgcolor = BRIGHT_BG_COLORS[channel % (len(BG_COLORS)-1) + 1]
                    notes[channel] = bgcolor + '     ' + CBLACKBG
                    
    print(CBLACK + CBLACKBG + '    ' + ''.join(notes))
        
