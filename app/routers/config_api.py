def create_configuration_fastapi(app):
    # Changes to the docs
    app.title = "CRUD FastAPI"
    app.version = "1.0"
    app.description = "My API"
    app.terms_of_service = "https://example.com/terms/"
    app.contact = {
        "name": "AAZG",
        "url": "https://github.com/AAZG",
        "email": "telocreistewey@gmail.com"
    }
    app.license_info = {
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }