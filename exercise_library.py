from __future__ import annotations

FOCUSES = {
    "abs": {
        "name": "Abs & core",
        "short": "CORE",
        "icon": "◉",
        "description": "Build a steadier core with controlled, no-rush movements.",
        "duration": 18,
        "color": "mint",
    },
    "chest": {
        "name": "Chest",
        "short": "PUSH",
        "icon": "↗",
        "description": "Pressing movements to train your chest, shoulders, and triceps.",
        "duration": 30,
        "color": "peach",
    },
    "back": {
        "name": "Back",
        "short": "PULL",
        "icon": "⌁",
        "description": "Build pulling strength and a stronger upper back.",
        "duration": 30,
        "color": "blue",
    },
    "arms": {
        "name": "Arms",
        "short": "ARMS",
        "icon": "↟",
        "description": "A focused session for biceps, triceps, and shoulders.",
        "duration": 25,
        "color": "violet",
    },
    "legs": {
        "name": "Legs & glutes",
        "short": "LOWER",
        "icon": "⌄",
        "description": "Squat, hinge, and step your way to stronger legs.",
        "duration": 32,
        "color": "peach",
    },
    "full-body": {
        "name": "Full body",
        "short": "TOTAL",
        "icon": "✳",
        "description": "A balanced head-to-toe workout for the days you want it all.",
        "duration": 35,
        "color": "mint",
    },
}


def movement(
    name: str,
    bodyweight: str,
    cue: str,
    target: str = "8–12 reps",
) -> dict[str, str]:
    return {
        "name": name,
        "bodyweight": bodyweight,
        "cue": cue,
        "target": target,
    }

MOVEMENTS = {
    "abs": [
        movement("Dead bug", "No equipment", "Keep your lower back gently pressed into the floor as you extend opposite arm and leg.", "8 each side"),
        movement("Forearm plank", "No equipment", "Make a long line from head to heels; brace gently and keep breathing.", "20–40 sec"),
        movement("Glute bridge", "No equipment", "Press through your feet and squeeze your glutes at the top without arching your back."),
        movement("Bird dog", "No equipment", "From hands and knees, reach opposite hand and foot long; keep your hips level.", "8 each side"),
        movement("Bent-knee reverse crunch", "No equipment", "Curl your pelvis up slowly; avoid swinging your legs for momentum.", "10–12 reps"),
    ],
    "chest": [
        movement("Wall push-up", "No equipment", "Stand arm’s length from a wall, place your palms at chest height, and bend your elbows to bring your chest toward it.", "8–12 reps"),
        movement("Knee push-up", "No equipment", "Keep a straight line from shoulders to knees and lower with control.", "6–10 reps"),
        movement("Push-up", "No equipment", "Hands just wider than shoulders; keep elbows angled and brace your body.", "6–12 reps"),
        movement("Pike push-up", "No equipment", "Keep your hips high and bend your elbows to lower your head between your hands.", "6–10 reps"),
        movement("Close-grip push-up", "No equipment", "Keep elbows close to your sides as you lower; use a smaller range if needed.", "6–10 reps"),
    ],
    "back": [
        movement("Prone W raise", "No equipment", "Lie face down, draw shoulder blades gently together, and lift your hands into a W.", "8–12 reps"),
        movement("Reverse snow angel", "No equipment", "Lie face down and sweep straight arms from your sides overhead without shrugging.", "8–12 reps"),
        movement("Bird dog", "No equipment", "From hands and knees, reach opposite hand and foot long; keep your hips level.", "8 each side"),
        movement("Superman pull-down", "No equipment", "Lie face down, lift your chest slightly, and draw your elbows toward your ribs.", "8–10 reps"),
        movement("Prone cobra hold", "No equipment", "Lie face down, draw your shoulder blades back, and gently lift your chest and hands without straining your neck.", "20–30 sec"),
    ],
    "arms": [
        movement("Knee triceps push-up", "No equipment", "Keep elbows tucked by your sides and lower your chest with control.", "6–10 reps"),
        movement("Close-grip knee push-up", "No equipment", "Place hands a little inside shoulder-width; keep elbows pointing back.", "8–12 reps"),
        movement("Self-resisted biceps curl", "Use your opposite hand for resistance", "Keep your upper arm still and lower slowly against gentle resistance.", "8 each side"),
        movement("Pike shoulder tap", "No equipment", "Keep hips lifted and shift your weight slowly before tapping the opposite shoulder.", "6 each side"),
        movement("Self-resisted biceps hold", "Use your opposite hand for resistance", "Hold your elbow close to your side at about 90 degrees and press gently against your opposite hand; switch sides halfway through.", "20 sec each side"),
    ],
    "legs": [
        movement("Bodyweight squat", "No equipment", "Push your hips back, then stand by pressing through your whole foot.", "8–12 reps"),
        movement("Glute bridge", "No equipment", "Press through your heels and pause to squeeze your glutes at the top.", "8–12 reps"),
        movement("Reverse lunge", "No equipment", "Step back gently and lower only as far as feels steady.", "6–8 each side"),
        movement("Hip hinge / good morning", "No equipment", "Soften your knees and send your hips back while keeping your spine long.", "8–12 reps"),
        movement("Calf raise", "No equipment", "Rise onto the balls of your feet, pause briefly, then lower slowly.", "12–15 reps"),
    ],
    "full-body": [
        movement("Bodyweight squat", "No equipment", "Push your hips back and stand tall through your whole foot.", "8–12 reps"),
        movement("Knee push-up", "No equipment", "Brace your middle and keep a straight line as you press.", "8–12 reps"),
        movement("Glute bridge", "No equipment", "Press through your feet and squeeze glutes without arching your back.", "8–12 reps"),
        movement("Bird dog", "No equipment", "Reach long and keep your hips level; move slowly.", "8 each side"),
        movement("March in place", "No equipment", "Stand tall and march at a comfortable pace while keeping your balance.", "30 sec"),
    ],
}

