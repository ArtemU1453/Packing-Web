# Industrial Packing System

## Открыть на телефоне

Прямая ссылка для браузера телефона:

**https://artemu1453.github.io/Packing-Web/**

> Если ссылка пока не открывается, включите GitHub Pages в настройках репозитория:
> `Settings → Pages → Deploy from a branch → main → /root`.

### Добавить на главный экран

#### Android / Chrome

1. Откройте ссылку: https://artemu1453.github.io/Packing-Web/
2. Нажмите меню браузера `⋮`.
3. Выберите **Добавить на главный экран** или **Install app**.
4. Подтвердите установку.

#### iPhone / Safari

1. Откройте ссылку: https://artemu1453.github.io/Packing-Web/
2. Нажмите кнопку **Поделиться**.
3. Выберите **На экран «Домой»**.
4. Нажмите **Добавить**.

## Features

- Matrix based full box packaging
- Smart remainder box optimization
- Weight control (max 21 kg)
- Industrial GUI
- Mobile browser PWA mode
- Input parameters + packing report
- EXE ready

## Web / PWA

The web version is served by `index.html`, uses `manifest.json`, and registers
`sw.js` for offline caching. It can be opened directly from a phone browser and
added to the home screen as a standalone app.

## Desktop

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the desktop application:

```bash
python main.py
```

## Build EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```
