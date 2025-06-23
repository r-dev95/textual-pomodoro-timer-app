<!-- ============================================================
  Project Image
 ============================================================ -->
<div align=center>
  <img
    src='docs/image/icon.png'
    alt='Project Image.'
    width=300
  />
</div>

<!-- ============================================================
  Overview
 ============================================================ -->
# :book:Overview

[![English](https://img.shields.io/badge/English-018EF5.svg?labelColor=d3d3d3&logo=readme)](./README.md)
[![Japanese](https://img.shields.io/badge/Japanese-018EF5.svg?labelColor=d3d3d3&logo=readme)](./README_JA.md)
[![license](https://img.shields.io/github/license/r-dev95/textual-pomodoro-timer-app)](./LICENSE)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

[![Python](https://img.shields.io/badge/Python-3776AB.svg?labelColor=d3d3d3&logo=python)](https://github.com/python)
[![Sphinx](https://img.shields.io/badge/Sphinx-000000.svg?labelColor=d3d3d3&logo=sphinx&logoColor=000000)](https://github.com/sphinx-doc/sphinx)
[![Pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?labelColor=d3d3d3&logo=pytest)](https://github.com/pytest-dev/pytest)
[![Pydantic](https://img.shields.io/badge/Pydantic-ff0055.svg?labelColor=d3d3d3&logo=pydantic&logoColor=ff0055)](https://github.com/pydantic/pydantic)

This is a pomodoro timer app by TUI using [Textual].

We use [Plyer] to notify you when work or break time is over.

[Textual]: https://github.com/textualize/textual/
[Plyer]: https://github.com/kivy/plyer

<!-- ============================================================
  Features
 ============================================================ -->
## :desktop_computer:Features

<img
  src='docs/image/demo.gif'
  alt='demo screen'
/>

|item                                          |feature                               |
| ---                                          | ---                                  |
|Work time input field (left side of screen)   |Set the working time. (unit: minutes) |
|Break time input field (right side of screen) |Set break time. (unit: minutes)       |
|Start button                                  |Start the timer.                      |
|Pause button                                  |Pause the timer.                      |
|Reset button                                  |Reset the timer.                      |
|Status display field                          |Shows the status (see below).         |
|Time display field                            |Show time.                            |

### Status

<table>
  <tr>
    <th>Wait status</th>
    <th>Work status</th>
  </tr>
  <tr>
    <td>
      <img
          src='docs/image/app_wait.png'
          alt='Wait status screen'
      />
    </td>
    <td>
      <img
        src='docs/image/app_work.png'
        alt='Work status screen'
      />
    </td>
  </tr>
</table>
<table>
  <tr>
    <th>Bleak status</th>
    <th>Pause status</th>
  </tr>
  <tr>
    <td>
      <img
        src='docs/image/app_break.png'
        alt='Break status screen'
      />
    </td>
    <td>
      <img
        src='docs/image/app_pause.png'
        alt='Pause status screen'
      />
    </td>
  </tr>
</table>

<!-- ============================================================
  Usage
 ============================================================ -->
## :keyboard:Usage

### Install

```bash
git clone https://github.com/r-dev95/textual-pomodoro-timer-app.git
```

### Build virtual environment

You need to install `uv`.

If you don't have a python development environment yet, see [here](https://github.com/r-dev95/env-python).

```bash
cd textual-pomodoro-timer-app/
uv sync
```

### Run

```bash
cd src
uv run python app.py
```

- Set work and break times.
- Press the start button to start the work status.

  When the working time is over, the status changes to Break.

- If you want to temporarily stop the timer, press the pause button.
- If you want to reset the timer, press the reset button.
- If you want to quit the app, press `Ctrl+q` or `Ctrl+c`.

<!-- ============================================================
  Structure
 ============================================================ -->
## :bookmark_tabs:Structure

<div align=center>
  <img
    src='docs/image/classes.png'
    alt='classes.'
  />
</div>

<!-- ============================================================
  License
 ============================================================ -->
## :key:License

This repository is licensed under the [MIT License](LICENSE).
