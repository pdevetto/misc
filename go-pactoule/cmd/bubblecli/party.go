package main

import (
	"fmt"
	"pactoule/party"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/charmbracelet/lipgloss/table"
)

var color_base = []string{"228", "202", "86", "99"}
var color_firewatch = []string{"#FFAF45", "#FB6D48", "#D74B76", "#673F69"}
var color_coffee = []string{"#0C0C0C", "#481E14", "#9B3922", "#F2613F"}
var color_neon_bluepink = []string{"#F67280", "#C06C84", "#6C5B7B", "#355C7D"}
var colors = color_neon_bluepink

func showParty(m model) string {

	var precalStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color(colors[0])).
		Align(lipgloss.Center)
	var valueStyle = lipgloss.NewStyle().Foreground(lipgloss.Color(colors[2]))

	scores := m.party.GetScores()

	t := table.New().
		Border(lipgloss.NormalBorder()).
		BorderStyle(lipgloss.NewStyle().Foreground(lipgloss.Color(colors[3]))).
		StyleFunc(func(row, col int) lipgloss.Style {
			switch {
			case row == 0:
				return lipgloss.NewStyle().Bold(true).
					PaddingLeft(1).PaddingRight(1).Align(lipgloss.Center).
					Foreground(lipgloss.Color(colors[3]))
			default:
				return lipgloss.NewStyle().
					PaddingLeft(1).PaddingRight(1)
			}
		}).
		Headers("Major", "score", "Minor", "score")

	for i := range 9 {
		row := []string{}

		for _, s := range []*party.Score{
			scores[party.Keys[i]],
			scores[party.Keys[i+9]],
		} {
			row = append(row, s.Label)
			if !s.Set && !s.Lock && m.party.GetStep() != party.START {
				row = append(row, precalStyle.Render(fmt.Sprintf("%d", s.Precal)))
			} else if !s.Set && !s.Lock {
				row = append(row, "")
			} else {
				row = append(row, valueStyle.Render(fmt.Sprintf("%d", s.Value)))
			}
		}

		t.Row(row...)
	}

	playground := lipgloss.NewStyle().
		Foreground(lipgloss.Color(colors[0])).
		Bold(true).
		Render("Pactoule") + "\n"
	strdices := []string{}

	for _, d := range m.party.GetDices() {
		value, style := getStrDice(d.Value, d.Lock != 0)
		strdices = append(strdices, style.Render(value))
	}

	playground += lipgloss.JoinHorizontal(lipgloss.Center, strdices...)

	playground = lipgloss.JoinVertical(
		lipgloss.Center,
		playground,
		getHelpers(m.party.GetStep() == party.MARK),
	)

	return lipgloss.JoinHorizontal(
		lipgloss.Top,
		pactouleStyle.Render(playground),
		pactouleStyle.Render(t.Render()),
	)
}

func getStrDice(value int, lock bool) (string, lipgloss.Style) {
	styleDice := lipgloss.NewStyle().Padding(0, 2, 0, 1).BorderStyle(lipgloss.RoundedBorder())
	styleDiceLock := styleDice.Copy().BorderForeground(lipgloss.Color(colors[1])).Foreground(lipgloss.Color(colors[1]))
	style := styleDice
	if lock {
		style = styleDiceLock
	}
	var svalue string
	//svalue := fmt.Sprintf("%v", value)
	// Try with ⚪ and ⚫ emoji instead of ⬤ (but after we successfully handle lock)
	switch value {
	case 1:
		svalue = "     \n  ⬤  \n     "
	case 2:
		svalue = "⬤    \n     \n    ⬤"
	case 3:
		svalue = "⬤    \n  ⬤  \n    ⬤"
	case 4:
		svalue = "⬤   ⬤\n     \n⬤   ⬤"
	case 5:
		svalue = "⬤   ⬤\n  ⬤  \n⬤   ⬤"
	case 6:
		svalue = "⬤   ⬤\n⬤   ⬤\n⬤   ⬤"
	case 7:
		svalue = "⬤   ⬤\n⬤ ⬤ ⬤\n⬤   ⬤"
	case 8:
		svalue = "⬤ ⬤ ⬤\n⬤   ⬤\n⬤ ⬤ ⬤"
	case 9:
		svalue = "⬤ ⬤ ⬤\n⬤ ⬤ ⬤\n⬤ ⬤ ⬤"
	default:
		svalue = "     \n  ❔ \n     "
	}

	return svalue, style
}

func getHelpers(scores bool) string {
	//helpHeader := lipgloss.NewStyle().Foreground(lipgloss.Color("252"))
	helpText := lipgloss.NewStyle().
		Foreground(lipgloss.Color("233"))
	helpKey := lipgloss.NewStyle().
		Foreground(lipgloss.Color("250"))

	keyb := map[string]string{
		"q":   "quit",
		"esc": "menu",
		" ":   " ",
		"x":   "roll dice",
		"m":   "mark score", // longest : 10 so %12v
		"a>t": "keep dice",

		"b":   party.Labels[party.Bre],
		"c":   party.Labels[party.Car],
		"f":   party.Labels[party.Ful],
		"s":   party.Labels[party.Psu],
		"g":   party.Labels[party.Gsu],
		"h":   party.Labels[party.Cha],
		"p":   party.Labels[party.Pac],
		"1":   party.Labels[party.Dc1],
		"2":   party.Labels[party.Dc2],
		"3":   party.Labels[party.Dc3],
		"4":   party.Labels[party.Dc4],
		"5":   party.Labels[party.Dc5],
		"6":   party.Labels[party.Dc6],
		"alt": "CANCEL",
	}
	var listHelpers []string
	var nHelp int
	if scores {
		listHelpers = []string{"alt", " ", "b", "c", "f", "s", "g", "h", "p",
			"1", "2", "3", "4", "5", "6", " ", "q", "esc"}
		nHelp = 8
	} else {
		listHelpers = []string{"x", "a>t", "m", "q", "esc"}
		nHelp = 3
	}

	helpers := []string{}

	for _, key := range listHelpers {
		helpers = append(helpers, helpText.Render(fmt.Sprintf("%3v", key))+" "+helpKey.Render(fmt.Sprintf("%-12v", keyb[key])))
	}

	return lipgloss.JoinHorizontal(
		lipgloss.Top,
		lipgloss.JoinVertical(lipgloss.Left, helpers[0:nHelp]...),
		lipgloss.JoinVertical(lipgloss.Left, helpers[nHelp:]...),
	)

}

func controlParty(msg tea.Msg, m model) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			return m, tea.Quit
		case "esc":
			m.step = menu
		case "up", "down":
		case " ", "x":
			s := "Roll: "
			if err := m.party.Roll(); err != nil {
				s += fmt.Sprintf("⚠️ %v", err)
			}
			m.logs = append(m.logs, s)
		case "1", "2", "3", "4", "5", //"6", "7", "8", "9", "0",
			"a", "z", "e", "r", "t": //"u", "i", "o", "p":
			s := "Keep: "
			di := map[string]int{
				"1": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": -1, "7": -1, "8": -1, "9": -1, "0": -1,
				"a": 0, "z": 1, "e": 2, "r": 3, "t": 4, "u": -1, "i": -1, "o": -1, "p": -1,
			}
			if di[msg.String()] >= 0 {
				if err := m.party.Keep(di[msg.String()]); err != nil {
					s += fmt.Sprintf("⚠️ %v", err)
				}
			}
			m.logs = append(m.logs, s)
		default:
			m.logs = append(m.logs, "Pressed:"+msg.String())
		}

	}
	return m, nil
}
