package party

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
type Score struct {
	label  string
	key    string
	lock   bool
	set    bool
	value  int
	precal string
}
type Party struct {
	dices  *[5]Dice
	scores map[string]*Score
	step   Step
	roll   int
}

func CreateParty() *Party {
	p := Party{
		&[5]Dice{},
		make(map[string]*Score),
		start,
		0,
	}
	for _, k := range Keys {
		p.scores[k] = &Score{Labels[k], k, k == "dpm" || k == "tt1" || k == "tt2" || k == "bon" || k == "tot", false, 0, "   "}
	}
	return &p
}
