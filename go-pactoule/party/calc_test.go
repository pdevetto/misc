package party

import (
	"fmt"
	"testing"
)

func genDices(dd []int) []Dice {
	dices := []Dice{}
	for _, i := range dd {
		dices = append(dices, Dice{i, 0})
	}
	return dices
}

func TestNdice(t *testing.T) {
	// NDICE 2
	if !nDice(genDices([]int{5, 4, 1, 1, 7}), 2) {
		fmt.Println("Failed duo")
	}
	if !nDice(genDices([]int{1, 1, 1, 5, 6}), 2) {
		fmt.Println("Failed duo on bre")
	}
	if nDice(genDices([]int{2, 1, 3, 4, 5}), 2) {
		fmt.Println("False duo")
	}
	// NDICE 3
	if !nDice(genDices([]int{5, 4, 1, 1, 1}), 3) {
		fmt.Println("Failed bre")
	}
	if !nDice(genDices([]int{1, 1, 1, 1, 5}), 3) {
		fmt.Println("Failed bre on carre")
	}
	if nDice(genDices([]int{1, 1, 3, 4, 5}), 3) {
		fmt.Println("False bre")
	}
	// NDICE 4
	if !nDice(genDices([]int{2, 2, 2, 2, 1}), 4) {
		fmt.Println("Failed car")
	}
	if !nDice(genDices([]int{2, 2, 2, 2, 2}), 4) {
		fmt.Println("Failed car on pactoule")
	}
	if nDice(genDices([]int{1, 2, 3, 4, 5}), 4) {
		fmt.Println("False car")
	}
	// NDICE 5
	if nDice(genDices([]int{2, 2, 2, 2, 5}), 5) {
		fmt.Println("False pactoule")
	}
	if !nDice(genDices([]int{2, 2, 2, 2, 2}), 5) {
		fmt.Println("Failed pactoule")
	}
}

func TestSumDice(t *testing.T) {
	if sumDice(genDices([]int{1, 2, 3, 4, 5})) != 15 {
		fmt.Println("Failed sum")
	}
	if sumDice(genDices([]int{4, 5})) != 9 {
		fmt.Println("Failed sum")
	}
	if sumDice(genDices([]int{1, 2, 3, 5})[1:3]) != 5 {
		fmt.Println("Failed sum")
	}
}

func TestSumDiceOfK(t *testing.T) {
	if sumDiceOfK(genDices([]int{1, 1, 1, 4, 5}), 1) != 3 {
		fmt.Println("Failed sum of 1")
	}
	if sumDiceOfK(genDices([]int{4, 5}), 4) != 4 {
		fmt.Println("Failed sum of 4")
	}
	if sumDiceOfK(genDices([]int{1, 2, 3, 5}), 6) != 0 {
		fmt.Println("Failed sum of 6")
	}
	if sumDiceOfK(genDices([]int{5, 5, 5, 5, 5}), 5) != 25 {
		fmt.Println("Failed sum of 5")
	}
}

func TestSuiteDice(t *testing.T) {
	if !suiteDice(genDices([]int{1, 2, 3, 4, 5}), 5) {
		fmt.Println("Failed big su")
	}
	if !suiteDice(genDices([]int{4, 1, 3, 2, 5}), 5) {
		fmt.Println("Failed big su des")
	}
	if !suiteDice(genDices([]int{4, 1, 3, 2, 5}), 4) {
		fmt.Println("Failed lil su des")
	}
	if suiteDice(genDices([]int{1, 1, 3, 2, 5}), 4) {
		fmt.Println("False lil su")
	}
	if suiteDice(genDices([]int{1, 2, 3, 5, 6}), 4) {
		fmt.Println("False lil su")
	}
	if suiteDice(genDices([]int{1, 2, 3, 5, 6}), 5) {
		fmt.Println("False big su")
	}
}
