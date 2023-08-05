# progress-text

Python package for printing progress in text.

## Important Note

**The `every_percent` in this tool can be achieved by setting the parameter `mininterval` to be equal to `num_max_iters * every_percent / 100`. The reason why I created this tool was that I did not read the documents of `tqdm` carefully (I have read it now on 2020-12-18) and I wanted a feature like `every_percent`.**

Now that this tool seems to be not so useful, however, I will not delete this project. Instead, I may keep improving this tool and regard it as a practice.

## Why not [tqdm](https://github.com/tqdm/tqdm)

[tqdm](https://github.com/tqdm/tqdm) is awesome, but I just want to print the progress to a log file by `nohup`.

## Install

```shell
pip3 install --upgrade progress-text
```

Or clone the project, go into the project directory, and execute

```shell
python setup.py install
```

or

```shell
pip install ./
```

Or simply copy the source code.

## Usage

See [`example.py`](./example.py).

## To do

None
