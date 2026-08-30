#!/usr/bin/env python3
#
# Writes a 'description' file into each sibling repo checkout so gitja picks
# up a human-readable description instead of falling back to the repo's
# folder name. Run this after cloning the repos listed in config.dhall and
# before running gitja itself (see .github/workflows/deploy.yaml).
#
# Make sure to re-run this after editing any descriptions or adding repos.

from pathlib import Path

repo_dir = Path(__file__).resolve().parent.parent.parent

descriptions = {
    "bdf2flf": "Convert BDF bitmap fonts to flf fonts for figlet",
    "gitja": "🐙 Templated web page generator for your git repositories",
    "mcol.xyz": "The main content of my blog mcol.xyz",
    "mini-theme": "A mini theme for the pelican static site generator",
    "mkinitcpio-welcome": 'mkinitcpio hooks that print the word "Welcome" in big letters and draw a box for inputting an encryption password and catching the fsck output during early userspace. See blog post for a video: https://mcol.xyz/2020/06/ricing-early-userspace.html',
    "pelican-microfeed": "Pelican plugin to create tiny single-page feeds",
    "pelican-minify-fontawesome": "Pelican plugin to minify fontawesome assets to include used icons.",
    "qtile-config": "My Qtile window manager configuration",
    "qtools": "An (outdated) collection of plugins for Qtile.",
    "sudoku-solver": "A small haskell script to solve sudoku puzzles",
    "tide": "A tiny vim plugin that sends a word/line/paragraph of text from vim into a tmux pane for execution.",
    "vim-misc": "My vim configuration",
    "wimp": "gimp but for windows: a wayland compositor",
    "xanadu": "Virtual desktop underlay for Wayland and X11",
    "xoop": "Loop your X cursor around the screen 👉😎👉",
    "zshrc": "My zsh configuration",
}

for name, desc in descriptions.items():
    path = repo_dir / name / ".git" / "description"
    if not path.parent.is_dir():
        print(f"skipping {name}: not checked out at {path.parent}")
        continue
    path.write_text(desc)
