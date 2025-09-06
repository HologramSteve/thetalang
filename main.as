CAL .Main
RET

.Main
; int x = 0
LDI r1 0
LDI r3 0
STR r3 r1
; int y = 1
LDI r1 1
LDI r3 1
STR r3 r1
; int z = 0
LDI r1 0
LDI r3 2
STR r3 r1
; forever {
.forever_1
; numdisplay.set(x)
LDI r4 0
LOD r4 r7
LDI r15 236
STR r15 r7
CAL .numdisplay.set
; z = x
LDI r4 0
LOD r4 r4
LDI r2 2
LOD r2 r6
MOV r4 r6
STR r2 r6
; z += y
LDI r4 1
LOD r4 r4
LDI r2 2
LOD r2 r6
ADD r6 r4 r6
STR r2 r6
; x = y
LDI r4 1
LOD r4 r4
LDI r2 0
LOD r2 r6
MOV r4 r6
STR r2 r6
; y = z
LDI r4 2
LOD r4 r4
LDI r2 1
LOD r2 r6
MOV r4 r6
STR r2 r6
; if x > 231 {
LDI r4 0
LOD r4 r4
LDI r5 231
CMP r4 r5
BRH LT .if_0
; x = 0
LDI r4 0
LDI r2 0
LOD r2 r6
MOV r4 r6
STR r2 r6
; y = 0
LDI r4 0
LDI r2 1
LOD r2 r6
MOV r4 r6
STR r2 r6
; z = 0
LDI r4 0
LDI r2 2
LOD r2 r6
MOV r4 r6
STR r2 r6
; numdisplay.set(233)
LDI r7 233
LDI r15 236
STR r15 r7
CAL .numdisplay.set
; }
.if_0
; }
JMP .forever_1
; return
RET
RET
.numdisplay.set
; write a to 250
LDI r4 236
LOD r4 r7
LDI r8 250
STR r8 r7
RET
.numdisplay.clear
; write 0 to 251
LDI r7 0
LDI r8 251
STR r8 r7
RET
