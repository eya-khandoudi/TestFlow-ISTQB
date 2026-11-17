from app import create_app

app = create_app()

if __name__ == '__main__':
    print("====================================================")
    print(" TestFlow - ISTQB Software Test Management System")
    print(" Starting development server at http://127.0.0.1:5000")
    print("====================================================")
    app.run(host='127.0.0.1', port=5000, debug=True)
