.PHONY: build link test watch clean publish

build:
	python3 -m adapters.build

link: build
	bash scripts/link.sh

test:
	python3 -m pytest tests/ -v

watch:
	bash scripts/dev.sh

clean:
	rm -rf dist/

publish: build
	rm -rf published/.claude/skills
	mkdir -p published/.claude/skills
	cp -r dist/.claude/skills/. published/.claude/skills/
