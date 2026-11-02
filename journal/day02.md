# Day 2 -> Commands, permissions, nginx service, ssh keygen

Date: 2026-11-02

## Target for today
Learn new terminal commands and permissions, start nginx service, generate SSH keys

## What I achieved
- Learned reading and setting permissions with `chmod`
- Installed nginx, opened it in browser through port forwarding and checked logs
- Loged in over SSH with a key pair


## What I learned

### Permissions

- Check permissions: `ls -l`
- Users categories: `u` (owner/user), `g` (group), `o` (others), `a` (all)
- Permission types: `r` (read = 4), `w` (write = 2), `x` (execute = 1)

How to read permissions to a file e.g. `- rwx rw- r--`

- Splits into 4 parts :  `- | rwx | rw- | r--`
-`-` means that it's a file, `d` means that's a directory
- Next three parts: user, group, others
- User has `rwx` permission, so it's read, write and execute.
- Group has `rw-` so it has read and write permission
- Others `r--` have just read
- Numeric value: `rwx = 4+2+1 = 7`, `rw- = 4+2 = 6`, `r--=4`, which gives mode `764`

In practice (shared folder for a group):

- Created second user `sudo adduser testuser` (my own `user` already existed)
- Created group `sudo groupadd labteam`
- Added both users to the group `sudo usermod -aG labteam <user/testuser>` (owner stays root)
- Made a folder `sudo mkdir /srv/shared`
- Changed the folder's group to `labteam`:  `sudo chown :labteam /srv/shared`
- Set permissions `sudo chmod 770 /srv/shared` so the owner and the group can read, write and enter, others have no access
- Both users could make changes and see every file in shared folder, other users that don't belong to the group can't

**What I noticed**

- I couldn't add any file to `/srv` directory, only in `/srv/shared`
- Only root has full permission to `/srv` with `drwxr-xr-x`, everyone else can only read and enter
- In order to access subfolder, permission to execute `x` is needed on every parent directory on the path

### Nginx service

Important commands: 

- `systemctl start|stop|restart|status nginx` controls the service
- `journalctl -u nginx -f` shows the service logs, `-u` specific service (nginx), `f` follows the log live
- `systemctl enable|disable nginx` enabling/disabling autostart

In practice:

- Installed with `sudo apt install nginx`
- Added port forwarding `host 127.0.01:8080 -> guest 80`
- Checked if service is working `systemctl status nginx`
- Opened `http://127.0.0.1:8080` in the browser
- When the service is stopped, the page doesn't load

### SSH keys authentication

- `ssh-keygen -t ed25519` generates pair of keys, private and public (.pub)
- Public key is installed on the server in `~/.ssh/authorized_keys`
- Private key stays on my computer and is never shared

**What I noticed**
- Adding passphrase to a file with private key increases safety by encrypting file locally, if someone steals the file they still need the passphrase in order to log in to the server
- Brute force guessing of the login is almost impossible
- The same public key can be installed in many servers so one private key can log me into all of them 
- Passphrase is not a password, it protects the private key locally

**Important commands**
- `id` shows information about logged user, shows user identification number (UID) and group identificator (GID)
- `ls -l` lists files in long format and shows permissions, owner, size and modification date
- `ls -a` lists all files (also hidden)
- `ls -la` combination of both commands above, displays all files and shows detailed information about each one
- `chmod` changes permissions of a file, what each user, group or guest can do with a file or directory
- `chown` changes who owns the file or directory, either user or a group
- `usermod -G <groupname> <username>` replaces all of the user's groups, if you change `-G` to `-aG` then it ADDS a group to existing ones
- `su <user>` switches user but keeps current environment, `su - <user>` starts a full login shell in that user's home
- `ps aux` shows all working processes

## Problems and solutions

### Accidentally generated keys on the server instead of my computer
- **Problem** ran `ssh-keygen` and `ssh-copy-id` inside the VM, so both keys ended up on the server
- **Diagnosis** the prompt was `user@lab-ubuntu`, not `PS C:\...`, and logging in from the host still asked for the account password
- **Solution** removed the keys and the `authorized_keys` entry then generated the pair on my computer locally
- **Conclusion** always check the prompt before running a command

