# 🎙️ XTTS & Edge Audio Lab

Une interface web simple et puissante (Gradio) réunissant deux des meilleures technologies actuelles pour la synthèse vocale (TTS) :
1. **XTTS v2 (Local)** : Clonage de voix haute fidélité.
2. **Microsoft Edge TTS (Cloud)** : Génération ultra-rapide et gratuite avec les voix Azure.

---

## ✨ Fonctionnalités

### 🦜 Onglet 1 : XTTS v2 (Voice Cloning)
* **Moteur** : Coqui TTS (XTTS v2).
* **Clonage de voix** : Fournissez un court extrait audio (6s+) d'une voix, et le modèle la clonera.
* **Local** : Tout tourne sur votre machine (GPU NVIDIA recommandé).
* **Multilingue** : Supporte 16 langues (Français, Anglais, Espagnol, Allemand, Japonais, etc.).
* **Réglages** : Contrôle de la vitesse, de la température (créativité) et gestion des références audio.

### ☁️ Onglet 2 : Microsoft Edge TTS
* **Moteur** : API Edge (via `edge-tts`).
* **Gratuit & Rapide** : Pas besoin de GPU puissant, utilise le cloud Microsoft.
* **Qualité Azure** : Accès aux voix "Neural" (ex: Henri, Denise, Guy, Jenny).
* **Réglages** : Ajustement fin de la prosodie (Vitesse et Hauteur/Pitch).

---

## 🛠️ Pré-requis

* **Système** : Windows 10/11 (testé) ou Linux.
* **Python** : Version **3.10** requise (impératif pour la compatibilité XTTS).
* **Matériel** :
    * Une carte graphique **NVIDIA** (CUDA) est fortement recommandée pour XTTS.
    * Sans GPU, XTTS sera lent (CPU only), mais Edge TTS fonctionnera parfaitement.

---

## 🚀 Installation (Windows)

### 1. Installation Automatique
Le projet contient un script facilitant l'installation.

1. Clonez ce dépôt ou téléchargez les fichiers.
2. Double-cliquez sur `install.bat`
3. Le script va :
    * Vérifier la présence de Python 3.10.
    * Créer un environnement virtuel (`venv`).
    * Installer PyTorch (compatible CUDA) et toutes les dépendances

### 2. Lancement
Une fois installé, lancez simplement l'application :


###  Si vous avez créé un fichier start.bat :
start.bat

###  Sinon, via la ligne de commande :
venv\Scripts\activate


L'interface s'ouvrira automatiquement dans votre navigateur à l'adresse : `http://127.0.0.1:7860`.

---

## 📂 Structure des dossiers

Lors du premier lancement, le script créera automatiquement les dossiers suivants :

* `models/` : Où le modèle XTTS v2 sera téléchargé (environ 2-3 Go).
* `voices/` : Placez ici vos fichiers `.wav` ou `.mp3` pour le clonage de voix.
* `output/` : Tous les fichiers audio générés sont sauvegardés ici avec un horodatage.

---

## 📦 Installation Manuelle (Linux / Mac / Expert)

Si vous n'utilisez pas le `install.bat`, voici les commandes :

```bash
# 1. Créer l'environnement virtuel
python3.10 -m venv venv
source venv/bin/activate

# 2. Mettre à jour pip
pip install --upgrade pip

# 3. Installer les dépendances
pip install -r requirements.txt

## ⚠️ Notes importantes

* **Premier lancement** : Le premier démarrage peut prendre quelques minutes car XTTS doit télécharger les modèles pré-entraînés.
* **Licence Coqui** : XTTS v2 est sous licence *Coqui Public Model License* (utilisation non-commerciale par défaut, vérifiez les conditions sur Hugging Face).
* **Connexion** : Edge TTS nécessite une connexion internet active.

---

## 🙏 Crédits

* **Interface** : [Gradio](https://gradio.app/)
* **IA Locale** : [Coqui AI TTS](https://github.com/coqui-ai/TTS)
* **IA Cloud** : [Edge-TTS](https://github.com/rany2/edge-tts)
