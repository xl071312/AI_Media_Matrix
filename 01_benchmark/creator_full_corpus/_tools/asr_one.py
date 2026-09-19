#!/usr/bin/env python3
"""Transcribe one local audio/video file with faster-whisper. Usage: asr_one.py in_path out_txt"""
import sys
from pathlib import Path

def main():
    if len(sys.argv) < 3:
        print('usage: asr_one.py <media> <out.txt>', file=sys.stderr); sys.exit(2)
    inp, outp = Path(sys.argv[1]), Path(sys.argv[2])
    from faster_whisper import WhisperModel
    model = WhisperModel('small', device='cpu', compute_type='int8')
    segments, info = model.transcribe(str(inp), language='zh', vad_filter=True)
    lines = []
    for seg in segments:
        lines.append(seg.text.strip())
    text = '\n'.join([x for x in lines if x])
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(text + ('\n' if text else ''), encoding='utf-8')
    print(f'OK lang={info.language} duration={info.duration:.1f}s chars={len(text)} -> {outp}')

if __name__ == '__main__':
    main()
