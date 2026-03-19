import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import urllib.parse

# Load classes and model (update paths as appropriate)
@st.cache_resource(show_spinner=False)
def load_model():
    interpreter = tf.lite.Interpreter(model_path="converted_tflite/model_unquant.tflite")
    interpreter.allocate_tensors()
    with open("converted_tflite/labels.txt", 'r') as f:
        classes = [line.strip() for line in f if line.strip()]
    return interpreter, classes


interpreter, CLASS_NAMES = load_model()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


# Waste info mappings with multiple reuse suggestions
waste_info = {
    "Pen": {
        "nature": "dry non-recyclable",
        "dustbin_color": "Red",
        "reuse_tip": [
            "Refill pens instead of discarding.",
            "Use empty pens as plant markers in your garden.",
            "Donate unused pens to schools or NGOs."
        ]
    },
    "Plastic": {
        "nature": "dry recyclable",
        "dustbin_color": "Blue",
        "reuse_tip": [
            "Use plastic bottles as planters or bird feeders.",
            "Create storage containers from large plastic jars.",
            "Make DIY crafts or organizers from plastic waste."
        ]
    },
    "Cardboard": {
    "nature": "dry recyclable",
    "dustbin_color": "Blue",
    "reuse_tip": [
        "Create organizers or storage boxes from sturdy cardboard pieces.",
        "Make DIY cardboard furniture like shelves or small tables.",
        "Use shredded cardboard as compost material or weed barrier in gardens.",
        "Craft decorative trays or picture frames from cardboard.",
        "Repurpose boxes into kids’ toys, puzzles, or play forts.",
        "Use flattened cardboard as protective packing material.",
        "Make biodegradable pots for seedlings.",
        "Turn old cardboard into gift tags or greeting cards."
        ]
    },
    "Paper": {
        "nature": "dry recyclable",
        "dustbin_color": "Blue",
        "reuse_tip": [
            "Reuse paper for notes or rough work.",
            "Shred and use as packing material.",
            "Make paper mache crafts."
        ]
    },
    "Green Glass": {
        "nature": "dry recyclable",
        "dustbin_color": "Green",
        "reuse_tip": [
            "Use bottles as flower vases.",
            "Create decorative lights from glass bottles.",
            "Store homemade juices or sauces."
        ]
    },
    "Glass": {
        "nature": "dry recyclable",
        "dustbin_color": "Green",
        "reuse_tip": [
            "Use bottles as flower vases.",
            "Create decorative lights from glass bottles.",
            "Store homemade juices or sauces."
        ]
    },
    "Metal": {
        "nature": "dry recyclable",
        "dustbin_color": "Blue",
        "reuse_tip": [
            "Use old metal cans as pencil holders or small storage containers.",
            "Create garden art sculptures or decorative garden stakes from scrap metal.",
            "Make wind chimes using discarded metal utensils or parts.",
            "Repurpose metal pipes or rods into furniture supports or curtain rods.",
            "Make custom jewelry or keychains by cutting and shaping scrap metal.",
            "Turn scrap metal pieces into wall art or industrial-style home décor.",
            "Use scrap metal bits to create unique photo frames or mirrors.",
            "Build functional items like lamp bases or small shelving units from recycled metal."
        ]
    },
    "Human": {
        "nature": "not waste",
        "dustbin_color": "N/A",
        "reuse_tip": []
    },
    "Unknown": {
        "nature": "unknown",
        "dustbin_color": "Gray",
        "reuse_tip": [
            "Handle cautiously or refer to local guidelines."
        ]
    },
    # Add more classes and suggestions as needed...
}


