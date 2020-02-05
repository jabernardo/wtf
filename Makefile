BIN = wtf.py

build:
	pyinstaller $(BIN) --onefile --noconfirm

all: build
