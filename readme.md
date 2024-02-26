# 1️⃣🐝🏎️ 🔥 The One Billion Row Challenge - But Mojo 🔥

After watching a [youtube video reacting](https://youtu.be/cYng524S-MA?si=tJ1I7QKifOiz-Kt8) to another developer's experience re-creating [Gunnar Morling's Java coding challenge](https://www.morling.dev/blog/1brc-results-are-in/) in Golang, where you process one billion rows of simple formated data and output the names of the weather station along with its min, max, and average temperatures in alphabetical order to `STDOUT`. The data will be read from a file and on each row the data is formatted as follows `<Name of Observation point>;<[-99.9, ..., 99.9]>` where there are no more than 10,000 unique locations.

I am also looking to use this as an introductory project to start learning the finer points of Mojo after my few years writing python professionally. Some of the topics of interest are SIMD, concurrency, and Mojo's data ownership model among others.

## Initial plans and project milestones

1. Tooling to help automate interation and validation

    - [ ] Generate test file
    - [ ] Timing
    - [ ] Profiling
    - [ ] Validation
    - [ ] Logging performance across commits

2. Initial naive python implementation
3. Iterate, Profile, and Validate. `Below is a list of what I expect will help decreate the total runtime of the script`

    - [ ] Converting to Mojo datastructures
    - [ ] Interactions with the file
    - [ ] Data typing and ownership
    - [ ] Concurrency
    - [ ] Removing un-needed validation
    - [ ] efficiently writing to `STDOUT`

## Performance/Implementation milestones

> [example link to commit](https://google.com) `00.0 sec` Relevant goal reached or implementation made
