# Zadanie 2

import sys
import urllib.request

import cv2
import matplotlib.pyplot as plt
import numpy as np

SOURCE = "https://commons.wikimedia.org/wiki/Special:FilePath/Lemon.jpg?width=800"
if len(sys.argv) > 1:
    SOURCE = sys.argv[1]


def load_image(source):
    if source.startswith(("http://", "https://")):
        request = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(request) as response:
                data = np.asarray(bytearray(response.read()), dtype=np.uint8)
        except Exception as error:
            raise SystemExit(f"Strona nie pozwala na pobranie zdjęcia: {error}")
        img_bgr = cv2.imdecode(data, cv2.IMREAD_COLOR)
    else:
        img_bgr = cv2.imread(source, cv2.IMREAD_COLOR)
    if img_bgr is None:
        raise SystemExit("Nie udało się wczytać obrazu.")
    return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)


def histogram(channel):
    return cv2.calcHist([channel], [0], None, [256], [0, 256]).ravel()


def neutral_means(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    mask = (hsv[:, :, 1] < 60) & (hsv[:, :, 2] > 40)
    if mask.mean() < 0.05:
        return None
    return image[mask].mean(axis=0)


def analyze(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    mean = float(gray.mean())
    std = float(gray.std())
    p1, p99 = np.percentile(gray, [1, 99])
    dark_clip = float((gray <= 5).mean())
    bright_clip = float((gray >= 250).mean())
    neutral = neutral_means(image)
    cast = float(neutral.max() - neutral.min()) if neutral is not None else 0.0

    problems = []
    if mean < 85:
        problems.append("niedoświetlone")
    if mean > 200 and bright_clip > 0.01:
        problems.append("prześwietlone")
    if std < 25 or (p99 - p1) < 80:
        problems.append("niski kontrast")
    if dark_clip > 0.05:
        problems.append("obcięte cienie")
    if bright_clip > 0.05:
        problems.append("obcięte światła")
    if cast > 20:
        problems.append("dominanta kolorystyczna")

    stats = {
        "średnia jasność": mean,
        "odch. std.": std,
        "zakres 1-99%": p99 - p1,
        "cienie (<=5) %": dark_clip * 100,
        "światła (>=250) %": bright_clip * 100,
        "różnica kanałów (neutralne piksele)": cast,
    }
    return problems, stats


def improve(image, problems):
    result = image.astype(np.float32)

    if "dominanta kolorystyczna" in problems:
        neutral = neutral_means(image)
        gains = np.clip(neutral.mean() / neutral, 0.85, 1.15)
        result = np.clip(result * gains, 0, 255)

    ycrcb = cv2.cvtColor(result.astype(np.uint8), cv2.COLOR_RGB2YCrCb).astype(np.float32)
    y = ycrcb[:, :, 0]

    if "niedoświetlone" in problems or "prześwietlone" in problems:
        mean = np.clip(y.mean(), 1, 254) / 255
        gamma = np.clip(np.log(0.5) / np.log(mean), 0.6, 1.6)
        y = 255 * (y / 255) ** gamma

    if "niski kontrast" in problems:
        low, high = np.percentile(y, [0.5, 99.5])
        if high > low:
            y = np.clip((y - low) / (high - low) * 255, 0, 255)

    if "obcięte cienie" in problems:
        y = np.where(y < 60, y * 0.85 + 9, y)
        y = 255 * (y / 255) ** 0.85

    if "obcięte światła" in problems:
        y = np.where(y > 200, 200 + (y - 200) * 0.6, y)

    ycrcb[:, :, 0] = np.clip(y, 0, 255)
    return cv2.cvtColor(ycrcb.astype(np.uint8), cv2.COLOR_YCrCb2RGB)


def plot_histograms(axes, image, prefix):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    items = [("jasność", gray, "gray"),
             ("kanał R", image[:, :, 0], "red"),
             ("kanał G", image[:, :, 1], "green"),
             ("kanał B", image[:, :, 2], "blue")]
    for ax, (name, channel, color) in zip(axes, items):
        ax.fill_between(range(256), histogram(channel), color=color, alpha=0.8)
        ax.set_xlim(0, 255)
        ax.set_title(f"{prefix} - {name}", fontsize=9)


image = load_image(SOURCE)
problems, stats = analyze(image)

print("Statystyki histogramu:")
for name, value in stats.items():
    print(f"  {name}: {value:.1f}")
verdict = ", ".join(problems) if problems else "zdjęcie poprawne"
print("Ocena:", verdict)

improved = improve(image, problems) if problems else image
improved_problems, _ = analyze(improved)
print("Po poprawie:", ", ".join(improved_problems) if improved_problems else "zdjęcie poprawne")

fig, axes = plt.subplots(2, 5, figsize=(20, 8), constrained_layout=True)
fig.suptitle(f"Ocena zdjęcia: {verdict}", fontsize=12)
axes[0, 0].imshow(image)
axes[0, 0].set_title("Oryginał", fontsize=10)
axes[1, 0].imshow(improved)
axes[1, 0].set_title("Po poprawie" if problems else "Bez zmian", fontsize=10)
for ax in (axes[0, 0], axes[1, 0]):
    ax.axis("off")
plot_histograms(axes[0, 1:], image, "Oryginał")
plot_histograms(axes[1, 1:], improved, "Po poprawie")
plt.show()
