# ThetaLang
Thetalang is a compiled programming language for the [BatPU-2](https://www.youtube.com/watch?v=3gBZHXqnleU).
> Links of the BatPU-2:
> - [Virtual machine](https://github.com/AdoHTQ/Batpu2-VM)
> - [Youtube video](https://www.youtube.com/watch?v=3gBZHXqnleU)
> - [Discord server](https://discord.gg/V5KFaF63mV)
> - [ISA](https://docs.google.com/spreadsheets/d/1Bj3wHV-JifR2vP4HRYoCWrdXYp3sGMG0Q58Nm56W4aI/edit?gid=0#gid=0)

## Table contents
1. Basic information
2. Syntax
3. Functions
4. Control Structures
5. I/O Operations
6. Examples
7. Compilation
8. Modules

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
- enum (predefined constants). Available enums: W (8), A (1), S (2), D (4), T (64), Y (128), J (16), K (32). Used for input keys or flags.

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
> See the Modules section for details.

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
}

### Compilation
To compile your .tl file:
1. Place your code in `main.tl`.
2. Run `python main.py` in the terminal.
3. The compiled assembly will be in `main.as`.
4. Load `main.as` into the BatPU-2 VM to run.

> Make sure all dependencies (modules) are in `tl_modules`.

## Modules
Modules are reusable code files that extend ThetaLang's functionality. They contain functions you can include in your programs to avoid rewriting common code.

### Including Modules
To use a module, add this at the top of your file (outside functions):
```
include moduleName;
```
> Modules are stored as `.tl` files in the `tl_modules` folder. The compiler automatically loads them when included.

### Creating Modules
Create a `.tl` file in `tl_modules` with your functions. For example:
```
fn myModule.myFunction {
    // your code
};
```
> Share your modules by opening a PR on the GitHub repo!

### Existing Modules
Here are the built-in modules available:

- **display.tl**: Graphics functions for the display.
  - `display.clear()`: Clears the screen.
  - `display.update()`: Updates the display.
  - `display.set(x, y, color)`: Sets a pixel at (x, y) to color.
  - `display.get(x, y)`: Returns the color at (x, y).

- **numdisplay.tl**: Numeric display functions.
  - `numdisplay.set(value)`: Displays a number.
  - `numdisplay.clear()`: Clears the numeric display.

- **random.tl**: Random number generation.
  - `random.randint(max)`: Returns a random integer from 0 to max.

- **input.tl**: Input handling.
  - `input.get()`: Returns the current input value from #255.