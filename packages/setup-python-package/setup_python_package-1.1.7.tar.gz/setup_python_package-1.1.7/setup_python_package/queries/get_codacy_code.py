from ..utils import load_repository_name, load_repository_author_name
import webbrowser
from userinput import userinput
import subprocess
from ..enablers import enable_codacy
import os


def validate_codacy_code(code: str):
    return len(code) == 32


def get_codacy_code(automatically_open_browser: bool):
    enable_codacy(automatically_open_browser)
    if automatically_open_browser:
        input("Press enter to go to the codacy project settings now to get the project token.")
        webbrowser.open(
            "https://app.codacy.com/app/{account}/{repository}/settings/integrations".format(
                account=load_repository_author_name(),
                repository=load_repository_name()
            ),
            new=2,
            autoraise=True
        )
    print("Go to your repository on Codacy and go to settings/Integrations.")
    print("Now add a new Integration (blue button on the top right).")
    print("Choose project API.")
    print("Copy the code available under the new project API button.")

    test_reported_id = userinput(
        "CODACY PROJECT TOKEN",
        validator=validate_codacy_code,
        cache=False
    )

    subprocess.run([
        "travis",
        "encrypt",
        "CODACY_PROJECT_TOKEN={}".format(test_reported_id),
        "--add"
    ], shell=True, input="\n", stdout=open(os.devnull, 'w'), encoding='ascii')
