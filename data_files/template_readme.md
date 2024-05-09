# 1️⃣🐝🏎️ 🔥 The One Billion Row Challenge - But Mojo 🔥

After watching a [youtube video reacting](https://youtu.be/cYng524S-MA?si=tJ1I7QKifOiz-Kt8) to another developer's experience re-creating [Gunnar Morling's Java coding challenge](https://www.morling.dev/blog/1brc-results-are-in/) in Golang, where you process one billion rows of simple formated data and output the names of the weather station along with its min, max, and average temperatures in alphabetical order to `STDOUT`. The data will be read from a file and on each row the data is formatted as follows `<Name of Observation point>;<[-99.9, ..., 99.9]>` where there are no more than 10,000 unique locations.

I am also looking to use this as an introductory project to start learning the finer points of Mojo after my few years writing python professionally. Some of the topics of interest are SIMD, concurrency, Mojo's data ownership model, and how mojo will interop with CPython.

## Initial plans and project milestones

1. Tooling to help automate interation and validation
    - [X] Generate test file
    - [X] Timing
      - [X] Python
      - [X] Mojo
    - [ ] Profiling
      - [X] Python
      - [ ] Mojo
    - [ ] Validation
      - [ ] Python
      - [ ] Mojo
    - [ ] Logging performance across commits
2. Initial naive python implementation
3. Iterate, Profile, and Validate. `Below is a list of what I expect will help decrease the total runtime of the script`
    - [ ] Converting to Mojo datastructures
    - [ ] generators
    - [ ] Interactions with the file
    - [ ] Data typing and ownership
    - [ ] Concurrency
    - [ ] Removing un-needed validation
    - [ ] efficiently writing to `STDOUT`

## Performance/Implementation milestones

{attempts_table}

> [example link to commit](https://google.com) `00.0 sec` Relevant goal reached or implementation made

## Project setup instructions

1. `curl https://pyenv.run | bash`
2. Follow instructions supplied in STDOUT to add pyenv to $PATH
3. Follow [this link](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) for instructions to install all build requirements for your machine
4. `pyenv install 3.12.2`
