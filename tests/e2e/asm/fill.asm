// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// R0 is used as a color register
// size = 8192
// black = -1 (hex 0xffff)
// white = 0 (hex 0x0)
// state = 0 (0 for white, 1 for black)
// LOOP:
//   i=0
//   if (KBD == 0) goto ELSE
//   if (state == 1) goto LOOP
//   R0 = black
//   goto COLOR
// ELSE:
//     if (state == 0) goto LOOP
//     R0 = white
//     goto COLOR
// COLOR:
//   if (i != size) goto CONT
//   state = R0 & 0x1
//   goto LOOP
// CONT:
//   RAM[SCREEN + i] = R0
//   i = i + 1
//   goto COLOR

// size = 8192
@8192
D=A
@size
M=D
// black = -1 
@black
M=-1
// white = 0
@white
M=0
// state = 0
@state
M=0
(LOOP)
  //i=0
  @i
  M=0
  // if (KBD == 0) goto ELSE
  @KBD
  D=M
  @ELSE
  D;JEQ
  
  //if (state == 1) goto LOOP
  @state
  D=M
  D=D-1
  @LOOP
  D;JEQ
 
  //R0 = black
  @black
  D=M
  @R0
  M=D
  
  //goto COLOR
  @COLOR
  0;JMP

(ELSE)
  // if (state == 0) goto LOOP
  @state
  D=M
  @LOOP
  D;JEQ
  //R0 = white
  @white
  D=M
  @R0
  M=D
  //goto COLOR
  @COLOR
  0;JMP

(COLOR)
  //if (i != size) goto CONT
  @i
  D=M
  @size
  D=D-M
  @CONT
  D;JNE
  //state = R0 & 0x1
  @1
  D=A
  @R0
  D=D&M
  @state
  M=D
  //goto LOOP
  @LOOP
  0;JMP

(CONT)
  //RAM[SCREEN + i] = R0
  @i
  D=M
  @SCREEN
  D=D+A
  @temp
  M=D
  @R0
  D=M
  @temp
  A=M
  M=D
  //i = i + 1
  @i
  M=M+1
  @COLOR
  0;JMP
  
