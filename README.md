# word2vec_exporter

Python scripts that exports words from a [spaCy](https://spacy.io/) dictionary to vectors, based on the word2vec algorithm [Mikolov et al., 2015].

## Getting Started

To run this script, please make sure to clone this repository:

```bash
git clone git@github.com:Cynnexis/word2vec_exporter.git
```

Open a terminal in the cloned directory, and setup the Python environment:

```bash
pip install -r requirements.txt
```

Install the spaCy module you need to export:

```bash
python -m spacy download en_core_web_lg
```

> Note that module that ends with `trf` are not compatible as they do not have vectors. Please consider using modules that ends with `lg`.

To export the English words into vectors as a JSON file, use the following command:

```bash
python -m word2vec_exporter --lang en_core_web_lg
```

### Arguments

* **`--help`, `-h`:** show this help message and exit
* **`--lang LANGUAGE`, `-l LANGUAGE`:** The language. It must be an installed spacy module name. Make sure that the module has vectors associated to its lexemes. See the full list here: https://github.com/explosion/spacy-models/blob/a82b4615a6ae547e99fe9514dc1137b344d8db4e/compatibility.json
* **`--output FILE`, `-o FILE`:** The output file. If it exists, it will be overwritten. If none given, it defaults to the name of the given language, and the extension will depends of the exporter, in the current directory. For example, if you use the spaCy module `en_core_web_lg` with the JSON exporter, the output file will be `./en_core_web_lg.json`.
* **`--exporter {json}`, `-e {json}`:** The name of the exporter. Defaults to `json`.
* **`--key-transform {text,hash,lower,upper}`, `-k {text,hash,lower,upper}`:** The transformation to apply to the key. Defaults to `text`.
* **`--json-indent JSON_INDENT`:** The indentation. It can be a 0 (compact), a positive number, `compact`, `tab`, `tabs`, `space` or `spaces`. `space` and `spaces` will be replaced by 2 whitespaces. Defaults to `compact`.
* **`--verbose`, `-v`:** Verbose mode.
* **`--debug`, `-d`:** Debug mode.
* **`--version`, `-V`:** Print the version of the script and exit.

## :handshake: Contributing

To contribute to this project, please read our [`CONTRIBUTING.md`][contributing] file.

We also have a [code of conduct][code-of-conduct] to help create a welcoming and friendly
environment.

## :writing_hand: Authors

Please see the [`CONTRIBUTORS.md`][contributors] file.

## :page_facing_up: License

This project is under the GNU Affero General Public License v3. Please see the [LICENSE][license] file for more detail (it's a really fascinating story written in there!).

[cynnexis]: https://github.com/Cynnexis
[contributing]: CONTRIBUTING.md
[contributors]: CONTRIBUTORS.md
[code-of-conduct]: CODE_OF_CONDUCT.md
[license]: LICENSE
