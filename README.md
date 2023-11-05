# Generator of streamlit web apps for maturity assessments
This program allows to generate complete streamlit web applications to perform business maturity assessments. 
The generated web applications are multipage web applications that allow to collect and display real time updated data.

To create a web application you need to:
- Store a "configuration file" in the Configuration_file directory, whith informations on model for the maturity assessments. An example of a configuration file is provided.
- Store a json file containing credentials to connect to a Firestore DB to use as back-end in the DataManagement/Firestore directory.
- Run the launch_app.py script.


