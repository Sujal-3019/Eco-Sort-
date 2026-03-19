# 🌱 Eco Sort – AI Powered Waste Classification & Recycling Assistant

> Turning waste into opportunity using Artificial Intelligence ♻️

---

## 🚀 Overview

**Eco Sort** is an AI-based web application that helps users identify different types of waste and promotes sustainable living by suggesting smart reuse ideas.

Users can:
- 📷 Upload an image of waste  
- 🎥 Use live webcam detection  

The system:
- 🔍 Classifies waste (Plastic, Paper, Metal, etc.)
- 💡 Suggests reuse ideas
- ▶️ Provides a YouTube link to learn how to reuse it  

---

## 🧠 How It Works

1. User uploads image or captures using webcam  
2. Image is processed using **PIL & NumPy**  
3. A trained **TensorFlow model (Teachable Machine)** predicts waste type  
4. Based on prediction:
   - Reuse ideas are displayed  
   - A YouTube search link is generated  

---

## ✨ Features

- 📸 Image Upload & 🎥 Webcam Detection  
- 🤖 AI-based Waste Classification  
- ♻️ Smart Reuse Suggestions  
- 🎬 YouTube Learning Integration  
- ⚡ Fast UI using Streamlit  

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit  
- **Machine Learning**: TensorFlow  
- **Image Processing**: PIL, NumPy  
- **Other**: urllib  

---

## 📂 Project Structure
Eco-Sort/
  │
  ├── app.py
  ├── converted_tflite/
    ├── model_unquant
    └── labels.txt


---

## ⚙️ Installation & Setup

### 1. Clone the repository
```git clone https://github.com/your-username/eco-sort.git```
```cd eco-sort```

### 2. Install dependencies
```pip install -r requirements.txt```

### 3. Run the app
```streamlit run app.py```

---

## 🌍 Impact

- Encourages **eco-friendly habits**
- Promotes **waste reuse and recycling**
- Helps users make **sustainable decisions**

---

## 🔮 Future Improvements

- 🔥 Improve model accuracy  
- 📊 Add waste tracking dashboard  
- 📱 Convert to mobile app  
- 🌐 Multi-language support  
- 🤖 AI-generated reuse ideas  

---

## 🙋‍♂️ Author

**Sujal Shukla**  
- B.Tech Student | AI Enthusiast  
- Passionate about solving real-world problems  

---

## ⭐ Support

If you like this project:
- ⭐ Star the repository  
- 🍴 Fork it  
- 📢 Share it  
