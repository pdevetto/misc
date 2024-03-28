package party

var (
	Keys = []Key{bre, car, ful, psu, gsu, cha, pac, dpm, tt1,
		dc1, dc2, dc3, dc4, dc5, dc6, bon, tt2, tot}
	Labels = map[Key]string{
		bre: "Brelan",
		car: "Carré",
		ful: "Full",
		psu: "Petite",
		gsu: "Grande",
		cha: "Chance",
		pac: "Pactoule",
		dpm: "DPM",
		tt1: "Tot 1",
		dc1: "Uns",
		dc2: "Deux",
		dc3: "Trois",
		dc4: "Quatre",
		dc5: "Cinq",
		dc6: "Six",
		bon: "Bonus",
		tt2: "Total 2",
		tot: "Total",
	}
)

type Step int
type Key int

const (
	START Step = iota
	ROLL
	bre Key = iota
	car
	ful
	psu
	gsu
	cha
	pac
	dpm
	tt1
	dc1
	dc2
	dc3
	dc4
	dc5
	dc6
	bon
	tt2
	tot
)

func GetKey(cmd string) Key {
	switch cmd {
	case "bre":
		return bre
	case "car":
		return car
	case "ful":
		return ful
	case "psu":
		return psu
	case "gsu":
		return gsu
	case "cha":
		return cha
	case "pac":
		return pac
	case "dc1":
		return dc1
	case "dc2":
		return dc2
	case "dc3":
		return dc3
	case "dc4":
		return dc4
	case "dc5":
		return dc5
	case "dc6":
		return dc6
	}
	return 0
}

type Dice struct {
	Value int
	Lock  int
}
type Dices = []*Dice
type Score struct {
	Label  string
	Key    Key
	Lock   bool
	Set    bool
	Value  int
	Precal int
}
type Party struct {
	dices  []*Dice
	scores map[Key]*Score
	step   Step
	roll   int
}

func (p *Party) GetStep() Step {
	return p.step
}

func (p *Party) GetScores() map[Key]*Score {
	return p.scores
}

func (p *Party) GetDices() []*Dice {
	return p.dices
}
