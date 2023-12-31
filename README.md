
<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<!-- Replace with 1-sentence description about what this tool is or does.-->

<h3 align="center">WORD-ALIGNER</h3>

The primary goal of this project is to create a robust and comprehensive bi-term dictionary for translating between Tibetan and English. And we are using Mgiza++ application to achieve that, but to use Mgiza++, we will parallel corpus of the two language (sentence by sentence) and each sentence also be word segmented.

## Project owner(s)

<!-- Link to the repo owners' github profiles -->

- [@ngawangtrinley](https://github.com/ngawangtrinley)
- [@drupchen](https://github.com/drupchen)
- [@tenzin3](https://github.com/tenzin3)


## Installation

mgiza++ installation steps:

- `cd mgiza`
- `sudo apt-get install -y cmake libboost-all-dev`
- `git clone https://github.com/moses-smt/mgiza.git`
- `cd mgiza/mgizapp`
- `cmake . && make && make install`
- `add the path to your system PATH`

## Integrations

<!-- Add any intregrations here or delete `- []()` and write None-->

None

## Docs

<!-- Update the link to the docs -->

Read the docs [here](https://wiki.openpecha.org/#/dev/coding-guidelines).

## Note

TODO:

- test botok / dictionary
- swap direction and find Buddhist English n-grams
- improve file cleanup
- run on all Monlam AI data

```WARNING: The following sentence pair has source/target sentence length ratio more than
the maximum allowed limit for a source word fertility
 source length = 5 target length = 57 ratio 11.4 ferility limit : 9
Shortening sentence
Sent No: 17167 , No. Occurrences: 1
0 127 149 10 6394 1064
251 174 143 1352 555 36 343 44 483 3191 89 26 322 360 170 143 583 254 839 619 143 583 564 31 108 1635 3218 82 2394 254 143 11 1643 100 88 1852 6272 251 174 555 26 89 374 317 289 115 201 202 26 3323 820 746 44 352 14 153 708
WARNING: The following sentence pair has source/target sentence length ratio more than
the maximum allowed limit for a source word fertility
 source length = 6 target length = 55 ratio 9.16667 ferility limit : 9```
