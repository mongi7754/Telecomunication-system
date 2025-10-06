If you use PyCharm:
1. Open this folder as a project.
2. Create and select a Python interpreter (virtualenv).
3. Install requirements: pip install -r requirements.txt
4. Mark the folder containing 'app' as Sources Root (optional).
5. Run this configuration:
   - Script path: <path to uvicorn executable in your venv>
   - Parameters: app.main:app --reload --host 0.0.0.0 --port 8000
Alternatively run in terminal:
   uvicorn app.main:app --reload
