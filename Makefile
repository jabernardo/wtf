BIN = wtf
SRC = $(BIN).py
INSTALL = ~/.local/bin/

install_dep:
	pip install -r ./requirements.txt

build: install_dep
	pyinstaller $(SRC) --onefile --noconfirm  --hidden-import pkg_resources.py2_warn

install: build
	cp -f ./dist/$(BIN) $(INSTALL)$(BIN)

uninstall:
	rm -f $(INSTALL)$(BIN)

all: build
