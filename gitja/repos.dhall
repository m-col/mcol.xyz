-- The single source of truth for which repos appear on /code. Imported by
-- ./config.dhall, and parsed directly by .github/workflows/deploy.yaml to
-- know which repos to clone - so this is the only place to edit when
-- adding, removing or renaming a repo.

let repos = ".."

in  [ "${repos}/bdf2flf"
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
