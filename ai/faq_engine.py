import pandas as pd


def search_incidents(question):

    try:
        df = pd.read_csv("data/incidents.csv")

        question = question.lower()

        matches = []

        for _, row in df.iterrows():

            row_text = " ".join(
                str(value).lower()
                for value in row.values
            )

            if question in row_text:
                matches.append(row)

        if not matches:
            return None

        response = "📁 Similar Incidents Found\n\n"

        for row in matches[:5]:   # Show top 5 matches

            response += f"""
━━━━━━━━━━━━━━━━━━

🎫 Incident ID : {row['Id']}

📌 Issue :
{row['ShortDescription']}

🏢 Area :
{row['Affectedarea']}

📍 Location :
{row['Location']}

👨‍💻 Assigned To :
{row['AssignedTo']}

⚠ Priority :
{row['Priority']}

📊 Status :
{row['State']}

📅 Created :
{row['Created']}
"""

        return response

    except Exception as e:
        print("CSV Error:", e)
        return None