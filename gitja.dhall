-- After adding repos, make sure to re-run gitja_descriptions.py

let repos = ".."

let folders = [
    , "${repos}/bdf2flf"
    , "${repos}/gitja"
    , "${repos}/mcol.xyz"
    , "${repos}/mini-theme"
    , "${repos}/mkinitcpio-welcome"
    , "${repos}/pelican-microfeed"
    , "${repos}/pelican-minify-fontawesome"
    , "${repos}/pixels"
    , "${repos}/pywayland"
    , "${repos}/pywlroots"
    , "${repos}/qtile"
    , "${repos}/qtools"
    , "${repos}/reach"
    , "${repos}/screenshot-gallery-generator"
    , "${repos}/sudoku-solver"
    , "${repos}/tide"
    , "${repos}/unix.sexy-react"
    , "${repos}/vim-misc"
    , "${repos}/wimp"
    , "${repos}/xanadu"
    , "${repos}/xoop"
    , "${repos}/zshrc"
    ]

let config =
    { repos = folders
    , scan = False
    , template = "./gitja-template"
    , output = "./output-gitja"
    , host = "https://mcol.xyz"
    --, host = "http://localhost:8000"
    }

in config
