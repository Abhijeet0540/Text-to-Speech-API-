"""
Test script to verify that the app can be imported correctly.
"""

try:
    from app import app
    print("Successfully imported app from app.py")
    print(f"App name: {app.name}")
    print(f"App routes: {[rule.rule for rule in app.url_map.iter_rules()]}")
    print("Import test passed!")
except Exception as e:
    print(f"Error importing app: {str(e)}")
