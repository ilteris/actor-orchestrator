#!/Users/ilteris/soul_venv/bin/python3
import json
import os
import sys
from datetime import datetime

class InsightDelivery:
    def __init__(self, template_path="soul/delivery/templates/insight_report.md"):
        self.template_path = template_path
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template not found: {self.template_path}")
        
        with open(self.template_path, 'r') as f:
            self.template = f.read()

    def generate_report(self, data, output_path):
        """
        Simple template engine for high-fidelity insight delivery.
        """
        report = self.template
        report = report.replace("{{ study_id }}", data.get("study_id", "N/A"))
        report = report.replace("{{ date }}", datetime.now().strftime("%Y-%m-%d"))
        report = report.replace("{{ pillar }}", data.get("pillar", "UXR Analysis Platform"))
        report = report.replace("{{ summary }}", data.get("summary", ""))
        report = report.replace("{{ next_steps }}", data.get("next_steps", ""))

        # Handle insights loop
        insights_str = ""
        for insight in data.get("insights", []):
            i_str = "### [ " + insight.get("title", "Untitled") + " ]\n"
            i_str += f"- **Description**: {insight.get('description', '')}\n"
            i_str += f"- **Evidence**: {insight.get('evidence', '')}\n"
            i_str += f"- **Confidence**: {insight.get('confidence', '0')}%\n\n"
            insights_str += i_str
        
        # This is a very basic replacement since we don't have Jinja2 installed
        # In a production system, we'd use a real template engine.
        start_tag = "{% for insight in insights %}"
        end_tag = "{% endfor %}"
        
        if start_tag in report and end_tag in report:
            prefix = report.split(start_tag)[0]
            suffix = report.split(end_tag)[1]
            report = prefix + insights_str + suffix

        with open(output_path, 'w') as f:
            f.write(report)
        return output_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: insight_delivery.py <input_json> <output_md>")
        sys.exit(1)
    
    with open(sys.argv[1], 'r') as f:
        data = json.load(f)
    
    delivery = InsightDelivery()
    out = delivery.generate_report(data, sys.argv[2])
    print(f"Report generated at: {out}")
