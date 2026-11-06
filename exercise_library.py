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
        movement("Alternating heel tap", "No equipment", "Keep your shoulders relaxed and reach side to side only as far as you can control.", "8 each side"),
        movement("Bent-knee leg raise", "No equipment", "Keep your lower back comfortable against the floor and lower your legs only as far as you can control.", "8–10 reps"),
        movement("Dead bug heel drop", "No equipment", "Lower one heel at a time while keeping your ribs relaxed and your back comfortable.", "8 each side"),
        movement("Tabletop toe tap", "No equipment", "Keep your knees over your hips and tap one toe down at a time without arching your back.", "8 each side"),
        movement("Reverse crunch pause", "No equipment", "Curl your pelvis gently and pause briefly; avoid swinging your legs.", "8–10 reps"),
        movement("Seated knee tuck", "No equipment", "Lean back only as far as you can stay balanced, then draw your knees in smoothly.", "8–10 reps"),
        movement("Straight-leg floor scissor", "No equipment", "Keep the range small and your back comfortable; bend your knees if needed.", "8 each side"),
        movement("Flutter kick", "No equipment", "Keep your movements small and controlled; bend your knees or rest whenever needed.", "10 each side"),
        movement("Crunch reach", "No equipment", "Reach toward your knees with a small lift and keep your neck relaxed.", "10–12 reps"),
        movement("Cross-body crunch", "No equipment", "Rotate gently through your ribs and keep your neck relaxed.", "8 each side"),
        movement("Seated torso rotation", "No equipment", "Sit tall, brace gently, and rotate through your upper body without forcing the range.", "8 each side"),
        movement("High plank hold", "No equipment", "Place your hands under your shoulders and keep breathing in a comfortable straight line.", "15–30 sec"),
        movement("Knee side plank", "No equipment", "Support yourself on a forearm and bent knees; lift your hips only as high as feels steady.", "15–20 sec each side"),
        movement("Plank walk-back", "No equipment", "From hands and knees, walk your hands forward a comfortable distance and return slowly.", "5–8 reps"),
        movement("Bear hover", "No equipment", "Start on hands and knees, gently lift your knees, and keep your back steady while breathing.", "10–20 sec"),
        movement("Bird dog elbow-to-knee", "No equipment", "Reach long, then bring opposite elbow and knee together without rocking your hips.", "6 each side"),
        movement("Seated knee lift", "No equipment", "Sit tall and lift one knee at a time without leaning back.", "8 each side"),
        movement("Dead bug arm reach", "No equipment", "Lie comfortably with knees bent and reach one arm overhead at a time while keeping your back relaxed.", "8 each side"),
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
        movement("Incline knee push-up", "No equipment", "Use a stable wall or counter, keep your body aligned, and lower through a comfortable range.", "8–12 reps"),
        movement("Wide-knee push-up", "No equipment", "From your knees, place hands a little wider than shoulders and lower with control.", "6–10 reps"),
        movement("Push-up plus", "No equipment", "At the top of a comfortable push-up, gently spread your shoulder blades without rounding your back.", "6–10 reps"),
        movement("Eccentric push-up", "No equipment", "Lower slowly from your hands or knees, then reset in the easiest position that feels good.", "5–8 reps"),
        movement("Alternating shoulder-tap push-up", "No equipment", "Use a wide stance and tap one shoulder at a time from a comfortable high plank.", "6 each side"),
        movement("Staggered knee push-up", "No equipment", "Set one hand slightly forward, lower through a comfortable range, and switch hand positions.", "5 each side"),
        movement("Paused wall push-up", "No equipment", "Pause briefly near the wall, then push away smoothly without locking your elbows.", "8–12 reps"),
        movement("Narrow knee push-up", "No equipment", "Keep your hands just inside shoulder width and your elbows close as you lower.", "6–10 reps"),
        movement("Push-up to down-dog", "No equipment", "Use a comfortable push-up variation, then gently shift your hips back; shorten the range as needed.", "5–8 reps"),
        movement("Knee push-up hold", "No equipment", "Hold a steady position on your hands and knees with your shoulders comfortable.", "10–20 sec"),
        movement("Alternating hand-release push-up", "No equipment", "Lower from your knees or toes, briefly lift one hand at a time, then press up smoothly.", "5 each side"),
        movement("Incline close-grip push-up", "No equipment", "Use a stable elevated surface and keep your elbows near your sides through a comfortable range.", "8–12 reps"),
        movement("Push-up shoulder shift", "No equipment", "From a comfortable high plank, shift your shoulders gently forward and back without sagging.", "6–10 reps"),
        movement("Knee push-up to child’s pose", "No equipment", "Perform an easy knee push-up, then sit your hips back to rest; keep every repetition smooth.", "6–10 reps"),
        movement("Slow wall push-up", "No equipment", "Take three comfortable counts to bend your elbows, then press away smoothly.", "8–12 reps"),
        movement("Alternating staggered push-up", "No equipment", "Use a wall, counter, knees, or toes and switch which hand is forward halfway through.", "5 each side"),
        movement("Push-up bottom hold", "No equipment", "Pause only at a comfortable depth, using your knees or a wall to reduce effort.", "5–10 sec"),
        movement("Knee push-up plus", "No equipment", "At the top of a knee push-up, gently spread your shoulder blades while keeping your neck relaxed.", "6–10 reps"),
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
        movement("Prone A raise", "No equipment", "Lie face down and lift your arms in a small A shape while keeping your neck relaxed.", "8–10 reps"),
        movement("Prone swimmer", "No equipment", "Lie face down and slowly sweep your arms through a comfortable arc without forcing your shoulders.", "6–8 reps"),
        movement("Prone alternating W raise", "No equipment", "Lift one arm into a W at a time and gently draw your shoulder blade toward your spine.", "6 each side"),
        movement("Reverse snow angel hold", "No equipment", "Pause with your arms at a comfortable angle and keep your shoulders away from your ears.", "10–15 sec"),
        movement("Prone shoulder-blade squeeze", "No equipment", "Rest your arms by your sides and gently draw your shoulder blades together without shrugging.", "8–12 reps"),
        movement("Prone low cobra", "No equipment", "Keep your gaze down and lift your chest only a small amount while breathing easily.", "8–10 reps"),
        movement("Bird dog row", "No equipment", "From hands and knees, draw one elbow toward your ribs while keeping your hips level.", "6 each side"),
        movement("Quadruped arm reach", "No equipment", "From hands and knees, reach one arm forward without letting your torso twist.", "8 each side"),
        movement("Prone T hold", "No equipment", "Reach your arms out to the sides and hold a gentle shoulder-blade squeeze without straining.", "10–20 sec"),
        movement("Prone W to Y", "No equipment", "Sweep your arms from a comfortable W toward a small Y while keeping your neck relaxed.", "6–8 reps"),
        movement("Prone alternating swimmer", "No equipment", "Lift opposite arm and leg only slightly, then switch sides with steady breathing.", "6 each side"),
        movement("Prone elbow pull", "No equipment", "With your chest resting down, draw your elbows toward your ribs and squeeze gently.", "8–12 reps"),
        movement("Prone goalpost raise", "No equipment", "Bend your elbows into a goalpost shape and lift your hands only as high as comfortable.", "8–10 reps"),
        movement("Quadruped shoulder extension", "No equipment", "From hands and knees, reach one arm alongside your body without shifting your weight.", "6 each side"),
        movement("Prone long-arm pull", "No equipment", "Reach both arms overhead, then draw your elbows toward your sides in a slow, small motion.", "8–10 reps"),
        movement("Prone T to W", "No equipment", "Move your arms from a small T into a W and gently squeeze your shoulder blades.", "6–8 reps"),
        movement("Bird dog pause", "No equipment", "Reach opposite hand and foot, pause while keeping your hips level, then switch sides.", "6 each side"),
        movement("Prone shoulder-blade pulse", "No equipment", "With arms resting by your sides, make small controlled shoulder-blade squeezes.", "10–12 reps"),
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
        movement("Wall triceps push-up", "No equipment", "Face a wall, place hands around chest height, and keep elbows close as you bend and press.", "8–12 reps"),
        movement("Close-grip incline push-up", "No equipment", "Use a stable wall or counter and keep your elbows close to your sides.", "8–12 reps"),
        movement("Knee triceps push-up pause", "No equipment", "Keep elbows tucked and pause only at a comfortable depth before pressing up.", "5–8 reps"),
        movement("Pike shoulder press", "No equipment", "From hands and feet or hands and knees, bend your elbows slightly and keep the range easy.", "5–8 reps"),
        movement("Self-resisted biceps curl", "No equipment", "Press one hand gently against the other forearm as you curl; switch sides and use light effort.", "8 each side"),
        movement("Self-resisted triceps extension", "No equipment", "Use one hand to provide gentle resistance as the other arm straightens; switch sides.", "8 each side"),
        movement("Arm circle", "No equipment", "Stand tall and make small, controlled circles with relaxed shoulders.", "10 each direction"),
        movement("Bent-arm arm circle", "No equipment", "Keep elbows bent and make small circles without shrugging or forcing your range.", "10 each direction"),
        movement("Plank up-down", "No equipment", "From hands and knees or a high plank, lower one forearm at a time and switch leading arms.", "5 each side"),
        movement("Bear plank shoulder tap", "No equipment", "Use a hands-and-knees hover or keep your knees down while tapping one shoulder at a time.", "5 each side"),
        movement("Wall triceps press", "No equipment", "Place hands on a wall, keep elbows pointing forward, and bend and straighten with control.", "8–12 reps"),
        movement("Alternating self-resisted curl", "No equipment", "Use your opposite hand for gentle resistance and keep your shoulders relaxed as you switch.", "8 each side"),
        movement("Overhead triceps reach", "No equipment", "Reach one arm overhead, bend the elbow only through a comfortable range, then switch sides.", "8 each side"),
        movement("Shoulder blade push-up", "No equipment", "Keep your elbows straight and gently move your shoulder blades apart and together.", "8–12 reps"),
        movement("Wrist push-up from knees", "No equipment", "On hands and knees, shift your weight only a little and stop if your wrists feel uncomfortable.", "5–8 reps"),
        movement("High plank weight shift", "No equipment", "From hands and knees or a high plank, shift your shoulders gently from side to side.", "8 each side"),
        movement("Self-resisted hammer curl", "No equipment", "Use your opposite hand for gentle resistance with your palm facing inward; switch sides.", "8 each side"),
        movement("Arm raise and lower", "No equipment", "Raise your arms only to a comfortable height and lower them slowly without shrugging.", "8–12 reps"),
        movement("Self-resisted wrist curl", "No equipment", "Use your opposite hand to give gentle resistance as you bend your wrist, then switch sides.", "8 each side"),
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
        movement("Chair sit-to-stand", "No equipment", "Use a stable chair, stand by pressing through your feet, then sit down with control.", "8–12 reps"),
        movement("Wide-stance squat", "No equipment", "Stand comfortably wide, point toes slightly out, and squat only as far as feels steady.", "8–12 reps"),
        movement("Wall-supported split squat", "No equipment", "Hold a wall for balance, use a comfortable split stance, and keep the range small at first.", "6 each side"),
        movement("Alternating lateral lunge", "No equipment", "Step gently to one side, sit your hips back, and return before switching sides.", "6 each side"),
        movement("Glute bridge march", "No equipment", "Lift your hips gently and alternate small foot lifts while keeping your pelvis steady.", "6 each side"),
        movement("Hamstring walkout", "No equipment", "From a bridge, take small heel steps away and back; keep the range short and comfortable.", "4–6 reps"),
        movement("Standing hip extension", "No equipment", "Hold a wall if helpful and move one leg gently behind you without arching your back.", "8 each side"),
        movement("Standing hip abduction", "No equipment", "Hold a wall for balance and lift one leg out to the side without leaning your trunk.", "8 each side"),
        movement("Standing knee drive", "No equipment", "Stand tall and lift one knee to a comfortable height while keeping your balance.", "8 each side"),
        movement("Calf raise hold", "No equipment", "Rise onto both feet and hold at a comfortable height while keeping a wall nearby for balance.", "10–20 sec"),
        movement("Toe raise", "No equipment", "Stand near a wall and lift your toes while keeping your heels on the floor.", "10–15 reps"),
        movement("Supported single-leg hinge", "No equipment", "Hold a wall, soften one knee, and hinge a small amount while keeping your back long.", "6 each side"),
        movement("Alternating step-back", "No equipment", "Step one foot back to a comfortable split stance, return upright, and switch sides.", "6 each side"),
        movement("Glute bridge hold", "No equipment", "Lift your hips only as high as comfortable and keep breathing without arching your back.", "15–25 sec"),
        movement("Squat hold to stand", "No equipment", "Pause briefly in a comfortable squat, then stand smoothly; use a shallow range if needed.", "6–8 reps"),
        movement("Side-lying leg raise", "No equipment", "Lie on your side and lift the top leg a small distance without rolling your hips.", "8 each side"),
        movement("Side-lying clam", "No equipment", "Keep your feet together, bend your knees, and open the top knee only as far as comfortable.", "8–12 each side"),
        movement("Wall sit", "No equipment", "Rest your back lightly against a wall and hold a comfortable bend in your knees.", "15–30 sec"),
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
        movement("Sit-to-stand with reach", "No equipment", "Stand from a stable chair and reach overhead only as far as comfortable, then sit with control.", "8–10 reps"),
        movement("Squat and calf raise", "No equipment", "Stand from a comfortable squat and finish with a gentle calf raise.", "8–10 reps"),
        movement("Step-back lunge and reach", "No equipment", "Step one foot back as you reach forward comfortably, return upright, then switch sides.", "6 each side"),
        movement("Bear crawl hold", "No equipment", "Stay on hands and knees or hover your knees briefly while keeping your back steady.", "10–20 sec"),
        movement("Standing cross-body knee drive", "No equipment", "Lift one knee toward the opposite hand at an easy pace while standing tall.", "8 each side"),
        movement("Walkout to knee plank", "No equipment", "Walk your hands forward to a hands-and-knees or knee-plank position, then return slowly.", "4–6 reps"),
        movement("Lateral step and reach", "No equipment", "Step gently to one side and reach across your body without twisting forcefully.", "6 each side"),
        movement("Glute bridge with reach", "No equipment", "Lift your hips comfortably and reach one arm upward at a time while keeping your pelvis steady.", "6 each side"),
        movement("Standing hinge and reach", "No equipment", "Hinge your hips back with a long spine, then stand and reach forward comfortably.", "8–10 reps"),
        movement("Knee push-up to shoulder tap", "No equipment", "From your knees, hold a steady top position and tap one shoulder at a time.", "5 each side"),
        movement("Alternating reverse lunge and knee lift", "No equipment", "Step back into a comfortable lunge, return to standing, and lift the same knee gently.", "5 each side"),
        movement("Dead bug with arm reach", "No equipment", "Keep your back comfortable and slowly reach one arm overhead at a time.", "8 each side"),
        movement("Side step squat", "No equipment", "Take a small side step, sit your hips back gently, and stand before switching sides.", "6 each side"),
        movement("Bird dog to child’s pose", "No equipment", "Reach opposite arm and leg from hands and knees, then sit back to rest between sides.", "5 each side"),
        movement("Standing calf raise and march", "No equipment", "Rise onto both feet, lower slowly, then march gently while keeping a wall nearby.", "8 each side"),
        movement("Wall push-up and reach", "No equipment", "Perform an easy wall push-up, then reach one arm forward while keeping your body steady.", "5 each side"),
        movement("Glute bridge march", "No equipment", "Lift your hips gently and alternate small foot lifts while keeping your pelvis steady.", "5 each side"),
        movement("Squat to alternating reach", "No equipment", "Stand from a comfortable squat and reach one arm overhead at a time.", "6 each side"),
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
    ("bird dog row", "Bird_Dog"),
    ("dead bug", "Dead_Bug"),
    ("hollow-body", "Plank"),
    ("side plank", "Plank"),
    ("side-lying leg raise", "Butt_Lift_Bridge"),
    ("heel tap", "Reverse_Crunch"),
    ("leg raise", "Reverse_Crunch"),
    ("knee tuck", "Reverse_Crunch"),
    ("toe tap", "Dead_Bug"),
    ("floor scissor", "Reverse_Crunch"),
    ("flutter kick", "Reverse_Crunch"),
    ("crunch", "Reverse_Crunch"),
    ("torso rotation", "Reverse_Crunch"),
    ("bear hover", "Plank"),
    ("seated knee lift", "Chair_Squat"),
    ("quadruped", "Bird_Dog"),
    ("plank shoulder tap", "Plank"),
    ("plank knee-to-elbow", "Plank"),
    ("mountain climber", "Pushups"),
    ("bicycle crunch", "Reverse_Crunch"),
    ("v-sit", "Reverse_Crunch"),
    ("prone y raise", "Lying_Rear_Delt_Raise"),
    ("prone t raise", "Lying_Rear_Delt_Raise"),
    ("prone", "Lying_Rear_Delt_Raise"),
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
    ("push-up", "Pushups"),
    ("arm circle", "Dumbbell_Shoulder_Press"),
    ("arm raise", "Side_Lateral_Raise"),
    ("triceps", "Push-Ups_-_Close_Triceps_Position"),
    ("wrist push-up", "Push-Ups_-_Close_Triceps_Position"),
    ("toe raise", "Standing_Calf_Raises"),
    ("side-lying leg raise", "Standing_Calf_Raises"),
    ("side-lying clam", "Butt_Lift_Bridge"),
    ("wall sit", "Chair_Squat"),
    ("bear crawl", "Bird_Dog"),
    ("knee drive", "Bodyweight_Walking_Lunge"),
    ("lateral step", "Bodyweight_Walking_Lunge"),
    ("step-back", "Bodyweight_Walking_Lunge"),
    ("standing hinge", "Good_Morning"),
    ("single-leg hinge", "Good_Morning"),
    ("hip extension", "Bodyweight_Walking_Lunge"),
    ("hip abduction", "Bodyweight_Walking_Lunge"),
    ("weight shift", "Plank"),
    ("down-dog", "Pushups"),
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
    progression_step = 1
    progression_stages = (len(movement_pool) + progression_step - 1) // progression_step
    progression_stage = completed_sessions % progression_stages
    movement_start = progression_stage * progression_step % len(movement_pool)
    movement_order = movement_pool[movement_start:] + movement_pool[:movement_start]
    selected = []
    for index, item in enumerate(movement_order[:5]):
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
        "progression_stage": progression_stage + 1,
        "progression_stages": progression_stages,
        "next_stage_unlocked": progression_stage + 1 < progression_stages,
        "equipment": "bodyweight",
        "title": title,
        "duration": (total_seconds + 59) // 60,
        "sets": set_count,
        "work_seconds": duration_seconds,
        "rest": rest,
        "exercises": selected,
    }