ANIMATION_PATTERNS = {
    "floor-core": (
        "dead bug",
        "reverse crunch",
    ),
    "plank": ("plank",),
    "push-up": ("push-up", "push up"),
    "bridge": ("bridge",),
    "bird-dog": ("bird dog",),
    "squat": ("squat", "sit-to-stand"),
    "lunge": ("lunge",),
    "hinge": ("hinge", "romanian deadlift", "good morning"),
    "calf-raise": ("calf raise",),
    "press": (
        "dumbbell",
        "cable",
        "shoulder press",
        "triceps extension",
    ),
    "row": (
        "row",
        "reverse fly",
        "snow angel",
        "w raise",
        "pull-down",
        "pull-down",
    ),
    "arms": (
        "curl",
        "lateral raise",
        "shoulder tap",
        "march",
        "farmer",
    ),
}


DEMO_IMAGE_ALIASES = (
    ("bird dog row", "One-Arm_Dumbbell_Row"),
    ("dead bug", "Dead_Bug"),
    ("forearm plank", "Plank"),
    ("plank", "Plank"),
    ("glute bridge", "Butt_Lift_Bridge"),
    ("prone cobra", "Lying_Rear_Delt_Raise"),
    ("bird dog", "Bird_Dog"),
    ("reverse crunch", "Reverse_Crunch"),
    ("pike push-up", "wger_pike_pushups"),
    ("pike shoulder tap", "wger_pike_pushups"),
    ("wall push-up", "Incline_Push-Up"),
    ("close-grip incline push-up", "Push-Ups_-_Close_Triceps_Position"),
    ("incline push-up", "Incline_Push-Up"),
    ("close-grip push-up", "Push-Ups_-_Close_Triceps_Position"),
    ("triceps push-up", "Push-Ups_-_Close_Triceps_Position"),
    ("push-up", "Pushups"),
    ("dumbbell floor press", "Dumbbell_Floor_Press"),
    ("cable chest press", "Cable_Chest_Press"),
    ("dumbbell shoulder press", "Dumbbell_Shoulder_Press"),
    ("shoulder press", "Dumbbell_Shoulder_Press"),
    ("triceps press-down", "Triceps_Pushdown"),
    ("triceps extension", "Standing_Dumbbell_Triceps_Extension"),
    ("reverse snow angel", "Lying_Rear_Delt_Raise"),
    ("reverse fly", "Reverse_Flyes"),
    ("w raise", "Lying_Rear_Delt_Raise"),
    ("pull-down", "Wide-Grip_Lat_Pulldown"),
    ("lat pull-down", "Wide-Grip_Lat_Pulldown"),
    ("lat pulldown", "Wide-Grip_Lat_Pulldown"),
    ("one-arm dumbbell row", "One-Arm_Dumbbell_Row"),
    ("row", "Seated_One-arm_Cable_Pulley_Rows"),
    ("hammer curl", "Alternate_Hammer_Curl"),
    ("curl", "Dumbbell_Bicep_Curl"),
    ("biceps hold", "Dumbbell_Bicep_Curl"),
    ("lateral raise", "Side_Lateral_Raise"),
    ("chair", "Chair_Squat"),
    ("sit-to-stand", "Chair_Squat"),
    ("goblet squat", "Dumbbell_Squat"),
    ("squat", "Bodyweight_Squat"),
    ("reverse lunge", "Bodyweight_Walking_Lunge"),
    ("lunge", "Bodyweight_Walking_Lunge"),
    ("romanian deadlift", "Romanian_Deadlift"),
    ("good morning", "Good_Morning"),
    ("hip hinge", "Good_Morning"),
    ("calf raise", "Standing_Calf_Raises"),
    ("march", "Farmers_Walk"),
)


