#!/usr/bin/env python3
#
# Generate a 'descriptions' file in each repo folder
#
# Make sure to re-run this script after editing any descriptions or adding repos.

from pathlib import Path

repo_dir = Path("~/git/").expanduser()

descriptions = {
    "bdf2flf": "Convert BDF bitmap fonts to flf fonts for figlet",
    "gitja": "🐙 Templated web page generator for your git repositories",
    "mcol.xyz": "The main content of my blog mcol.xyz",
    "mini-theme": "A mini theme for the pelican static site generator",
    "mkinitcpio-welcome": 'mkinitcpio hooks that print the word "Welcome" in big letters and draw a box for inputting an encryption password and catching the fsck output during early userspace. See blog post for a video: https://mcol.xyz/2020/06/ricing-early-userspace.html',
    "pelican-microfeed": "Pelican plugin to create tiny single-page feeds",
    "pelican-minify-fontawesome": "Pelican plugin to minify fontawesome assets to include used icons.",
    "pixels": "Neuropixels recording data processing and analysis pipeline",
    "pywayland": "Python bindings to libwayland",
    "pywlroots": "Python bindings to the wlroots Wayland library",
    "qtile": "A pure-Python tiling window manager for X11 and Wayland.",
    "qtools": "An (outdated) collection of plugins for Qtile.",
    "reach": "Rodent reaching task control software",
    "screenshot-gallery-generator": "Screenshot gallery generator for nixers",
    "sudoku-solver": "A small haskell script to solve sudoku puzzles",
    "tide": "A tiny vim plugin that sends a word/line/paragraph of text from vim into a tmux pane for execution.",
    "unix.sexy-react": "A web app to help you design beautiful desktop environments.",
    "vim-misc": "My vim configuration",
    "wimp": "gimp but for windows: a wayland compositor",
    "xanadu": "Virtual desktop underlay for Wayland and X11",
    "xoop": "Loop your X cursor around the screen 👉😎👉",
    "zshrc": "My zsh configuration",
}

for name, desc in descriptions.items():
    path = repo_dir / name / ".git" / "description"
    with path.open("w") as f:
        f.write(desc)
