package main

import (
	"fmt"
	"log"
	. "pactoule/party"

	"github.com/fatih/color"
	"github.com/mattn/go-tty"
)

func main() {
	fmt.Println("Pactoule")

	p := CreateParty()
	PlayCLI(p)

}

func colorPrecal(s int) string {
	return color.RedString(fmt.Sprintf("%3d", s))
}

func Print(p *Party) string {
	scores := p.GetScores()
	output := "\n┌─────────────────╥─────────────────╖\n"
	for i := range 9 {
		s1 := scores[Keys[i]]
		s2 := scores[Keys[i+9]]
		if !s1.Set && !s1.Lock && p.GetStep() != START {
			output += fmt.Sprintf("│ %-9v │ %v ║", s1.Label, colorPrecal(s1.Precal))
		} else if !s1.Set && !s1.Lock {
			output += fmt.Sprintf("│ %-9v │     ║", s1.Label)
		} else {
			output += fmt.Sprintf("│ %-9v │ %3d ║", s1.Label, s1.Value)
		}
		if !s2.Set && !s2.Lock && p.GetStep() != START {
			output += fmt.Sprintf(" %-9v │ %s ║\n", s2.Label, colorPrecal(s2.Precal))
		} else if !s2.Set && !s2.Lock {
			output += fmt.Sprintf(" %-9v │     ║\n", s2.Label)
		} else {
			output += fmt.Sprintf(" %-9v │ %3d ║\n", s2.Label, s2.Value)
		}
	}
	output += "╘═════════════════╩═════════════════╝\n"
	if p.GetStep() != START {
		dicestring := generateDices(p.GetDices())
		for _, d := range dicestring {
			output += d + "\n"
		}
	}
	return output
}

func generateDices(dices Dices) [3]string {
	// ═ ║ ┌╖╘╝│─
	diceoutput := [3]string{}
	for _, d := range dices {
		if d.Value != 0 {
			lockprint := func(s string) string { return s }
			if d.Lock != 0 {
				lockprint = func(s string) string { return color.HiRedString(s) }
			}

			diceoutput[0] = diceoutput[0] + "  " + lockprint("┌───┒")
			diceoutput[1] = diceoutput[1] + "  " + lockprint(fmt.Sprintf("│ %d ┃", d.Value))
			diceoutput[2] = diceoutput[2] + "  " + lockprint("┕━━━┛")
		}
	}
	return diceoutput
}

func PlayCLI(p *Party) {
	tty, err := tty.Open()
	if err != nil {
		log.Fatal(err)
	}
	defer tty.Close()
	char, _ := tty.ReadRune()
	fmt.Println(char)

	for {
		fmt.Printf("%s\n", Print(p))
		fmt.Println("*******************")
		color.Green(GetCMD())

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
			if err := KeepRune(p, char); err != nil {
				fmt.Printf("⚠️ %v\n", err)
			}
		case 'm':
			if err := MarkRune(p, tty); err != nil {
				fmt.Printf("⚠️ %v\n", err)
			}
		default:
			fmt.Printf("⌨️ You pressed: %q", char)
		}
	}
}

func GetCMD() string {
	var cmd string
	cmd += " x: roll \t 12345,azert : keep dices \t m: mark score \t 0: reset \t q: quit \t "
	return cmd
}

func KeepRune(p *Party, dice rune) error {
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

func MarkRune(p *Party, tty *tty.TTY) error {
	if p.GetStep() != ROLL && p.GetStep() != MARK {
		return fmt.Errorf("NOT THE RIGHT TIME TO MARK")
	}
	color.Cyan(" 1-6 > . | b > bre | c > car | f > ful | s > psu | g > gsu | h > cha | p > pac")
	scored := false
	for !scored {
		char, err := tty.ReadRune()
		if err != nil {
			panic(err)
		}
		var subcmd Key
		switch char {
		case '1', '2', '3', '4', '5', '6':
			subcmd = GetKey(fmt.Sprintf("dc%s", string(char)))
		case 'b':
			subcmd = GetKey("bre")
		case 'c':
			subcmd = GetKey("car")
		case 'f':
			subcmd = GetKey("ful")
		case 's':
			subcmd = GetKey("psu")
		case 'g':
			subcmd = GetKey("gsu")
		case 'h':
			subcmd = GetKey("cha")
		case 'p':
			subcmd = GetKey("pac")
		default:
			subcmd = 0
		}
		if subcmd != 0 {
			err := p.Mark(subcmd)
			if err != nil {
				fmt.Printf("⚠️ couldn' mark : %v -> %v \n", err, subcmd)
			} else {
				scored = true
			}
		} else {
			fmt.Printf("⚠️ Nope : %c \n", char)
		}
	}
	return nil
}
