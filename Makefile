# New version
VERSION=0.1.1


new_version:
	@git add Makefile
	@git commit -m 'new version $(VERSION)'
	@bumpversion \
	   --new-version  $(VERSION) \
	   major


publish:
	@git push
	@git tag $(VERSION)
	@git push --tags


code_check:
	@flake8 --docstring-convention google

