import librosa
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd

audio_file = 'output.wav'
data,samplerate = librosa.load(audio_file)
times = np.arange(len(data))/float(samplerate)
sd.play(data, samplerate)
plt.plot(times, data)
plt.xlim(times[0], times[-1])
plt.xlabel('time')
plt.ylabel('amplitude')
plt.show()