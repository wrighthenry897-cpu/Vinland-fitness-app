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
        "color": "gold",
    },
    "full-body": {
        "name": "Full body",
        "short": "TOTAL",
        "icon": "✳",
        "description": "A balanced head-to-toe workout for the days you want it all.",
        "duration": 35,
        "color": "teal",
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
        movement("Side plank", "No equipment", "Stack your shoulders and hips, keep your breathing easy, and bend your lower knee for support if needed.", "15–25 sec each side"),
        movement("Plank shoulder tap", "No equipment", "Widen your stance and tap one shoulder at a time without letting your hips sway.", "6 each side"),
        movement("Hollow-body hold", "No equipment", "Keep your lower back comfortable against the floor; bend your knees or shorten the hold as needed.", "10–20 sec"),
        movement("Slow mountain climber", "No equipment", "From a comfortable high plank, bring one knee forward at a time without bouncing.", "6 each side"),
        movement("V-sit hold", "No equipment", "Lean back only as far as you can stay balanced; keep your knees bent if that feels better.", "10–20 sec"),
        movement("Bicycle crunch", "No equipment", "Move slowly, rotate through your ribs, and keep your neck relaxed.", "8 each side"),
        movement("Plank knee-to-elbow", "No equipment", "Bring one knee toward the same-side elbow with control; use a hands-and-knees version if needed.", "6 each side"),
    ],
    "chest": [
        movement("Wall push-up", "No equipment", "Stand arm’s length from a wall, place your palms at chest height, and bend your elbows to bring your chest toward it.", "8–12 reps"),
        movement("Knee push-up", "No equipment", "Keep a straight line from shoulders to knees and lower with control.", "6–10 reps"),
        movement("Push-up", "No equipment", "Hands just wider than shoulders; keep elbows angled and brace your body.", "6–12 reps"),
        movement("Paused knee push-up", "No equipment", "Pause briefly near your comfortable lowering point, then press up without losing your body line.", "5–8 reps"),
        movement("Close-grip push-up", "No equipment", "Keep elbows close to your sides as you lower; use a smaller range if needed.", "6–10 reps"),
        movement("Tempo push-up", "No equipment", "Lower for three comfortable counts, then press up smoothly; switch to your knees when needed.", "5–8 reps"),
        movement("Wide-hand push-up", "No equipment", "Place your hands only a little wider than usual and keep your shoulders comfortable.", "6–10 reps"),
        movement("Diamond knee push-up", "No equipment", "From your knees, bring your hands closer together only as far as your wrists and shoulders feel comfortable.", "5–8 reps"),
        movement("Push-up negative", "No equipment", "Lower for three comfortable counts, pausing if needed; use your knees or a wall when helpful.", "5–8 reps"),
        movement("Staggered-hand push-up", "No equipment", "Set one hand slightly forward, keep the range comfortable, and switch hand positions halfway through.", "5 each side"),
        movement("Close-grip knee push-up", "No equipment", "Keep your elbows close and lower only through a range you can control.", "6–10 reps"),
        movement("Push-up hold", "No equipment", "Hold a steady high plank or a comfortable lowered position while breathing normally.", "10–20 sec"),
    ],
    "back": [
        movement("Prone W raise", "No equipment", "Lie face down, draw shoulder blades gently together, and lift your hands into a W.", "8–12 reps"),
        movement("Reverse snow angel", "No equipment", "Lie face down and sweep straight arms from your sides overhead without shrugging.", "8–12 reps"),
        movement("Bird dog", "No equipment", "From hands and knees, reach opposite hand and foot long; keep your hips level.", "8 each side"),
        movement("Superman pull-down", "No equipment", "Lie face down, lift your chest slightly, and draw your elbows toward your ribs.", "8–10 reps"),
        movement("Prone cobra hold", "No equipment", "Lie face down, draw your shoulder blades back, and gently lift your chest and hands without straining your neck.", "20–30 sec"),
        movement("Prone Y raise", "No equipment", "Lie face down and lift your arms into a relaxed Y only as high as feels comfortable.", "8–10 reps"),
        movement("Prone T raise", "No equipment", "With your forehead supported, lift your arms out to the sides and gently squeeze your shoulder blades.", "8–10 reps"),
        movement("Alternating bird dog", "No equipment", "Reach opposite arm and leg, pause briefly, then switch sides without rushing.", "8 each side"),
        movement("Reverse snow angel pause", "No equipment", "Sweep your arms only through a comfortable range and pause briefly before returning.", "6–10 reps"),
        movement("Prone W hold", "No equipment", "Keep your neck relaxed and hold a gentle shoulder-blade squeeze in a W shape.", "10–20 sec"),
        movement("Superman pull-down pause", "No equipment", "Lift only slightly, draw your elbows toward your ribs, and stop if your back feels uncomfortable.", "6–8 reps"),
        movement("Prone alternating Y raise", "No equipment", "Lift one arm at a time into a small Y while keeping your ribs relaxed against the floor.", "6–8 each side"),
    ],
    "arms": [
        movement("Knee triceps push-up", "No equipment", "Keep elbows tucked by your sides and lower your chest with control.", "6–10 reps"),
        movement("Close-grip knee push-up", "No equipment", "Place hands a little inside shoulder-width; keep elbows pointing back.", "8–12 reps"),
        movement("Incline push-up", "No equipment", "Place your hands on a stable wall or counter, keep your body in a straight line, and lower with control.", "8–12 reps"),
        movement("Plank shoulder tap", "No equipment", "Widen your stance and tap one shoulder at a time without letting your hips sway.", "6 each side"),
        movement("Close-grip push-up", "No equipment", "Keep elbows near your sides as you lower; use your knees or a wall if needed.", "6–10 reps"),
        movement("Diamond knee push-up", "No equipment", "From your knees, bring your hands closer only as far as your wrists and shoulders feel comfortable.", "5–8 reps"),
        movement("Push-up", "No equipment", "Place your hands just wider than your shoulders, brace gently, and lower only through a comfortable range.", "6–12 reps"),
        movement("Incline push-up pause", "No equipment", "Pause briefly in a comfortable lowering position, then press up smoothly.", "5–8 reps"),
        movement("Wide-hand push-up", "No equipment", "Place your hands only a little wider than usual and keep your shoulders comfortable.", "6–10 reps"),
        movement("Push-up hold", "No equipment", "Hold a steady high plank or a comfortable lowered position while breathing normally.", "10–20 sec"),
        movement("Tempo push-up", "No equipment", "Lower for three comfortable counts, then press up smoothly; switch to your knees when needed.", "5–8 reps"),
    ],
    "legs": [
        movement("Bodyweight squat", "No equipment", "Push your hips back, then stand by pressing through your whole foot.", "8–12 reps"),
        movement("Glute bridge", "No equipment", "Press through your heels and pause to squeeze your glutes at the top.", "8–12 reps"),
        movement("Reverse lunge", "No equipment", "Step back gently and lower only as far as feels steady.", "6–8 each side"),
        movement("Hip hinge / good morning", "No equipment", "Soften your knees and send your hips back while keeping your spine long.", "8–12 reps"),
        movement("Calf raise", "No equipment", "Rise onto the balls of your feet, pause briefly, then lower slowly.", "12–15 reps"),
        movement("Tempo squat", "No equipment", "Lower for three comfortable counts and stand smoothly; use a shallower range if needed.", "8–10 reps"),
        movement("Split squat", "No equipment", "Take a comfortable split stance, hold a wall for balance if helpful, and lower only as far as steady.", "6 each side"),
        movement("Single-leg glute bridge", "No equipment", "Keep your hips level; leave both feet down if lifting one leg feels uncomfortable.", "6 each side"),
        movement("Lateral lunge", "No equipment", "Step to the side and sit your hips back gently, using a small range at first.", "6 each side"),
        movement("Single-leg calf raise", "No equipment", "Use a wall for balance and keep both feet down if needed; rise and lower slowly.", "8 each side"),
        movement("Split squat pause", "No equipment", "Pause briefly in a comfortable split stance, then stand with control; hold a wall for balance if helpful.", "5 each side"),
        movement("Single-leg glute bridge pause", "No equipment", "Keep your hips level and pause only briefly; use a two-foot bridge whenever needed.", "5 each side"),
    ],
    "full-body": [
        movement("Bodyweight squat", "No equipment", "Push your hips back and stand tall through your whole foot.", "8–12 reps"),
        movement("Knee push-up", "No equipment", "Brace your middle and keep a straight line as you press.", "8–12 reps"),
        movement("Glute bridge", "No equipment", "Press through your feet and squeeze glutes without arching your back.", "8–12 reps"),
        movement("Bird dog", "No equipment", "Reach long and keep your hips level; move slowly.", "8 each side"),
        movement("Standing calf raise", "No equipment", "Rise onto the balls of your feet, pause briefly, then lower slowly; use a wall for balance if helpful.", "12–15 reps"),
        movement("Tempo squat", "No equipment", "Lower for three comfortable counts and stand smoothly, using a range that feels steady.", "8–10 reps"),
        movement("Tempo knee push-up", "No equipment", "Lower for three counts while keeping a straight line from shoulders to knees.", "6–8 reps"),
        movement("Single-leg glute bridge", "No equipment", "Keep your hips level; keep both feet down if lifting one leg feels uncomfortable.", "6 each side"),
        movement("Slow mountain climber", "No equipment", "From a comfortable high plank, bring one knee forward at a time without bouncing.", "6 each side"),
        movement("Reverse lunge", "No equipment", "Step back gently and use a small, steady range; hold a wall for balance if useful.", "6 each side"),
        movement("Walkout", "No equipment", "Hinge forward with soft knees, walk your hands out only as far as comfortable, and step back in.", "4–6 reps"),
        movement("Squat-to-calf raise", "No equipment", "Stand from a comfortable squat and finish with a controlled calf raise; keep the range easy.", "8 reps"),
    ],
}

