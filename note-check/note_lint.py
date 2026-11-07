# note 記事の公開前チェック。基準は skills/note-growth。最後に RESULT OK が出なければ公開しない
# python tools/note_lint.py 本文.txt --title "タイトル" [--cover 見出し画像]
import argparse, re, sys
from pathlib import Path
from PIL import Image

BAD = ['と言えるでしょう', '重要です', 'いかがでしたか', 'さまざまな', 'ことが可能です', '本記事では', 'まとめると', '革新的', '〜について解説', '徹底解説']
LEAK = re.compile(r'\b(TODO|qwen3\.8|監督|task_\w+|progress\.md)\b|C:[\\/]Users')
a = argparse.ArgumentParser()
a.add_argument('body'); a.add_argument('--title', required=True); a.add_argument('--cover')
a = a.parse_args()
raw = Path(a.body).read_text(encoding='utf-8')
fails, warns = [], []
# コードとファイルパスの画像行は文章の検査から外す
parts = re.split(r'^```.*?^```\s*$', raw, flags=re.M | re.S)
text = '\n'.join(parts)
lines = [l.strip() for l in text.split('\n')]
prose = [l for l in lines if l and not l.startswith(('![', '#', '|', '- ', '> '))]
chars = sum(len(l) for l in prose)

if not 15 <= len(a.title) <= 60: fails.append(f'タイトル {len(a.title)} 字(15〜60)')
heads = [l for l in lines if l.startswith('## ') or l.startswith('### ')]
need = max(3, chars // 400)
if len(heads) < need: fails.append(f'見出し {len(heads)} 本(本文 {chars} 字なら {need} 本以上)')
if re.search(r'^# ', text, flags=re.M): fails.append('# の見出しが残っている')
# 見出しの間が長すぎないか
gap = run = 0
for l in lines:
    if l.startswith('#'): run = 0
    elif l and not l.startswith('!['): run += len(l); gap = max(gap, run)
if gap > 900: fails.append(f'見出しのない区間 {gap} 字(900まで)')
long_s = [s for l in prose for s in re.split(r'(?<=[。!?！？])', l) if len(s) > 80]
if long_s: warns.append(f'80字を超える文 {len(long_s)} 個: {long_s[0][:30]}…')
long_p = [l for l in prose if len(l) > 220]
if long_p: fails.append(f'220字を超える段落 {len(long_p)} 個')
ends = re.findall(r'(です|ます|でした|ました)。', text)
seq = best = 0
for s in re.split(r'(?<=。)', ' '.join(prose)):
    if re.search(r'(です|ます|でした|ました)。$', s.strip()): seq += 1; best = max(best, seq)
    elif s.strip(): seq = 0
k = len(re.findall(r'(です|ます|でした|ました|ません)[。！]', text)); d = len(re.findall(r'(?<!でし)(?<!まし)(だ|である|た|ない|いる|する)[。！]', text))
if k + d and .15 < k / (k + d) < .85: fails.append(f'文体が混ざっている(です体 {k}、だ体 {d})。どちらかに統一する')
# 2026-11-06 ユーザー指示: やわらかい です・ます で書く。同じ文末の語(例: です。)が4回続くのだけ止める
same = re.findall(r'(です|ます|でした|ました|ません)。', text)
run = mx = 0; prev = None
for e in same:
    run = run + 1 if e == prev else 1; prev = e; mx = max(mx, run)
if mx >= 4: fails.append(f'同じ文末「{prev}。」が {mx} 回続く(3まで)。言い方を変える')
for w in BAD:
    if w in text: fails.append(f'機械的な言い回し: {w}')
leak = [l[:50] for l in lines if not l.startswith('![') and LEAK.search(l)]
if leak: fails.append(f'内部の文字が残っている: {leak[0]}')
if not re.search(r'^!\[', '\n'.join(lines[:12]), flags=re.M): fails.append('冒頭に完成品の画像がない')
# 本文の画像: 余白ばかりを検出
for cap, p in re.findall(r'^!\[(.*?)\]\((.+?)\)', raw, flags=re.M):
    if not Path(p).exists(): fails.append(f'画像がない: {p[-40:]}'); continue
    im = Image.open(p).convert('RGB'); s = im.resize((160, int(160 * im.height / im.width)))
    px = list(s.getdata()); bg = sum(1 for c in px if min(c) > 238) / len(px)
    if bg > .82: fails.append(f'白い余白が {bg:.0%}: {Path(p).name}({cap[:16]})')
if a.cover:
    c = Image.open(a.cover)
    if abs(c.width / c.height - 1280 / 670) > .03: fails.append(f'見出し画像の比率が違う {c.width}x{c.height}(1280x670)')
    if c.width < 1280: fails.append(f'見出し画像の幅が足りない {c.width}')
    thumb = Path(a.cover).with_suffix('.thumb200.png'); c.convert('RGB').resize((200, 105)).save(thumb)
    warns.append(f'縮小画像を目で確かめる: {thumb}')
else:
    warns.append('見出し画像を指定していない')
for w in warns: print('WARN', w)
for f in fails: print('NG', f)
print(f'本文 {chars} 字 見出し {len(heads)} 本')
print('RESULT OK' if not fails else f'RESULT NG {len(fails)}')
sys.exit(1 if fails else 0)
