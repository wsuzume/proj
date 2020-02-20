# proj

## Requirements

* pyenv

`proj`コマンドは pyenv による仮想化によって動作しなくなることを
防ぐために`pyenv global`の環境にインストールする必要がある。

## Install
`pyenv global` の環境化で

```
pip install proj
```

を実行する。`proj` をインストールしたあとで

```
proj --reset-profile
```

を設定すると`~/.config/proj`に初期化された設定ファイルを作成する。

## Usage
```
proj --reset-profile
```

によって`~/.config/proj`に設定ファイルを作成したあとで、
`.zshrc`または`.bashrc`に

```
source ~/.config/proj/projrc
```

を追記する。