ANIMATION_PATTERNS = {
    "floor-core": (
        "dead bug",
        "reverse crunch",
    ),
    "plank": ("plank", "hollow-body", "mountain climber"),
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
    ("hollow-body", "Plank"),
    ("side plank", "Plank"),
    ("plank shoulder tap", "Plank"),
    ("plank knee-to-elbow", "Plank"),
    ("mountain climber", "Pushups"),
    ("bicycle crunch", "Reverse_Crunch"),
    ("v-sit", "Reverse_Crunch"),
    ("prone y raise", "Lying_Rear_Delt_Raise"),
    ("prone t raise", "Lying_Rear_Delt_Raise"),
    ("alternating bird dog", "Bird_Dog"),
    ("reverse snow angel pause", "Lying_Rear_Delt_Raise"),
    ("prone w hold", "Lying_Rear_Delt_Raise"),
    ("superman pull-down pause", "Lying_Rear_Delt_Raise"),
    ("alternating y raise", "Lying_Rear_Delt_Raise"),
    ("tempo knee push-up", "Pushups"),
    ("tempo push-up", "Pushups"),
    ("wide-hand push-up", "Pushups"),
    ("diamond knee push-up", "Push-Ups_-_Close_Triceps_Position"),
    ("pause push-up", "Pushups"),
    ("staggered-hand push-up", "Pushups"),
    ("push-up hold", "Pushups"),
    ("close-grip knee push-up", "Push-Ups_-_Close_Triceps_Position"),
    ("tempo squat", "Bodyweight_Squat"),
    ("split squat", "Bodyweight_Walking_Lunge"),
    ("single-leg glute bridge", "Butt_Lift_Bridge"),
    ("lateral lunge", "Bodyweight_Walking_Lunge"),
    ("single-leg calf raise", "Standing_Calf_Raises"),
    ("split squat pause", "Bodyweight_Walking_Lunge"),
    ("single-leg glute bridge pause", "Butt_Lift_Bridge"),
    ("walkout", "Pushups"),
    ("squat-to-calf raise", "Bodyweight_Squat"),
    ("forearm plank", "Plank"),
    ("plank", "Plank"),
    ("glute bridge", "Butt_Lift_Bridge"),
    ("prone cobra", "Lying_Rear_Delt_Raise"),
    ("bird dog", "Bird_Dog"),
    ("reverse crunch", "Reverse_Crunch"),
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
    movement_pool = MOVEMENTS[focus]
    movement_start = min(
        completed_sessions + (0 if is_beginner else 2),
        len(movement_pool) - 5,
    )
    selected = []
    for index, item in enumerate(movement_pool[movement_start : movement_start + 5]):
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
        "progression_stage": movement_start + 1,
        "progression_stages": len(movement_pool) - 4,
        "next_stage_unlocked": movement_start < len(movement_pool) - 5,
        "equipment": "bodyweight",
        "title": title,
        "duration": (total_seconds + 59) // 60,
        "sets": set_count,
        "work_seconds": duration_seconds,
        "rest": rest,
        "exercises": selected,
    }
