# Startup script
A simple script to start multiple bots in separate tmux sessions on a linux server.

## Requirements
- Every bot has its own directory with an executable file
- The bot prints a message containing the word `online` if it starts successfully
- All bot directories are placed in a `main` directory or in a subdirectory of the main directory

### Possible
  - `/main/bot`
  - `/main/subdir1/bot`
### Not possible
  - `/main/subdir1/subdir2/bot`
  - `/main/bot1/bot2`

## How to use the script
1. Modify the `config.py` file
2. Run `startup.py` anywhere on the server