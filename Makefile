BIN = wtf
SRC = $(BIN).py
INSTALL = /usr/local/bin/

build:
	pyinstaller $(SRC) --onefile --noconfirm

install: build
	cp -f ./dist/$(BIN) $(INSTALL)$(BIN)

uninstall:
	rm -f $(INSTALL)$(BIN)

all: build
