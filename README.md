# MealMode PIN Lookup

Simple Flask app for teachers to look up student PINs during lunch check-in. Pulls student data directly from Supabase.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
export SUPABASE_URL="your-supabase-url"
export SUPABASE_KEY="your-supabase-key"
export TEACHER_PASSWORD="your-teacher-password"
```

Or create a `.env` file:
```
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
TEACHER_PASSWORD=your-teacher-password
```

3. Run the app:
```bash
python pin_lookup_app.py
```

4. Open `http://localhost:5000` in your browser

## Usage

1. **Select School**: Choose from the dropdown of schools in Supabase
2. **Login**: Enter teacher password
3. **Search**: Type student name (first, last, or full)
4. **Display**: Click student to show PIN in large font
5. **Logout**: Click logout button when done

## Supabase Schema

You need two tables in Supabase:

### `schools` table
```
- id (UUID, primary key)
- name (text)
```

### `students` table
```
- id (UUID, primary key)
- student_id (text)
- first_name (text)
- last_name (text)
- full_name (text)
- grade_level (text)
- pin (text)
- school (UUID, foreign key to schools.id)
```

## Configuration

- **TEACHER_PASSWORD**: Set in environment variable or `.env` file
- **SUPABASE_URL**: Your Supabase project URL
- **SUPABASE_KEY**: Your Supabase anon key (public key is fine for this)

## Features

- Real-time student data from Supabase
- Session-based authentication
- Real-time search across first/last/full names
- Minimal, responsive UI
- Works great on phone/tablet
- Secure backend authentication

## Claude Code Deployment

To run with Claude Code:
1. Set environment variables in Claude Code settings
2. Run `pip install -r requirements.txt && python pin_lookup_app.py`
3. Claude Code will provide a public URL

For production, use gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:5000 pin_lookup_app:app
```
