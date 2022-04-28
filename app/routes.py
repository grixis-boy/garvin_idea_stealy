from app import app


@app.route("/")
@app.route("/index")
def index():
    user = {"first_name": "Matthew", "last_name": "Irwin"}
    return (
        """<html>
    <head>
        <title>Home Page - Microblog</title>
    </head>
    <body>
        <h1>Hello, """
        + user["first_name"]
        + " "
        + user["last_name"]
        + """!</h1>
    </body>
</html>
    """
    )
    return "Hello, World!"
