package party

import (
	"fmt"
	"slices"
)

func (p *Party) Precalc() {
	for _, s := range p.scores {
		if !s.Set && !s.Lock {
			p.scores[s.Key].Precal = funcalc[s.Key](p.dices)
		}
	}
}

func Compute(key Key, d []*Dice) int {
	fmt.Printf("Compute it is %#v for key %v\n", d, key)
	fun := funcalc[key]
	return fun(d)
}

func nDice(dices Dices, n int) bool {
	values := make(map[int]int)
	for _, dice := range dices {
		values[dice.Value] = values[dice.Value] + 1
		if values[dice.Value] == n {
			return true
		}
	}
	return false
}

func differentDices(dices Dices) int {
	diff_dice := make(map[int]int)
	for _, dice := range dices {
		n := dice.Value
		diff_dice[n] = diff_dice[n] + 1
	}
	return len(diff_dice)
}

func sumDice(dices Dices) int {
	n := 0
	for _, dice := range dices {
		n += dice.Value
	}
	return n
}

func sumDiceOfK(dices Dices, k int) int {
	n := 0
	for _, dice := range dices {
		if dice.Value == k {
			n += dice.Value
		}
	}
	return n
}

func suiteDice(dices Dices, n int) bool {
	v_keys := map[int]int{}
	v_vals := make([]int, 0)
	for _, d := range dices {
		v_keys[d.Value] += 1
		v_vals = append(v_vals, d.Value)
	}
	if len(v_keys) < n {
		return false
	}
	if len(v_keys) == n {
		return slices.Max(v_vals)-slices.Min(v_vals) == n-1
	}
	for i := range len(v_keys) - n + 1 {
		if slices.Max(v_vals[i:i+n])-slices.Min(v_vals[i:i+n]) == n-1 {
			return true
		}
	}
	return false
}

var funcalc = map[Key]func(dices Dices) int{
	Bre: func(dices Dices) int {
		if nDice(dices[:], 3) {
			return sumDice(dices[:])
		}
		return 0
	},
	Car: func(dices Dices) int {
		if nDice(dices[:], 4) {
			return sumDice(dices[:])
		}
		return 0
	},
	Ful: func(dices Dices) int {
		if nDice(dices[:], 5) ||
			(differentDices(dices[:]) == 2 && !nDice(dices[:], 4)) { // TODO
			return 25
		}
		return 0
	},
	Psu: func(dices Dices) int {
		if suiteDice(dices[:], 4) {
			return 30
		}
		return 0
	},
	Gsu: func(dices Dices) int {
		if suiteDice(dices[:], 5) {
			return 40
		}
		return 0
	},
	Cha: func(dices Dices) int {
		return sumDice(dices[:])
	},
	Pac: func(dices Dices) int {
		if nDice(dices[:], 5) {
			return 50
		}
		return 0
	},
	Dc1: func(dices Dices) int {
		return sumDiceOfK(dices, 1)
	},
	Dc2: func(dices Dices) int {
		return sumDiceOfK(dices, 2)
	},
	Dc3: func(dices Dices) int {
		return sumDiceOfK(dices, 3)
	},
	Dc4: func(dices Dices) int {
		return sumDiceOfK(dices, 4)
	},
	Dc5: func(dices Dices) int {
		return sumDiceOfK(dices, 5)
	},
	Dc6: func(dices Dices) int {
		return sumDiceOfK(dices, 6)
	},
}
