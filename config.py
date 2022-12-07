import os

base_dir = os.path.dirname(os.path.abspath(__file__))


class BaseConfig(object):
    """Base configuration."""

    APP_NAME = "Cost Calc"

    DEBUG_TB_ENABLED = False
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "Ensure you set a secret key, this is important!"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

    # Mail config
    MAIL_SERVER = os.getenv("MAIL_SERVER", "localhost")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "465"))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "unknown_user_name")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "no-password")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "sender_name")

    DEFAULT_BIN_SIZES = [
        {"name": "A0", "width": 841, "height": 1188},
        {"name": "A1", "width": 594, "height": 841},
        {"name": "A2", "width": 420, "height": 594},
        {"name": "A3", "width": 297, "height": 420},
        {"name": "A4", "width": 210, "height": 297},
        {"name": "A5", "width": 148, "height": 210},
    ]

    METRIC_TO_SQR_UNIT_VALUE = {
        "cm": 100 * 100,
        "in": 12 * 12,
    }

    # colors
    COLOR_WHITE = "white"
    COLOR_BLACK = "black"
    COLOR_GREY = "#efe6e6"

    RECT_PACK_IMG_MAX_SIDE_SIZE = 1024

    # default calculator settings
    MOQ = ""
    MOQ_UNIT = ""
    COST = ""
    COST_PER = ""
    ORDER_URL = ""
    ORDER_ENABLED = False
    CUT_SPACING = 0.5
    METRIC_SYSTEM = None
    SHEETS = None

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEVEL_DATABASE_URL",
        "sqlite:///" + os.path.join(base_dir, "database-devel.sqlite3"),
    )


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL",
        "sqlite:///" + os.path.join(base_dir, "database-test.sqlite3"),
    )


class ProductionConfig(BaseConfig):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(base_dir, "database.sqlite3")
    )
    WTF_CSRF_ENABLED = True


config = dict(
    development=DevelopmentConfig, testing=TestingConfig, production=ProductionConfig
)
