package party

import (
	"fmt"
	"math/rand/v2"

	"github.com/eiannone/keyboard"
	"github.com/fatih/color"
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
			fmt.Printf("(%v) | %-9v |     |", s1.key, s1.label)
		} else {
			fmt.Printf("      | %-9v | %3d |", s1.label, s1.value)
		}
		if !s2.set && !s2.lock {
			fmt.Printf("| %-9v |     | (%v)\n", s2.label, s2.key)
		} else {
			fmt.Printf("| %-9v | %3d |\n", s2.label, s2.value)
		}

	}
}

func (p *Party) PlayCLI() {
	cmd := ""
	for {
		p.Print()
		fmt.Println("\n*******************")
		fmt.Print("Your input : \n")
		color.Green("space: roll \t q: quit \t 12345,azert : keep dices \t s: score")
		fmt.Print("> ")

		char, _, err := keyboard.GetSingleKey()
		if err != nil {
			panic(err)
		}

		switch char {
		case '\x00':
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
			fmt.Printf("key ? >")
			fmt.Scan(&cmd)
			err := p.Mark(cmd)
			if err != nil {
				fmt.Printf("Command broken : %v\n", cmd)
			}
		default:
			fmt.Printf("You pressed: %q\r\n", char)

		}

	}
}

func (p *Party) Roll() error {
	if (p.step != "init" && p.step != "roll") || p.roll > 2 {
		return fmt.Errorf("can't roll on step %v (roll %v)", p.step, p.roll)
	}
	fmt.Printf("...<roll%d>\n", p.roll+1)

	for i, dice := range p.dices {
		if p.step == "init" {
			p.dices[i].lock = 0
		}
		if dice.lock == 0 {
			p.dices[i].value = rand.IntN(5) + 1
		}
	}

	p.step = "roll"
	p.roll += 1

	return nil
}

func (p *Party) Keep(dice rune) error {
	if p.step != "roll" {
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
	p.step = "1"
	return nil
}
