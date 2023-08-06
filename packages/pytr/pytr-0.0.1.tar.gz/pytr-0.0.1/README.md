# pytr: Use TradeRepublic in terminal

This is a library for the private API of the Trade Republic online brokerage. I am not affiliated with Trade Republic Bank GmbH.

## Installation

Install with `pip install pytr`

Or you can clone the repo like so:

```sh
git clone https://github.com/marzzzello/pytr.git
cd pytr
pip install .
```

## Usage

```
$ pytr help
usage: pytr [-h] [-s {bash,zsh}] [-v {warning,info,debug}]
             {help,login,portfolio,dl_docs,set_price_alarms} ...

positional arguments:
  {help,login,portfolio,dl_docs,set_price_alarms}
                        Desired action to perform
    help                Print this help message
    login               Check if credentials file exists. If not create it and
                        ask for input. Try to login. Ask for device reset if
                        needed
    portfolio           Show current portfolio
    dl_docs             Download all pdf documents from the timeline and sort
                        them into folders
    set_price_alarms    Set price alarms based on diff from current price

optional arguments:
  -h, --help            show this help message and exit
  -s {bash,zsh}, --print-completion {bash,zsh}
                        print shell completion script
  -v {warning,info,debug}, --verbosity {warning,info,debug}
                        Set verbosity level
```

## Authentication

First you need to perform a device reset - a private key will be generated that pins your "device". The private key is saved to your keyfile. This procedure will log you out from your mobile device.

```sh
$ pytr login
$ # or
$ pytr login --phone_no +49123456789 --pin 1234
```

If no arguments are supplied pytr will look for them in the file `~/.pytr/credentials` (the first line must contain the phone number, the second line the pin). If the file doesn't exist pytr will ask for for the phone number and pin.
