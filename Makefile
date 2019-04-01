# Makefile

# 此定义只支持GNU make
currentPath := $(shell pwd)/$(lastword $(MAKEFILE_LIST))
currentDir := $(shell dirname $(currentPath))

python3 = `which python3`
pip3 = `which pip3`
# Makefile不支持awk
# pipInstallPath := $(shell $(pip3) show pip | grep 'Location' | awk '{print $2}')
pipInstallPath := $(shell $(pip3) show pip | grep 'Location' | cut -d ' ' -f2)

# make all
# 	function: packageing app
#	command:  python setup.py sdist
#	usage: pip install dist/svnlab-1.0.tar.gz
all:
	$(python3) setup.py sdist

# make install
#	function: package and install
install:
	$(python3) setup.py sdist
	$(pip3) install dist/svnlab-1.0.tar.gz

# make uninstall
#	function: delete useless file and uninstall app
uselessDirs = dist __pycache__ migrations *.egg-info
uninstall:
	echo $(uselessDirs)
	for uselessDir in `echo $(uselessDirs)`; do \
		find $(currentDir) -type d -name $$uselessDir | xargs -i rm -rf {}; \
	done
	$(pip3) uninstall svnlab -y
	rm -rf $(pipInstallPath)/svnlab

# make clean
#	function: delete useless file
clean:
	echo $(uselessDirs)
	for uselessDir in `echo $(uselessDirs)`; do \
		find $(currentDir) -type d -name $$uselessDir | xargs -i rm -rf {}; \
	done
