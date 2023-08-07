from tracker import create_app

app = create_app()

if __name__ == '__main__':
    #app.app_context().push()
    app.run(debug=True)
