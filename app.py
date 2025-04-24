from flask import Flask, render_template, request, jsonify
from Routes.mainpages_routes import main_pages
from Routes.dashboard_routes import dashboard_pages
from Routes.register_emp import register_user
from Callbacks.checklogin import check_credentials
from Routes.dashresumes import dash_resumes
from Routes.savejobs_routes import dashboard_savedjobs

app = Flask(__name__)

app.secret_key = 'this_is_secret'
# Home route
app.register_blueprint(main_pages)
app.register_blueprint(dashboard_pages)
app.register_blueprint(register_user)
app.register_blueprint(check_credentials)
app.register_blueprint(dash_resumes)
app.register_blueprint(dashboard_savedjobs)
app.config['SECRET_KEY'] = 'your_secret_key'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
