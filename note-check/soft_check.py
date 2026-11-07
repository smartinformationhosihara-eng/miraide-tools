# note 本文のやわらか文体チェック。note_lint の後にかく。
# python tools/soft_check.py 本文.txt
# 合格基準(2026-11-06 実測較正: 公開4本の body_pulled vs body_soft):
#   だ・である文末 = 0 / です・ます率 50%以上 / 80字超の文は全体の15%未満
import re, sys
from pathlib import Path

raw = Path(sys.argv[1]).read_text(encoding='utf-8')
parts = re.split(r'^```.*?^```\s*$', raw, flags=re.M | re.S)
text = '\n'.join(parts)
lines = [l.strip() for l in text.split('\n') if l.strip()
         and not l.startswith(('![', '#', '|', '- ', '> '))]
sents = [s.strip() for s in re.split(r'(?<=[。！？])', ' '.join(lines)) if s.strip()]

hard = [s for s in sents if re.search(r'(?:だ|である|だった|であった)[。」]?$', s)]
soft_end = [s for s in sents if re.search(r'(?:です|ます|でした|ました|ですか|ませんか|ですね|でしょう)(?:[。！」])?$', s)]
long80 = [s for s in sents if len(s) > 80]
paras = [p for p in text.split('\n\n') if p.strip() and not p.strip().startswith(('![', '#', '|', '- ', '>', '`'))]
paras4 = [p for p in paras if len(re.findall(r'[。！？]', p)) > 3]

print(f'文数 {len(sents)}')
print(f'だ・である文末 {len(hard)}  (基準 0)')
for s in hard[:5]:
    print('  硬:', s[:60])
ratio = 100 * len(soft_end) / max(1, len(sents))
print(f'です・ます率 {ratio:.0f}%  (基準 50%以上)')
r80 = 100 * len(long80) / max(1, len(sents))
print(f'80字超の文 {len(long80)} 本 {r80:.0f}%  (基準 15%未満)')
print(f'4文以上の段落 {len(paras4)}  (目安 2まで。参考)')
ok = len(hard) == 0 and ratio >= 50 and r80 < 15
print('SOFT OK' if ok else 'SOFT NG')
