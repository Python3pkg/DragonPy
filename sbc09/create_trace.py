
"""
    Hacked script to create a *short* trace
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    commandline output e.g.:

$ python create_trace.py
Welcome to BUGGY version 1.0
r
X=0000 Y=0000 U=0000 S=0400 A=00 B=00 D=00 C=00
P=0400 NEG   $00
r
X=0000 Y=0000 U=0000 S=0400 A=00 B=00 D=00 C=00
P=0400 NEG   $00
ss
S11300007EE45A7EE4717EE4807EE4E47EE4F57E60
S1130010E4657EED447EED677EED8C7EEDCF7EED76
S1130020AC7EE5180C660000000000000000000033
S113003000000000000000000000000000000000BC
S113004000000000000000000000000000000000AC
S1130050000000000000000000000000000000009C
S1130060000000000000000000000000000000008C
S1130070000000000000000000000000000000007C
S1130080000000000000000000000000000000006C
S1130090000000000000000000000000000000005C
S11300A0000000000000000000000000000000004C
S11300B0000000000000000000000000000000003C
S11300C0000000000000000000000000000000002C
S11300D0000000000000000000000000000000001C
S11300E0000000000000000000000000000000000C
S11300F000000000000000000000000000000000FC
S9030000FC
x
Unknown command
"""

import time
import subprocess

cmd_args = [
    "./v09", "-t", "../v09trace.txt"
]
p=subprocess.Popen(cmd_args,
    cwd="sbc09",
    stdin=subprocess.PIPE,
    #~ stdout=subprocess.PIPE
)
p.stdin.write(
    "r\n" # Register display
    "r\n" # Register display
    "ss\n" # Register display

    # FIXME: Doesn't work:
    "\x1d" # escape character
    "x\n" # exit
)
p.stdin.flush()

# work-a-round:
time.sleep(1)
p.kill()
