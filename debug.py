"""
this file is used for debug flask in vscode.
"""

from cloudr import create_app


app = create_app()
app.run(debug=True, use_reloader=False)