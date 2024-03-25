package party

import (
	"fmt"
	"log"

	"github.com/fatih/color"
	"github.com/mattn/go-tty"
)

func (p *Party) Print() string {
	output := "\n_________________________________________\n"
	for i := range 8 {
		s1 := p.scores[Keys[i]]
		s2 := p.scores[Keys[i+9]]
		if !s1.set && !s1.lock {
			output += fmt.Sprintf("| %-9v | %v |", s1.label, s1.precal)
		} else {
			output += fmt.Sprintf("| %-9v | %3d |", s1.label, s1.value)
		}
		if !s2.set && !s2.lock {
			output += fmt.Sprintf("| %-9v | %s |\n", s2.label, s2.precal)
		} else {
			output += fmt.Sprintf("| %-9v | %3d |\n", s2.label, s2.value)
		}
	}
	output += "--------------------------------------------\n"
	dicestring := generateDices(p.dices)

	for _, d := range dicestring {
		output += d + "\n"
	}
	return output
}

func generateDices(dices Dices) [3]string {
	// ═ ║ ┌╖╘╝│─
	diceoutput := [3]string{}
	for _, d := range dices {
		if d.value != 0 {
			lockprint := func(s string) string { return s }
			if d.lock != 0 {
				lockprint = func(s string) string { return color.HiRedString(s) }
			}

			diceoutput[0] = diceoutput[0] + "  " + lockprint("┌──╖")
			diceoutput[1] = diceoutput[1] + "  " + lockprint(fmt.Sprintf("│ %d║", d.value))
			diceoutput[2] = diceoutput[2] + "  " + lockprint("╘══╝")
		}
	}
	return diceoutput
}

func (p *Party) PlayCLI() {
	tty, err := tty.Open()
	if err != nil {
		log.Fatal(err)
	}
	defer tty.Close()
	char, _ := tty.ReadRune()
	fmt.Println(char)

	for {
		fmt.Printf("%s\n", p.Print())
		fmt.Println("\n*******************")
		color.Green(p.GetCMD())
		fmt.Println(">")

		//char, _, err := keyboard.GetSingleKey()
		char = 0
		for char == 0 {
			char, err = tty.ReadRune()
			if err != nil {
				panic(err)
			}
		}
		fmt.Println("GOT:>", char, "which is ", string(char))

		switch char {
		case ' ', 'x':
			if err := p.Roll(); err != nil {
				fmt.Printf("⚠️ %v\n", err)
			}
		case 'q':
			return
		case '1', '2', '3', '4', '5', 'a', 'z', 'e', 'r', 't':
			if err := p.KeepRune(char); err != nil {
				fmt.Printf("⚠️ %v\n", err)
			}
		case 's':
			if err := p.MarkRune(tty); err != nil {
				fmt.Printf("⚠️ %v\n", err)
			}
		default:
			fmt.Printf("⌨️ You pressed: %q", char)
		}
	}
}

func (p *Party) GetCMD() string {
	var cmd string
	cmd += " x: roll \t 12345,azert : keep dices \t s: score \t 0: reset \t q: quit \t "
	return cmd
}

func (p *Party) KeepRune(dice rune) error {
	if p.step != roll {
		return fmt.Errorf("NOT THE RIGHT TIME TO KEEP")
	}
	di := 0
	switch dice {
	case '1', 'a':
		di = 0
	case '2', 'z':
		di = 1
	case '3', 'e':
		di = 2
	case '4', 'r':
		di = 3
	case '5', 't':
		di = 4
	default:
		return fmt.Errorf("WTF BRO")
	}
	p.Keep(di)
	return nil
}

func (p *Party) MarkRune(tty *tty.TTY) error {
	if p.step != roll {
		return fmt.Errorf("NOT THE RIGHT TIME TO MARK")
	}
	fmt.Println("\n*******************")
	color.Green(" 1-6 | b:bre | c:car | f:ful | s:psu | g:gsu | h:cha | p:pac")
	fmt.Println("Where >")
	scored := false
	for !scored {
		char, err := tty.ReadRune()
		if err != nil {
			panic(err)
		}
		subcmd := ""
		switch char {
		case '1', '2', '3', '4', '5', '6':
			subcmd = fmt.Sprintf("dc%s", string(char))
		case 'b':
			subcmd = "bre"
		case 'c':
			subcmd = "car"
		case 'f':
			subcmd = "ful"
		case 's':
			subcmd = "psu"
		case 'g':
			subcmd = "gsu"
		case 'p':
			subcmd = "pac"
		default:
			fmt.Println("print %v", char)
		}
		if subcmd != "" {
			err := p.Mark(subcmd)
			if err != nil {
				fmt.Printf("⚠️ couldn' mark : %v -> %v \n", err, subcmd)
			}
			scored = true
		}
	}
	return nil
}
