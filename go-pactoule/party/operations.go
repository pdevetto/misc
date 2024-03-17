package party

import (
	"fmt"
	"log"
	"math/rand/v2"

	"github.com/fatih/color"
	"github.com/mattn/go-tty"
)

func (p *Party) Print() {
	dices := ""
	for _, d := range p.dices {
		if d.lock != 0 {
			dices += fmt.Sprintf("[%v]", d.value)
		} else {
			dices += fmt.Sprintf(" %v ", d.value)
		}

	}
	fmt.Printf("🎲 : %v \n", dices)
	fmt.Println("_____")
	for i := range 8 {
		s1 := p.scores[Keys[i]]
		s2 := p.scores[Keys[i+9]]
		if !s1.set && !s1.lock {
			fmt.Printf("(%v) | %-9v | %v |", s1.key, s1.label, s1.precal)
		} else {
			fmt.Printf("      | %-9v | %3d |", s1.label, s1.value)
		}
		if !s2.set && !s2.lock {
			fmt.Printf("| %-9v | %s | (%v)\n", s2.label, s2.precal, s2.key)
		} else {
			fmt.Printf("| %-9v | %3d |\n", s2.label, s2.value)
		}

	}
}

func (p *Party) PlayCLI() {
	tty, err := tty.Open()
	if err != nil {
		log.Fatal(err)
	}
	defer tty.Close()
	char, _ := tty.ReadRune()
	fmt.Println(char)

	cmd := ""
	for {
		p.Print()
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
			if err := p.Keep(char); err != nil {
				fmt.Printf("⚠️ %v\n", err)
			}
		case 's':
			fmt.Printf("key ? > \n")
			_, err := fmt.Scan(&cmd)
			if err != nil {
				fmt.Printf("Command broken : %v\n", cmd)
			}
			err = p.Mark(cmd)
			if err != nil {
				fmt.Printf("Command broken : %v\n", cmd)
			}
		default:
			fmt.Printf("You pressed: %q\r\n", char)
		}
	}
}

func (p *Party) GetCMD() string {
	var cmd string
	cmd += " x: roll \t 12345,azert : keep dices \t s: score \t 0: reset \t q: quit \t "
	return cmd
}

func (p *Party) Roll() error {
	if (p.step != start && p.step != roll) || p.roll > 2 {
		return fmt.Errorf("can't roll on step %v (roll %v)", p.step, p.roll)
	}
	precalc := false
	fmt.Printf("...<roll%d>\n", p.roll+1)

	for i, dice := range p.dices {
		if p.step == start {
			p.dices[i].lock = 0
		}
		if dice.lock == 0 {
			p.dices[i].value = rand.IntN(5) + 1
			precalc = precalc || true
		}
	}

	p.step = roll
	p.roll += 1

	if precalc {
		p.Precalc()
	}

	return nil
}

func (p *Party) Keep(dice rune) error {
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
	fmt.Printf("so: %v \n", dice)

	if p.dices[di].lock == 0 {
		p.dices[di].lock = p.roll
	} else if p.dices[di].lock == p.roll {
		p.dices[di].lock = 0
	}

	return nil
}

func (p *Party) Mark(cmd string) error {
	//p.step =
	return nil
}
