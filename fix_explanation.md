# Gemini TTS Generation - Fixes Applied

## Problems in Original Code

### 1. **Incorrect speech_config format**
```python
# ❌ WRONG - speech_config as list
generation_config={
    "speech_config": [
        {"voice": "Kore"}
    ]
}

# ✅ CORRECT - speech_config as dict
generation_config={
    "speech_config": {"voice": "Kore"}
}
```

### 2. **Writing compressed audio to WAV with raw PCM parameters**
```python
# ❌ WRONG - Creates broken WAV files
# Gemini returns compressed audio (MP3), not raw PCM
wave_file('out.wav', base64.b64decode(interaction.output_audio.data))
# Tries to decode base64 and write as WAV with hardcoded PCM params
# Result: Corrupted file that won't play

# ✅ CORRECT approach:
# Option A: Save as MP3 (Gemini's native format)
with open('out.mp3', 'wb') as f:
    f.write(audio_bytes)

# Option B: Convert to WAV using ffmpeg
subprocess.run([
    "ffmpeg", "-i", "temp.mp3", "-acodec", "pcm_s16le", 
    "-ar", "24000", "out.wav", "-y"
], capture_output=True, check=True)
```

### 3. **No validation of audio data integrity**
```python
# ❌ WRONG - No checks
with open('out.wav', 'wb') as f:
    f.write(audio_bytes)

# ✅ CORRECT - Validate before saving
if not audio_bytes or len(audio_bytes) < 100:
    raise ValueError(f"Invalid audio data, size: {len(audio_bytes)}")
with open('out.mp3', 'wb') as f:
    f.write(audio_bytes)
```

### 4. **Incorrect audio data extraction**
```python
# ❌ PROBLEMATIC - May fail with different response formats
base64.b64decode(interaction.output_audio.data)

# ✅ ROBUST - Handles multiple formats
if isinstance(audio_data, bytes):
    audio_bytes = audio_data
elif hasattr(audio_data, 'data'):
    data = audio_data.data
    if isinstance(data, bytes):
        audio_bytes = data
    elif isinstance(data, str):
        audio_bytes = base64.b64decode(data)
else:
    audio_bytes = bytes(audio_data)
```

## Key Takeaways

1. **Gemini TTS returns compressed audio (MP3)**, not raw PCM
2. **Save directly to MP3** (simplest approach)
3. **Only convert to WAV if needed** (requires ffmpeg)
4. **Never write compressed audio to WAV** with hardcoded PCM parameters
5. **Validate data size** before writing to files

## Usage

```bash
# Save as MP3 (default)
python generate_tts_gemini_fixed.py 01-rabbit-tale

# Convert to WAV (requires ffmpeg)
python generate_tts_gemini_fixed.py 01-rabbit-tale wav
```
