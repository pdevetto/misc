package party

import (
	"fmt"
	"slices"

	"github.com/fatih/color"
)

func (p *Party) Precalc() {
	for _, s := range p.scores {
		if !s.set && !s.lock {
			p.scores[s.key].precal = color.RedString(fmt.Sprintf("%3d", funcalc[s.key](p.dices)))
		}
	}
}

func nDice(dices []Dice, n int) bool {
	fmt.Printf("\n Do %v for %v", dices, n)
	values := make(map[int]int)
	for _, dice := range dices {
		values[dice.value] = values[dice.value] + 1
		print(" h:", values[dice.value])
		if values[dice.value] == n {
			return true
		}
	}
	return false
}

func sumDice(dices []Dice) int {
	fmt.Printf("SUM : %v = ", dices)
	n := 0
	for _, dice := range dices {
		n += dice.value
	}
	fmt.Printf(" %v ", n)
	return n
}

func sumDiceOfK(dices []Dice, k int) int {
	fmt.Printf("SUM of K")
	n := 0
	for _, dice := range dices {
		if dice.value == k {
			n += dice.value
		}
	}
	fmt.Printf(" %v ", n)
	return n
}

func suiteDice(dices []Dice, n int) bool {
	v_keys := map[int]int{}
	v_vals := make([]int, 0)
	for _, d := range dices {
		v_keys[d.value] += 1
		v_vals = append(v_vals, d.value)
	}

	//fmt.Printf("???Suite %v  \n", dices)
	//fmt.Printf("len(k) %v min : %v max %v \n", len(v_keys), slices.Min(v_vals), slices.Max(v_vals))

	return (len(v_keys) == n && slices.Max(v_vals)-slices.Min(v_vals) == n-1) ||
		(len(v_keys) == n+1 && slices.Max(v_vals)-slices.Min(v_vals) == n)
}

var funcalc = map[string]func(dices *[5]Dice) int{
	"bre": func(dices *[5]Dice) int {
		fmt.Println("BRELAN")
		if nDice(dices[:], 3) {
			return sumDice(dices[:])
		}
		return 0
	},
	"car": func(dices *[5]Dice) int {
		fmt.Println("CARRE")
		if nDice(dices[:], 4) {
			return sumDice(dices[:])
		}
		return 0
	},
	"ful": func(dices *[5]Dice) int {
		fmt.Println("PACFULL")
		if nDice(dices[:], 3) { // TODO
			return 25
		}
		return 0
	},
	"psu": func(dices *[5]Dice) int {
		fmt.Println("PSU")
		if suiteDice(dices[:], 4) {
			return 30
		}
		return 0
	},
	"gsu": func(dices *[5]Dice) int {
		fmt.Println("PSU")
		if suiteDice(dices[:], 5) {
			return 40
		}
		return 0
	},
	"cha": func(dices *[5]Dice) int {
		fmt.Println("CHANCE")
		return sumDice(dices[:])
	},
	"pac": func(dices *[5]Dice) int {
		fmt.Println("PACTOULE")
		if nDice(dices[:], 5) {
			return 50
		}
		return 0
	},
	"dc1": func(dices *[5]Dice) int {
		fmt.Println("DICE:1")
		return sumDiceOfK(dices[:], 1)
	},
	"dc2": func(dices *[5]Dice) int {
		fmt.Println("DICE:2")
		return sumDiceOfK(dices[:], 2)
	},
	"dc3": func(dices *[5]Dice) int {
		fmt.Println("DICE:3")
		return sumDiceOfK(dices[:], 3)
	},
	"dc4": func(dices *[5]Dice) int {
		fmt.Println("DICE:4")
		return sumDiceOfK(dices[:], 4)
	},
	"dc5": func(dices *[5]Dice) int {
		fmt.Println("DICE:5")
		return sumDiceOfK(dices[:], 5)
	},
	"dc6": func(dices *[5]Dice) int {
		fmt.Println("DICE:6")
		return sumDiceOfK(dices[:], 6)
	},
}
