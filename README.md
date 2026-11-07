# miraide-tools

note の記事で使った小さな道具をまとめた置き場です。どれも Windows 11 と Python 3.12、Node.js 22 で動かしています。

| フォルダ | 中身 | 使い方 | 関連記事 |
|---|---|---|---|
| `note-check/` | 記事を出す前の文章チェック (`note_lint.py`、`soft_check.py`) | `python note_lint.py 本文.txt --title "タイトル"` | [AI に記事を書かせている自分が通している検査](https://note.com/humble_hornet125) |
| `dance/` | 透過ダンス動画のフレーム数を BPM から検算する (`dance_calc.py`) | `python dance_calc.py 動画.webm` | [ステージで踊り続ける透過ダンス動画の作り方](https://note.com/humble_hornet125/n/nd9fd9e23d72d) |
| `video-demos/hyperframes/` | HTML と GSAP で文字が跳ねるタイトル動画 | `npx hyperframes render -o out.mp4` | |
| `video-demos/remotion/` | React で作るタイトル動画 | `npx remotion render index.jsx Title out.mp4` | |
| `video-demos/manim/` | LaTeX なしで動く棒グラフの説明アニメ | `manim -ql scene.py Compare` | |

## 入れ方

```
git clone https://github.com/smartinformationhosihara-eng/miraide-tools
```

ZIP でも取れます (緑の Code ボタン → Download ZIP)。

- Python の道具は `pip install pillow` だけで動きます。動画系は FFmpeg が必要です。
- HyperFrames と Remotion は `npm i hyperframes remotion @remotion/cli react react-dom gsap` で入ります。
- 送信される利用統計を止めるには、環境変数 `HYPERFRAMES_NO_TELEMETRY=1` と `DO_NOT_TRACK=1` を設定します。

## ライセンス

このリポジトリのコードは MIT です。使っている外部ツールはそれぞれのライセンスに従ってください (Remotion は個人と社員3人以下の会社は無料、GSAP は無料の標準ライセンス、HyperFrames と Manim と three.js はオープンソース)。
