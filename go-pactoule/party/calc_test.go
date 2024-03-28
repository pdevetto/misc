package party

import (
	"testing"
)

func genDices(dd []int) []*Dice {
	dices := []*Dice{}
	for _, i := range dd {
		dices = append(dices, &Dice{i, 0})
	}
	return dices
}

func Test_nDice(t *testing.T) {
	type args struct {
		dd []int
		n  int
	}
	tests := []struct {
		name string
		args args
		want bool
	}{
		{"Duo", args{[]int{5, 4, 1, 1, 7}, 2}, true},
		{"Duo on Pac", args{[]int{5, 5, 5, 5, 5}, 2}, true},
		{"Not duo", args{[]int{5, 4, 1, 3, 7}, 2}, false},
		{"Bre", args{[]int{5, 3, 3, 3, 7}, 3}, true},
		{"Bre on Car", args{[]int{4, 4, 4, 4, 7}, 3}, true},
		{"Not bre", args{[]int{1, 2, 3, 4, 5}, 3}, false},
		{"Car", args{[]int{5, 3, 3, 3, 3}, 4}, true},
		{"Not car", args{[]int{1, 4, 4, 4, 7}, 4}, false},
		{"Pac", args{[]int{6, 6, 6, 6, 6}, 5}, true},
		{"Not Pac", args{[]int{6, 6, 6, 6, 5}, 5}, false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := nDice(genDices(tt.args.dd), tt.args.n); got != tt.want {
				t.Errorf("nDice() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_suiteDice(t *testing.T) {
	type args struct {
		dd []int
		n  int
	}
	tests := []struct {
		name string
		args args
		want bool
	}{
		{"big s", args{[]int{1, 2, 3, 4, 5}, 5}, true},
		{"BIG S", args{[]int{2, 3, 4, 5, 6}, 5}, true},
		{"Not big S", args{[]int{2, 3, 4, 4, 5}, 5}, false},
		{"GBI S", args{[]int{4, 3, 2, 6, 5}, 5}, true},

		{"lil s", args{[]int{1, 2, 3, 4, 5}, 4}, true},
		{"LIL S", args{[]int{2, 3, 4, 5, 6}, 4}, true},
		{"lli S", args{[]int{2, 3, 4, 4, 5}, 4}, true},
		{"not lil S", args{[]int{2, 3, 5, 6, 1}, 4}, false},

		{"strange", args{[]int{1, 2, 3, 4, 6}, 4}, true},
		{"strange", args{[]int{1, 2, 3, 5, 6}, 4}, false},

		{"small 3 su 1", args{[]int{1, 2, 3, 5, 6}, 3}, true},
		{"small 3 su 2", args{[]int{1, 3, 4, 5, 7}, 3}, true},
		{"small 3 su 3", args{[]int{1, 3, 5, 6, 7}, 3}, true},
		{"not small 3 su", args{[]int{1, 2, 4, 6, 7, 9}, 3}, false},
		{"small_su", args{[]int{1, 2, 3, 4, 5, 6, 7}, 2}, true},
		{"not small_su", args{[]int{1, 3, 5, 7, 9, 11, 13}, 2}, false},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := suiteDice(genDices(tt.args.dd), tt.args.n); got != tt.want {
				t.Errorf("nDice() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_sumDice(t *testing.T) {
	tests := []struct {
		name string
		dd   []int
		want int
	}{
		{"Sum 1", []int{1, 2, 3, 4, 5}, 15},
		{"Sum 1", []int{4, 5}, 9},
		{"Sum 1", []int{1, 2, 3, 5}[1:3], 5},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := sumDice(genDices(tt.dd)); got != tt.want {
				t.Errorf("sumDice() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_sumDiceOfK(t *testing.T) {
	tests := []struct {
		name string
		dd   []int
		di   int
		want int
	}{
		{"Sum 1", []int{1, 1, 1, 1, 5}, 1, 4},
		{"Sum 4", []int{4, 4, 5}, 4, 8},
		{"Sum 5", []int{5, 5, 5, 5, 5}, 5, 25},
		{"Sum 6", []int{5, 5, 5, 5, 5}, 6, 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := sumDiceOfK(genDices(tt.dd), tt.di); got != tt.want {
				t.Errorf("sumDice() = %v, want %v", got, tt.want)
			}
		})
	}
}

func TestCompute(t *testing.T) {
	tests := []struct {
		name string
		key  Key
		dd   []int
		want int
	}{
		{"bre", bre, []int{2, 2, 3, 2, 5}, 14},
		{"not bre", bre, []int{2, 2, 3, 1, 5}, 0},

		{"car", car, []int{2, 2, 2, 2, 5}, 13},
		{"not car", car, []int{2, 2, 3, 1, 5}, 0},

		{"ful", ful, []int{2, 2, 2, 3, 3}, 25},
		{"ful", ful, []int{5, 5, 5, 5, 5}, 25},
		{"not ful", ful, []int{1, 2, 3, 4, 5}, 0},
		{"not ful", ful, []int{2, 2, 3, 3, 5}, 0},
		{"not ful", ful, []int{2, 2, 2, 2, 5}, 0},
		{"psu", psu, []int{4, 3, 2, 1, 6}, 30},
		{"not psu", psu, []int{2, 2, 3, 1, 5}, 0},
		{"gsu", gsu, []int{1, 2, 3, 4, 5}, 40},
		{"not gsu", gsu, []int{2, 2, 3, 1, 5}, 0},
		{"cha", cha, []int{2, 2, 3, 2, 5}, 14},
		{"cha", cha, []int{4, 1, 6, 2, 1}, 14},
		{"pac", pac, []int{1, 1, 1, 1, 1}, 50},
		{"not pac", pac, []int{2, 2, 3, 1, 5}, 0},
		{"dc1", dc1, []int{2, 1, 3, 1, 5}, 2},
		{"dc1", dc1, []int{2, 2, 3, 4, 5}, 0},
		{"dc2", dc2, []int{2, 2, 3, 2, 5}, 6},
		{"dc3", dc3, []int{2, 2, 3, 2, 5}, 3},
		{"dc4", dc4, []int{2, 4, 3, 4, 5}, 8},
		{"dc5", dc5, []int{2, 2, 3, 2, 5}, 5},
		{"dc6", dc6, []int{2, 2, 3, 2, 5}, 0},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := Compute(tt.key, genDices(tt.dd)); got != tt.want {
				t.Errorf("Compute() = %v, want %v", got, tt.want)
			}
		})
	}
}

func Test_differentDices(t *testing.T) {
	tests := []struct {
		name string
		dd   []int
		want int
	}{
		{"1 diff", []int{1, 1, 1, 1, 1}, 1},
		{"2 diff", []int{1, 2, 1, 1, 1}, 2},
		{"5 diff", []int{1, 2, 3, 4, 5}, 5},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			if got := differentDices(genDices(tt.dd)); got != tt.want {
				t.Errorf("differentDices() = %v, want %v", got, tt.want)
			}
		})
	}
}
