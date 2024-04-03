import tkinter as tk
from tkinter import ttk
import pyaudio
import wave
import threading
import creds  # Ensure this contains Duration and SAMPLERATE variables

class RecorderApp:
    def __init__(self, master):
        self.should_stop = threading.Event()

        self.master = master
        master.title("Segmented Audio Recorder")

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False

        # Dropdown for mic selection with placeholder
        self.mic_var = tk.StringVar(master)
        self.populate_input_devices()
        self.mic_menu = ttk.Combobox(master, textvariable=self.mic_var, values=['Please select microphone'] + list(self.input_devices.keys()))
        self.mic_menu.current(0)  # Set the current item to the placeholder
        self.mic_menu.pack()

        # Record/Stop buttons
        self.record_button = tk.Button(master, text="Start Recording", command=self.toggle_recording)
        self.record_button.pack()

        self.stop_button = tk.Button(master, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack()

    def populate_input_devices(self):
        self.input_devices = {}
        info = self.audio.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        for i in range(num_devices):
            if self.audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
                self.input_devices[self.audio.get_device_info_by_host_api_device_index(0, i).get('name')] = i

    def toggle_recording(self):
        if self.mic_var.get() == 'Please select microphone':
            print("Please select a microphone from the dropdown.")
            return
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        self.is_recording = True
        self.record_button.config(text="Recording...", state=tk.DISABLED)
        threading.Thread(target=self.record_loop).start()

    def stop_recording(self):
        self.is_recording = False
        self.should_stop.set()  # Signal threads to stop
        self.record_button.config(text="Start Recording", state=tk.NORMAL)

    def record_loop(self):
        file_counter = 1
        while not self.should_stop.is_set():
            filename = f'audio{file_counter}.wav'
            self.record_audio(creds.Duration, creds.SAMPLERATE, filename)
            if self.should_stop.is_set():
                break
            file_counter = file_counter + 1 if file_counter < 6 else 1

    def record_audio(self, duration, samplerate, filename):
        print(f"Recording {filename}...")
        device_index = self.input_devices.get(self.mic_var.get())
        stream = self.audio.open(format=pyaudio.paInt16,
                                 channels=1,
                                 rate=samplerate,
                                 input=True,
                                 frames_per_buffer=1024,
                                 input_device_index=device_index)
        frames = []
        for _ in range(0, int(samplerate / 1024 * duration)):
            data = stream.read(1024)
            frames.append(data)
        stream.stop_stream()
        stream.close()

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(samplerate)
            wf.writeframes(b''.join(frames))
        print(f"Recording finished for {filename}")

    def on_close(self):
        self.should_stop.set()  # Ensure threads stop
        self.stop_recording()  # Stop recording if it's happening
        self.audio.terminate()  # Clean up PyAudio
        self.master.after(100, self.master.destroy)  # Give threads time to exit

def main():
    root = tk.Tk()
    app = RecorderApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()
