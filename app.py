import tempfile
import streamlit as st

from github_data import get_repo_data
from evidence_engine import analyze_repository
from confidence_engine import calculate_confidence
from safety_checker import safety_report
from impact_engine import calculate_impact
from report_generator import generate_report

st.set_page_config(
    page_title="AI Impact Proof",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Impact Proof")
st.caption("Measure, explain and prove the impact of AI on software delivery.")

st.header("1. Connect a GitHub project")

repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/owner/repository"
)

github_token = st.text_input(
    "GitHub Token (optional for public repositories)",
    type="password"
)

if st.button("Analyze Project", type="primary"):
    if not repo_url:
        st.error("Please enter a GitHub repository URL.")
        st.stop()

    try:
        with st.spinner("Collecting GitHub evidence..."):
            data = get_repo_data(repo_url, github_token or None)

        repository = data["repository"]
        evidence = analyze_repository(data)

        has_reviews = any(
            len(pr.get("reviews", [])) > 0
            for pr in data["pull_requests"]
        )

        confidence = calculate_confidence(
            evidence_count=len(evidence),
            has_pr_reviews=has_reviews,
            has_test_data=False,
            has_baseline=False
        )

        all_text = ""
        for commit in data["commits"]:
            all_text += commit.get("commit", {}).get("message", "") + "\n"

        for pr in data["pull_requests"]:
            all_text += str(pr.get("title", "")) + "\n"
            all_text += str(pr.get("body", "")) + "\n"

        safety = safety_report(all_text)

        st.success("Evidence collection completed.")

        st.header("2. Project Evidence")
        c1, c2, c3 = st.columns(3)

        c1.metric("Commits analyzed", len(data["commits"]))
        c2.metric("Pull Requests analyzed", len(data["pull_requests"]))
        c3.metric("AI Evidence", len(evidence))

        st.header("3. AI Impact Inputs")
        left, right = st.columns(2)

        with left:
            time_saved = st.number_input(
                "Estimated hours saved by AI",
                min_value=0.0, value=10.0, step=0.5
            )
            quality_score = st.slider(
                "Quality score", 0, 100, 80
            )
            rework_hours = st.number_input(
                "AI-related rework hours",
                min_value=0.0, value=2.0, step=0.5
            )

        with right:
            ai_cost = st.number_input(
                "AI tool cost ($)",
                min_value=0.0, value=20.0, step=1.0
            )
            hourly_rate = st.number_input(
                "Developer value per hour ($)",
                min_value=1.0, value=30.0, step=1.0
            )

        impact = calculate_impact(
            time_saved,
            quality_score,
            rework_hours,
            ai_cost,
            hourly_rate,
            confidence["score"]
        )

        st.header("4. AI Impact")
        a, b, c, d = st.columns(4)
        a.metric("AI Impact", f"{impact['impact_score']}/100")
        b.metric("Time Saved", f"{impact['time_saved']} h")
        c.metric("Estimated Value", f"${impact['saved_value']}")
        d.metric("Estimated Net Value", f"${impact['net_value']}")

        st.header("5. Confidence")
        st.metric("Confidence Level", confidence["level"])
        st.progress(confidence["score"] / 100)
        st.caption(f"Confidence score: {confidence['score']}/100")

        st.header("6. AI Safety")
        st.metric("Safety Score", f"{safety['score']}/100")

        if safety["findings"]:
            st.warning("Potential sensitive information was detected in analyzed metadata.")
            for finding in safety["findings"]:
                st.write(f"⚠ {finding}")
        else:
            st.success("No obvious secrets detected by the prototype scanner.")

        st.header("7. AI Evidence")
        if evidence:
            for item in evidence:
                st.write(
                    f"**{item['type']}** — {item['title']}"
                )
                st.caption(
                    f"Evidence confidence: {item['confidence']}"
                )
        else:
            st.info(
                "No explicit AI references were found in the analyzed GitHub metadata. "
                "This does not prove that AI was not used."
            )

        st.header("8. Management Report")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            report_path = temp_file.name

        try:
            generate_report(
                report_path,
                repository.get("full_name", "GitHub Project"),
                impact,
                confidence,
                safety,
                evidence
            )

            with open(report_path, "rb") as file:
                st.download_button(
                    "📄 Download AI Impact Report",
                    data=file,
                    file_name="AI_Impact_Report.pdf",
                    mime="application/pdf"
                )
        except Exception as report_error:
            st.warning(f"Report generation encountered an issue: {report_error}")
            st.info("Analysis complete, but PDF report could not be generated.")

    except Exception as error:
        st.error(f"Analysis failed: {error}")
        st.info(
            "For a public repository, a GitHub token is normally not required. "
            "For private repositories, provide a suitable token."
        )
