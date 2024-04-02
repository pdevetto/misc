package main

import (
	"fmt"
	"math/rand"
	"pactoule/party"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/charmbracelet/lipgloss/table"
)

var subcmd = map[string]party.Key{
	"b": party.Bre,
	"c": party.Car,
	"f": party.Ful,
	"s": party.Psu,
	"g": party.Gsu,
	"h": party.Cha,
	"p": party.Pac,
	"1": party.Dc1,
	"2": party.Dc2,
	"3": party.Dc3,
	"4": party.Dc4,
	"5": party.Dc5,
	"6": party.Dc6,
}

func controlParty(msg tea.Msg, m model) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			return m, tea.Quit
		case "esc":
			m.step = menu
			if m.party.GetStep() == party.FINISH {
				m.scores = append(m.scores, highScore{"Piotr", m.party.GetScores()[party.Tot].Value})
				m.party = nil
			}
		case "=":
			colors = allcolors[rand.Intn(len(allcolors))]
		case "up", "down":

		case " ", "x":
			s := "Roll: "
			if err := m.party.Roll(); err != nil {
				s += fmt.Sprintf("⚠️ %v", err)
			}
			m.logs = append(m.logs, s)
		case "a", "z", "e", "r", "t", "y", "u", "i", "o":
			s := "Keep: "
			di := map[string]int{
				"a": 0, "z": 1, "e": 2, "r": 3, "t": 4, "y": 5, "u": 6, "i": 7, "o": 8,
			}
			if di[msg.String()] >= 0 {
				if err := m.party.Keep(di[msg.String()]); err != nil {
					s += fmt.Sprintf("⚠️ %v", err)
				}
			}
			m.logs = append(m.logs, s)
		case "m":
			m.party.SwitchMark()
		case "alt":
			m.party.SwitchMark()
		case "b", "c", "f", "s", "g", "h", "p", "1", "2", "3", "4", "5", "6":
			if m.party.GetStep() == party.MARK {
				err := m.party.Mark(subcmd[msg.String()])
				if err != nil {
					m.logs = append(m.logs, fmt.Sprintf("⚠️ couldn' mark : %v -> %v \n", err, subcmd))
				}
				for _, ss := range m.party.GetScores() {
					if !ss.Set {
						m.logs = append(m.logs, fmt.Sprintf("Rest %v", ss.Label))
						return m, nil
					}
				}
			}
		default:
			m.logs = append(m.logs, "Pressed:"+msg.String())
		}
	}
	return m, nil
}

type color = []string

var allcolors = []color{
	[]string{"#FFAF45", "#FB6D48", "#D74B76", "#673F69", "firewatch"},
	[]string{"#FFEDD8", "#EABE6C", "#891652", "#240A34", "VHS"},
	[]string{"#F5F5F5", "#F5EACB", "#dcd2b6", "#3F2305", "pyjamas"},
	[]string{"#ECE3CE", "#739072", "#4F6F52", "#3A4D39", "forest"},
	[]string{"#f7a08b", "#F2613F", "#6c2717", "#0C0C0C", "halloween"}, /*"#F2613F", "#9B3922", "#481E14"*/
	[]string{"#DCF2F1", "#7FC7D9", "#365486", "#0F1035", "deepblue"},

	//[]string{"", "", "", "", ""},

}
var colors = allcolors[rand.Intn(len(allcolors))]

func showParty(m model) string {
	head := lipgloss.NewStyle().
		Foreground(lipgloss.Color(colors[0])).
		Bold(true)
	playground := head.Render("Pactoule") + "\n" +
		head.Copy().Background(lipgloss.Color(colors[0])).Render("   ") +
		head.Copy().Background(lipgloss.Color(colors[1])).Render("   ") +
		head.Copy().Background(lipgloss.Color(colors[2])).Render("   ") +
		head.Copy().Background(lipgloss.Color(colors[3])).Render("   ") + "\n" +
		head.Copy().Bold(false).Render(fmt.Sprintf("roll: %v/%v", m.party.GetRoll(), m.party.GetMaxRoll())) + "\n\n"
	strdices := []string{}

	for _, d := range m.party.GetDices() {
		value, style := getStrDice(d.Value, d.Lock != 0)
		strdices = append(strdices, style.Render(value))
	}

	playground += lipgloss.JoinHorizontal(lipgloss.Center, strdices...) + "\n"

	playground = lipgloss.JoinVertical(
		lipgloss.Center,
		playground,
		getHelpers(m.party.GetStep()),
	)

	scoreTable := getScoreTable(m.party.GetScores(), m.party.GetStep())

	return lipgloss.JoinHorizontal(
		lipgloss.Top,
		pactouleStyle.Render(playground),
		pactouleStyle.Render(scoreTable),
	)
}

