fn txtdisplay.clear {
    write 0 to 249
    write 0 to 248
}

fn txtdisplay.set {
    txtdisplay.clear()
    int p = a
    int result = 255

    while result != 0 {
        result = #p
        write result to 247
        p += 1 
    }

    write 0 to 248
}