SRC=$(shell find video_gallery -type f -name '*.py')
TEST_SRC=$(shell find tests -type f -name '*.py')

.PHONY: all clean

all: video_gallery tests

tests: video_gallery $(TEST_SRC) Pipfile Pipfile.lock .coveragerc mypy.ini pylintrc
	mypy tests
	pylint --disable=duplicate-code tests
	pytest --cov=video_gallery --cov-report=term:skip-covered tests -v
	@touch tests

video_gallery: $(SRC) Pipfile Pipfile.lock .coveragerc mypy.ini pylintrc
	mypy video_gallery
	pylint video_gallery
	@touch video_gallery

clean:
	@touch $(SRC) $(TEST_SRC)
	rm -r .mypy_cache .pytest_cache
