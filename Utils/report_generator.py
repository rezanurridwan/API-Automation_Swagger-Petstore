from datetime import datetime
from pathlib import Path
from html import escape

test_results = []

def add_test_result(
    test_case,
    category,
    status,
    status_code,
    message="",
    data=""
):
    """Add test result to list"""

    test_results.append({
        "Test Case": test_case,
        "Testing Category": category,
        "Testing Status": status,
        "Status_code": status_code,
        "Message": message,
        "Data": data,
        "Date Execute": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    })


def generate_html_report():

    """Generate HTML report"""

    total = len(test_results)

    passed = sum(
        1 for r in test_results
        if r["Testing Status"] == "PASS"
    )

    failed = sum(
        1 for r in test_results
        if r["Testing Status"] == "FAIL"
    )

    positive = sum(
        1 for r in test_results
        if r["Testing Category"] == "POSITIVE"
    )

    negative = sum(
        1 for r in test_results
        if r["Testing Category"] == "NEGATIVE"
    )

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>API AUTOMATION Test Report</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }}

            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #333;
                font-size: 32px;
            }}

            .summary {{
                display: flex;
                gap: 15px;
                margin: 20px 0;
                flex-wrap: wrap;
            }}

            .summary-item {{
                flex: 1;
                min-width: 120px;
                padding: 15px;
                border-radius: 5px;
                text-align: center;
                color: white;
            }}

            .passed, .positive {{
                background-color: #4CAF50;
            }}

            .failed, .negative {{
                background-color: #f44336;
            }}

            .total {{
                background-color: #2196F3;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #ddd;
                overflow-wrap: anywhere;
                vertical-align: top;
            }}

            th {{
                background-color: #2196F3;
                color: white;
            }}

            tr:hover {{
                background-color: #f5f5f5;
            }}

            .pass {{
                color: #4CAF50;
                font-weight: bold;
            }}

            .fail {{
                color: #f44336;
                font-weight: bold;
            }}

            .timestamp {{
                color: #666;
                font-size: 12px;
            }}

            pre {{
                white-space: pre-wrap;
                margin: 0;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <h1>API AUTOMATION Test Report</h1>

            <p class="timestamp">
                Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </p>

            <div class="summary">

                <div class="summary-item total">
                    <h3>Total Tests</h3>
                    <p style="font-size: 24px;">{total}</p>
                </div>

                <div class="summary-item passed">
                    <h3>Passed</h3>
                    <p style="font-size: 24px;">{passed}</p>
                </div>

                <div class="summary-item failed">
                    <h3>Failed</h3>
                    <p style="font-size: 24px;">{failed}</p>
                </div>

                <div class="summary-item positive">
                    <h3>Positive</h3>
                    <p style="font-size: 24px;">{positive}</p>
                </div>

                <div class="summary-item negative">
                    <h3>Negative</h3>
                    <p style="font-size: 24px;">{negative}</p>
                </div>

            </div>

            <table>

                <tr>
                    <th>Test Case</th>
                    <th>Testing Category</th>
                    <th>Testing Status</th>
                    <th>Status Code</th>
                    <th>Message</th>
                    <th>Expected Result</th>
                    <th>Date Execute</th>
                </tr>
    """

    for result in test_results:

        status_class = (
            "pass"
            if result["Testing Status"] == "PASS"
            else "fail"
        )

        html_content += f"""
            <tr>
                <td>{escape(str(result['Test Case']))}</td>
                <td>{escape(str(result['Testing Category']))}</td>
                <td>
                    <span class="{status_class}">
                        {escape(str(result['Testing Status']))}
                    </span>
                </td>
                <td>{escape(str(result['Status_code']))}</td>
                <td><pre>{escape(str(result['Message']))}</pre></td>
                <td><pre>{escape(str(result['Data']))}</pre></td>
                <td>{escape(str(result['Date Execute']))}</td>
            </tr>
        """

    html_content += """
            </table>

        </div>

    </body>
    </html>
    """

    # Save report
    report_dir = Path("reports")
    report_dir.mkdir(parents=True, exist_ok=True)

    report_path = report_dir / "petstore_api_report.html"

    report_path.write_text(
        html_content,
        encoding="utf-8"
    )

    print(f"\\nHTML Report generated: {report_path.resolve()}")
