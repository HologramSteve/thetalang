# ThetaLang
A lightweight compiled programming language for [Mattbatwing's BatPU-2 computer](https://github.com/mattbatwings/BatPU-2?tab=readme-ov-file).
Important to note:
- Code written by the compiler is made to work on the [official emulator](https://github.com/AdoHTQ/Batpu2-VM/), not the actual redstone machine (it may work there, idk).
- It won't be able to do everything.
- There might be errrors.

## Structure
The language is function-based. All code must be in a function. The program starts executing at the `Main` function. All functions must use the `return` keyword at the end (the compiler only checks for an appearance of this keyword - watch out!). Functions support parameters, more on this later.

## Contents of documentation
1. Types
2. Variables
3. Functions
4. If-statements
5. Values
6. Loops
7. Modules
8. All keywords
___
### 1. Types
Thetalang supports 3 types, `int`, `char` and `String`.
#### Int
A number from 0-255 (1 byte). Can be used for almost anything.
#### Char
A single charachter (must be surrounded by ""). The emulator converts this to a number, but text displays can use these numbers. Note: the `char` type currently has 0 use cases.
#### String
Just a string. Must be surrounded by "". Warning: these take up a lot of memory (1 byte/character). This type has one use: the text display.
___
### 2. Variables
Variables allow you to store data. Variable declaration goes as follows:
```var type name = value```
`var`: the var keyword.
`type`: the type, as specified above, `int`, `char` or `String`.
`name`: the name for your variable.
`value`: the actual value (more on this later).
Variables can be changed with the `mutate` keyword, like this:
```mutate name += / -= / == value```
`mutate`: the keyword
`name`: the name of the variable
`+= / -= / ==`, one of the three. Use `==` to enter a new value.
Variables can be deleted with the `free` keyword, like this:
```free varname```
This will free the variable's memory (useful when it won't be used anymore).

Variables can be called with `$varname`, more on this later.
___
### 3. Functions
Functions are re-usable chunks of code. Define a function with the `fn` keyword, followed by brackets. Every function must `return` at the end. You can get parameters by using `#para` as a value (para, parb, parc or pard). Example function:
```
fn Test {
	return
}
```
Functions can not return values (yet).
Call a function with the `call` keyword, followed by it's parameters (max 4), seperated by spaces. For example:
`call Test 10 20 30 40`
___
### 4. If-statements
You can make code that only executes when a condition is met using if-statements. They are formatted as follows:
```
if value condition value {
	code
}
```
"value" must be a value. Condition is either `==` or `!==` (will add `>` soon). Pretty simple.
___
### 5. Values
There are a few types of values. 
#### Direct value: a number, charachter or String
Just a value.
#### Variable
Call a variable by doing `$varname`. This will use the variable's value.
#### System values
Use `#something` to use a system value, this can be:
- `#random`: a random number from 0-255
- `#para`: (replace the last $a$ with $b, c$ or $d$). This returns a parameter.
- `#controls`: returns the current control input (`int`)
___
### 6. Loops
There are 2 types of loops, `forever` and `while`.
#### Forever
```
forever {
	code
}
```
This executes the code in a loop, forever.

#### While
```
while value condition value {
	code
}
```
This executes the code in a loop while the condition is met.
___
### 7. Modules
There are a few modules built in (modules.json). Add a module using `include moduleName`. Call a function by doing `call moduleName.test`. All modules and their functions:
| Module      | Name               | Parametera   | Parameterb | Description                       |
|-------------|--------------------|--------------|------------|-----------------------------------|
| display     | display.draw       | x            | y          | Light a pixel at (x, y)           |
| display     | display.render     |              |            | Render the changes on screen      |
| display     | display.clear      |              |            | Clear the entire screen           |
| display     | display.clearpixel | x            | y          | Clear a pixel at (x, y)           |
| numdisplay  | numdisplay.set     | num          |            | Set the number display            |
| numdisplay  | numdisplay.clear   |              |            | Clear the number display          |
| txtdisplay  | txtdisplay.set     | varname      |            | Set the text display (String var) |
___
### 8. All keywords
| Keyword       | Example Usage                | Description                                                                                                                                  |
|---------------|------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| return        | `return`                     | Returns from a function. Compiles to the `RET` opcode.                                                                                     |
| var           | `var int x = 5`              | Declares a new variable with a type (`int`, `char`, or `String`), assigns an initial value, and reserves memory.                               |
| mutate        | `mutate x + 1`               | Modifies an existing variable’s value using an operation (addition, subtraction, or assignment).                                             |
| call          | `call myFunction arg1 arg2`  | Invokes a function or module. Manages parameter passing and handles special cases such as calling `txtdisplay.set` for String variables.       |
| include       | `include "moduleName"`       | Imports a module. Loads external function definitions from a JSON file (`modules.json`) and adds them to the current module context.          |
| free          | `free x`                     | Frees allocated memory for a variable. For String types, it returns each occupied memory cell; for others, it returns the variable’s address. |
| ! (tag)       | `!start`                     | Defines a label/tag (using the `!` prefix) that can be used as a jump target.                                                                |
| goto          | `goto start`                 | Jumps to a previously defined label.                                                                                                         |
| if            | `if x == 10`                 | Begins an if-statement for conditional execution. Compares two values and branches based on the result.                                        |
| forever       | `forever {}`                    | Starts an infinite loop. Creates a loop label for repeated execution without an exit condition.                                              |
| while         | `while $x != 0 {}`               | Begins a while loop that repeatedly executes as long as a condition holds true. Establishes a loop with a condition check.                      |
| fn             | `fn Test {}`                         | Declare's a function                            |
___
### 9. Tags
Tags can be used to jump around. 
Make a tag:
`!tag`
Jump to one:
`goto tag`

# That was most of the language!
I will add some examples soon, have fun!
Thanks for reading :)