st.set_page_config(page_title="Eco-Sort", page_icon="♻️", layout="centered")
st.markdown("""
    <style>
        .stApp {
            background:linear-gradient(rgba(0, 128, 0, 0.4), rgba(0, 128, 0, 0.4)),url("https://images.unsplash.com/photo-1476842634003-7dcca8f832de?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
        }
        .title {
            color: #1E5564;
            font-size: 2.2rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 0rem;
        }
        .subtitle {
            color: #36747D;
            font-size: 1.05rem;
            font-style: italic;
            margin-bottom: 1.8rem;
            text-align: center;
        }
        .upload-area {
            background-color: #BAC4C8;
            border: 2px dashed #3896A7;
            border-radius: 18px;
            padding: 2rem 1rem;
            text-align: center;
            font-weight: 600;
            color: #3896A7;
            margin-top: 1rem;
            margin-bottom: 2rem;
            transition: background-color 0.2s ease;
        }
        .upload-area:hover {
            background-color: #e6f6fa;
        }
        .result-title {
            color: #1E5564;
            font-size: 1.45rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            text-align: center;
        }
        .result-subtitle {
            font-size: 1.05rem;
            color: #36747D;
            margin-bottom: 1rem;
            text-align: center;
        }
        .dustbin-box {
            max-width: 150px;
            margin: 0.7rem auto 1.5rem auto;
            display: block;
        }
        .reuse-tip {
            background-color: #d2e3e6;
            padding: 1rem;
            border-radius: 14px;
            font-weight: 600;
            color: #0e4e60;
            margin-top: 1.2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .inline-images {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 10px;
        }
            
    </style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="title"  style="color:#ffffff">Eco-Sort</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle"  style="color:#ffffff">Smart Waste Classification & Reuse Guidance</p>', unsafe_allow_html=True)


# Input method toggle
input_method = st.radio(
    "Select Input Method:",
    ["Upload Image", "Scan (Webcam)"],
    horizontal=True
)


# Image input
image = None
if input_method == "Upload Image":
    uploaded_file = st.file_uploader("", type=['jpg', 'jpeg', 'png'], label_visibility="hidden")
    if uploaded_file is not None:
        image = Image.open(uploaded_file).convert('RGB')
else:
    camera_file = st.camera_input("Capture image")
    if camera_file is not None:
        image = Image.open(camera_file).convert('RGB')


# Drag & drop placeholder box (shown only if upload method selected)
if input_method == "Upload Image":
    st.markdown('<div class="upload-area">Drag & drop files here or click Browse to upload</div>', unsafe_allow_html=True)


# Prediction and results display
if image is not None:
    def preprocess(img):
        img = img.resize((input_details[0]['shape'][2], input_details[0]['shape'][1]))
        img = np.array(img).astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)
        return img

    input_data = preprocess(image)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])[0]
    class_idx = np.argmax(output)
    confidence = output[class_idx]
    pred_class = CLASS_NAMES[class_idx]

    # Clean label if index present (e.g., "9 Pen" -> "Pen")
    pred_class_clean = pred_class.split(' ', 1)[-1] if ' ' in pred_class else pred_class

    # Get info for class or fall back to Unknown
    info = waste_info.get(pred_class_clean, waste_info.get("Unknown"))

    # Show selected image and dustbin image side by side
    dustbin_img = None
    if info['dustbin_color'] == 'Red':
        dustbin_img = "dustbin imgs/red.jpg"
    elif info['dustbin_color'] == 'Green':
        dustbin_img = "dustbin imgs/green.jpg"
    elif info['dustbin_color'] == 'Blue':
        dustbin_img = "dustbin imgs/blue dustbin.jpg"
    elif info['dustbin_color'] == 'Gray':
        dustbin_img = "dustbin imgs/grey.jpg"

    # Special message for Human detection
    if pred_class_clean == "Human":
        st.success("You are Human")
    else:
        st.markdown('<div class="inline-images">', unsafe_allow_html=True)
        st.image(image, caption='Selected Image', width=200)
        if dustbin_img:
            st.image(dustbin_img, caption=f"{info['dustbin_color']} Dustbin", width=200)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f'<div style="color:#ffffff; font-size:1.7rem; font-weight:700; text-align:center;">Predicted waste type: {pred_class_clean}</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#ffffff; font-size:1.16rem; text-align:center;">Confidence:{confidence * 100:.2f}%</div>', unsafe_allow_html=True)

        tips_html = '<ul>' + ''.join([f'<li>{tip}</li>' for tip in info["reuse_tip"]]) + '</ul>'
        st.markdown(f'<div class="reuse-tip">💡 <b>Reuse Suggestions:</b>{tips_html}</div>', unsafe_allow_html=True)
        st.markdown('<div style="margin-top:24px"></div>', unsafe_allow_html=True)  # Adds 24px vertical space
        if pred_class_clean !="Unknown":
            st.warning(f"Dispose this item in the **{info['dustbin_color']} dustbin**.")
        st.info("Follow local waste management guidelines.")

        search_query = f"how to reuse {pred_class_clean.lower()}"
        youtube_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
        st.markdown(
            f'<br><b>If you want to reuse in more creative way, check this out:</b> '
            f'<a href="{youtube_url}" target="_blank">Creative Reuse Ideas on YouTube</a>',
            unsafe_allow_html=True
        )
