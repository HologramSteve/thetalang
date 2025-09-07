# ThetaLang
Thetalang is a compiled programming language for the [BatPU-2](https://www.youtube.com/watch?v=3gBZHXqnleU).
> Links of the BatPU-2:
> - [Virtual machine](https://github.com/AdoHTQ/Batpu2-VM)
> - [Youtube video](https://www.youtube.com/watch?v=3gBZHXqnleU)
> - [Discord server](https://discord.gg/V5KFaF63mV)
> - [ISA](https://www.youtube.com/redirect?event=video_description&redir_token=QUFFLUhqblhPeWp5cklPREY5MTNiejNScTBSUExDMlc2Z3xBQ3Jtc0tsSUtzTGtLZUlVTFQxcjNyVWN3S2lrN0NoOGRrRkxsR1doY3hnSGRIbkVWUURiSjR2dVQ1U1RZVDdWOGVWcDRRS0VYVGU5YS1qeWJfSTNTdTVNYWw3cjVkVnFzM25vM3d6dTBObVlpVzRLZW1UdW9VZw&q=https%3A%2F%2Fdocs.google.com%2Fspreadsheets%2Fd%2F1Bj3wHV-JifR2vP4HRYoCWrdXYp3sGMG0Q58Nm56W4aI&v=3gBZHXqnleU)

## Table contents
1. Basic information
2. Syntax
3. Functions
4. Control Structures
5. I/O Operations
6. Examples
7. Compilation

## Syntax
Some important things to note:
- Each line must have a semicolon (;) at the end (except empty lines)
- You can not have code outside of functions (exeption: the `include` keyword)
- Every program starts running at the `Main` function.

### Variables
Variables are auto-stored in RAM by the compiler (starts at 0). **There is currently no way to free a variable from memory - this'll be added in a later update.**

Declare a variable like this:
```
type name = value;
```
For example
```
int num = 0;
int num;
```
> Using `type varname;` will default to 0

Variable mutation (only after declaring one first):
```
varname = value;
varname += value;
varname -= value;
```

That's it!

### Types
- int (a number (max 255)). Example: `int num = 100;`
- char (single character). Example: `char letter = 'A';`
- Array (list of either int or char). Example: `array list[3] = [1,2,3];`. 
> With arrays, you must specify the length before (`varname[X]`)
- String (list of chars). Example: `String word = "hello";`

### Functions
Functions are defined using the `fn` keyword followed by the name and a block.

```
fn myFunction {
    // code here
};
```

- The `Main` function is required and is the entry point.
- Functions can be called with `functionName();`
- Parameters are passed via registers (up to 4: a, b, c, d).
- Return values are stored in a special address.

Include external modules with:
```
include moduleName;
```
> Modules are .tl files in the `tl_modules` folder.
> NOTE: If you made a module and you want to add it, open a PR on the github!

### Control Structures
- **If Statement**: `if condition { ... }`
  - Conditions: `==`, `!=`, `>`, `<`, `>=`, `<=`
  - Example: `if x == 5 { y = 10; };`

- **While Loop**: `while condition { ... }`
  - Example: `while x < 10 { x += 1; };`

- **Forever Loop**: `forever { ... }`
  - Runs indefinitely.
  - Example: `forever { numdisplay.set(x); x += 1; };`

### I/O Operations
- **Write to Address**: `write value to address;`
  - Writes a value to a specific memory address.
  - Example: `write 255 to 240;`

- System variables can be accessed with `#address`.
  - Example: `int sysval = #254;`

### Examples
A simple program that increments a number forever:

```
include numdisplay;

fn Main {
    int x = 0;
    forever {
        numdisplay.set(x);
        x += 1;
    };
    return;
};
```

### Compilation
To compile your .tl file:
1. Place your code in `main.tl`.
2. Run `python main.py` in the terminal.
3. The compiled assembly will be in `main.as`.
4. Load `main.as` into the BatPU-2 VM to run.

> Make sure all dependencies (modules) are in `tl_modules`.