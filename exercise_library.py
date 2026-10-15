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
    gym: str,
    cue: str,
    target: str = "8–12 reps",
    gym_cue: str | None = None,
) -> dict[str, str]:
    return {
        "name": name,
        "bodyweight": bodyweight,
        "gym": gym,
        "cue": cue,
        "gym_cue": gym_cue or cue,
        "target": target,
    }


MOVEMENTS = {
    "abs": [
        movement("Dead bug", "No equipment", "Exercise mat", "Keep your lower back gently pressed into the floor as you extend opposite arm and leg.", "8 each side"),
        movement("Forearm plank", "No equipment", "Exercise mat", "Make a long line from head to heels; brace gently and keep breathing.", "20–40 sec"),
        movement("Glute bridge", "No equipment", "Exercise mat", "Press through your feet and squeeze your glutes at the top without arching your back."),
        movement("Bird dog", "No equipment", "Exercise mat", "From hands and knees, reach opposite hand and foot long; keep your hips level.", "8 each side"),
        movement("Bent-knee reverse crunch", "No equipment", "Exercise mat", "Curl your pelvis up slowly; avoid swinging your legs for momentum.", "10–12 reps"),
    ],
    "chest": [
        movement("Incline push-up", "Wall or sturdy counter", "Bench incline push-up", "Keep your body in one straight line and lower your chest toward the edge.", "8–12 reps", "Set a stable bar or bench at chest height. Keep your body straight and lower your chest toward the support."),
        movement("Knee push-up", "No equipment", "Bench push-up", "Keep a straight line from shoulders to knees and lower with control.", "6–10 reps", "Place hands on a secure bench, brace your body, and lower your chest toward its edge."),
        movement("Push-up", "No equipment", "Dumbbell floor press", "Hands just wider than shoulders; keep elbows angled and brace your body.", "6–12 reps", "Lie on the floor with a light dumbbell in each hand. Lower elbows gently to the floor, then press up."),
        movement("Pike push-up", "No equipment", "Seated dumbbell shoulder press", "Keep your hips high and bend your elbows to lower your head between your hands.", "6–10 reps", "Sit tall, start with light dumbbells at shoulder height, and press overhead without arching your back."),
        movement("Close-grip push-up", "No equipment", "Cable chest press", "Keep elbows close to your sides as you lower; use a smaller range if needed.", "6–10 reps", "Set the cable handles around chest height. Press forward smoothly and return without letting the stack pull you."),
    ],
    "back": [
        movement("Prone W raise", "No equipment", "Incline bench W raise", "Lie face down, draw shoulder blades gently together, and lift your hands into a W.", "8–12 reps", "Set a low incline and use very light dumbbells. Draw elbows into a W and avoid shrugging."),
        movement("Reverse snow angel", "No equipment", "Cable reverse fly", "Lie face down and sweep straight arms from your sides overhead without shrugging.", "8–12 reps", "With light cables at chest height, open your arms out to the sides and return slowly."),
        movement("Bird dog row", "Water bottle", "One-arm dumbbell row", "Brace your trunk and pull your elbow toward your hip without twisting.", "8 each side", "Support one hand on a bench, keep your back long, and row a light dumbbell toward your hip."),
        movement("Superman pull-down", "No equipment", "Lat pull-down machine", "Lift only as comfortably as you can; draw elbows down toward your ribs.", "8–10 reps", "Sit tall, hold the bar wider than shoulder-width, and pull it toward your upper chest without rocking."),
        movement("Towel row hold", "Towel and sturdy post", "Cable seated row", "Sit tall and squeeze your shoulder blades gently back; use a secure anchor only.", "20–30 sec", "Sit upright, row the handle toward your lower ribs, and return slowly without rounding your back."),
    ],
    "arms": [
        movement("Knee triceps push-up", "No equipment", "Cable triceps press-down", "Keep elbows tucked by your sides and lower your chest with control.", "6–10 reps", "Keep elbows close to your torso and press the handle down; return slowly."),
        movement("Close-grip incline push-up", "Wall or sturdy counter", "Dumbbell triceps extension", "Place hands a little inside shoulder-width; keep elbows pointing back.", "8–12 reps", "Use light dumbbells. Keep elbows pointing up as you bend and straighten your arms."),
        movement("Self-resisted biceps curl", "Use your opposite hand for resistance", "Dumbbell biceps curl", "Keep your upper arm still and lower slowly against gentle resistance.", "8 each side", "Keep elbows by your sides, curl light dumbbells without swinging, and lower slowly."),
        movement("Pike shoulder tap", "No equipment", "Dumbbell lateral raise", "Keep hips lifted and shift your weight slowly before tapping the opposite shoulder.", "6 each side", "With light dumbbells, raise arms out to the sides only to a comfortable height; keep shoulders relaxed."),
        movement("Towel biceps curl", "Towel and opposite-foot resistance", "Hammer curl", "Stand tall and use light, steady resistance; avoid leaning your body back.", "8–12 reps", "Hold light dumbbells with palms facing inward; curl without swinging and lower under control."),
    ],
    "legs": [
        movement("Sit-to-stand squat", "Sturdy chair", "Goblet squat to a box", "Push your hips back to the chair, then stand by pressing through your whole foot.", "8–12 reps", "Hold one light dumbbell close to your chest. Sit your hips back toward a box, then stand smoothly."),
        movement("Glute bridge", "No equipment", "Dumbbell glute bridge", "Press through your heels and pause to squeeze your glutes at the top.", "8–12 reps", "Place a light dumbbell securely across your hips. Press through your heels and lift without arching."),
        movement("Supported reverse lunge", "Hold a sturdy support", "Dumbbell reverse lunge", "Step back gently and lower only as far as feels steady.", "6–8 each side", "Hold light dumbbells at your sides, step back, and lower only as far as feels steady."),
        movement("Hip hinge / good morning", "No equipment", "Dumbbell Romanian deadlift", "Soften your knees and send your hips back while keeping your spine long.", "8–12 reps", "Hold light dumbbells in front of your thighs. Soften your knees and hinge at the hips with a long spine."),
        movement("Calf raise", "Wall for balance", "Dumbbell calf raise", "Rise onto the balls of your feet, pause briefly, then lower slowly.", "12–15 reps", "Hold light dumbbells at your sides, rise onto your toes, pause, and lower slowly."),
    ],
    "full-body": [
        movement("Sit-to-stand squat", "Sturdy chair", "Goblet squat", "Push hips back and stand tall through your whole foot.", "8–12 reps", "Hold a light dumbbell close to your chest, sit your hips back, and stand smoothly."),
        movement("Incline push-up", "Wall or sturdy counter", "Dumbbell floor press", "Brace your middle and keep a straight line as you press.", "8–12 reps", "Lie on the floor with light dumbbells. Lower your elbows gently to the floor, then press up."),
        movement("Glute bridge", "No equipment", "Dumbbell glute bridge", "Press through your feet and squeeze glutes without arching your back.", "8–12 reps", "Place a light dumbbell securely across your hips. Press through your feet and lift without arching."),
        movement("Bird dog", "No equipment", "One-arm dumbbell row", "Reach long and keep your hips level; move slowly.", "8 each side", "Support one hand on a bench, keep your back long, and row a light dumbbell toward your hip."),
        movement("March in place", "No equipment", "Dumbbell farmer march", "Stand tall and march at a comfortable pace while keeping your balance.", "30 sec", "Hold light dumbbells at your sides and march slowly while staying tall and balanced."),
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
    ("bird dog", "wger_bird_dog"),
    ("reverse crunch", "Reverse_Crunch"),
    ("pike push-up", "wger_pike_pushups"),
    ("pike shoulder tap", "wger_pike_pushups"),
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
    focus: str, level: str = "beginner", equipment: str = "bodyweight"
) -> dict[str, object] | None:
    if focus not in FOCUSES or level not in {"beginner", "intermediate"}:
        return None
    if equipment not in {"bodyweight", "gym"}:
        return None
    category = FOCUSES[focus]
    is_beginner = level == "beginner"
    set_count = 2 if is_beginner else 3
    rest = 45 if is_beginner else 30
    selected = []
    for index, item in enumerate(MOVEMENTS[focus]):
        name = item["name"]
        if equipment == "gym" and focus != "abs":
            name = item["gym"]
        selected.append(
            {
                **item,
                "name": name,
                "cue": item["gym_cue"] if equipment == "gym" and focus != "abs" else item["cue"],
                "sets": set_count,
                "target": item["target"],
                "rest": rest,
                "animation": animation_pattern(name, focus, index),
                "demo_id": demo_image_id(name),
            }
        )
    title = (
        f"Beginner {category['name'].lower()}"
        if is_beginner
        else f"Intermediate {category['name'].lower()}"
    )
    return {
        "focus": focus,
        "category": category,
        "level": level,
        "equipment": equipment,
        "title": title,
        "duration": category["duration"] + (0 if is_beginner else 5),
        "sets": set_count,
        "rest": rest,
        "exercises": selected,
    }
