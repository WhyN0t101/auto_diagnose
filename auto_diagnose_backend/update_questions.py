import json

# Define recommendations based on score
RECOMMENDATION_MAP = {
    "Access Control": {
        10: "Continue enforcing strict access controls and review policies regularly.",
        5: "Enhance access control measures by implementing multi-factor authentication.",
        0: "Implement strict access control mechanisms to prevent unauthorized access."
    },
    "Data Protection": {
        10: "Ensure encryption standards remain updated and review data protection policies regularly.",
        5: "Expand encryption and data protection measures to cover all critical information.",
        0: "Implement encryption and data loss prevention tools to safeguard sensitive data."
    },
    "Employee Awareness and Training": {
        10: "Continue regular security awareness training and phishing simulations.",
        5: "Increase training frequency and introduce interactive security awareness programs.",
        0: "Develop a mandatory security training program to educate employees on risks."
    },
    "Governance and Policies": {
        10: "Maintain a strong governance framework and review policies periodically.",
        5: "Enhance governance measures by aligning with industry best practices.",
        0: "Develop formal security policies and ensure organization-wide enforcement."
    },
    "Incident Response and Recovery": {
        10: "Test and refine the incident response plan regularly to improve effectiveness.",
        5: "Expand and formalize the incident response plan with clear response actions.",
        0: "Develop and implement an incident response plan to minimize downtime."
    },
    "Network Security": {
        10: "Regularly review and update network security configurations and segment networks appropriately.",
        5: "Strengthen network security by adding additional monitoring and segmentation controls.",
        0: "Implement firewall, IDS/IPS, and network segmentation to improve security."
    },
    "Third-Party Risk Management": {
        10: "Maintain regular audits of third-party vendors and enforce compliance requirements.",
        5: "Strengthen vendor security assessments and require compliance documentation.",
        0: "Implement a vendor risk management program to evaluate third-party security."
    }
}

# Load existing JSON file
with open("questions.json", "r", encoding="utf-8") as file:
    questions = json.load(file)

# Update each question with recommendations based on the selected answer
for question in questions:
    category = question["category"]
    
    for option in question["options"]:
        score = option["score"]
        if category in RECOMMENDATION_MAP and score in RECOMMENDATION_MAP[category]:
            option["recommendation"] = RECOMMENDATION_MAP[category][score]

# Save the updated JSON file
with open("updated_questions.json", "w", encoding="utf-8") as file:
    json.dump(questions, file, indent=4, ensure_ascii=False)

print("questions.json has been updated and saved as updated_questions.json.")
