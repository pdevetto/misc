package party

import (
	"fmt"
	"math/rand/v2"
)

var (
	maxroll = 3
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
		maxroll,
		maxdice,
	}
	for _, k := range Keys {
		p.scores[k] = &Score{Labels[k], k, k == Dpm || k == Tt1 || k == Tt2 || k == Bon || k == Tot, false, 0, 0}
	}
	return &p
}

func (p *Party) Roll() error {
	if p.step == ROLL && p.roll >= p.maxroll {
		p.SwitchMark()
		return nil
	}
	if (p.step != START && p.step != ROLL) || p.roll >= p.maxroll {
		return fmt.Errorf("CAN'T ROLL NOW")
	}
	precalc := false

	for i, dice := range p.dices {
		if p.step == START {
			p.dices[i].Lock = 0
		}
		if dice.Lock == 0 {
			p.dices[i].Value = rand.IntN(p.maxdice) + 1
			precalc = precalc || true
		}
	}

	p.step = ROLL
	p.roll += 1

	if p.roll >= p.maxroll {
		p.step = MARK
	}

	if precalc {
		p.Precalc()
	}

	return nil
}

func (p *Party) Keep(dice int) error {
	if p.step != ROLL {
		return fmt.Errorf("NOT THE RIGHT TIME TO KEEP")
	}

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

func (p *Party) SwitchMark() {
	if p.step == ROLL {
		p.step = MARK
		return
	}
	if p.step == MARK {
		p.step = ROLL
		return
	}
}

func (p *Party) Mark(cmd Key) error {
	if p.step != ROLL && p.step != MARK {
		return fmt.Errorf("NOT THE RIGHT TIME TO MARK")
	}
	if p.scores[cmd].Set {
		return fmt.Errorf("SCORE ALREADY SET")
	}

	has_dpm := false
	if p.scores[Pac].Set && Compute(Pac, p.dices) == 50 {
		has_dpm = true
	}

	p.setScore(cmd, Compute(cmd, p.dices))

	if has_dpm {
		p.setScore(Dpm, p.scores[Dpm].Value+100)
	}

	p.setScore(Tt1, p.scores[Bre].Value+
		p.scores[Car].Value+
		p.scores[Ful].Value+
		p.scores[Psu].Value+
		p.scores[Gsu].Value+
		p.scores[Cha].Value+
		p.scores[Pac].Value)

	dcsum := p.scores[Dc1].Value +
		p.scores[Dc2].Value +
		p.scores[Dc3].Value +
		p.scores[Dc4].Value +
		p.scores[Dc5].Value +
		p.scores[Dc6].Value
	if dcsum >= 63 {
		p.setScore(Bon, 37)
	}

	p.setScore(Tt2, dcsum+p.scores[Bon].Value)
	p.setScore(Tot, p.scores[Tt1].Value+p.scores[Tt2].Value)
	p.step = START
	p.roll = 0
	return nil
}
