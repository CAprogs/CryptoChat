# CryptoChat 💬🔐

<div align="center">

![GitHub Repo stars](https://img.shields.io/github/stars/CAprogs/CryptoChat?color=yellow) 
![GitHub](https://img.shields.io/github/license/CAprogs/CryptoChat?color=blue)
![total downloads](https://img.shields.io/github/downloads/CAprogs/CryptoChat/total?color=purple)
![latest release](https://img.shields.io/github/v/release/CAprogs/CryptoChat?label=latest&color=darkgreen)
  
</div>

Cryptochat is a project that allows two users to communicate securely via the command line interface (CLI).

- The server is implemented in Python with the socket module.
- A network sniffer is implemented to capture the packets sent and received and ensure that the data is properly encrypted.
- An authentication is required before accessing the server.

## About 🥢

- Cryptochat uses the [RSA](https://en.wikipedia.org/wiki/RSA_(cryptosystem)) algorithm to encrypt messages.
- All datas are stored into a [SQLite](https://www.sqlite.org/index.html) database.
- All roles run on the same machine by default.

## Demo 📸

https://github.com/CAprogs/CryptoChat/assets/104645407/b9ee4a11-84b7-4f35-906c-11e2a41257d3

## Installation 📦

| Role              | Link                                                                                       | Description                                                     | Max clients |
|-------------------|--------------------------------------------------------------------------------------------|-----------------------------------------------------------------|-------------|
| Server (P2P)      | [⇩](https://github.com/CAprogs/CryptoChat/releases/download/v0.0.1/CryptoChat_server.zip)  | **Host**, **send**, **receive** and **save** messages.          |      1      |
| Client            | [⇩](https://github.com/CAprogs/CryptoChat/releases/download/v0.0.1/CryptoChat_client.zip)  | **Send** and **receive** messages.                              |      /      |
| Sniffer           | [⇩](https://github.com/CAprogs/CryptoChat/releases/download/v0.0.1/CryptoChat_sniffer.zip) | **Analyze** a specified  number of TCP packets containing datas.|      /      |
| All roles         | [⇩](https://github.com/CAprogs/CryptoChat/releases/download/v0.0.1/CryptoChat.zip)         | Contains the **entire project** with all roles.                 |      /      |

## Run the project 🚀

Consider installing python 3.12 or higher.

- Create a virtual environment and install the requirements.
```
pip install -r requirements.txt
```

### Server

```
python3 srv.py
```

### Client

```
python3 clt.py
```

### Sniffer

```
python3 snf.py
```

## As simple as that 🤯

The figure below represents how CryptoChat works.

## Author ✍️

- [@CAprogs](https://github.com/CAprogs)

## License 📝

CryptoChat 💬🔐 is under [```MIT License```](LICENSE)

## Donations & Support ❤️

If you **like this project**, feel free to **give it a ⭐**!

<a href="https://www.buymeacoffee.com/CAprogs"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a pizza&emoji=🍕&slug=CAprogs&button_colour=FFDD00&font_colour=000000&font_family=Arial&outline_colour=000000&coffee_colour=ffffff" /></a>
