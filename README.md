\# Explainability Hackathon — Trusted AI × HR



\*\*Themes:\*\* Frugal AI and Explainable AI



\## Context



A fictional company faces high employee turnover and wants an AI-powered solution to help HR understand why people leave and take preventive action. We build a prediction model that is both \*\*lightweight (frugal)\*\* and \*\*transparent (explainable)\*\*.



\## Team workstreams



| Workstream | Folder |

|------------|--------|

| Data cleaning \& augmentation | `data/` |

| Model (training, XAI, frugality) | `model/` |

| Frontend / demo UI | `frontend/` | 



\## Repo structure

```

Explainability\_Hackaton/

├── data/

│   ├── raw/                  # Original dataset (do not modify)

│   ├── cleaned/              # Output of cleaning pipeline

│   └── augmented/            # Synthetic text data

├── model/                    # Training, SHAP/LIME, CodeCarbon

├── frontend/                 # Demo UI

├── notebooks/                # Exploration

├── docs/                     # Data card, model card, architecture, summary

├── assets/                   # Charts, plots, screenshots

├── slides/                   # Pitch deck

├── requirements.txt

└── .gitignore

```



\## Quick start

```bash

git clone <repo-url>

cd Explainability\_Hackaton

pip install -r requirements.txt

```



\## Deliverables



| # | Deliverable | Location | Status |

|---|-------------|----------|--------|

| 1 | README | `README.md` | ✅ |

| 2 | Data card | `docs/DATA\_CARD.md` | ⬜ |

| 3 | Model card | `docs/MODEL\_CARD.md` | ⬜ |

| 4 | Architecture diagram | `docs/ARCHITECTURE.md` | ⬜ |

| 5 | Executive summary | `docs/EXECUTIVE\_SUMMARY.md` | ⬜ |

| 6 | Demo script | `docs/DEMO\_SCRIPT.md` | ⬜ |

| 7 | Slides / Pitch | `slides/` | ⬜ |



\## Key tools



| Purpose | Tool |

|---------|------|

| Explainability | SHAP, LIME |

| Carbon tracking | CodeCarbon, Ecologits |

| Model comparison | ComparAI |

