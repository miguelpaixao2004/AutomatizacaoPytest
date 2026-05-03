# AutomatizacaoPytest

This is a FastAPI project with automated testing using Pytest.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

3. Run tests:
   ```bash
   pytest
   ```

## API Endpoints

- GET / : Returns {"Hello": "World"}
- GET /items/{item_id} : Returns item details