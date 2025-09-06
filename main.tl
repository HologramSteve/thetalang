include numdisplay

fn Main {
    int x = 0
    int y = 1
    int z = 0
    
    forever {
        numdisplay.set(x)

        z = x
        z += y
        x = y
        y = z

        if x > 231 {
            x = 0
            y = 0
            z = 0
            numdisplay.set(233)
        }
        
    }
    return
}