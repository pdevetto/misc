package party

import (
	"fmt"
	"math/rand/v2"
)

var (
	maxroll = 124
	maxdice = 6
)

func CreateParty() *Party {
	dices := make([]*Dice, 0, 5)
	for range 5 {
		dices = append(dices, &Dice{})
	}
	p := Party{
		dices,
		make(map[Key]*Score),
		START,
		0,
	}
	for _, k := range Keys {
		p.scores[k] = &Score{Labels[k], k, k == dpm || k == tt1 || k == tt2 || k == bon || k == tot, false, 0, 0}
	}
	return &p
}

func (p *Party) Roll() error {
	if (p.step != START && p.step != ROLL) || p.roll > maxroll {
		return fmt.Errorf("CAN'T ROLL NOW")
	}
	precalc := false
	fmt.Printf("...<roll%d>\n", p.roll+1)

	for i, dice := range p.dices {
		if p.step == START {
			p.dices[i].Lock = 0
		}
		if dice.Lock == 0 {
			p.dices[i].Value = rand.IntN(maxdice) + 1
			precalc = precalc || true
		}
	}
	fmt.Printf("Dices : %+v", p.dices)
	for j := range 5 {
		fmt.Printf("D %v : %+v", j, p.dices[j])
	}

	p.step = ROLL
	p.roll += 1

	if precalc {
		p.Precalc()
	}

	return nil
}

func (p *Party) Keep(dice int) error {
	if p.step != ROLL {
		return fmt.Errorf("NOT THE RIGHT TIME TO KEEP")
	}

	fmt.Printf("Keep: %v \n", dice)

	if p.dices[dice].Lock == 0 {
		p.dices[dice].Lock = p.roll
	} else if p.dices[dice].Lock == p.roll {
		p.dices[dice].Lock = 0
	}

	return nil
}

func (p *Party) setScore(key Key, val int) {
	score := p.scores[key]
	score.Set = true
	score.Value = val
	p.scores[key] = score
}

func (p *Party) Mark(cmd Key) error {
	if p.step != ROLL {
		return fmt.Errorf("NOT THE RIGHT TIME TO MARK")
	}
	if p.scores[cmd].Set {
		return fmt.Errorf("SCORE ALREADY SET")
	}

	has_dpm := false
	if p.scores[pac].Set && Compute(pac, p.dices) == 50 {
		has_dpm = true
	}

	p.setScore(cmd, Compute(cmd, p.dices))

	if has_dpm {
		p.setScore(dpm, p.scores[dpm].Value+100)
	}

	p.setScore(tt1, p.scores[bre].Value+
		p.scores[car].Value+
		p.scores[ful].Value+
		p.scores[psu].Value+
		p.scores[gsu].Value+
		p.scores[cha].Value+
		p.scores[pac].Value)

	dcsum := p.scores[dc1].Value +
		p.scores[dc2].Value +
		p.scores[dc3].Value +
		p.scores[dc4].Value +
		p.scores[dc5].Value +
		p.scores[dc6].Value
	if dcsum >= 63 {
		p.setScore(bon, 37)
	}

	p.setScore(tt2, dcsum+p.scores[bon].Value)
	p.setScore(tot, p.scores[tt1].Value+p.scores[tt2].Value)
	p.step = START
	p.roll = 0
	return nil
}
