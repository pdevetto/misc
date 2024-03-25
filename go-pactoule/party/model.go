package party

import (
	"fmt"
	"math/rand/v2"
)

var (
	Keys = []string{"car", "bre", "ful", "psu", "gsu", "cha", "pac", "dpm", "tt1",
		"dc1", "dc2", "dc3", "dc4", "dc5", "dc6", "bon", "tt2", "tot"}
	Labels = map[string]string{
		"bre": "Brelan",
		"car": "Carré",
		"ful": "Full",
		"psu": "Petite",
		"gsu": "Grande",
		"cha": "Chance",
		"pac": "Pactoule",
		"dpm": "DPM",
		"tt1": "Tot 1",
		"dc1": "Uns",
		"dc2": "Deux",
		"dc3": "Trois",
		"dc4": "Quatre",
		"dc5": "Cinq",
		"dc6": "Six",
		"bon": "Bonus",
		"tt2": "Total 2",
		"tot": "Total",
	}
)

type Step int

const (
	start Step = iota
	roll
)

type Dice struct {
	value int
	lock  int
}
type Dices = []*Dice
type Score struct {
	label  string
	key    string
	lock   bool
	set    bool
	value  int
	precal string
}
type Party struct {
	dices  []*Dice
	scores map[string]*Score
	step   Step
	roll   int
}

func CreateParty() *Party {
	dices := make([]*Dice, 0, 5)
	for range 5 {
		dices = append(dices, &Dice{})
	}
	p := Party{
		dices,
		make(map[string]*Score),
		start,
		0,
	}
	for _, k := range Keys {
		p.scores[k] = &Score{Labels[k], k, k == "dpm" || k == "tt1" || k == "tt2" || k == "bon" || k == "tot", false, 0, "   "}
	}
	return &p
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
	fmt.Printf("Dices : %+v", p.dices)
	for j := range 5 {
		fmt.Printf("D %v : %+v", j, p.dices[j])
	}

	p.step = roll
	p.roll += 1

	if precalc {
		p.Precalc()
	}

	return nil
}

func (p *Party) Keep(dice int) error {
	fmt.Printf("Keep: %v \n", dice)

	if p.dices[dice].lock == 0 {
		p.dices[dice].lock = p.roll
	} else if p.dices[dice].lock == p.roll {
		p.dices[dice].lock = 0
	}

	return nil
}

func (p *Party) setScore(key string, val int) {
	score := p.scores[key]
	score.set = true
	score.value = val
	p.scores[key] = score
}

func (p *Party) Mark(cmd string) error {
	dpm := false
	if p.scores["pac"].set && Compute("pac", p.dices) == 50 {
		dpm = true
	}

	p.setScore(cmd, Compute(cmd, p.dices))

	if dpm {
		p.setScore("dpm", p.scores["dpm"].value+100)
	}

	p.setScore("tt1", p.scores["bre"].value+p.scores["car"].value+p.scores["ful"].value+
		p.scores["psu"].value+p.scores["gsu"].value+p.scores["cha"].value+p.scores["pac"].value)

	dcsum := p.scores["dc1"].value + p.scores["dc2"].value + p.scores["dc3"].value +
		p.scores["dc4"].value + p.scores["dc5"].value + p.scores["dc6"].value
	if dcsum >= 63 {
		p.setScore("bon", 37)
	}

	p.setScore("tt2", dcsum+p.scores["bon"].value)
	p.setScore("tot", p.scores["tt1"].value+p.scores["tt2"].value)
	p.step = start
	p.roll = 0
	return nil
}
