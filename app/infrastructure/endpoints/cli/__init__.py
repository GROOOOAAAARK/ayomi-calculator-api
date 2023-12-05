from typer import Option, Typer
from uvicorn import run

from app.infrastructure.endpoints.api import get_app
from app.infrastructure.configs import get_config

app = Typer()

@app.command()
def start(
    host: str = Option('0.0.0.0', '--host', help='Bind socket to the defined host'),
    port: int = Option(8000, '--port', help='Bind socket to socket with the defined port'),
    env: str = Option('', '--env', help='Env where the app is launched (test / dev / prod)')
):
    config = get_config(env)
    api = get_app(config)
    run(
        app=api,
        host=host,
        port=port,
    )

if __name__ == '__main__':
    app()
