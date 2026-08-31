basedir := justfile_directory()
inputdir := basedir / "content"
outputdir := basedir / "output"
conffile := basedir / "pelicanconf.py"
publishconf := basedir / "publishconf.py"

ssh_host := "mcol.xyz"
ssh_port := "22"
ssh_user := "mcol"
ssh_target_dir := "/home/mcol/mcol.xyz"

ftp_user := "mcol@mcol.xyz"
ftp_host := "mcol.xyz"

# List available recipes
default:
    @just --list

# (Re)generate the web site. Pass extra pelican flags after `--`, e.g. `just html -- -D`
html *flags: clean
    uv run pelican {{ inputdir }} -o {{ outputdir }} -s {{ conffile }} {{ flags }}

# Remove the generated files
clean:
    rm -rf {{ outputdir }}

# Regenerate files upon modification
regenerate *flags:
    uv run pelican -r {{ inputdir }} -o {{ outputdir }} -s {{ conffile }} {{ flags }}

# Serve site at http://localhost:8000
serve port="8000" *flags:
    uv run pelican -l {{ inputdir }} -o {{ outputdir }} -s {{ conffile }} -p {{ port }} {{ flags }}

# Serve (as root) to 0.0.0.0:80
serve-global server="0.0.0.0" port="80" *flags:
    uv run pelican -l {{ inputdir }} -o {{ outputdir }} -s {{ conffile }} -p {{ port }} -b {{ server }} {{ flags }}

# Serve and regenerate together
devserver port="8000" *flags:
    uv run pelican -lr {{ inputdir }} -o {{ outputdir }} -s {{ conffile }} -p {{ port }} {{ flags }}

# Generate using production settings
publish *flags: clean
    uv run pelican {{ inputdir }} -o {{ outputdir }} -s {{ publishconf }} --fatal errors {{ flags }}

# Upload the web site via SSH
ssh-upload: publish
    scp -P {{ ssh_port }} -r {{ outputdir }}/* {{ ssh_user }}@{{ ssh_host }}:{{ ssh_target_dir }}

# Upload the web site via rsync+ssh
rsync-upload: publish
    rsync -e "ssh -p {{ ssh_port }}" -P -rczz --cvs-exclude --delete --chmod=D755,F644 --copy-dirlinks \
        {{ outputdir }}/ {{ ssh_user }}@{{ ssh_host }}:{{ ssh_target_dir }}

# Upload the web site via FTP
ftp-upload: publish
    ncftpput -vRz -u {{ ftp_user }} {{ ftp_host }} / {{ outputdir }}/*
