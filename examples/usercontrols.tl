fn Main {
    include display
    include txtdisplay
    var String title = "Movement"
    call txtdisplay.set title
    var int x = 16
    var int y = 16
    call Update
    forever {
        var int input = #controls
        if $input == 1 {
            mutate x -= 1
            call Update
        }
        if $input == 4 {
            mutate x += 1
            call Update
        }
        if $input == 2 {
            mutate y -= 1
            call Update
        }
        if $input == 8 {
            mutate y += 1
            call Update
        }
        
    }
    return
}

fn Update {
    call display.clear
    call display.draw $x $y
    call display.render
    return
}
CAL .Main
HLT
.Main
LDI r6 1
LDI r7 2
CMP r6 r7
Expand
main.as
1 KB
