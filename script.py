import requests
from datetime import datetime

def get_github_status():
    url = "https://www.githubstatus.com/api/v2/components.json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        failed_components = []

        for component in data["components"]:
            if component["status"] != "operational":
                failed_components.append(
                    f"{component['name']} : {component['status']}"
                )

        return failed_components

    except Exception as e:
        return [f"Unable to retrieve GitHub Status API: {str(e)}"]


def generate_emc():
    failed_components = get_github_status()

    today = datetime.now().strftime("%d-%b-%Y")

    if len(failed_components) == 0:
        result = "PASS"

        subject = f"{today} - GitHubStatus EMC {result}"

        body = f"""
GitHub Status EMC Check

Date: {today}

Result: PASS

All GitHub services are operational.
"""

    else:
        result = "FAIL"

        subject = f"{today} - GitHubStatus EMC {result}"

        body = f"""
GitHub Status EMC Check

Date: {today}

Result: FAIL

Affected Components:

{chr(10).join(failed_components)}
"""

    return subject, body


if __name__ == "__main__":
    subject, body = generate_emc()

    print("=" * 60)
    print("EMAIL SUBJECT")
    print("=" * 60)
    print(subject)

    print("\n" + "=" * 60)
    print("EMAIL BODY")
    print("=" * 60)
    print(body)