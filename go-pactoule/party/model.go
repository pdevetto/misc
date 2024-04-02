package party

var (
	Keys = []Key{Bre, Car, Ful, Psu, Gsu, Cha, Pac, Dpm, Tt1,
		Dc1, Dc2, Dc3, Dc4, Dc5, Dc6, Bon, Tt2, Tot}
	Labels = map[Key]string{
		Bre: "Brelan",
		Car: "Carré",
		Ful: "Full",
		Psu: "Petite",
		Gsu: "Grande",
		Cha: "Chance",
		Pac: "Pactoule",
		Dpm: "DPM",
		Tt1: "Subtot 1",
		Dc1: "Uns",
		Dc2: "Deux",
		Dc3: "Trois",
		Dc4: "Quatre",
		Dc5: "Cinq",
		Dc6: "Six",
		Bon: "Bonus",
		Tt2: "Subtot 2",
		Tot: "Total",
	}
)

type Step int
type Key int

const (
	START Step = iota
	ROLL
	MARK
	Bre Key = iota
	Car
	Ful
	Psu
	Gsu
	Cha
	Pac
	Dpm
	Tt1
	Dc1
	Dc2
	Dc3
	Dc4
	Dc5
	Dc6
	Bon
	Tt2
	Tot
)

func GetKey(cmd string) Key {
	switch cmd {
	case "bre":
		return Bre
	case "car":
		return Car
	case "ful":
		return Ful
	case "psu":
		return Psu
	case "gsu":
		return Gsu
	case "cha":
		return Cha
	case "pac":
		return Pac
	case "dc1":
		return Dc1
	case "dc2":
		return Dc2
	case "dc3":
		return Dc3
	case "dc4":
		return Dc4
	case "dc5":
		return Dc5
	case "dc6":
		return Dc6
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
	dices   []*Dice
	scores  map[Key]*Score
	step    Step
	roll    int
	maxroll int
	maxdice int
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

func (p *Party) GetRoll() int {
	return p.roll
}
