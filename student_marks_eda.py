"""
Student Marks EDA Project
Run: python student_marks_eda.py
Pass rule: a student passes only if they score at least 40 in EVERY subject.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "student_marks.xlsx"
OUT_DIR = BASE_DIR / "student_marks_outputs"
OUT_DIR.mkdir(exist_ok=True)

SUBJECTS = ["Maths", "Physics", "Chemistry", "English", "Computer"]
PASS_MARK = 40

def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {DATA_FILE.name}. Keep it in the same folder as this Python file."
        )

    data = pd.read_excel(DATA_FILE)
    required = ["Student_Name"] + SUBJECTS
    missing = [col for col in required if col not in data.columns]
    if missing:
        raise ValueError(f"Excel file is missing columns: {missing}")

    # Data cleaning
    data = data.dropna(subset=["Student_Name"]).copy()
    for subject in SUBJECTS:
        data[subject] = pd.to_numeric(data[subject], errors="coerce")
    data = data.dropna(subset=SUBJECTS)
    for subject in SUBJECTS:
        data[subject] = data[subject].clip(0, 100)

    # Feature engineering
    data["Total_Marks"] = data[SUBJECTS].sum(axis=1)
    data["Average_Marks"] = data[SUBJECTS].mean(axis=1).round(2)
    data["Percentage"] = (data["Total_Marks"] / (len(SUBJECTS) * 100) * 100).round(2)
    data["Result"] = data[SUBJECTS].ge(PASS_MARK).all(axis=1).map({True: "Pass", False: "Fail"})
    data["Grade"] = pd.cut(
        data["Percentage"],
        bins=[-1, 39.99, 49.99, 59.99, 69.99, 79.99, 89.99, 100],
        labels=["F", "E", "D", "C", "B", "A", "A+"]
    )
    data["Rank"] = data["Total_Marks"].rank(method="min", ascending=False).astype(int)
    data = data.sort_values(["Rank", "Student_Name"])

    # Summary statistics
    subject_summary = pd.DataFrame({
        "Subject": SUBJECTS,
        "Highest_Mark": [data[s].max() for s in SUBJECTS],
        "Highest_Scoring_Student": [data.loc[data[s].idxmax(), "Student_Name"] for s in SUBJECTS],
        "Lowest_Mark": [data[s].min() for s in SUBJECTS],
        "Lowest_Scoring_Student": [data.loc[data[s].idxmin(), "Student_Name"] for s in SUBJECTS],
        "Average_Mark": [round(data[s].mean(), 2) for s in SUBJECTS],
        "Median_Mark": [round(data[s].median(), 2) for s in SUBJECTS],
    })
    overall_summary = pd.DataFrame({
        "Metric": [
            "Number of students", "Highest total", "Top student", "Lowest total",
            "Lowest-total student", "Class average total", "Class average percentage",
            "Passed students", "Failed students", "Pass rate (%)"
        ],
        "Value": [
            len(data), int(data["Total_Marks"].max()),
            data.loc[data["Total_Marks"].idxmax(), "Student_Name"],
            int(data["Total_Marks"].min()),
            data.loc[data["Total_Marks"].idxmin(), "Student_Name"],
            round(data["Total_Marks"].mean(), 2),
            round(data["Percentage"].mean(), 2),
            int((data["Result"] == "Pass").sum()),
            int((data["Result"] == "Fail").sum()),
            round((data["Result"] == "Pass").mean() * 100, 2)
        ]
    })

    # Console output
    print("\\n=== STUDENT MARKS EDA ===")
    print(data[["Rank", "Student_Name"] + SUBJECTS + ["Total_Marks", "Average_Marks", "Percentage", "Grade", "Result"]].to_string(index=False))
    print("\\n=== OVERALL SUMMARY ===")
    print(overall_summary.to_string(index=False))
    print("\\n=== SUBJECT-WISE SUMMARY ===")
    print(subject_summary.to_string(index=False))

    # Charts
    charts = [
        ("top_students_total_marks.png", data.nsmallest(10, "Rank").sort_values("Total_Marks"),
         "Student_Name", "Total_Marks", "Top 10 Students by Total Marks", "Total marks (out of 500)"),
        ("subject_average_marks.png", subject_summary, "Subject", "Average_Mark",
         "Average Marks by Subject", "Average marks (out of 100)"),
        ("pass_fail_count.png", data["Result"].value_counts().rename_axis("Result").reset_index(name="Count"),
         "Result", "Count", "Pass vs Fail Count", "Number of students"),
        ("student_average_marks.png", data.sort_values("Average_Marks"),
         "Student_Name", "Average_Marks", "Average Marks by Student", "Average marks (out of 100)"),
        ("subject_highest_lowest.png", subject_summary, None, None,
         "Highest and Lowest Marks by Subject", "Marks (out of 100)"),
        ("grade_distribution.png", data["Grade"].astype(str).value_counts().sort_index().rename_axis("Grade").reset_index(name="Count"),
         "Grade", "Count", "Grade Distribution", "Number of students"),
    ]

    for filename, frame, xcol, ycol, title, ylabel in charts:
        plt.figure(figsize=(10, 6))
        if filename == "subject_highest_lowest.png":
            x = range(len(subject_summary))
            plt.bar([i - 0.18 for i in x], subject_summary["Highest_Mark"], width=0.36, label="Highest")
            plt.bar([i + 0.18 for i in x], subject_summary["Lowest_Mark"], width=0.36, label="Lowest")
            plt.xticks(list(x), subject_summary["Subject"])
            plt.legend()
        elif filename == "pass_fail_count.png":
            plt.bar(frame[xcol], frame[ycol])
        elif filename == "grade_distribution.png":
            plt.bar(frame[xcol], frame[ycol])
        else:
            plt.bar(frame[xcol].astype(str), frame[ycol])
            if xcol == "Student_Name":
                plt.xticks(rotation=55, ha="right")
        plt.title(title)
        plt.ylabel(ylabel)
        plt.tight_layout()
        plt.savefig(OUT_DIR / filename, dpi=150)
        plt.close()

    # Save all useful tables into one Excel workbook
    output_excel = OUT_DIR / "student_marks_eda_report.xlsx"
    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        data.to_excel(writer, sheet_name="Student Results", index=False)
        overall_summary.to_excel(writer, sheet_name="Overall Summary", index=False)
        subject_summary.to_excel(writer, sheet_name="Subject Summary", index=False)

    print(f"\\nDone! Report and 6 charts saved in: {OUT_DIR}")
    print(f"Excel report: {output_excel.name}")

if __name__ == "__main__":
    main()
