from PHASE_1 import *
from INTERMEDIARY_ENCRYPTION_PHASE import *
from PHASE_2 import *

def encrypt(file):
    #Phase 1
    im = Image.open(file)
    C, p, N, im2 = ImageToRGB (im)
    print("Image successfully converted to RGB Values.")

    #Phase 2
    fr = 1000
    audio = generate_audio_data(C, T=0.01, sample_rate = fr)
    fname = str(input("What do you want to name the encrypted file: "))
    if fname[-4:-1] != ".wav":
        fname = fname + ".wav"
    write_wav(audio, fname, framerate = fr)
    print("File %s successfully created." % fname)
    
def decrypt(file):
    #Phase 2
    framerate = get_sample_rate(file)
    Encrypted =wav_to_notes(file, framerate, T=0.01)
    Encrypted = [round(e) for e in Encrypted]
    print("Frequencies extracted from WAV file.")
    


    #Phase 1
    p = int(math.log((len(Encrypted)/3), 4))
    PaddingColour2, im2 = RGBToImage (Encrypted, p, 2)
    RemovePadding(im2, PaddingColour2)
    
    
file = str(input("Enter file name to be encrypted or decrypted: "))
file = file.lower()
if file[-2] == "p" or file[-2] == "e":
    encrypt(file)
elif file [-2]=="a":
    decrypt(file)
    
    
