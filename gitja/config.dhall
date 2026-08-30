-- gitja config for generating the /code section of mcol.xyz.
--
-- This expects to be run from the mcol.xyz repo root, with the repos below
-- checked out as sibling directories of that checkout (see
-- .github/workflows/deploy.yaml), mirroring gitja's own CI setup. Paths
-- here are resolved relative to the working directory gitja is invoked
-- from, not relative to this file.

let repos = ".."

let folders =
    [ "${repos}/bdf2flf"
    , "${repos}/gitja"
    , "${repos}/mcol.xyz"
    , "${repos}/mini-theme"
    , "${repos}/mkinitcpio-welcome"
    , "${repos}/pelican-microfeed"
    , "${repos}/pelican-minify-fontawesome"
    , "${repos}/qtile-config"
    , "${repos}/qtools"
    , "${repos}/sudoku-solver"
    , "${repos}/tide"
    , "${repos}/vim-misc"
    , "${repos}/wimp"
    , "${repos}/xanadu"
    , "${repos}/xoop"
    , "${repos}/zshrc"
    ]

let config =
    { repos = folders
    , scan = False
    , template = "./gitja/template"
    , output = "./gitja/output"
    , host = "https://mcol.xyz"
    }

in config
