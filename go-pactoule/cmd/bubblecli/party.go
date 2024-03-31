package main

import (
	"fmt"
	"pactoule/party"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/charmbracelet/lipgloss/table"
)

func showParty(m model) string {

	var precalStyle = lipgloss.NewStyle().
		Foreground(lipgloss.Color("202")).
		Align(lipgloss.Center)
	var valueStyle = lipgloss.NewStyle().Foreground(lipgloss.Color("86"))

	scores := m.party.GetScores()

	t := table.New().
		Border(lipgloss.NormalBorder()).
		BorderStyle(lipgloss.NewStyle().Foreground(lipgloss.Color("99"))).
		StyleFunc(func(row, col int) lipgloss.Style {
			switch {
			case row == 0:
				return lipgloss.NewStyle().Bold(true).
					PaddingLeft(1).PaddingRight(1).Align(lipgloss.Center).
					Foreground(lipgloss.Color("99"))
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

	playground := "Pactoule\n\n"
	strdices := []string{}
	styleDice := lipgloss.NewStyle().BorderStyle(lipgloss.RoundedBorder())
	styleDiceLock := styleDice.Copy().BorderForeground(lipgloss.Color("202")).Foreground(lipgloss.Color("202"))

	for _, d := range m.party.GetDices() {
		style := styleDice
		if d.Lock != 0 {
			style = styleDiceLock
		}
		strdices = append(strdices, style.Render(fmt.Sprintf("%v", d.Value)))
	}

	playground += lipgloss.JoinHorizontal(lipgloss.Center, strdices...) + "\n\n"

	logs := lipgloss.NewStyle().
		Border(lipgloss.NormalBorder()).
		BorderStyle(lipgloss.RoundedBorder()).
		BorderForeground(lipgloss.Color("228")).
		Render(m.logs)

	playground = lipgloss.NewStyle().
		AlignHorizontal(lipgloss.Center).
		Render(playground)

	return lipgloss.JoinHorizontal(
		lipgloss.Center,
		pactouleStyle.Render(t.Render()),
		pactouleStyle.Render(
			lipgloss.JoinVertical(lipgloss.Center, playground, getHelpers(false))),
		pactouleStyle.Render(logs),
	)
}

func getHelpers(scores bool) string {
	helpText := lipgloss.NewStyle().
		PaddingLeft(3).
		Foreground(lipgloss.Color("253"))
	helpKey := lipgloss.NewStyle().
		Foreground(lipgloss.Color("210"))

	helpers := []string{}
	keyb := map[string]string{
		"q": "quit", "esc": "menu",
		"x": "roll dice", "m": "mark score", "1-6/a-t": "keep dice",
	}
	for key, bind := range keyb {
		helpers = append(helpers, helpText.Render(fmt.Sprintf("%-3v", key))+" : "+helpKey.Render(bind))
	}

	return lipgloss.JoinHorizontal(
		lipgloss.Top,
		lipgloss.JoinVertical(lipgloss.Left, helpers[0:4]...),
		lipgloss.JoinVertical(lipgloss.Left, helpers[4:]...),
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
			m.logs += "Roll\n"
			if err := m.party.Roll(); err != nil {
				m.logs += fmt.Sprintf("⚠️ %v\n", err)
			}
		default:
			m.logs += "\nPressed:" + msg.String()
		}

	}
	return m, nil
}
