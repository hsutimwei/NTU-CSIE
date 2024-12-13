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

    @SCREEN
    D = A
    @0   //R[0]存當下位置
    M = D
(LOOP)
    @KBD
    D = M
    @black
    D;JGT
    @white
    0;JMP
(black)
    @KBD
    D = A - 1
    @0
    D = D - M
    @LOOP
    D;JLT
    @0
    A = M
    M = -1
    @0
    M = M + 1
    @black
    0;JMP
(white)
    @SCREEN
    D = A
    @0
    D = D - M
    @LOOP
    D;JGT
    @0
    A = M
    M = 0
    @0
    M = M - 1
    @white
    0;JMP