def demo_image_id(name: str) -> str:
    lowered = name.casefold()
    for term, image_id in DEMO_IMAGE_ALIASES:
        if term in lowered:
            if "dumbbell" in lowered and "calf raise" in lowered:
                return "Standing_Dumbbell_Calf_Raise"
            return image_id
    raise ValueError(f"No licensed movement demo is mapped for {name!r}")


def animation_pattern(name: str, focus: str, index: int) -> str:
    lowered = name.lower()
    for pattern, terms in ANIMATION_PATTERNS.items():
        if any(term in lowered for term in terms):
            return pattern
    if focus == "abs" and index in (0, 4):
        return "floor-core"
    if focus in {"back"}:
        return "row"
    if focus == "arms":
        return "arms"
    return "bird-dog"


def build_routine(
    focus: str,
    level: str = "beginner",
    completed_sessions: int = 0,
) -> dict[str, object] | None:
    if focus not in FOCUSES or level not in {"beginner", "intermediate"}:
        return None
    category = FOCUSES[focus]
    is_beginner = level == "beginner"
    completed_sessions = max(0, completed_sessions)
    base_sets = 2 if is_beginner else 3
    maximum_sets = 4 if is_beginner else 5
    set_count = min(maximum_sets, base_sets + completed_sessions // 3)
    rest = 45 if is_beginner else 30
    duration_seconds = (30 if is_beginner else 40) + min(
        completed_sessions, 4
    ) * 5
    selected = []
    for index, item in enumerate(MOVEMENTS[focus]):
        name = item["name"]
        selected.append(
            {
                **item,
                "name": name,
                "cue": item["cue"],
                "sets": set_count,
                "target": item["target"],
                "rest": rest,
                "duration_seconds": duration_seconds,
                "animation": animation_pattern(name, focus, index),
                "demo_id": demo_image_id(name),
            }
        )
    title = (
        f"Beginner {category['name'].lower()}"
        if is_beginner
        else f"Intermediate {category['name'].lower()}"
    )
    total_seconds = (
        len(selected) * set_count * selected[0]["duration_seconds"]
        + (len(selected) * set_count - 1) * rest
    )
    return {
        "focus": focus,
        "category": category,
        "level": level,
        "progression_sessions": completed_sessions,
        "equipment": "bodyweight",
        "title": title,
        "duration": (total_seconds + 59) // 60,
        "sets": set_count,
        "work_seconds": duration_seconds,
        "rest": rest,
        "exercises": selected,
    }
