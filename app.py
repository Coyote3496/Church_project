from flask import Flask, render_template, request
import pandas as pd
from questions import get_questions
from data_processing import get_paginated_responses, generate_summary_html
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
questions = get_questions()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Collect responses from the form, making optional questions optional
        response = {
            "gender": request.form.get("gender", ""),
            "age": request.form.get("age", ""),
            "marriage_status": request.form.get("marriage_status", ""),
            "christian_status": request.form.get("christian_status", ""),
            **{f"q{i+1}": request.form.get(f"q{i+1}") for i in range(128)}
        }

        email = request.form.get("email", "")

        df = pd.DataFrame([response])
        df.index.name = 'Respondent'
        detailed_responses_array, total_pages, dic = get_paginated_responses(df, 16, 8)
        summary_html = generate_summary_html(detailed_responses_array)

        df = mod_dataframe(df, dic)
        combined_df = save_responses(df)

        if email:
            send_email(email, summary_html)

        return render_template(
            "thank_you.html",
            summary_html=summary_html,
            detailed_responses_array=detailed_responses_array,
            total_pages=total_pages,
            current_page=1
        )
    return render_template("index.html", questions=questions)
#Email pass word:ptpfceaxmmgmzykt

def mod_dataframe(df, dic):
    for val in dic:
        df[val] = dic[val]
    return df


def send_email(recipient, summary_html):
    sender = "shadyjaynose@gmail.com"
    app_password = "ptpfceaxmmgmzykt"  # App password generated from your Google account
    subject = "Your Spiritual Gifts Inventory Results"

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(summary_html, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, app_password)
            server.sendmail(sender, recipient, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")


@app.route("/thank_you", methods=["GET"])
def thank_you_page():
    page = int(request.args.get('page', 1))
    try:
        df = pd.read_csv("responses.csv", index_col=0)
    except FileNotFoundError:
        return "No responses found."

    detailed_responses_array, total_pages, pulled = get_paginated_responses(df, 16, 8, page)
    summary_html = generate_summary_html(df)
    
    return render_template(
        "thank_you.html",
        summary_html=summary_html,
        detailed_responses_array=detailed_responses_array,
        total_pages=total_pages,
        current_page=page
    )

def save_responses(df):
    try:
        existing_df = pd.read_csv("responses.csv", index_col=0)
        combined_df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        combined_df = df

    combined_df.index.name = 'Respondent'
    combined_df.to_csv("responses.csv", index_label='Respondent')
    return combined_df

if __name__ == "__main__":
    app.run(debug=True)
