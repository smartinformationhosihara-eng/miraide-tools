# 152BPM のダンスに 1.3 倍再生をかけた 1 周期を、フレームで測る
# 用途: 曲BPMとダンス周期と再生速度が既知の時、webm の生成フレーム数が想定通りか検算する
import subprocess, sys, json

def frame_count(video):
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-select_streams', 'v:0',
         '-count_packets', '-show_entries', 'stream=nb_read_packets',
         '-of', 'csv=p=0', video],
        capture_output=True, text=True, check=True).stdout.strip()
    return int(out)

def duration(video):
    return float(subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'csv=p=0', video],
        capture_output=True, text=True, check=True).stdout.strip())

def cycle_frames(bpm, cycles_per_music_sec, speed):
    """曲BPM、1秒あたりの踊り周期、再生倍速 -> 踊り1周期の実フレーム数(60fps想定)"""
    beat = 60.0 / bpm
    music_sec_per_cycle = cycles_per_music_sec * beat
    return 60.0 * music_sec_per_cycle / speed

if __name__ == '__main__':
    # 実測例(stage_dance_v5c): 曲152BPM、踊り周期1.04秒(音楽時間)、再生1.3倍、実測362f/14.084s
    v = sys.argv[1]
    f, d = frame_count(v), duration(v)
    print(json.dumps({
        'video': v, 'frames': f, 'duration_s': round(d, 3),
        'fps_effective': round(f / d, 2),
    }, ensure_ascii=False))
