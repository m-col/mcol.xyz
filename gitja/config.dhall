-- gitja config for generating the /code section of mcol.xyz.
--
-- This expects to be run from the mcol.xyz repo root, with the repos
-- listed in ./repos.dhall checked out as sibling directories of that
-- checkout (see .github/workflows/deploy.yaml), mirroring gitja's own CI
-- setup. Paths here are resolved relative to the working directory gitja
-- is invoked from, not relative to this file.

let folders = ./repos.dhall

let config =
    { repos = folders
    , scan = False
    , template = "./gitja/template"
    , output = "./gitja/output"
    , host = "https://mcol.xyz"
    }

in config
