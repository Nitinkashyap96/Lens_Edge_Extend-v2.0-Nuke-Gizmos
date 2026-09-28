# Lens_Edge_Extend-v2.0
LENS EDGE EXTEND v2.0  Nuke gizmo by Nitin Kashyap  ==============================================================  Compatible Nuke versions : 10 or later (Nuke 10 -> 16)  Compatibility : Linux, Mac, Windows  Python : 2.7 / 3.7 / 3.9 / 3.10 / 3.11  Menu location : NK_Tools > Lens_Edge_Extend



# 🔍 Lens Edge Extend

**A Nuke gizmo that extends and distorts the edges of your plate through a lens matte, with optional chromatic separation.**

Created by **Nitin Kashyap** · Version 2.0

![Nuke](https://img.shields.io/badge/Nuke-10%20→%2016-yellow)
![Python](https://img.shields.io/badge/Python-2.7%20%7C%203.7%20→%203.11-blue)
![Qt](https://img.shields.io/badge/Qt-PySide%20%7C%20PySide2%20%7C%20PySide6-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

<!-- Add a preview image or GIF here:
![Preview](docs/preview.gif)
-->

---

## ✨ Features

- Drive the effect from a lens matte using **Alpha** or **Luma**
- **Blur**, **size** and **multiplier** controls for the lens shape
- Adjustable **distortion amount** (positive and negative)
- Optional **matte mode**: distortion only where the lens is
- Optional **alpha distortion** and **chromatic separation**
- One-click **Reset all settings** button (undo-safe)
- Animated **credit splash screen** (auto-detects PySide / PySide2 / PySide6)
- Works on Nuke 10 to 16, on Windows, macOS and Linux

---

## 📁 Repository Structure

```
NK_Tools/
├── init.py              # Adds the Icons and gizmos folders to the Nuke plugin path
├── menu.py              # Creates the NK_Tools menu and loads the credit module
├── nk_credit.py         # Credit + animated splash screen
├── gizmos/
│   └── Lens_Edge_Extend.gizmo
└── Icons/               # Optional, for menu icons
```

---

## 📦 Installation

### Step 1: Download

Download the repository as a ZIP (**Code → Download ZIP**) and extract it, or clone it:

```bash
git clone https://github.com/<your-username>/Lens_Edge_Extend.git
```

### Step 2: Find your `.nuke` folder

| OS | Location |
|---|---|
| Windows | `C:\Users\<username>\.nuke` |
| macOS | `/Users/<username>/.nuke` |
| Linux | `/home/<username>/.nuke` |

### Step 3: Copy the files

Copy the following into your `.nuke` folder, keeping this layout:

```
.nuke/
├── init.py
├── menu.py
├── nk_credit.py
└── gizmos/
    └── Lens_Edge_Extend.gizmo
```

> ⚠️ **Already have an `init.py` or `menu.py`?** Do **not** overwrite them. Append the contents of this repo's files to your existing ones instead.

### Step 4: Restart Nuke

Close and reopen Nuke. The Script Editor should print something like:

```
nk_credit installed: Lens Edge Extend v2.0 by Nitin Kashyap | Nuke 15.x | Qt: PySide2
```

### Step 5: Create the node

In the menu bar go to **NK_Tools → Lens_Edge_Extend**, or press `Tab` and type `Lens_Edge_Extend`.

---

## 🚀 Usage

### Inputs

| Input | Label | Description |
|---|---|---|
| `Src` | Source | The plate you want to extend / distort |
| `Lens` | Matte | The lens shape (alpha or luma) that drives the effect |
| `Mask` | Mask | Optional mask input |

### Quick start

1. Connect your plate to **Src**.
2. Connect your lens matte to **Lens**.
3. Choose **Alpha** or **Luma** in the *Lens* dropdown.
4. Adjust **Lens Size**, **Blur Lens** and **Distortion Amount** until the edge looks right.
5. Enable **Distort Chroma** and tweak **Chroma Separation** for colour fringing.

---

## 🎛️ Controls

| Knob | Default | Range | Description |
|---|---|---|---|
| **Lens** | Alpha | Alpha / Luma | Which channel of the lens input drives the effect |
| **Use Lens as Matte** | Off | On / Off | Restricts the distortion to only where the lens is |
| **Blur Lens** | 6 | – | Softens the lens matte |
| **Lens Size** | 3 | 0 – 100 | Size of the lens effect |
| **Lens Multiplier** | 1 | 1 – 100 | Multiplies the displacement strength |
| **Distortion Amount** | -4 | -100 – 100 | Strength and direction of the distortion |
| **Distort Alpha** | Off | On / Off | Also distorts the alpha channel |
| **Distort Chroma** | Off | On / Off | Enables chromatic separation |
| **Chroma Separation** | 0 | -10 – 10 | Amount of RGB channel offset |
| **all Settings Reset** | – | Button | Restores every control above to its default |
| **About / Splash** | – | Button | Shows the credit splash screen |

---

## ⚙️ Configuration (`nk_credit.py`)

All options live in the `CONFIG` dictionary at the top of `nk_credit.py`:

| Option | Default | Description |
|---|---|---|
| `enabled` | `True` | Master switch. `False` disables the whole module |
| `author` | `"Nitin Kashyap"` | Name shown on the splash and label |
| `tool_name` | `"Lens Edge Extend"` | Tool name shown on the splash |
| `version` | `"v2.0"` | Version shown on the splash |
| `contact` | `""` | Optional e-mail / link (hidden when empty) |
| `splash_seconds` | `3.5` | How long the splash stays on screen |
| `splash_on_create` | `False` | Show the splash when the node is created |
| `auto_credit` | `False` | Auto-add credit knobs (the gizmo already includes them) |
| `show_label` | `True` | Show "by \<author\>" under the node |

To disable the credit module without editing code, set the environment variable:

```bash
NK_CREDIT_DISABLE=1
```

---

## 🧩 Compatibility

| Nuke | Python | Qt binding |
|---|---|---|
| 10.x | 2.7 | PySide (Qt4) |
| 11.x – 15.x | 2.7 / 3.7 / 3.9 / 3.10 | PySide2 (Qt5) |
| 16.x | 3.11 | PySide6 (Qt6) |

The module picks the same Qt binding that Nuke itself uses, so it will not conflict with other installed PySide versions.

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---|---|
| **NK_Tools menu missing** | Check that `menu.py` is directly inside `.nuke` and restart Nuke. |
| **Node not found / "Unknown command"** | Make sure the `.gizmo` file is inside `.nuke/gizmos/` and that `init.py` is installed. |
| **Splash does not appear** | Make sure `enabled` is `True` and `NK_CREDIT_DISABLE` is not set. Check the Script Editor for messages starting with `nk_credit:`. |
| **"Must construct a QApplication" error** | Update to the latest `nk_credit.py`. It loads the Qt binding matching your Nuke version. |
| **Reset button reports missing knobs** | Do not rename the knob labels inside the gizmo. The reset script finds them by label. |

---

## 🗺️ Roadmap

- [ ] Add preview images / demo GIF
- [ ] Add example `.nk` script
- [ ] Add icon for the menu entry

---

## 🤝 Contributing

Contributions, bug reports and feature requests are welcome.

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

Released under the **MIT License**. See [`LICENSE`](LICENSE) for details.

> Add a `LICENSE` file to the repo (GitHub: **Add file → Create new file → name it `LICENSE`** and choose the MIT template).

---

## 👤 Author   **Nitin Kashyap**
