# TuneID – Music Recognition System

A Shazam-style music recognition system built using **audio fingerprinting**, **spectral peak hashing**, and a **FastAPI backend**, capable of identifying songs from short audio clips.

---

## 📌 Project Overview

This project implements a simplified version of Shazam’s core idea:
- Songs are converted into **audio fingerprints**
- Fingerprints are stored in a database
- A short query audio clip is matched using **time-aligned hash voting**

The system is robust to noise, compression, and partial audio clips.

---

## ✨ Features

- 🎧 Identify songs from 5–10 second audio clips  
- 🔊 Robust to background noise and distortion  
- ⚡ Fast matching using hash-based indexing  
- 🧠 Audio fingerprinting using spectrogram peak constellations  
- 🌐 REST API built with FastAPI  
- 🖥️ Simple web frontend for uploading audio files  

---

## 🏗️ System Architecture

Frontend (HTML/JS)
↓
FastAPI Backend
↓
Audio Processing (STFT)
↓
Constellation Map (Spectral Peaks)
↓
Fingerprint Hashing
↓
SQLite Database
↓
Time Offset Histogram Matching
↓
Matched Song Result


---

## 🧠 How It Works

1. **Audio Preprocessing**
   - Audio is converted to mono and resampled
   - Short-Time Fourier Transform (STFT) is applied

2. **Constellation Map**
   - Local spectral peaks are extracted from the spectrogram

3. **Fingerprint Generation**
   - Pairs of peaks are hashed using frequency and time difference
   - Each hash represents a fingerprint

4. **Database Storage**
   - Fingerprints are stored in SQLite with time offsets

5. **Matching**
   - Query fingerprints are matched against the database
   - Correct song produces strong alignment at a consistent time offset

---

## ⚙️ Tech Stack

### Backend
- Python
- FastAPI
- Librosa
- NumPy
- SciPy
- SQLite

### Frontend
- HTML
- CSS
- JavaScript (Fetch API)

---
