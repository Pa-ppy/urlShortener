# Django URL Shortener

This is a backend URL shortener application built with Django and Django REST Framework.

## Features

- Generates unique short codes for long URLs.
- Redirects short URLs to their original long URLs.
- Tracks click counts for each short URL.

## Setup

Follow these steps to set up and run the application locally.

### 1. Clone the Repository (if applicable)

If you haven't already, clone this repository to your local machine:

```bash
git clone https://github.com/Pa-ppy/urlShortener.git
cd urlShortener
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

- **On macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
- **On Windows:**
  ```bash
  .\venv\Scripts\activate
  ```

### 4. Install Dependencies

Install the required Python packages using pip:

```bash
pip install django djangorestframework
```

### 5. Run Database Migrations

Apply the database migrations to create the necessary tables:

```bash
python3 manage.py makemigrations shortener

python3 manage.py migrate
```

## Running the Application

Start the Django development server:

```bash
python3 manage.py runserver
```

The server will typically run on `http://127.0.0.1:8000/`.

## Running Tests

To run the tests, run the following command:

```bash
python3 manage.py test shortener
```

## API Usage

### 1. Shorten a URL

To shorten a long URL, send a `POST` request to the `/api/shorten/` endpoint.

- **Method:** `POST`
- **URL:** `http://127.0.0.1:8000/api/shorten/`
- **Headers:** `Content-Type: application/json`
- **Body (JSON):**
  ```json
  {
    "original_url": "https://www.example.com/your-very-long-url-here"
  }
  ```

**Example using `curl`:**

```bash
curl -X POST -H "Content-Type: application/json" -d '{"original_url": "https://www.google.com"}' http://127.0.0.1:8000/api/shorten/

curl -X POST -H "Content-Type: application/json" -d '{"original_url": "https://www.loom.com/looms/videos"}' http://127.0.0.1:8000/api/shorten/

curl -X POST -H "Content-Type: application/json" -d '{"original_url": "https://en.wikipedia.org/wiki/Power_Rangers"}' http://127.0.0.1:8000/api/shorten/
```

**Successful Response (example):**

```json
{
  "original_url": "https://www.google.com",
  "short_code": "aBcDeF",
  "created_at": "2023-10-27T10:00:00.000000Z",
  "clicks": 0
}
```

The `short_code` is the generated short URL identifier.

### 2. Redirect to the Original URL

To redirect to the original URL, simply access the short URL in your browser or via a `GET` request.

- **Method:** `GET`
- **URL:** `http://127.0.0.1:8000/<your_short_code>` (replace `<your_short_code>` with the actual short code obtained from the shortening API)

**Example using `curl`:**

If your short code is `aBcDeF`:

```bash
curl -L http://127.0.0.1:8000/aBcDeF
```

This will redirect you to the `original_url` associated with `aBcDeF`.
