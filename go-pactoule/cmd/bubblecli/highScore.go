package main

import (
	"fmt"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

func showHighscore(m model) string {
	scores := []string{}
	for _, highscore := range m.scores {
		scores = append(scores, fmt.Sprintf("%v - %v", highscore.name, highscore.score))
	}
	return lipgloss.JoinVertical(
		lipgloss.Top,
		scores...,
	)
}

func controlHighscore(msg tea.Msg, m model) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "ctrl+c", "q":
			return m, tea.Quit
		case "esc":
			m.step = menu
		}
	}
	return m, nil
}
