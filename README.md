# Generator of streamlit web apps for maturity assessments
This programs allows to generate a complete streamlit web app for business maturity assessments. 
The generated web applications are multipage web applications that allow to collect and display real time updated data. The web applications provide user-authentication and data persistency. The data inserted is stored in a Firestore DB.

To create a web application you need to:
- Store a "configuration file" in the Configuration_file directory, whith informations on model for the maturity assessment. An example of a configuration file is provided.
- Store a json file containing credentials to connect to a Firestore DB to use as back-end in the DataManagement/Firestore directory.
- Run the launch_app.py script.


