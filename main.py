import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Gym Coach API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Gym Coach Backend is running"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

# ---------- Diet ----------
@app.get("/api/diet")
def get_diet():
    return {
        "title": "Smart Diet Guide",
        "tips": [
            "Aim for 0.7–1g protein per lb of bodyweight",
            "Fill half your plate with veggies",
            "Drink at least 2–3L of water daily",
            "Prioritize whole, minimally processed foods",
            "80/20 rule: be consistent, not perfect"
        ],
        "meals": [
            {
                "name": "Greek Yogurt Protein Bowl",
                "calories": 420,
                "protein": 38,
                "carbs": 45,
                "fat": 10,
                "ingredients": ["Greek yogurt", "berries", "honey", "granola", "chia seeds"],
                "time": "5 min"
            },
            {
                "name": "Chicken, Rice & Greens",
                "calories": 560,
                "protein": 46,
                "carbs": 62,
                "fat": 14,
                "ingredients": ["Chicken breast", "jasmine rice", "broccoli", "olive oil"],
                "time": "25 min"
            },
            {
                "name": "Tofu Stir‑Fry",
                "calories": 510,
                "protein": 28,
                "carbs": 58,
                "fat": 18,
                "ingredients": ["Firm tofu", "mixed veggies", "soy sauce", "garlic", "sesame oil"],
                "time": "20 min"
            },
            {
                "name": "Egg & Avocado Toast",
                "calories": 390,
                "protein": 20,
                "carbs": 34,
                "fat": 20,
                "ingredients": ["Sourdough", "eggs", "avocado", "chili flakes", "lemon"],
                "time": "10 min"
            }
        ],
        "hydration": {
            "note": "General guidance. Adjust for climate and activity level.",
            "liters_per_day_by_weight": [
                {"weight_lb": 120, "liters": 2.0},
                {"weight_lb": 160, "liters": 2.5},
                {"weight_lb": 200, "liters": 3.0}
            ]
        }
    }

# ---------- Workouts ----------
@app.get("/api/workouts")
def get_workouts():
    return {
        "title": "Workouts",
        "programs": [
            {
                "name": "Full‑Body Starter",
                "level": "Beginner",
                "days": 3,
                "exercises": [
                    {"name": "Bodyweight Squat", "sets": 3, "reps": "12–15"},
                    {"name": "Push‑ups", "sets": 3, "reps": "8–12"},
                    {"name": "Bent‑over Dumbbell Row", "sets": 3, "reps": "10–12"},
                    {"name": "Glute Bridge", "sets": 3, "reps": "12–15"},
                    {"name": "Plank", "sets": 3, "reps": "30–45s"}
                ]
            },
            {
                "name": "Upper / Lower Split",
                "level": "Intermediate",
                "days": 4,
                "exercises": [
                    {"name": "Back Squat", "sets": 4, "reps": "5–8"},
                    {"name": "Romanian Deadlift", "sets": 3, "reps": "8–10"},
                    {"name": "Bench Press", "sets": 4, "reps": "5–8"},
                    {"name": "Pull‑ups", "sets": 3, "reps": "6–10"},
                    {"name": "Hanging Leg Raise", "sets": 3, "reps": "10–12"}
                ]
            },
            {
                "name": "Push / Pull / Legs",
                "level": "Advanced",
                "days": 6,
                "exercises": [
                    {"name": "Overhead Press", "sets": 4, "reps": "6–10"},
                    {"name": "Weighted Pull‑ups", "sets": 4, "reps": "5–8"},
                    {"name": "Barbell Row", "sets": 4, "reps": "6–10"},
                    {"name": "Deadlift", "sets": 3, "reps": "3–5"},
                    {"name": "Front Squat", "sets": 4, "reps": "6–8"}
                ]
            }
        ]
    }

# ---------- Recovery ----------
@app.get("/api/recovery")
def get_recovery():
    return {
        "title": "Recovery Toolkit",
        "pillars": [
            {
                "name": "Sleep",
                "checklist": [
                    "7–9 hours in a cool, dark room",
                    "Fixed wake time",
                    "No screens 60 minutes before bed",
                    "Limit caffeine after noon"
                ]
            },
            {
                "name": "Mobility",
                "stretches": [
                    {"name": "Hip Flexor Stretch", "time": "60s/side"},
                    {"name": "Thoracic Opener", "time": "60s"},
                    {"name": "Hamstring Stretch", "time": "60s/side"}
                ]
            },
            {
                "name": "Breathwork",
                "routines": [
                    {"name": "Box Breathing", "pattern": "4‑4‑4‑4", "duration": "5 min"},
                    {"name": "Nasal 5‑second inhale / slow exhale", "duration": "3 min"}
                ]
            }
        ],
        "post_workout": [
            "Light walk 5–10 minutes",
            "Protein + carbs within 1–2 hours",
            "Hydrate and add electrolytes if needed"
        ]
    }

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
