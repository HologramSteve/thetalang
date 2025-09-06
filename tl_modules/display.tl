fn display.clear {
    write 0 to 246
}

fn display.update {
    write 0 to 245
}

fn display.set {
    write a to 240
    write b to 241

    if c == 0 {
        write 0 to 243
    }
    if c == 1 {
        write 0 to 242
    }
}

fn display.get {
    write a to 240
    write b to 241

    return #244
}