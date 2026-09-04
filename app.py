import json
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from brandflow.evaluator import evaluate_brand_consistency
from brandflow.models import BrandProfile, ContentRequest
from brandflow.profiles import delete_profile, load_profiles, save_profile
from brandflow.prompting import build_brief
from brandflow.providers import get_provider


PROFILE_STORE = Path("data/brand_profiles.json")

st.set_page_config(
    page_title="BrandFlow AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .block-container {padding-top: 2.2rem; padding-bottom: 4rem;}
      [data-testid="stSidebar"] {border-right: 1px solid rgba(255,255,255,.08);}
      .hero {
        padding: 1.4rem 1.5rem;
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 20px;
        background: linear-gradient(135deg, rgba(124,140,255,.14), rgba(25,211,218,.06));
        margin-bottom: 1.2rem;
      }
      .hero h1 {margin: 0 0 .35rem 0; font-size: 2.15rem;}
      .hero p {margin: 0; color: #b8c0d6;}
      .pill {
        display: inline-block; padding: .28rem .62rem; margin-right: .35rem;
        border-radius: 999px; border: 1px solid rgba(255,255,255,.13);
        color: #cfd5e8; font-size: .78rem;
      }
      .section-label {
        color: #8f9ab8; text-transform: uppercase; font-size: .72rem;
        letter-spacing: .12em; font-weight: 700; margin-bottom: .2rem;
      }
      .small-note {color:#8f9ab8; font-size:.82rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="section-label">Portfolio project · Python + AI authoring</div>
      <h1>BrandFlow AI</h1>
      <p>Reusable brand context for emails, landing pages and forms — without re-explaining the brand every time.</p>
      <div style="margin-top:.8rem">
        <span class="pill">Python</span>
        <span class="pill">Streamlit</span>
        <span class="pill">AI-ready</span>
        <span class="pill">Local profiles</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

profiles = load_profiles(PROFILE_STORE)

with st.sidebar:
    st.header("Brand context")

    if profiles:
        selected = st.selectbox(
            "Saved profiles",
            ["— New profile —"] + sorted(profiles.keys()),
        )
    else:
        selected = "— New profile —"

    current = profiles.get(selected)

    name = st.text_input("Brand name", current.name if current else "Northstar Studio")
    audience = st.text_input(
        "Audience",
        current.audience if current else "independent creators and small businesses",
    )
    tone = st.text_input("Tone", current.tone if current else "clear, confident, practical")
    offer = st.text_area(
        "Offer",
        current.offer if current else "brand-consistent content workflows",
        height=90,
    )
    values = st.text_input(
        "Values",
        current.values if current else "clarity, consistency, usefulness",
    )
    forbidden = st.text_input(
        "Forbidden phrases",
        current.forbidden_phrases if current else "revolutionary, guaranteed",
    )

    sidebar_profile = BrandProfile(
        name=name,
        audience=audience,
        tone=tone,
        offer=offer,
        values=values,
        forbidden_phrases=forbidden,
    )

    save_col, delete_col = st.columns(2)
    if save_col.button("Save profile", use_container_width=True):
        if name.strip():
            save_profile(PROFILE_STORE, sidebar_profile)
            st.success("Saved locally.")
            st.rerun()
        else:
            st.error("Brand name is required.")

    if delete_col.button("Delete", use_container_width=True, disabled=selected == "— New profile —"):
        delete_profile(PROFILE_STORE, selected)
        st.rerun()

    st.caption("Profiles are stored locally in `data/` and are not committed to Git.")

left, right = st.columns([1, 1], gap="large")

with left:
    st.markdown('<div class="section-label">1 · Authoring request</div>', unsafe_allow_html=True)
    st.subheader("What are we creating?")

    content_type = st.segmented_control(
        "Content type",
        ["Email", "Landing page", "Form"],
        default="Email",
    )

    preset = st.selectbox(
        "Quick example",
        ["Custom", "Creator launch", "Small SaaS", "Coffee brand"],
    )

    examples = {
        "Creator launch": (
            "Launch a new creator toolkit",
            "Explore the toolkit",
            "Focus on reducing repetitive work while keeping the creator's own brand voice.",
        ),
        "Small SaaS": (
            "Introduce a workflow automation feature",
            "Start a free trial",
            "Keep the copy practical and aimed at small teams with limited time.",
        ),
        "Coffee brand": (
            "Launch a seasonal coffee collection",
            "See the collection",
            "Use warm, sensory language without sounding exaggerated.",
        ),
    }

    default_goal, default_cta, default_extra = examples.get(
        preset,
        ("Launch a new creator toolkit", "Explore the toolkit", "Focus on reducing repetitive work while keeping the creator's own brand voice."),
    )

    goal = st.text_input("Goal", default_goal)
    cta = st.text_input("Call to action", default_cta)
    extra = st.text_area("Extra context", default_extra, height=125)

    request = ContentRequest(
        content_type=content_type or "Email",
        goal=goal,
        call_to_action=cta,
        extra_context=extra,
    )

    profile = sidebar_profile
    brief = build_brief(profile, request)

    generate = st.button("Generate content", type="primary", use_container_width=True)

with right:
    st.markdown('<div class="section-label">2 · Brand-aware brief</div>', unsafe_allow_html=True)
    st.subheader("Structured context")
    st.code(brief, language="text")
    st.caption("The brief is deliberately inspectable: brand context and task context stay separate.")

if generate:
    try:
        provider = get_provider()
        st.session_state["result"] = provider.generate(brief, profile, request)
        st.session_state["last_brief"] = brief
    except Exception as exc:
        st.error(f"Generation failed: {exc}")

if "result" in st.session_state:
    st.divider()
    st.markdown('<div class="section-label">3 · Generated result</div>', unsafe_allow_html=True)

    output_col, score_col = st.columns([2.1, 0.9], gap="large")

    with output_col:
        st.subheader("Content")
        edited_result = st.text_area(
            "Generated output",
            st.session_state["result"],
            height=300,
            label_visibility="collapsed",
        )
        st.session_state["result"] = edited_result

        export_payload = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "brand": profile.as_dict(),
            "request": {
                "content_type": request.content_type,
                "goal": request.goal,
                "call_to_action": request.call_to_action,
                "extra_context": request.extra_context,
            },
            "content": edited_result,
        }

        st.download_button(
            "Export result as JSON",
            data=json.dumps(export_payload, indent=2),
            file_name="brandflow_export.json",
            mime="application/json",
            use_container_width=True,
        )

    evaluation = evaluate_brand_consistency(edited_result, profile)

    with score_col:
        st.subheader("Quick checks")
        st.metric("Consistency signal", f"{evaluation.score}/100")
        st.progress(evaluation.score / 100)

        labels = {
            "brand_name_present": "Brand name present",
            "audience_signal_present": "Audience signal present",
            "forbidden_phrases_avoided": "Forbidden phrases avoided",
        }

        for key, passed in evaluation.checks.items():
            st.write(("✅ " if passed else "⚠️ ") + labels[key])

        st.caption("Deterministic checks only — not an AI quality score.")

st.divider()
st.caption("Built by Kamil Jozef Ginter · Portfolio project · Trieste, Italy")
