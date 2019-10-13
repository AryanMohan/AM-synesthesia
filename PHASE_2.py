import numpy as np
import simpleaudio as sa
import wave
import struct
from scipy.io.wavfile import read

def generate_audio_data(notes, sample_rate = 8000, T = 0.25, playback = False):
    t = np.linspace(0, T, T * sample_rate, False)
    for i in range(len(notes)):
        notes[i] = np.sin(notes[i] * t * 2 * np.pi)
    notes = tuple(notes)
        
    # concatenate notes
    audio = np.hstack(notes)
    # normalize to 16-bit range
    audio *= 32767
    # convert to 16-bit data
    audio = audio.astype(np.int16)

    if playback:
        # start playback
        play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

        # wait for playback to finish before exiting
        play_obj.wait_done()

    return audio


#write wav file

def write_wav(audio, fname, nchannels = 1, sampwidth = 2, framerate = 8000, comptype = "NONE", compname = "not compressed"):
    wav_file = wave.open(fname, "w")
    nframes = len(audio)
    
    wav_file.setparams((nchannels, sampwidth, framerate, nframes,
        comptype, compname))
    # write the audio frames to file
    wav_file.writeframes(struct.pack('%sh' % len(audio), *audio))
    wav_file.close()


#read wav file info

def get_sample_rate(fname):
    wave_read = wave.open(fname, 'rb')
    sample_rate = wave_read.getframerate()

    return sample_rate

#convert wav file into notes

def wav_to_notes (fname, framerate=8000, T=0.25):
    t = np.linspace(0, T, T * framerate, False)
    audio_data = read(fname)
    audio = np.array(audio_data[1],dtype=float)
    audio *= 1/32767
    noOfNotes = (len(audio)/framerate)/T
    notes = np.split(audio, noOfNotes)
    Notes = []
    for note in notes:
        n = np.arcsin(note) / (2 * t * np.pi)
        Notes.append((n[1]))
    Notes = [int(round(n)) for n in Notes]

    return Notes
