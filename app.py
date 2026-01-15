# =========================================================
# XTTS Audio Lab V2 — XTTS + Edge TTS
# =========================================================

import os
import torch
import datetime
import gradio as gr
from TTS.api import TTS
import edge_tts
import asyncio
import tempfile

# =========================================================
# CONFIG
# =========================================================

BASE_DIR = os.getcwd()
MODELS_DIR = os.path.join(BASE_DIR, "models")
VOICES_DIR = os.path.join(BASE_DIR, "voices")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(MODELS_DIR, exist_ok=True)
os.makedirs(VOICES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

os.environ["TTS_HOME"] = MODELS_DIR
os.environ["COQUI_TOS_AGREED"] = "1"

# Langues pour XTTS
XTTS_LANGUAGES = ["fr", "en", "es", "de", "it", "pt", "pl", "tr", "ru", "nl", "cs", "ar", "zh-cn", "ja", "hu", "ko"]

# Voix principales pour Edge TTS (Sélection)
EDGE_VOICES = {
    "🇫🇷 French - Denise (Neural)": "fr-FR-DeniseNeural",
    "🇫🇷 French - Henri (Neural)": "fr-FR-HenriNeural",
    "🇫🇷 French - Eloise (Neural)": "fr-FR-EloiseNeural",  # Voix enfant/jeune
    "🇺🇸 English - Guy (Neural)": "en-US-GuyNeural",
    "🇺🇸 English - Jenny (Neural)": "en-US-JennyNeural",
    "🇬🇧 English - Sonia (Neural)": "en-GB-SoniaNeural",
    "🇪🇸 Spanish - Alvaro (Neural)": "es-ES-AlvaroNeural",
    "🇪🇸 Spanish - Elvira (Neural)": "es-ES-ElviraNeural",
    "🇩🇪 German - Conrad (Neural)": "de-DE-ConradNeural",
    "🇩🇪 German - Katja (Neural)": "de-DE-KatjaNeural",
    "🇮🇹 Italian - Diego (Neural)": "it-IT-DiegoNeural",
    "🇮🇹 Italian - Elsa (Neural)": "it-IT-ElsaNeural"
}

# =========================================================
# MODEL XTTS LOADING
# =========================================================

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🖥️ Device pour XTTS: {device}")

# On charge XTTS au démarrage
print("⏳ Chargement de XTTS v2...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)
print("✅ XTTS chargé !")


# =========================================================
# UTILS
# =========================================================

def get_voice_files():
    """Récupère les fichiers audio dans le dossier voices pour le clonage XTTS"""
    return sorted([
        f for f in os.listdir(VOICES_DIR)
        if f.lower().endswith((".wav", ".mp3", ".flac"))
    ])

def timestamp_path(prefix="audio", ext="wav"):
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(OUTPUT_DIR, f"{prefix}_{ts}.{ext}")


# =========================================================
# FONCTIONS GENERATION
# =========================================================

# --- XTTS ---
def generate_xtts(text, language, voice_file, upload_voice, speed, temperature):
    if not text.strip():
        raise gr.Error("Le texte est vide.")

    # Priorité : Upload > Fichier stocké
    speaker = upload_voice if upload_voice else (os.path.join(VOICES_DIR, voice_file) if voice_file else None)
    
    if not speaker:
        raise gr.Error("Veuillez sélectionner ou uploader une voix de référence.")

    out_path = timestamp_path("xtts")

    tts.tts_to_file(
        text=text,
        speaker_wav=speaker,
        language=language,
        file_path=out_path,
        speed=speed,
        temperature=temperature,
        split_sentences=True
    )

    return out_path

# --- EDGE TTS (Microsoft) ---
async def generate_edge(text, voice_friendly_name, rate_offset, pitch_offset):
    if not text.strip():
        raise gr.Error("Le texte est vide.")
    
    voice_key = EDGE_VOICES[voice_friendly_name]
    out_path = timestamp_path("edge", "mp3") # Edge sort souvent du mp3 par défaut
    
    # Formatage des paramètres pour edge-tts (ex: "+10%", "-5Hz")
    rate_str = f"{rate_offset:+d}%"
    pitch_str = f"{pitch_offset:+d}Hz"

    communicate = edge_tts.Communicate(text, voice_key, rate=rate_str, pitch=pitch_str)
    
    await communicate.save(out_path)
    
    return out_path


# =========================================================
# UI GRADIO
# =========================================================

with gr.Blocks(title="XTTS & Edge Audio Lab") as demo:
    gr.Markdown("# 🎙️ Audio Lab : XTTS v2 & Microsoft Edge")
    gr.Markdown("Générez de la parole via clonage de voix (XTTS) ou via le cloud Microsoft (Edge).")

    with gr.Tabs():

        # ---------------- TAB 1 : XTTS v2 (Clonage) ----------------
        with gr.Tab("🦜 XTTS v2 (Voice Cloning)"):
            with gr.Row():
                with gr.Column(scale=1):
                    xtts_text = gr.Textbox(lines=5, label="Texte à dire", placeholder="Entrez votre texte ici...")
                    xtts_lang = gr.Dropdown(XTTS_LANGUAGES, value="fr", label="Langue")
                    
                    with gr.Group():
                        gr.Markdown("### 🗣️ Voix de référence")
                        xtts_voice_file = gr.Dropdown(get_voice_files(), label="Voix stockée (dossier /voices)")
                        xtts_upload = gr.Audio(type="filepath", label="Ou uploader un fichier WAV/MP3")
                    
                    with gr.Accordion("⚙️ Paramètres avancés", open=False):
                        xtts_speed = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="Vitesse (Speed)")
                        xtts_temp = gr.Slider(0.01, 1.0, value=0.75, step=0.05, label="Température (Créativité/Stabilité)")
                    
                    xtts_btn = gr.Button("🚀 Générer XTTS", variant="primary")

                with gr.Column(scale=1):
                    gr.Markdown("### 🎧 Résultat")
                    xtts_output = gr.Audio(label="Audio Généré", type="filepath")

            xtts_btn.click(
                generate_xtts,
                inputs=[xtts_text, xtts_lang, xtts_voice_file, xtts_upload, xtts_speed, xtts_temp],
                outputs=[xtts_output]
            )

        # ---------------- TAB 2 : EDGE TTS (Cloud) ----------------
        with gr.Tab("☁️ Microsoft Edge TTS"):
            with gr.Row():
                with gr.Column(scale=1):
                    edge_text = gr.Textbox(lines=5, label="Texte à dire", placeholder="Entrez votre texte ici...")
                    
                    edge_voice = gr.Dropdown(list(EDGE_VOICES.keys()), value="🇫🇷 French - Henri (Neural)", label="Modèle de voix")
                    
                    with gr.Accordion("⚙️ Paramètres de prosodie", open=True):
                        edge_rate = gr.Slider(-50, 50, value=0, step=1, label="Vitesse (%)")
                        edge_pitch = gr.Slider(-50, 50, value=0, step=1, label="Hauteur/Pitch (Hz)")

                    edge_btn = gr.Button("⚡ Générer Edge TTS", variant="primary")

                with gr.Column(scale=1):
                    gr.Markdown("### 🎧 Résultat")
                    edge_output = gr.Audio(label="Audio Généré (Edge)", type="filepath")

            edge_btn.click(
                generate_edge,
                inputs=[edge_text, edge_voice, edge_rate, edge_pitch],
                outputs=[edge_output]
            )

if __name__ == "__main__":
    print("🚀 Lancement de l'interface...")
    demo.queue().launch(inbrowser=True)