func getScoreTable(scores map[party.Key]*party.Score, step party.Step) string {
	var precalStyle = lipgloss.NewStyle().Foreground(lipgloss.Color(colors[1])).Align(lipgloss.Center).Render
	var valueStyle = lipgloss.NewStyle().Foreground(lipgloss.Color(colors[2])).Render
	var preczStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("233")).Render

	t := table.New().
		Border(lipgloss.NormalBorder()).
		BorderStyle(lipgloss.NewStyle().Foreground(lipgloss.Color(colors[1]))).
		StyleFunc(func(row, col int) lipgloss.Style {
			switch {
			case row == 0:
				return lipgloss.NewStyle().Bold(true).
					PaddingLeft(1).PaddingRight(3).
					Foreground(lipgloss.Color(colors[1]))
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
			if !s.Set && step != party.START {
				if s.Precal != 0 {
					row = append(row, "> "+precalStyle(fmt.Sprintf("%2d", s.Precal)))
				} else {
					row = append(row, preczStyle(fmt.Sprintf("> %2d", s.Precal)))
				}

			} else if !s.Set {
				row = append(row, "")
			} else if s.Key == party.Bon && s.Precal != 0 && step != party.START {
				row = append(row, valueStyle(fmt.Sprintf("%3d (-%d)", s.Value, s.Precal)))
			} else {
				row = append(row, valueStyle(fmt.Sprintf("%3d", s.Value)))
			}
		}

		t.Row(row...)
	}
	return t.Render()
}

func getStrDice(value int, lock bool) (string, lipgloss.Style) {
	styleDice := lipgloss.NewStyle().Padding(0, 2, 0, 1).BorderStyle(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color(colors[0])).Foreground(lipgloss.Color(colors[0]))
	styleDiceLock := styleDice.Copy().BorderForeground(lipgloss.Color(colors[3])).Foreground(lipgloss.Color(colors[3]))
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

func getHelpers(step party.Step) string {
	//helpHeader := lipgloss.NewStyle().Foreground(lipgloss.Color("252"))
	helpText := lipgloss.NewStyle().
		Foreground(lipgloss.Color("#070606"))
	helpKey := lipgloss.NewStyle().
		Foreground(lipgloss.Color("254"))

	keyb := map[string]string{
		"q":   "quit",
		"esc": "menu",
		"=":   "(" + colors[4] + ")",
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
	var n1 int
	var n2 int
	if step == party.FINISH {
		listHelpers = []string{
			"=", "esc", "q",
		}
		n1 = 3
		n2 = 3
	} else if step == party.MARK {
		keyb["m"] = keyb["alt"]
		listHelpers = []string{
			"b", "c", "f", "s", "g", "h", "p",
			"1", "2", "3", "4", "5", "6",
			"=", "m", "esc", "q",
		}
		n1 = 7
		n2 = 13
	} else {
		listHelpers = []string{"x", "a>t", "m", "=", "esc", "q"}
		n1 = 3
		n2 = 6
	}

	helpers := []string{}

	for _, key := range listHelpers {
		helpers = append(helpers, helpKey.Render(fmt.Sprintf("%3v", key))+" "+helpText.Render(fmt.Sprintf("%-12v", keyb[key])))
	}

	return lipgloss.JoinHorizontal(
		lipgloss.Top,
		lipgloss.JoinVertical(lipgloss.Left, helpers[0:n1]...),
		lipgloss.JoinVertical(lipgloss.Left, helpers[n1:n2]...),
		lipgloss.JoinVertical(lipgloss.Left, helpers[n2:]...),
	)

}
