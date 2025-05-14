# 🕒 Timezone Converter FastAPI Application

A FastAPI application that allows you to convert time between different timezones, list all timezones, and retrieve timezones for a specific country.

---

## 📦 Features

- Convert time between timezones
- List all available timezones
- Get timezones for a specific country (with support for ambiguous names)

---

## 🚀 How to Run Locally

### ✅ Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### ⚙️ Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/antidude900/Fast-API-Time-Converter.git
   cd Fast-API-Time-Converter
   ```

2. **Create and activate a virtual environment:**

   **On Linux/macOS:**

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   **On Windows:**

   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

### ▶️ Running the Application

```bash
python -m app.run
```

The application will be accessible at default at: `http://127.0.0.1:8000`

---

## 🐳 Run with Docker

### ✅ Prerequisite

- Docker installed on your system.

### 🗐 Clone the repository:

```bash
git clone https://github.com/antidude900/Fast-API-Time-Converter.git
cd Fast-API-Time-Converter
```

### 🏗️Build the Docker Image

Navigate to the project root directory and run:

```bash
docker build -t timezone-converter .
```

### 🚢 Run the Docker Container

```bash
docker run -p 8000:8000 timezone-converter
```

The application will be accessible at default at: `http://127.0.0.1:8000`

### 🔨 Custom Host and Port Example

To run on custom host say 0.0.0.0 and custom port say 3000:

```bash
docker run -e APP_HOST="0.0.0.0" -e APP_PORT="3000" -p 3000:3000 timezone-converter
```

Then the application will be accessible at: `http://0.0.0.0:3000`

---

## 🔗 Example API Endpoints

### ✅ Welcome Message

**GET** `/`

Response:

```json
{ "message": "Hello from the Timezone Converter!" }
```

### 🔄 Convert Time

**GET** `/convert_time?time=10:00&from_tz=Nepal&to_tz=Europe/London`

Response:

```json
{
	"original_time": "10:00 Asia/Kathmandu (Nepal)",
	"converted_time": "05:15 Europe/London"
}
```

**GET** `/convert_time?time=10:00&from_tz=America/New_York&to_tz=Philippines`

Response:

```json
{
	"original_time": "10:00 America/New_York",
	"converted_time": "22:00 Asia/Manila (Philippines)"
}
```

### 🌐 List All Timezones

**GET** `/all_timezones`

Response:

```json
{
  "timezones": ["Africa/Abidjan","Africa/Accra","Africa/Addis_Ababa","Africa/Algiers",...]
}
```

### 🗺️ Get Timezones of a Country

**GET** `/timezones/Nepal`

Response:

```json
{
	"country": "Nepal",
	"timezone": ["Asia/Shanghai", "Asia/Urumqi"]
}
```
