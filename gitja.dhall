let repos = ".."

let folders =
    [ "${repos}/gitja"
    , "${repos}/AUR-qtile-git"
    , "${repos}/bdf2flf"
    , "${repos}/gitja"
    , "${repos}/mcol.xyz"
    , "${repos}/mini-theme"
    , "${repos}/mkinitcpio-welcome"
    , "${repos}/pelican-microfeed"
    , "${repos}/pelican-minify-fontawesome"
    , "${repos}/pixels"
    , "${repos}/pixels-analysis"
    , "${repos}/pywayland"
    , "${repos}/pywlroots"
    , "${repos}/qtile"
    , "${repos}/qtile-examples"
    , "${repos}/qtools"
    , "${repos}/reach"
    , "${repos}/screenshot-gallery-generator"
    , "${repos}/sudoku-solver"
    , "${repos}/tide"
    , "${repos}/unix.sexy-react"
    , "${repos}/wimp"
    , "${repos}/xanadu"
    , "${repos}/xoop"
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
