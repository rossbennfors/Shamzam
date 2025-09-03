# Shamzam 🎵

_A microservice-based music recognition MVP (Shazam clone)_

This project implements **Shamzam**, a Shazam-like music recognition service, as specified in the ECM3408 — Enterprise Computing coursework. Shamzam uses **microservices**, an **SQLite database**, and the **[AudD.io API](https://audd.io/)** for music fragment recognition.

---

## 📖 Features (User Stories)

-   **S1 — Add Track**: Administrator can add a music track to the catalogue.
-   **S2 — Remove Track**: Administrator can remove a music track from the catalogue.
-   **S3 — List Catalogue**: Administrator can list all available tracks.
-   **S4 — Recognise Fragment**: User can upload a music fragment and match it to a track in the catalogue.

---

## 🏗️ Architecture

The project is composed of loosely coupled microservices:

-   **`catalogue.py`** — manages track storage and retrieval (add, remove, list).
-   **`audDio.py`** — interfaces with the **AudD.io** API to recognise audio fragments.
-   **`database_service.py`** — provides an abstraction layer over the SQLite database.
-   **`repository.py`** — repository pattern implementation for consistent DB access.
-   **Tests (`test-*.py`)** — end-to-end tests for each user story, covering both _happy paths_ and _unhappy paths_.

All services expose **RESTful APIs**, communicating using JSON.

---

## 🛠️ Tech Stack

-   **Python 3**
-   **Flask (REST APIs)**
-   **SQLite (database)**
-   **AudD.io API (audio recognition)**
-   **Pytest (testing)**

---

## 📚 Acknowledgements

-   [AudD.io](https://audd.io/) for music recognition
-   Provided audio samples (The Weeknd, Oasis, Backstreet Boys, Olivia Rodrigo, etc.)
